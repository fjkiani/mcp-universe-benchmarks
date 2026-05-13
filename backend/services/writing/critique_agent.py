"""CritiqueAgent — ruthlessly evaluates a draft against a 5-dimension rubric."""

import json
import logging
import re
from typing import Any

from services.openrouter_service import call_llm

logger = logging.getLogger(__name__)

_RUBRIC = """
SCORING RUBRIC (each dimension: 0–2 points, total max 10):

1. CLARITY (0–2): Is the central argument crystal clear from start to finish?
   0 = reader has no idea what the point is
   1 = argument is present but muddled
   2 = argument is unmistakable on first read

2. EVIDENCE (0–2): Are claims backed by specifics — numbers, examples, case studies?
   0 = pure assertion, zero evidence
   1 = some evidence but mostly vague
   2 = every major claim has a concrete backing

3. TONE CONSISTENCY (0–2): Does the piece match the requested tone throughout?
   0 = completely wrong tone (e.g., zeta_warlord that reads like a corporate memo = 0)
   1 = tone present but inconsistent
   2 = tone locked in from first word to last

4. HOOK STRENGTH (0–2): Does the opening demand attention?
   0 = generic, forgettable opener
   1 = decent but not compelling
   2 = reader cannot stop reading after the first line

5. ACTIONABILITY (0–2): Does the reader know exactly what to do or think after reading?
   0 = no clear takeaway
   1 = vague direction
   2 = crystal-clear next step or position

PASS THRESHOLD: 8/10. Below 8 = must refine.
SPECIAL RULE: Any zeta_warlord piece that sounds like a corporate memo scores maximum 2/10 on tone consistency.
"""


class CritiqueAgent:
    """Evaluates drafts using a thinking LLM with a strict 5-dimension rubric."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def evaluate(self, draft: str, tone: str) -> dict:
        """Score *draft* against the rubric for the requested *tone*.

        Returns:
            {
                score: float,          # 0–10
                strengths: list[str],
                weaknesses: list[str],
                specific_fixes: list[str],
                verdict: str,
            }
        """
        prompt = self._build_prompt(draft, tone)

        try:
            raw = await call_llm(role="thinking", prompt=prompt)
            result = self._parse_json_response(raw)

            if not result or "score" not in result:
                raise ValueError("LLM returned incomplete critique structure")

            # Clamp score to valid range
            result["score"] = max(0.0, min(10.0, float(result.get("score", 0))))
            result.setdefault("strengths", [])
            result.setdefault("weaknesses", [])
            result.setdefault("specific_fixes", [])
            result.setdefault(
                "verdict",
                "PASS" if result["score"] >= 8 else "REFINE REQUIRED",
            )

            logger.info(
                "CritiqueAgent: score=%.1f verdict=%s tone=%r",
                result["score"],
                result["verdict"],
                tone,
            )
            return result

        except Exception as exc:
            logger.error("CritiqueAgent.evaluate failed: %s", exc)
            return self._fallback_critique()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, draft: str, tone: str) -> str:
        return f"""You are a brutal, uncompromising editor. Your job is to find every flaw.

REQUESTED TONE: {tone}

{_RUBRIC}

DRAFT TO EVALUATE:
---
{draft}
---

Score each dimension honestly. Be harsh. A mediocre piece that almost passes is still a failure.
Provide SPECIFIC fixes — not "improve the hook" but "replace the opening line with X because Y".

Respond ONLY with valid JSON:
{{
  "score": <float 0.0–10.0, sum of all 5 dimension scores>,
  "dimension_scores": {{
    "clarity": <0–2>,
    "evidence": <0–2>,
    "tone_consistency": <0–2>,
    "hook_strength": <0–2>,
    "actionability": <0–2>
  }},
  "strengths": ["<what works>", "..."],
  "weaknesses": ["<what fails>", "..."],
  "specific_fixes": [
    "<exact actionable fix 1>",
    "<exact actionable fix 2>",
    "..."
  ],
  "verdict": "<PASS or REFINE REQUIRED — with one sentence explanation>"
}}

No markdown fences. No explanation outside the JSON."""

    @staticmethod
    def _fallback_critique() -> dict:
        return {
            "score": 5.0,
            "dimension_scores": {
                "clarity": 1,
                "evidence": 1,
                "tone_consistency": 1,
                "hook_strength": 1,
                "actionability": 1,
            },
            "strengths": ["Draft exists and covers the topic"],
            "weaknesses": [
                "Critique agent failed — manual review required",
                "Score defaulted to 5.0 (below pass threshold)",
            ],
            "specific_fixes": [
                "Re-run critique agent",
                "Manually review tone consistency",
                "Verify all claims have concrete evidence",
            ],
            "verdict": "REFINE REQUIRED — critique agent encountered an error; defaulting to fail-safe score",
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

        logger.warning("CritiqueAgent: could not parse JSON from LLM response")
        return {}
