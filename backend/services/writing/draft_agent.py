"""DraftAgent — writes the full article draft from an outline."""

import json
import logging
import re
from typing import Any

from services.openrouter_service import call_llm

logger = logging.getLogger(__name__)


class DraftAgent:
    """Writes a complete draft from an outline using a write-optimised LLM."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def write(self, outline: dict, tone: str) -> dict:
        """Write a full draft from *outline* in the requested *tone*.

        Returns:
            {
                content: str,
                word_count: int,
                sections_written: int,
                tone_applied: str,
            }
        """
        prompt = self._build_prompt(outline, tone)

        try:
            raw = await call_llm(role="write", prompt=prompt)
            result = self._parse_json_response(raw)

            if not result or "content" not in result:
                raise ValueError("LLM returned no content field")

            content = result.get("content", "")
            result.setdefault("word_count", len(content.split()))
            result.setdefault("sections_written", len(outline.get("sections", [])))
            result.setdefault("tone_applied", tone)

            logger.info(
                "DraftAgent: draft written — %d words, %d sections",
                result["word_count"],
                result["sections_written"],
            )
            return result

        except Exception as exc:
            logger.error("DraftAgent.write failed: %s", exc)
            return self._fallback_draft(outline, tone)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, outline: dict, tone: str) -> str:
        sections_text = ""
        for i, sec in enumerate(outline.get("sections", []), 1):
            points = "\n".join(f"  - {p}" for p in sec.get("key_points", []))
            sections_text += (
                f"\nSection {i}: {sec.get('heading', 'Untitled')}\n"
                f"Key points:\n{points}\n"
                f"Target words: {sec.get('word_count_target', 300)}\n"
            )

        tone_instructions = self._tone_instructions(tone, outline.get("tone_notes", ""))

        return f"""You are an elite writer executing a battle-plan outline.

TITLE: {outline.get('title', 'Untitled')}
HOOK: {outline.get('hook', '')}
TONE: {tone}

TONE EXECUTION RULES:
{tone_instructions}

OUTLINE:
{sections_text}

Write the COMPLETE article now. Start with the hook. Cover every section. Hit the word count targets.

Respond ONLY with valid JSON:
{{
  "content": "<the full article text — use \\n for newlines>",
  "word_count": <integer>,
  "sections_written": <integer>,
  "tone_applied": "{tone}"
}}

No markdown fences around the JSON. No explanation outside the JSON."""

    @staticmethod
    def _tone_instructions(tone: str, tone_notes: str) -> str:
        base = {
            "zeta_warlord": (
                "- ZERO hedging. Never write 'it could be argued', 'perhaps', 'might', 'some say'.\n"
                "- Active voice ONLY. Subject → verb → object. Always.\n"
                "- Every claim gets a concrete example or number. No vague assertions.\n"
                "- End with a call to action that DEMANDS a response — not 'consider this' but 'do this now'.\n"
                "- If it sounds like a corporate memo, rewrite it. Burn the memo."
            ),
            "professional": (
                "- Authoritative and evidence-based. Every major claim cites a source or data point.\n"
                "- Measured tone — confident without being aggressive.\n"
                "- Clear structure: state the point, support it, move on.\n"
                "- End with a clear recommendation or takeaway."
            ),
            "technical": (
                "- Precision over accessibility. Use correct terminology.\n"
                "- Define technical terms on first use, then use freely.\n"
                "- Include specifics: versions, metrics, thresholds, formulas where relevant.\n"
                "- Assume a knowledgeable audience — don't over-explain basics."
            ),
            "satirical": (
                "- Use irony and exaggeration to expose absurdity.\n"
                "- The joke should make the argument land harder than a straight take.\n"
                "- Funny but devastating — the reader should laugh, then feel the sting.\n"
                "- Don't break character to explain the joke."
            ),
        }.get(tone, "- Match the tone described in the tone notes below.")

        if tone_notes:
            base += f"\n\nAdditional tone notes from outline:\n{tone_notes}"
        return base

    def _fallback_draft(self, outline: dict, tone: str) -> dict:
        hook = outline.get("hook", "")
        sections = outline.get("sections", [])

        parts = [hook, ""]
        for sec in sections:
            parts.append(f"## {sec.get('heading', 'Section')}")
            for point in sec.get("key_points", []):
                parts.append(f"{point}.")
            parts.append("")

        content = "\n".join(parts)
        return {
            "content": content,
            "word_count": len(content.split()),
            "sections_written": len(sections),
            "tone_applied": tone,
        }

    @staticmethod
    def _parse_json_response(raw: Any) -> dict:
        """Extract JSON from LLM output — handles fences, raw JSON, substring."""
        if isinstance(raw, dict):
            return raw

        text = str(raw).strip()

        # Strip markdown code fences
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if fence_match:
            text = fence_match.group(1).strip()

        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON object substring
        obj_match = re.search(r"\{[\s\S]*\}", text)
        if obj_match:
            try:
                return json.loads(obj_match.group(0))
            except json.JSONDecodeError:
                pass

        # Last resort: treat entire response as content
        logger.warning("DraftAgent: could not parse JSON — wrapping raw text as content")
        return {"content": text}
