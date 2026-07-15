"""Unified LLM call wrapper — routes through LiteLLM to any provider."""
import asyncio
import os
from typing import Any, Optional

import litellm
from dotenv import load_dotenv

load_dotenv()
litellm.suppress_debug_info = True


async def call_llm(
    model_slug: str,
    messages: list[dict],
    tools: Optional[list[dict]] = None,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    **kwargs,
) -> Any:
    # Optional per-call throttle to survive burst rate limits (Groq etc.).
    # Set MCPBENCH_LLM_SLEEP=1.5 to sleep 1.5s before each call.
    sleep_s = float(os.getenv("MCPBENCH_LLM_SLEEP", "0") or "0")
    if sleep_s > 0:
        await asyncio.sleep(sleep_s)
    """Call an LLM via LiteLLM with automatic provider routing.

    Model slug prefixes:
      - openrouter/<model> -> OpenRouter
      - groq/<model> -> Groq
      - gemini/<model> -> Google Gemini
      - openai/<model> -> OpenAI
      - anthropic/<model> -> Anthropic
    """
    call_kwargs = {
        "model": model_slug,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        call_kwargs["tools"] = tools
    call_kwargs.update(kwargs)
    return await litellm.acompletion(**call_kwargs)


async def call_llm_simple(
    model_slug: str,
    prompt: str,
    system: str = "You are a helpful assistant.",
    temperature: float = 0.0,
    max_tokens: int = 4096,
) -> str:
    """Simple single-prompt call — returns just the text content."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    response = await call_llm(model_slug, messages, temperature=temperature, max_tokens=max_tokens)
    if hasattr(response, "choices") and response.choices:
        return response.choices[0].message.content or ""
    return str(response)
