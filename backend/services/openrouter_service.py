"""
OpenRouter Multi-LLM Service
─────────────────────────────
Role-based model selection with fallback chains.
Uses httpx.AsyncClient — no openai SDK dependency.

Roles: manager, research, reasoning, vision, write, ocr, thinking, fast, code
"""
import os
import asyncio
import logging
from typing import Optional

import httpx

logger = logging.getLogger("openrouter_service")

# ─── Config ──────────────────────────────────────────────────────────────────

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_CHAT_URL = f"{OPENROUTER_BASE_URL}/chat/completions"

_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://openclaw.ai",
    "X-Title": "OpenClaw Benchmark",
}

# ─── Role → Model Map ─────────────────────────────────────────────────────────

ROLES: dict[str, dict] = {
    "manager": {
        "primary": "meta-llama/llama-3.3-70b-instruct:free",
        "fallback": ["qwen/qwen3-next-80b-a3b-instruct:free", "meta-llama/llama-3.2-3b-instruct:free"]
    },
    "research": {
        "primary": "qwen/qwen3-next-80b-a3b-instruct:free",
        "fallback": ["meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free"]
    },
    "reasoning": {
        "primary": "nousresearch/hermes-3-llama-3.1-405b:free",
        "fallback": ["meta-llama/llama-3.3-70b-instruct:free", "qwen/qwen3-next-80b-a3b-instruct:free"]
    },
    "vision": {
        "primary": "google/gemma-4-26b-a4b:free",
        "fallback": ["meta-llama/llama-3.3-70b-instruct:free"]
    },
    "write": {
        "primary": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
        "fallback": ["meta-llama/llama-3.3-70b-instruct:free"]
    },
    "ocr": {
        "primary": "baidu/qianfan-ocr-fast:free",
        "fallback": ["google/gemma-4-26b-a4b:free"]
    },
    "thinking": {
        "primary": "arcee-ai/trinity-large-thinking:free",
        "fallback": ["nousresearch/hermes-3-llama-3.1-405b:free"]
    },
    "fast": {
        "primary": "liquid/lfm-2.5-1.2b-instruct:free",
        "fallback": ["meta-llama/llama-3.2-3b-instruct:free"]
    },
    "code": {
        "primary": "qwen/qwen3-coder-480b-a35b:free",
        "fallback": ["meta-llama/llama-3.3-70b-instruct:free"]
    },
}


# ─── Internal HTTP helper ─────────────────────────────────────────────────────

async def _post_to_openrouter(
    model: str,
    messages: list[dict],
    tools: Optional[list] = None,
    temperature: float = 0.2,
    max_tokens: int = 2048,
    timeout: float = 60.0,
) -> dict:
    """
    POST a single request to OpenRouter.
    Returns the raw response dict on success.
    Raises httpx.HTTPStatusError on 4xx/5xx.
    """
    body: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "provider": {
            "sort": "throughput",
            "allow_fallbacks": True,
        },
    }
    if tools:
        body["tools"] = tools
        body["tool_choice"] = "auto"

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(OPENROUTER_CHAT_URL, headers=_HEADERS, json=body)
        resp.raise_for_status()
        return resp.json()


def _parse_response(raw: dict, model: str, role: str) -> dict:
    """
    Extract content and tool_calls from a raw OpenRouter response dict.
    Returns: {"content": str, "model_used": str, "role": str, "tool_calls": list|None}
    """
    choice = raw.get("choices", [{}])[0]
    message = choice.get("message", {})

    content = message.get("content") or ""
    raw_tool_calls = message.get("tool_calls")

    tool_calls = None
    if raw_tool_calls:
        tool_calls = []
        for tc in raw_tool_calls:
            tool_calls.append({
                "id": tc.get("id", ""),
                "type": tc.get("type", "function"),
                "function": {
                    "name": tc.get("function", {}).get("name", ""),
                    "arguments": tc.get("function", {}).get("arguments", "{}"),
                },
            })

    # Prefer the model reported by the API (may differ from requested due to fallbacks)
    model_used = raw.get("model", model)

    return {
        "content": content,
        "model_used": model_used,
        "role": role,
        "tool_calls": tool_calls,
    }


# ─── Public API ───────────────────────────────────────────────────────────────

async def call_llm(
    role: str,
    prompt: str,
    system: Optional[str] = None,
    tools: Optional[list] = None,
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> dict:
    """
    Call OpenRouter with role-based model selection and automatic fallback.

    Args:
        role:        One of the keys in ROLES (manager, research, reasoning, …)
        prompt:      User message content
        system:      Optional system prompt
        tools:       Optional OpenAI-format tools list
        temperature: Sampling temperature (default 0.2)
        max_tokens:  Max tokens to generate (default 2048)

    Returns:
        {"content": str, "model_used": str, "role": str, "tool_calls": list|None}

    Raises:
        ValueError:  Unknown role
        RuntimeError: All models (primary + fallbacks) failed
    """
    if role not in ROLES:
        raise ValueError(f"Unknown role '{role}'. Valid roles: {list(ROLES.keys())}")

    role_cfg = ROLES[role]
    models_to_try = [role_cfg["primary"]] + list(role_cfg.get("fallback", []))

    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    last_error: Optional[Exception] = None

    for model in models_to_try:
        try:
            raw = await _post_to_openrouter(
                model=model,
                messages=messages,
                tools=tools,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result = _parse_response(raw, model, role)
            if model != role_cfg["primary"]:
                logger.info(f"[openrouter] Role '{role}' used fallback model: {model}")
            return result

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in (429, 500, 502, 503, 504):
                logger.warning(
                    f"[openrouter] Model '{model}' returned {status} — trying next fallback"
                )
                last_error = exc
                continue
            # Non-retryable HTTP error (e.g. 400 bad request) — raise immediately
            logger.error(f"[openrouter] Non-retryable HTTP {status} for model '{model}': {exc}")
            raise

        except httpx.TimeoutException as exc:
            logger.warning(f"[openrouter] Timeout for model '{model}' — trying next fallback")
            last_error = exc
            continue

        except Exception as exc:
            logger.error(f"[openrouter] Unexpected error for model '{model}': {exc}")
            last_error = exc
            continue

    raise RuntimeError(
        f"All models for role '{role}' failed. "
        f"Tried: {models_to_try}. "
        f"Last error: {last_error}"
    )


async def call_llm_with_messages(
    role: str,
    messages: list[dict],
    tools: Optional[list] = None,
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> dict:
    """
    Like call_llm but accepts a full messages array (for agentic loops with history).

    Returns:
        {"content": str, "model_used": str, "role": str, "tool_calls": list|None}
    """
    if role not in ROLES:
        raise ValueError(f"Unknown role '{role}'. Valid roles: {list(ROLES.keys())}")

    role_cfg = ROLES[role]
    models_to_try = [role_cfg["primary"]] + list(role_cfg.get("fallback", []))

    last_error: Optional[Exception] = None

    for model in models_to_try:
        try:
            raw = await _post_to_openrouter(
                model=model,
                messages=messages,
                tools=tools,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result = _parse_response(raw, model, role)
            if model != role_cfg["primary"]:
                logger.info(f"[openrouter] Role '{role}' used fallback model: {model}")
            return result

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in (429, 500, 502, 503, 504):
                logger.warning(
                    f"[openrouter] Model '{model}' returned {status} — trying next fallback"
                )
                last_error = exc
                continue
            logger.error(f"[openrouter] Non-retryable HTTP {status} for model '{model}': {exc}")
            raise

        except httpx.TimeoutException as exc:
            logger.warning(f"[openrouter] Timeout for model '{model}' — trying next fallback")
            last_error = exc
            continue

        except Exception as exc:
            logger.error(f"[openrouter] Unexpected error for model '{model}': {exc}")
            last_error = exc
            continue

    raise RuntimeError(
        f"All models for role '{role}' failed. "
        f"Tried: {models_to_try}. "
        f"Last error: {last_error}"
    )


async def call_llm_parallel(
    role: str,
    prompts: list[str],
    system: Optional[str] = None,
) -> list[dict]:
    """
    Run the same role with multiple prompts concurrently.

    Args:
        role:    One of the keys in ROLES
        prompts: List of user messages to process in parallel
        system:  Optional shared system prompt

    Returns:
        List of result dicts (same format as call_llm), one per prompt.
        Failed calls return {"content": "", "model_used": "", "role": role, "tool_calls": None, "error": str}
    """
    async def _safe_call(prompt: str) -> dict:
        try:
            return await call_llm(role=role, prompt=prompt, system=system)
        except Exception as exc:
            logger.error(f"[openrouter] parallel call failed for role '{role}': {exc}")
            return {
                "content": "",
                "model_used": "",
                "role": role,
                "tool_calls": None,
                "error": str(exc),
            }

    return list(await asyncio.gather(*[_safe_call(p) for p in prompts]))


def get_model_for_role(role: str) -> str:
    """Return the primary model ID for a given role."""
    if role not in ROLES:
        raise ValueError(f"Unknown role '{role}'. Valid roles: {list(ROLES.keys())}")
    return ROLES[role]["primary"]


def list_all_models() -> dict:
    """Return the full ROLES dict (primary + fallback chains for every role)."""
    return ROLES
