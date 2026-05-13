"""RefineAgent — applies critique fixes and strengthens the draft."""

import json
import logging
import re
from typing import Any

from services.openrouter_service import call_llm

logger = logging.getLogger(__name__)


class RefineAgent:
    """Applies critique feedback to produce a stronger draft using a reasoning LLM."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def improve(self, draft: str, critique: dict, tone: str) -> dict:
        """Apply all *critique* fixes to *draft* and return an improved version.

        Returns:
            {
                content: str,
                word_count: int,
                changes_made: list[str],
                new_score_estimate: float,
            }
        """
        prompt = self._build_prompt(draft, critique, tone)

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)

            if not result or "content" not in result:
                raise ValueError("LLM returned no content field")

            content = result.get("content", "")
            result.setdefault("word_count", len(content.split()))
            result.setdefault("changes_made", [])
            result.setdefault("new_score_estimate", 7.0)

            logger.info(
                "RefineAgent: refined draft — %d words, estimated score=%.1f",
                result["word_count"],
                result["new_score_estimate"],
            )
            return result

        except Exception as exc:
            logger.error("RefineAgent.improve failed: %s", exc)
            return self._fallback_refine(draft, critique)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, draft: str, critique: dict, tone: str) -> str:
        score = critique.get("score", 0)
        weaknesses = critique.get("weaknesses", [])
        specific_fixes = critique.get("specific_fixes", [])
        verdict = critique.get("verdict", "REFINE REQUIRED")

        fixes_text = "\n".join(f"  {i+1}. {fix}" for i, fix in enumerate(specific_fixes))
        weaknesses_text = "\n".join(f"  - {w}" for w in weaknesses)

        return f"""You are a master editor executing a precise revision.

CURRENT SCORE: {score}/10
VERDICT: {verdict}
REQUESTED TONE: {tone}

WEAKNESSES IDENTIFIED:
{weaknesses_text}

SPECIFIC FIXES TO APPLY (apply ALL of them — no exceptions):
{fixes_text}

CRITICAL RULES:
- Do NOT soften the tone — STRENGTHEN it.
- Apply every single fix listed above.
- If the tone is zeta_warlord: eliminate every hedge, every passive construction, every corporate-speak phrase.
- Show what changed — list each change you made.
- The revised draft must score 8+ on the rubric.

ORIGINAL DRAFT:
---
{draft}
---

Respond ONLY with valid JSON:
{{
  "content": "<the fully revised article — use \\n for newlines>",
  "word_count": <integer>,
  "changes_made": [
    "<description of change 1>",
    "<description of change 2>",
    "..."
  ],
  "new_score_estimate": <float 0.0–10.0, your honest estimate of the revised score>
}}

No markdown fences. No explanation outside the JSON."""

    def _fallback_refine(self, draft: str, critique: dict) -> dict:
        """Return the original draft with a note when the LLM call fails."""
        fixes = critique.get("specific_fixes", [])
        return {
            "content": draft,
            "word_count": len(draft.split()),
            "changes_made": [
                "RefineAgent LLM call failed — original draft preserved",
                f"Pending fixes: {len(fixes)} items from critique",
            ],
            "new_score_estimate": critique.get("score", 5.0),
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
        logger.warning("RefineAgent: could not parse JSON — wrapping raw text as content")
        return {"content": text}
