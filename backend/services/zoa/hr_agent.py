"""
hr_agent.py — Talent Optimizer
Screens candidates, manages performance, handles exits.

Primary LLM: reasoning (Hermes 3 405B)
"""

import json
import logging
import uuid
from datetime import date, timedelta
from typing import Any, Dict, List

from services.openrouter_service import call_llm, call_llm_with_messages
from services.zoa.context_bus import bus

logger = logging.getLogger(__name__)


class HRAgent:
    """Talent Optimizer — ZOA human-resources intelligence agent."""

    # ------------------------------------------------------------------
    # screen_resume
    # ------------------------------------------------------------------

    async def screen_resume(
        self,
        resume_text: str,
        role_requirements: dict,
    ) -> dict:
        """
        Score a candidate against role requirements.
        Returns: {candidate_score, strengths, gaps, recommendation, interview_questions}
        """
        prompt = (
            "You are a senior talent acquisition specialist. "
            "Evaluate the following resume against the role requirements. "
            "Return JSON with keys: candidate_score (float 0-100), "
            "strengths (list of strings), gaps (list of strings), "
            "recommendation (string: strong_yes|yes|maybe|no), "
            "interview_questions (list of strings — 5 targeted questions).\n\n"
            f"Role requirements:\n{json.dumps(role_requirements, indent=2)}\n\n"
            f"Resume:\n{resume_text}"
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("candidate_score", 0.0)
            result.setdefault("strengths", [])
            result.setdefault("gaps", [])
            result.setdefault("recommendation", "maybe")
            result.setdefault("interview_questions", [])
            return result
        except Exception as exc:
            logger.error("screen_resume LLM failed: %s", exc)
            return {
                "candidate_score": 0.0,
                "strengths": [],
                "gaps": [f"Screening error: {exc}"],
                "recommendation": "manual_review",
                "interview_questions": [],
            }

    # ------------------------------------------------------------------
    # conduct_performance_review
    # ------------------------------------------------------------------

    async def conduct_performance_review(
        self,
        employee_id: str,
        metrics: dict,
        period: str,
    ) -> dict:
        """
        Generate a structured performance review.
        Returns: {rating, strengths, improvement_areas, goals, compensation_recommendation}
        """
        prompt = (
            "You are an experienced HR business partner. "
            f"Conduct a structured performance review for employee {employee_id} "
            f"for period {period}. "
            "Return JSON with keys: rating (string: exceptional|exceeds|meets|below|unsatisfactory), "
            "strengths (list of strings), improvement_areas (list of strings), "
            "goals (list of strings — 3 SMART goals for next period), "
            "compensation_recommendation (string).\n\n"
            f"Performance metrics:\n{json.dumps(metrics, indent=2)}"
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("rating", "meets")
            result.setdefault("strengths", [])
            result.setdefault("improvement_areas", [])
            result.setdefault("goals", [])
            result.setdefault("compensation_recommendation", "Maintain current compensation.")
            return result
        except Exception as exc:
            logger.error("conduct_performance_review LLM failed: %s", exc)
            return {
                "rating": "unknown",
                "strengths": [],
                "improvement_areas": [],
                "goals": [],
                "compensation_recommendation": (
                    f"Review failed: {exc}. Manual assessment required."
                ),
            }

    # ------------------------------------------------------------------
    # process_exit
    # ------------------------------------------------------------------

    async def process_exit(
        self,
        employee_id: str,
        reason: str,
    ) -> dict:
        """
        Generate exit documentation, knowledge transfer items, and offboarding checklist.
        Returns: {exit_report, knowledge_transfer_items, offboarding_checklist}
        """
        prompt = (
            "You are an HR specialist handling employee offboarding. "
            f"Generate comprehensive exit documentation for employee {employee_id}. "
            f"Reason for departure: {reason}. "
            "Return JSON with keys: exit_report (string), "
            "knowledge_transfer_items (list of strings), "
            "offboarding_checklist (list of strings)."
        )

        try:
            raw = await call_llm(role="write", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault(
                "exit_report",
                f"Exit report for employee {employee_id}. Reason: {reason}.",
            )
            result.setdefault("knowledge_transfer_items", [])
            result.setdefault(
                "offboarding_checklist",
                [
                    "Return company equipment",
                    "Revoke system access",
                    "Complete exit interview",
                    "Process final payroll",
                ],
            )
            return result
        except Exception as exc:
            logger.error("process_exit LLM failed: %s", exc)
            return {
                "exit_report": (
                    f"Exit report for {employee_id}. Reason: {reason}. "
                    "(Auto-generation failed.)"
                ),
                "knowledge_transfer_items": [],
                "offboarding_checklist": [
                    "Return company equipment",
                    "Revoke system access",
                    "Complete exit interview",
                    "Process final payroll",
                ],
            }

    # ------------------------------------------------------------------
    # flag_performance
    # ------------------------------------------------------------------

    async def flag_performance(
        self,
        employee_id: str,
        issue: str,
    ) -> dict:
        """
        Raise a performance flag and publish hr.performance_flag to context_bus.
        Returns: {flag_id, employee_id, issue, severity, next_review_date}
        """
        flag_id = str(uuid.uuid4())
        next_review_date = (date.today() + timedelta(days=30)).isoformat()

        issue_lower = issue.lower()
        if any(w in issue_lower for w in ["termination", "gross misconduct", "fraud", "harassment"]):
            severity = "critical"
        elif any(w in issue_lower for w in ["repeated", "persistent", "pattern", "multiple"]):
            severity = "high"
        elif any(w in issue_lower for w in ["missed", "late", "below target"]):
            severity = "medium"
        else:
            severity = "low"

        try:
            await bus.publish(
                "hr.performance_flag",
                {
                    "flag_id": flag_id,
                    "employee_id": employee_id,
                    "issue": issue,
                    "severity": severity,
                    "next_review_date": next_review_date,
                },
            )
            logger.info(
                "Published hr.performance_flag for employee_id=%s flag_id=%s",
                employee_id,
                flag_id,
            )
        except Exception as exc:
            logger.error("flag_performance publish failed: %s", exc)

        return {
            "flag_id": flag_id,
            "employee_id": employee_id,
            "issue": issue,
            "severity": severity,
            "next_review_date": next_review_date,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_json_response(raw: Any) -> dict:
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str):
            text = raw.strip()
            if text.startswith("```"):
                lines = text.splitlines()
                text = "\n".join(
                    line for line in lines if not line.startswith("```")
                ).strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start != -1 and end > start:
                    return json.loads(text[start:end])
        return {}
