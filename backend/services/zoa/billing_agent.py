"""
billing_agent.py — Invoice Reaver
Processes invoices, chases payments, detects fraud.

Primary LLM  : vision  (Gemma 4 26B — multimodal, handles PDFs/images)
Fallback LLM : reasoning
"""

import json
import logging
import uuid
from typing import Any, Dict, List

from services.openrouter_service import call_llm, call_llm_with_messages
from services.zoa.context_bus import bus

logger = logging.getLogger(__name__)


class BillingAgent:
    """Invoice Reaver — ZOA billing intelligence agent."""

    # ------------------------------------------------------------------
    # process_invoice
    # ------------------------------------------------------------------

    async def process_invoice(self, invoice_data: dict) -> dict:
        """
        Extract line items, validate amounts, flag anomalies from invoice data.
        Uses vision role; falls back to reasoning on error.
        Returns: {invoice_id, line_items, total, status, anomalies, confidence}
        """
        prompt = (
            "You are an expert accounts-receivable analyst. "
            "Analyse the following invoice data and return a JSON object with keys: "
            "invoice_id, line_items (list of {description, qty, unit_price, amount}), "
            "total (float), status (string: valid|invalid|needs_review), "
            "anomalies (list of strings), confidence (float 0-1).\n\n"
            f"Invoice data:\n{json.dumps(invoice_data, indent=2)}"
        )

        try:
            raw = await call_llm(role="vision", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("invoice_id", invoice_data.get("invoice_id", str(uuid.uuid4())))
            result.setdefault("line_items", [])
            result.setdefault("total", 0.0)
            result.setdefault("status", "needs_review")
            result.setdefault("anomalies", [])
            result.setdefault("confidence", 0.5)
            return result
        except Exception as exc:
            logger.warning("process_invoice vision failed (%s), falling back to reasoning", exc)
            try:
                raw = await call_llm(role="reasoning", prompt=prompt)
                result = self._parse_json_response(raw)
                result.setdefault("invoice_id", invoice_data.get("invoice_id", str(uuid.uuid4())))
                result.setdefault("line_items", [])
                result.setdefault("total", 0.0)
                result.setdefault("status", "needs_review")
                result.setdefault("anomalies", [])
                result.setdefault("confidence", 0.4)
                return result
            except Exception as exc2:
                logger.error("process_invoice fallback also failed: %s", exc2)
                return {
                    "invoice_id": invoice_data.get("invoice_id", "unknown"),
                    "line_items": [],
                    "total": 0.0,
                    "status": "error",
                    "anomalies": [str(exc2)],
                    "confidence": 0.0,
                }

    # ------------------------------------------------------------------
    # chase_payment
    # ------------------------------------------------------------------

    async def chase_payment(
        self, invoice_id: str, days_overdue: int, client_name: str
    ) -> dict:
        """
        Generate a firm (not threatening) payment follow-up message.
        Publishes billing.payment_overdue to context_bus if days_overdue > 30.
        Returns: {message, escalation_level, next_action}
        """
        escalation_level = (
            "critical" if days_overdue > 60
            else "high" if days_overdue > 30
            else "medium" if days_overdue > 14
            else "low"
        )

        prompt = (
            "You are a professional accounts-receivable specialist. "
            f"Write a firm but polite payment follow-up email for invoice {invoice_id}. "
            f"The invoice is {days_overdue} days overdue. Client: {client_name}. "
            f"Escalation level: {escalation_level}. "
            "Return JSON with keys: message (string), escalation_level (string), next_action (string)."
        )

        try:
            raw = await call_llm(role="write", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("message", raw if isinstance(raw, str) else "Payment follow-up sent.")
            result.setdefault("escalation_level", escalation_level)
            result.setdefault("next_action", "await_response")
        except Exception as exc:
            logger.error("chase_payment LLM failed: %s", exc)
            result = {
                "message": (
                    f"Dear {client_name}, invoice {invoice_id} is {days_overdue} days overdue. "
                    "Please arrange payment at your earliest convenience."
                ),
                "escalation_level": escalation_level,
                "next_action": "manual_follow_up",
            }

        if days_overdue > 30:
            try:
                await bus.publish(
                    "billing.payment_overdue",
                    {
                        "invoice_id": invoice_id,
                        "days_overdue": days_overdue,
                        "client_name": client_name,
                        "escalation_level": escalation_level,
                    },
                )
                logger.info("Published billing.payment_overdue for invoice %s", invoice_id)
            except Exception as exc:
                logger.error("Failed to publish billing.payment_overdue: %s", exc)

        return result

    # ------------------------------------------------------------------
    # detect_fraud
    # ------------------------------------------------------------------

    async def detect_fraud(self, invoice_data: dict) -> dict:
        """
        Analyse invoice patterns for fraud signals.
        Publishes billing.fraud_detected if confidence > 0.8.
        Returns: {is_fraud, confidence, flags, recommendation}
        """
        prompt = (
            "You are a forensic accounts analyst specialising in invoice fraud detection. "
            "Analyse the following invoice data for fraud indicators (duplicate billing, "
            "inflated amounts, fictitious vendors, round-number anomalies, etc.). "
            "Return JSON with keys: is_fraud (bool), confidence (float 0-1), "
            "flags (list of strings), recommendation (string).\n\n"
            f"Invoice data:\n{json.dumps(invoice_data, indent=2)}"
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("is_fraud", False)
            result.setdefault("confidence", 0.0)
            result.setdefault("flags", [])
            result.setdefault("recommendation", "No action required.")
        except Exception as exc:
            logger.error("detect_fraud LLM failed: %s", exc)
            result = {
                "is_fraud": False,
                "confidence": 0.0,
                "flags": [f"LLM error: {exc}"],
                "recommendation": "Manual review required due to analysis failure.",
            }

        if result.get("confidence", 0.0) > 0.8:
            try:
                await bus.publish(
                    "billing.fraud_detected",
                    {
                        "invoice_id": invoice_data.get("invoice_id", "unknown"),
                        "confidence": result["confidence"],
                        "flags": result.get("flags", []),
                    },
                )
                logger.warning(
                    "Published billing.fraud_detected for invoice %s (confidence=%.2f)",
                    invoice_data.get("invoice_id", "unknown"),
                    result["confidence"],
                )
            except Exception as exc:
                logger.error("Failed to publish billing.fraud_detected: %s", exc)

        return result

    # ------------------------------------------------------------------
    # generate_invoice
    # ------------------------------------------------------------------

    async def generate_invoice(self, contract_data: dict) -> dict:
        """
        Generate a structured invoice JSON from contract data.
        Uses code role for precise structured output.
        Returns: {invoice_json, pdf_ready, line_items, total}
        """
        prompt = (
            "You are an expert billing engineer. "
            "Given the following contract data, generate a complete, structured invoice as JSON. "
            "Return JSON with keys: invoice_json (object), pdf_ready (bool), "
            "line_items (list of {description, qty, unit_price, amount}), total (float).\n\n"
            f"Contract data:\n{json.dumps(contract_data, indent=2)}"
        )

        try:
            raw = await call_llm(role="code", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("invoice_json", {})
            result.setdefault("pdf_ready", False)
            result.setdefault("line_items", [])
            result.setdefault("total", 0.0)
            return result
        except Exception as exc:
            logger.error("generate_invoice LLM failed: %s", exc)
            return {
                "invoice_json": {},
                "pdf_ready": False,
                "line_items": [],
                "total": 0.0,
            }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_json_response(raw: Any) -> dict:
        """Attempt to parse a JSON dict from an LLM response string."""
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
