"""
payroll_agent.py — Wage Calculator
Computes pay, detects anomalies, manages compensation.

Primary LLM: code (Qwen3 Coder 480B — precise computation)
"""

import json
import logging
import uuid
from datetime import date, timedelta
from typing import Any, Dict, List

from services.openrouter_service import call_llm, call_llm_with_messages
from services.zoa.context_bus import bus

logger = logging.getLogger(__name__)


class PayrollAgent:
    """Wage Calculator — ZOA payroll intelligence agent."""

    # ------------------------------------------------------------------
    # calculate_payroll
    # ------------------------------------------------------------------

    async def calculate_payroll(
        self,
        employees: List[dict],
        period: str,
    ) -> dict:
        """
        Compute gross, deductions, net, and crypto equivalent for each employee.
        Each employee dict: {id, name, hours, rate, role, deductions}
        Returns: {period, employees: [{id, gross, deductions, net, crypto_equivalent}], total_payroll}
        """
        prompt = (
            "You are a precise payroll calculation engine. "
            f"Calculate payroll for period: {period}. "
            "For each employee compute: gross = hours * rate, "
            "net = gross - deductions, crypto_equivalent = net / 65000 (BTC approximation). "
            "Return JSON with keys: period (string), "
            "employees (list of {id, gross, deductions, net, crypto_equivalent}), "
            "total_payroll (float).\n\n"
            f"Employees:\n{json.dumps(employees, indent=2)}"
        )

        try:
            raw = await call_llm(role="code", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("period", period)
            result.setdefault("employees", [])
            result.setdefault("total_payroll", 0.0)
            return result
        except Exception as exc:
            logger.error("calculate_payroll LLM failed: %s — computing locally", exc)
            computed = []
            total = 0.0
            for emp in employees:
                gross = float(emp.get("hours", 0)) * float(emp.get("rate", 0))
                deductions = float(emp.get("deductions", 0))
                net = gross - deductions
                total += net
                computed.append({
                    "id": emp.get("id"),
                    "gross": round(gross, 2),
                    "deductions": round(deductions, 2),
                    "net": round(net, 2),
                    "crypto_equivalent": round(net / 65000, 8),
                })
            return {
                "period": period,
                "employees": computed,
                "total_payroll": round(total, 2),
            }

    # ------------------------------------------------------------------
    # detect_anomaly
    # ------------------------------------------------------------------

    async def detect_anomaly(
        self,
        employee_id: str,
        metrics: dict,
    ) -> dict:
        """
        Flag performance/productivity anomalies.
        metrics: {hours_logged, commits, tasks_completed, response_time_avg}
        Returns: {anomaly_detected, severity, flags, recommended_action}
        """
        prompt = (
            "You are a workforce analytics specialist. "
            f"Analyse the following productivity metrics for employee {employee_id} "
            "and identify any anomalies (unusually low output, excessive hours, "
            "poor response times, etc.). "
            "Return JSON with keys: anomaly_detected (bool), "
            "severity (string: low|medium|high|critical), "
            "flags (list of strings), recommended_action (string).\n\n"
            f"Metrics:\n{json.dumps(metrics, indent=2)}"
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("anomaly_detected", False)
            result.setdefault("severity", "low")
            result.setdefault("flags", [])
            result.setdefault("recommended_action", "No action required.")
            return result
        except Exception as exc:
            logger.error("detect_anomaly LLM failed: %s", exc)
            return {
                "anomaly_detected": False,
                "severity": "unknown",
                "flags": [f"Analysis error: {exc}"],
                "recommended_action": "Manual review required.",
            }

    # ------------------------------------------------------------------
    # hold_commission
    # ------------------------------------------------------------------

    async def hold_commission(
        self,
        employee_id: str,
        reason: str,
    ) -> dict:
        """
        Place a hold on an employee's commission.
        Triggered by context_bus from billing.payment_overdue.
        Returns: {employee_id, commission_held, amount, reason, release_condition}
        """
        logger.info(
            "hold_commission triggered for employee_id=%s reason=%s",
            employee_id,
            reason,
        )
        try:
            return {
                "employee_id": employee_id,
                "commission_held": True,
                "amount": 0.0,  # Actual amount resolved from payroll records at runtime
                "reason": reason,
                "release_condition": "Payment received and cleared by billing team.",
            }
        except Exception as exc:
            logger.error("hold_commission failed: %s", exc)
            return {
                "employee_id": employee_id,
                "commission_held": False,
                "amount": 0.0,
                "reason": reason,
                "release_condition": "Error — manual intervention required.",
            }

    # ------------------------------------------------------------------
    # review_compensation
    # ------------------------------------------------------------------

    async def review_compensation(
        self,
        employee_id: str,
        performance_data: dict,
    ) -> dict:
        """
        Recommend compensation adjustment based on performance data.
        Returns: {current_comp, recommended_comp, rationale, effective_date}
        """
        effective_date = (date.today() + timedelta(days=30)).isoformat()
        prompt = (
            "You are a compensation strategy specialist. "
            f"Review the compensation for employee {employee_id} "
            "based on the following performance data and recommend an adjustment. "
            "Return JSON with keys: current_comp (float), recommended_comp (float), "
            "rationale (string), effective_date (string ISO date).\n\n"
            f"Performance data:\n{json.dumps(performance_data, indent=2)}"
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("current_comp", performance_data.get("current_comp", 0.0))
            result.setdefault("recommended_comp", performance_data.get("current_comp", 0.0))
            result.setdefault("rationale", "Based on performance review.")
            result.setdefault("effective_date", effective_date)
            return result
        except Exception as exc:
            logger.error("review_compensation LLM failed: %s", exc)
            return {
                "current_comp": performance_data.get("current_comp", 0.0),
                "recommended_comp": performance_data.get("current_comp", 0.0),
                "rationale": f"Automated review failed: {exc}. Manual review required.",
                "effective_date": effective_date,
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
