"""PublishAgent — formats content for a target publishing platform."""

import json
import logging
import re
from typing import Any

from services.openrouter_service import call_llm

logger = logging.getLogger(__name__)

_PLATFORM_RULES = {
    "medium": (
        "FORMAT FOR MEDIUM:\n"
        "- Use ## for section headers (H2)\n"
        "- Add pull quotes using > blockquote syntax for the 2–3 most powerful lines\n"
        "- Include 3–5 relevant tags in the hashtags field\n"
        "- subject_line is null (Medium uses the title)\n"
        "- End with a clear CTA (follow, clap, respond)"
    ),
    "linkedin": (
        "FORMAT FOR LINKEDIN:\n"
        "- Max 1300 characters visible before 'see more' — hook MUST be in the first line\n"
        "- NO markdown headers (no ##, no **bold headers**)\n"
        "- Short paragraphs (1–3 lines max)\n"
        "- 3–5 relevant hashtags at the end\n"
        "- subject_line is null\n"
        "- End with a question or CTA that drives comments"
    ),
    "blog": (
        "FORMAT FOR BLOG:\n"
        "- Full markdown: ## headers, **bold**, *italic*, bullet lists\n"
        "- Add an SEO meta description (150–160 chars) as the first line: <!-- META: ... -->\n"
        "- Insert internal link placeholders as [LINK: relevant-topic] where appropriate\n"
        "- subject_line is null\n"
        "- End with a CTA section"
    ),
    "cold_email": (
        "FORMAT FOR COLD EMAIL:\n"
        "- Subject line: punchy, specific, under 60 chars — goes in subject_line field\n"
        "- Body: 150 words MAX. No fluff. No 'I hope this email finds you well'.\n"
        "- One clear CTA — a specific ask (book a call, reply with X, click this link)\n"
        "- No markdown formatting in the body\n"
        "- hashtags is an empty list"
    ),
}


class PublishAgent:
    """Formats content for a specific publishing platform using a fast LLM."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def format(self, content: str, platform: str) -> dict:
        """Format *content* for the target *platform*.

        Returns:
            {
                formatted_content: str,
                platform: str,
                char_count: int,
                word_count: int,
                hashtags: list[str],
                subject_line: str | None,
                cta: str,
            }
        """
        platform = platform.lower().strip()
        if platform not in _PLATFORM_RULES:
            logger.warning("PublishAgent: unknown platform %r — defaulting to blog", platform)
            platform = "blog"

        prompt = self._build_prompt(content, platform)

        try:
            raw = await call_llm(role="fast", prompt=prompt)
            result = self._parse_json_response(raw)

            if not result or "formatted_content" not in result:
                raise ValueError("LLM returned no formatted_content field")

            formatted = result.get("formatted_content", content)
            result["platform"] = platform
            result.setdefault("char_count", len(formatted))
            result.setdefault("word_count", len(formatted.split()))
            result.setdefault("hashtags", [])
            result.setdefault("subject_line", None)
            result.setdefault("cta", "")

            logger.info(
                "PublishAgent: formatted for %s — %d chars, %d words",
                platform,
                result["char_count"],
                result["word_count"],
            )
            return result

        except Exception as exc:
            logger.error("PublishAgent.format failed: %s", exc)
            return self._fallback_format(content, platform)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, content: str, platform: str) -> str:
        rules = _PLATFORM_RULES[platform]
        return f"""You are a platform-specialist editor. Your job: reformat this content perfectly for {platform.upper()}.

{rules}

ORIGINAL CONTENT:
---
{content}
---

Reformat the content following ALL rules above. Preserve the core message and tone.

Respond ONLY with valid JSON:
{{
  "formatted_content": "<the reformatted content — use \\n for newlines>",
  "platform": "{platform}",
  "char_count": <integer>,
  "word_count": <integer>,
  "hashtags": ["<tag1>", "<tag2>", "..."],
  "subject_line": <"<subject>" or null>,
  "cta": "<the call-to-action text>"
}}

No markdown fences. No explanation outside the JSON."""

    def _fallback_format(self, content: str, platform: str) -> dict:
        """Return minimally-formatted content when the LLM call fails."""
        hashtags: list[str] = []
        subject_line = None
        cta = "Read more."

        if platform == "linkedin":
            hashtags = ["#content", "#writing", "#insights"]
            cta = "What do you think? Drop a comment below."
        elif platform == "medium":
            hashtags = ["writing", "content", "insights"]
            cta = "Follow for more. Clap if this resonated."
        elif platform == "cold_email":
            subject_line = "Quick question"
            cta = "Worth a 15-minute call?"
        elif platform == "blog":
            cta = "Subscribe for more insights."

        return {
            "formatted_content": content,
            "platform": platform,
            "char_count": len(content),
            "word_count": len(content.split()),
            "hashtags": hashtags,
            "subject_line": subject_line,
            "cta": cta,
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

        logger.warning("PublishAgent: could not parse JSON from LLM response")
        return {}
