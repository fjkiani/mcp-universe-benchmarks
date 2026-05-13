# Adapted from SafeRL-Lab/cheetahclaws (Apache-2.0)
# Modifications: compact_messages uses Kairos OpenRouter provider;
#   get_context_limit uses local model registry; _restore_plan_context removed.
"""Context window management: two-layer compression for long conversations."""
from __future__ import annotations

# ── Context window registry for OpenRouter models used by Kairos ─────────────
_CONTEXT_WINDOWS: dict[str, int] = {
    "nousresearch/hermes-3-llama-3.1-405b": 131_072,
    "liquid/lfm-2.5-1.2b-instruct": 32_768,
    "liquid/lfm-40b": 32_768,
    "google/gemma-3-27b-it": 131_072,
    "qwen/qwen3-coder-480b-a35b-instruct": 131_072,
}
_DEFAULT_CONTEXT = 32_768


def get_context_limit(model: str, config: dict | None = None) -> int:
    """Return context window size for a model string."""
    return _CONTEXT_WINDOWS.get(model, _DEFAULT_CONTEXT)


def _count_str_chars(obj) -> int:
    if isinstance(obj, str):
        return len(obj)
    if isinstance(obj, dict):
        return sum(_count_str_chars(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(_count_str_chars(item) for item in obj)
    return 0


def estimate_tokens(messages: list) -> int:
    """Estimate token count using chars/2.8 (conservative for code-heavy content)."""
    total_chars = 0
    msg_count = 0
    for m in messages:
        msg_count += 1
        content = m.get("content", "")
        if isinstance(content, str):
            total_chars += len(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    for v in block.values():
                        if isinstance(v, str):
                            total_chars += len(v)
        for tc in m.get("tool_calls", []):
            total_chars += _count_str_chars(tc)
    content_tokens = int(total_chars / 2.8)
    framing_tokens = msg_count * 4
    return int((content_tokens + framing_tokens) * 1.1)


def snip_old_tool_results(messages: list, max_chars: int = 2000, preserve_last_n_turns: int = 6) -> list:
    """Layer 1: truncate old tool-role messages that exceed max_chars."""
    cutoff = max(0, len(messages) - preserve_last_n_turns)
    for i in range(cutoff):
        m = messages[i]
        if m.get("role") != "tool":
            continue
        content = m.get("content", "")
        if not isinstance(content, str) or len(content) <= max_chars:
            continue
        first_half = content[: max_chars // 2]
        last_quarter = content[-(max_chars // 4):]
        snipped = len(content) - len(first_half) - len(last_quarter)
        m["content"] = f"{first_half}\n[... {snipped} chars snipped ...]\n{last_quarter}"
    return messages


def _respect_tool_pairs(messages: list, split: int) -> int:
    n = len(messages)
    if split <= 0 or split >= n:
        return split
    prev = messages[split - 1]
    if prev.get("role") == "assistant" and (prev.get("tool_calls") or []):
        j = split
        while j < n and messages[j].get("role") == "tool":
            j += 1
        split = j
    while split < n and messages[split].get("role") == "tool":
        split += 1
    return split


def find_split_point(messages: list, keep_ratio: float = 0.3) -> int:
    if not messages:
        return 0
    keep_ratio = max(0.0, min(1.0, keep_ratio))
    total = estimate_tokens(messages)
    target = int(total * keep_ratio)
    running = 0
    raw = 0
    for i in range(len(messages) - 1, -1, -1):
        running += estimate_tokens([messages[i]])
        if running >= target:
            raw = i
            break
    adjusted = _respect_tool_pairs(messages, raw)
    if adjusted >= len(messages):
        return 0
    return adjusted


def sanitize_history(messages: list) -> list:
    """Enforce tool-calls ↔ tool-response invariant for OpenAI-compatible APIs."""
    cleaned: list = []
    pending: set[str] = set()

    def _strip_unanswered():
        if not pending:
            return
        target = None
        for k in range(len(cleaned) - 1, -1, -1):
            role_k = cleaned[k].get("role")
            if role_k == "tool":
                continue
            if role_k == "assistant":
                target = k
                break
        if target is None:
            return
        prev = cleaned[target]
        tcs = prev.get("tool_calls") or []
        kept = [tc for tc in tcs if tc.get("id") not in pending]
        if len(kept) == len(tcs):
            return
        new_prev = dict(prev)
        if kept:
            new_prev["tool_calls"] = kept
        else:
            new_prev.pop("tool_calls", None)
        if new_prev.get("content") in (None, ""):
            new_prev["content"] = ""
        cleaned[target] = new_prev

    for m in messages:
        role = m.get("role")
        if role == "tool":
            tid = m.get("tool_call_id")
            if tid in pending:
                cleaned.append(m)
                pending.discard(tid)
            continue
        _strip_unanswered()
        pending = set()
        if role == "assistant":
            tcs = m.get("tool_calls") or []
            if tcs:
                pending = {tc["id"] for tc in tcs if tc.get("id")}
        cleaned.append(m)

    _strip_unanswered()
    return cleaned


def compact_messages(messages: list, config: dict, focus: str = "") -> list:
    """Layer 2: compress old messages into a summary via LLM call.

    Uses Kairos providers.call_fast() for the summarization call.
    Falls back to returning original messages on any error.
    """
    split = find_split_point(messages)
    if split <= 0:
        return messages

    old = messages[:split]
    recent = messages[split:]

    old_text = ""
    for m in old:
        role = m.get("role", "?")
        content = m.get("content", "")
        if isinstance(content, str):
            old_text += f"[{role}]: {content[:500]}\n"
        elif isinstance(content, list):
            old_text += f"[{role}]: (structured content)\n"

    summary_prompt = (
        "Summarize the following conversation history concisely. "
        "Preserve key decisions, tool results, and context needed to continue."
    )
    if focus:
        summary_prompt += f"\n\nFocus especially on: {focus}"
    summary_prompt += "\n\n" + old_text

    try:
        from .providers import call_fast
        summary_text = call_fast(
            system="You are a concise summarizer.",
            user=summary_prompt,
            config=config,
        )
    except Exception:
        return messages

    if not summary_text or not summary_text.strip():
        return messages

    return [
        {"role": "user", "content": f"[Previous conversation summary]\n{summary_text}"},
        {"role": "assistant", "content": "Understood. I have the context. Let's continue."},
        *recent,
    ]


def maybe_compact(state, config: dict) -> bool:
    """Check if context window is getting full and compress if needed."""
    model = config.get("model", "")
    limit = get_context_limit(model, config)
    threshold = limit * 0.7

    if estimate_tokens(state.messages) <= threshold:
        return False

    snip_old_tool_results(state.messages)

    if estimate_tokens(state.messages) <= threshold:
        return True

    state.messages = compact_messages(state.messages, config)
    return True
