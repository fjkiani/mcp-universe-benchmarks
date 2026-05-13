# Kairos provider layer — OpenRouter streaming + non-streaming calls.
# Uses httpx (already a project dependency) for HTTP transport.
# Non-streaming calls delegate to openrouter_service.call_llm_with_messages
# so model routing, fallback chains, and headers stay in one place.
# Streaming is implemented here because openrouter_service is non-streaming.
"""OpenRouter provider for Kairos — streaming LLM calls with role-based model routing."""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from typing import Generator

import httpx

# ── Phase → ZOA role mapping ──────────────────────────────────────────────────
# Maps Kairos execution phases to the existing ZOA role names defined in
# openrouter_service.ROLES. Model selection stays consistent across all ZOA
# agents — no duplicate model strings maintained here.
PHASE_TO_ROLE: dict[str, str] = {
    "planning":  "reasoning",   # nousresearch/hermes-3-llama-3.1-405b:free
    "acting":    "fast",        # liquid/lfm-2.5-1.2b-instruct:free
    "observing": "reasoning",
    "refining":  "reasoning",
    "fast":      "fast",
    "default":   "reasoning",
}

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"

# Fallback model strings used when openrouter_service is unavailable (e.g. unit tests)
_FALLBACK_MODELS: dict[str, str] = {
    "planning":  "nousresearch/hermes-3-llama-3.1-405b:free",
    "acting":    "liquid/lfm-2.5-1.2b-instruct:free",
    "observing": "nousresearch/hermes-3-llama-3.1-405b:free",
    "refining":  "nousresearch/hermes-3-llama-3.1-405b:free",
    "fast":      "liquid/lfm-2.5-1.2b-instruct:free",
    "default":   "nousresearch/hermes-3-llama-3.1-405b:free",
}


# ── Event types ───────────────────────────────────────────────────────────────

@dataclass
class TextChunk:
    text: str


@dataclass
class ThinkingChunk:
    text: str


@dataclass
class AssistantTurn:
    text: str
    tool_calls: list = field(default_factory=list)
    in_tokens: int = 0
    out_tokens: int = 0


# ── Internal helpers ──────────────────────────────────────────────────────────

def _resolve_model(phase: str) -> str:
    """Return the primary model string for a Kairos phase.

    Resolves via openrouter_service.ROLES so the model map has a single
    source of truth. Falls back to _FALLBACK_MODELS if the import fails.
    """
    try:
        from services.openrouter_service import ROLES
        role = PHASE_TO_ROLE.get(phase, PHASE_TO_ROLE["default"])
        return ROLES[role]["primary"]
    except Exception:
        return _FALLBACK_MODELS.get(phase, _FALLBACK_MODELS["default"])


def _build_headers(config: dict) -> dict:
    """Build OpenRouter request headers. Allows per-run API key override via config."""
    api_key = config.get("openrouter_api_key") or os.environ.get("OPENROUTER_API_KEY", "")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "Kairos-ZOA",
    }


# ── Streaming provider ────────────────────────────────────────────────────────

def stream(
    model: str,
    system: str,
    messages: list,
    tool_schemas: list,
    config: dict,
) -> Generator:
    """Stream a chat completion from OpenRouter using httpx.

    Yields: TextChunk | ThinkingChunk | AssistantTurn
    AssistantTurn is yielded exactly once at the end with full text + tool_calls.

    Args:
        model:        OpenRouter model string (resolved via model_for_phase)
        system:       System prompt string
        messages:     List of {"role": ..., "content": ...} dicts (conversation history)
        tool_schemas: List of tool schema dicts (OpenAI function-call format)
        config:       Runtime config dict (may contain "openrouter_api_key" override)
    """
    payload: dict = {
        "model": model,
        "stream": True,
        "messages": [{"role": "system", "content": system}] + messages,
        "provider": {
            "sort": "throughput",
            "allow_fallbacks": True,
        },
    }
    if tool_schemas:
        payload["tools"] = [
            {"type": "function", "function": s} for s in tool_schemas
        ]
        payload["tool_choice"] = "auto"

    full_text = ""
    tool_calls_acc: dict[int, dict] = {}
    in_tokens = 0
    out_tokens = 0

    try:
        with httpx.Client(timeout=120.0) as client:
            with client.stream(
                "POST",
                OPENROUTER_CHAT_URL,
                headers=_build_headers(config),
                json=payload,
            ) as resp:
                resp.raise_for_status()
                for raw_line in resp.iter_lines():
                    line = raw_line.strip()
                    if not line or not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue

                    # Usage (may appear in last chunk)
                    if "usage" in chunk:
                        usage = chunk["usage"]
                        in_tokens = usage.get("prompt_tokens", 0)
                        out_tokens = usage.get("completion_tokens", 0)

                    choices = chunk.get("choices", [])
                    if not choices:
                        continue
                    delta = choices[0].get("delta", {})

                    # Text content
                    content = delta.get("content")
                    if content:
                        full_text += content
                        yield TextChunk(content)

                    # Thinking / reasoning tokens (model-dependent field names)
                    reasoning = delta.get("reasoning") or delta.get("thinking")
                    if reasoning:
                        yield ThinkingChunk(reasoning)

                    # Tool call deltas — accumulate by index
                    for tc_delta in delta.get("tool_calls", []):
                        idx = tc_delta.get("index", 0)
                        if idx not in tool_calls_acc:
                            tool_calls_acc[idx] = {
                                "id": tc_delta.get("id", str(uuid.uuid4())),
                                "name": "",
                                "input_str": "",
                            }
                        tc = tool_calls_acc[idx]
                        fn = tc_delta.get("function", {})
                        if fn.get("name"):
                            tc["name"] += fn["name"]
                        if fn.get("arguments"):
                            tc["input_str"] += fn["arguments"]
                        if tc_delta.get("id"):
                            tc["id"] = tc_delta["id"]

    except httpx.HTTPStatusError as e:
        body_text = e.response.text[:500]
        raise RuntimeError(f"OpenRouter HTTP {e.response.status_code}: {body_text}") from e
    except httpx.TimeoutException as e:
        raise RuntimeError(f"OpenRouter request timed out after 120s") from e

    # Parse accumulated tool calls
    tool_calls = []
    for idx in sorted(tool_calls_acc.keys()):
        tc = tool_calls_acc[idx]
        try:
            parsed_input = json.loads(tc["input_str"]) if tc["input_str"] else {}
        except json.JSONDecodeError:
            parsed_input = {"raw": tc["input_str"]}
        tool_calls.append({
            "id": tc["id"],
            "name": tc["name"],
            "input": parsed_input,
        })

    yield AssistantTurn(
        text=full_text,
        tool_calls=tool_calls,
        in_tokens=in_tokens,
        out_tokens=out_tokens,
    )


# ── Non-streaming fast call ───────────────────────────────────────────────────

def call_fast(system: str, user: str, config: dict) -> str:
    """Non-streaming single call using the 'fast' role. Returns full text.

    Delegates to openrouter_service.call_llm_with_messages so fallback chains
    and model selection stay consistent with the rest of ZOA.

    Called from compaction.compact_messages — non-critical path. Returns empty
    string on any error so compaction degrades gracefully.

    Note: engine.run() executes in a BackgroundTask thread (not the async event
    loop), so asyncio.run() is safe here.
    """
    try:
        import asyncio
        from services.openrouter_service import call_llm_with_messages
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        result = asyncio.run(call_llm_with_messages(role="fast", messages=messages))
        return result.get("content", "")
    except Exception:
        return ""


# ── Public helper ─────────────────────────────────────────────────────────────

def model_for_phase(phase: str) -> str:
    """Return the OpenRouter model string for a given execution phase."""
    return _resolve_model(phase)
