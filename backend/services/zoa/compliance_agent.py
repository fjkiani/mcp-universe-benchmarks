"""
compliance_agent.py — Regulation Navigator
Interprets regulations, generates audit docs, monitors risk.

Primary LLM: thinking (Arcee Trinity — deep reasoning for complex regulatory analysis)
"""

import json
import logging
import uuid
from datetime import date, timedelta
from typing import Any, Dict, List

from services.openrouter_service import call_llm, call_llm_with_messages
from services.zoa.context_bus import bus

logger = logging.getLogger(__name__)


class ComplianceAgent:
    """Regulation Navigator — ZOA compliance intelligence agent."""

    # ------------------------------------------------------------------
    # interpret_regulation
    # ------------------------------------------------------------------

    async def interpret_regulation(
        self,
        regulation_text: str,
        business_context: str,
    ) -> dict:
        """
        Analyse a regulation and identify applicable requirements.
        Uses thinking role for deep regulatory reasoning.
        Returns: {requirements, applicable_sections, risk_level, action_items, deadline}
        """
        prompt = (
            "You are a senior regulatory compliance counsel with expertise across "
            "GDPR, SOX, HIPAA, PCI-DSS, and international trade law. "
            "Analyse the following regulation in the context of the business described. "
            "Identify all applicable requirements, risk level, and required actions. "
            "Return JSON with keys: requirements (list of strings), "
            "applicable_sections (list of strings), "
            "risk_level (string: low|medium|high|critical), "
            "action_items (list of strings), deadline (string ISO date or 'ongoing').\n\n"
            f"Business context:\n{business_context}\n\n"
            f"Regulation text:\n{regulation_text}"
        )

        try:
            raw = await call_llm(role="thinking", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("requirements", [])
            result.setdefault("applicable_sections", [])
            result.setdefault("risk_level", "medium")
            result.setdefault("action_items", [])
            result.setdefault("deadline", "ongoing")
            return result
        except Exception as exc:
            logger.error("interpret_regulation LLM failed: %s", exc)
            return {
                "requirements": [],
                "applicable_sections": [],
                "risk_level": "unknown",
                "action_items": [f"Manual regulatory review required. Error: {exc}"],
                "deadline": "immediate",
            }

    # ------------------------------------------------------------------
    # generate_audit_doc
    # ------------------------------------------------------------------

    async def generate_audit_doc(
        self,
        audit_type: str,
        data: dict,
    ) -> dict:
        """
        Generate compliant audit documentation.
        Uses write role for professional document generation.
        Returns: {document_type, content, compliance_checklist, sign_off_required}
        """
        prompt = (
            "You are a compliance documentation specialist. "
            f"Generate a complete, audit-ready {audit_type} document. "
            "Ensure the document meets regulatory standards and includes all required sections. "
            "Return JSON with keys: document_type (string), content (string — full document), "
            "compliance_checklist (list of strings), sign_off_required (bool).\n\n"
            f"Audit data:\n{json.dumps(data, indent=2)}"
        )

        try:
            raw = await call_llm(role="write", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("document_type", audit_type)
            result.setdefault(
                "content",
                f"{audit_type} audit document. Data: {json.dumps(data)}",
            )
            result.setdefault("compliance_checklist", [])
            result.setdefault("sign_off_required", True)
            return result
        except Exception as exc:
            logger.error("generate_audit_doc LLM failed: %s", exc)
            return {
                "document_type": audit_type,
                "content": f"Document generation failed: {exc}. Manual creation required.",
                "compliance_checklist": [],
                "sign_off_required": True,
            }

    # ------------------------------------------------------------------
    # assess_risk
    # ------------------------------------------------------------------

    async def assess_risk(
        self,
        operation: str,
        jurisdiction: str,
        data: dict,
    ) -> dict:
        """
        Assess regulatory risk for a business operation in a given jurisdiction.
        Uses thinking role for deep risk analysis.
        Returns: {risk_score, risk_factors, mitigations, recommendation}
        """
        prompt = (
            "You are a regulatory risk assessment specialist. "
            f"Assess the regulatory risk of the following operation in {jurisdiction}. "
            "Consider applicable laws, enforcement history, and industry standards. "
            "Return JSON with keys: risk_score (float 0-10), "
            "risk_factors (list of strings), mitigations (list of strings), "
            "recommendation (string).\n\n"
            f"Operation: {operation}\n\n"
            f"Supporting data:\n{json.dumps(data, indent=2)}"
        )

        try:
            raw = await call_llm(role="thinking", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("risk_score", 5.0)
            result.setdefault("risk_factors", [])
            result.setdefault("mitigations", [])
            result.setdefault("recommendation", "Proceed with standard compliance controls.")
            return result
        except Exception as exc:
            logger.error("assess_risk LLM failed: %s", exc)
            return {
                "risk_score": 5.0,
                "risk_factors": [f"Risk assessment error: {exc}"],
                "mitigations": ["Manual risk review required."],
                "recommendation": (
                    "Do not proceed until manual risk assessment is complete."
                ),
            }

    # ------------------------------------------------------------------
    # handle_alert
    # ------------------------------------------------------------------

    async def handle_alert(
        self,
        alert_type: str,
        details: dict,
    ) -> dict:
        """
        Respond to a compliance alert (e.g. triggered by billing.fraud_detected).
        Uses reasoning role to determine response plan.
        Returns: {alert_id, severity, response_plan, escalation_required}
        """
        alert_id = str(uuid.uuid4())
        prompt = (
            "You are a compliance incident response specialist. "
            f"A compliance alert of type '{alert_type}' has been triggered. "
            "Determine the severity, response plan, and whether escalation is required. "
            "Return JSON with keys: alert_id (string), "
            "severity (string: low|medium|high|critical), "
            "response_plan (list of strings — ordered action steps), "
            "escalation_required (bool).\n\n"
            f"Alert details:\n{json.dumps(details, indent=2)}"
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result["alert_id"] = alert_id  # Always use our generated ID
            result.setdefault("severity", "high")
            result.setdefault(
                "response_plan",
                [
                    "Preserve all relevant records",
                    "Notify compliance officer",
                    "Initiate internal investigation",
                    "Prepare regulatory disclosure if required",
                ],
            )
            result.setdefault("escalation_required", True)
            logger.warning(
                "handle_alert: alert_id=%s type=%s severity=%s escalation=%s",
                alert_id,
                alert_type,
                result["severity"],
                result["escalation_required"],
            )
            return result
        except Exception as exc:
            logger.error("handle_alert LLM failed: %s", exc)
            return {
                "alert_id": alert_id,
                "severity": "critical",
                "response_plan": [
                    "Immediate manual review required",
                    f"Alert processing error: {exc}",
                ],
                "escalation_required": True,
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
