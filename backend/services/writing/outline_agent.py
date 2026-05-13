"""OutlineAgent — builds a battle-plan outline for ZOA-W writing pipeline."""

import json
import logging
import re
from typing import Any

from services.openrouter_service import call_llm

logger = logging.getLogger(__name__)

_TONE_DESCRIPTIONS = {
    "zeta_warlord": (
        "ZETA WARLORD: aggressive, data-driven, no apologies. "
        "Every sentence hits like a hammer. No hedging. No passive voice. "
        "Concrete numbers and examples only. Demand action."
    ),
    "professional": (
        "PROFESSIONAL: authoritative, evidence-based. "
        "Credible, measured, backed by data. Commands respect without shouting."
    ),
    "technical": (
        "TECHNICAL: precise, jargon-acceptable. "
        "Accuracy over accessibility. Assume a knowledgeable audience. "
        "Define terms once, then use them freely."
    ),
    "satirical": (
        "SATIRICAL: sharp wit, expose absurdity. "
        "Use irony and exaggeration to make the point land harder than a straight argument. "
        "Funny but devastating."
    ),
}


class OutlineAgent:
    """Generates a structured battle-plan outline using a reasoning LLM."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate(self, topic: str, tone: str) -> dict:
        """Generate a full outline for *topic* in the requested *tone*.

        Returns:
            {
                title: str,
                hook: str,
                sections: [{heading, key_points: list[str], word_count_target: int}],
                total_word_count: int,
                tone_notes: str,
            }
        """
        tone_desc = _TONE_DESCRIPTIONS.get(tone, _TONE_DESCRIPTIONS["professional"])
        prompt = self._build_prompt(topic, tone, tone_desc)

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            if not result or "sections" not in result:
                raise ValueError("LLM returned incomplete outline structure")
            logger.info("OutlineAgent: outline generated for topic=%r tone=%r", topic, tone)
            return result
        except Exception as exc:
            logger.error("OutlineAgent.generate failed: %s", exc)
            return self._fallback_outline(topic, tone, tone_desc)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, topic: str, tone: str, tone_desc: str) -> str:
        return f"""You are a master content strategist building a battle-plan outline.

TOPIC: {topic}
TONE: {tone_desc}

Your job: produce a razor-sharp outline that will guide a writer to create a piece that cannot be ignored.

Requirements:
1. A killer HOOK — the opening line that stops the reader cold.
2. 4–6 SECTIONS, each with:
   - A punchy heading
   - 3–5 specific key points (not vague — concrete, actionable, or provocative)
   - A word count target (realistic for the depth needed)
3. TONE NOTES — specific instructions for the writer on how to execute this tone for this topic.
4. TOTAL WORD COUNT — sum of all section targets.

Respond ONLY with valid JSON matching this exact schema:
{{
  "title": "<compelling article title>",
  "hook": "<the killer opening line>",
  "sections": [
    {{
      "heading": "<section heading>",
      "key_points": ["<point 1>", "<point 2>", "<point 3>"],
      "word_count_target": <integer>
    }}
  ],
  "total_word_count": <integer>,
  "tone_notes": "<specific writer instructions for this tone + topic combo>"
}}

No markdown fences. No explanation. Pure JSON only."""

    def _fallback_outline(self, topic: str, tone: str, tone_desc: str) -> dict:
        return {
            "title": f"The Definitive Take on {topic}",
            "hook": f"Everything you think you know about {topic} is wrong.",
            "sections": [
                {
                    "heading": "The Problem Nobody Wants to Admit",
                    "key_points": [
                        f"The conventional wisdom on {topic} is broken",
                        "Three data points that prove it",
                        "Who benefits from the status quo",
                    ],
                    "word_count_target": 300,
                },
                {
                    "heading": "What the Evidence Actually Shows",
                    "key_points": [
                        "Primary research findings",
                        "Case studies that contradict the narrative",
                        "The numbers they don't want you to see",
                    ],
                    "word_count_target": 400,
                },
                {
                    "heading": "The Path Forward",
                    "key_points": [
                        "Concrete step 1",
                        "Concrete step 2",
                        "What success looks like",
                    ],
                    "word_count_target": 300,
                },
            ],
            "total_word_count": 1000,
            "tone_notes": tone_desc,
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

        logger.warning("OutlineAgent: could not parse JSON from LLM response")
        return {}
