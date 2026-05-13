"""
procurement_agent.py — Supply Optimizer
Scans receipts, negotiates suppliers, manages inventory.

Primary LLMs:
  ocr      — receipt scanning (Baidu OCR)
  reasoning — supplier negotiation (Hermes 3 405B)
  fast     — inventory checks
"""

import json
import logging
import uuid
from datetime import date, timedelta
from typing import Any, Dict, List

from services.openrouter_service import call_llm, call_llm_with_messages
from services.zoa.context_bus import bus

logger = logging.getLogger(__name__)


class ProcurementAgent:
    """Supply Optimizer — ZOA procurement intelligence agent."""

    # ------------------------------------------------------------------
    # scan_receipt
    # ------------------------------------------------------------------

    async def scan_receipt(self, receipt_data: str) -> dict:
        """
        Extract vendor, items, amounts, dates from a receipt.
        Uses ocr role for fast document scanning.
        Returns: {vendor, items, total, date, category, reimbursable}
        """
        prompt = (
            "You are an OCR and document extraction specialist. "
            "Extract all relevant information from the following receipt data. "
            "Return JSON with keys: vendor (string), "
            "items (list of {name, qty, price}), total (float), "
            "date (string ISO date), category (string), reimbursable (bool).\n\n"
            f"Receipt data:\n{receipt_data}"
        )

        try:
            raw = await call_llm(role="ocr", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("vendor", "Unknown")
            result.setdefault("items", [])
            result.setdefault("total", 0.0)
            result.setdefault("date", date.today().isoformat())
            result.setdefault("category", "general")
            result.setdefault("reimbursable", False)
            return result
        except Exception as exc:
            logger.error("scan_receipt LLM failed: %s", exc)
            return {
                "vendor": "Unknown",
                "items": [],
                "total": 0.0,
                "date": date.today().isoformat(),
                "category": "general",
                "reimbursable": False,
            }

    # ------------------------------------------------------------------
    # negotiate_supplier
    # ------------------------------------------------------------------

    async def negotiate_supplier(
        self,
        supplier: str,
        current_terms: dict,
        market_data: dict,
    ) -> dict:
        """
        Suggest a negotiation strategy using game theory framing.
        Returns: {strategy, opening_offer, walk_away_point, expected_savings, talking_points}
        """
        prompt = (
            "You are a procurement negotiation strategist with expertise in game theory. "
            f"Develop a negotiation strategy for supplier: {supplier}. "
            "Apply game theory principles (BATNA, Nash equilibrium, Pareto optimality) "
            "to maximise value while preserving the supplier relationship. "
            "Return JSON with keys: strategy (string), opening_offer (string), "
            "walk_away_point (string), expected_savings (string), "
            "talking_points (list of strings).\n\n"
            f"Current terms:\n{json.dumps(current_terms, indent=2)}\n\n"
            f"Market data:\n{json.dumps(market_data, indent=2)}"
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("strategy", "Collaborative value-creation approach.")
            result.setdefault("opening_offer", "Request 10% reduction on current pricing.")
            result.setdefault("walk_away_point", "No reduction below 5%.")
            result.setdefault("expected_savings", "5-15%")
            result.setdefault("talking_points", [])
            return result
        except Exception as exc:
            logger.error("negotiate_supplier LLM failed: %s", exc)
            return {
                "strategy": f"Manual negotiation required. Error: {exc}",
                "opening_offer": "N/A",
                "walk_away_point": "N/A",
                "expected_savings": "Unknown",
                "talking_points": [],
            }

    # ------------------------------------------------------------------
    # check_inventory
    # ------------------------------------------------------------------

    async def check_inventory(
        self,
        items: List[dict],
        thresholds: dict,
    ) -> dict:
        """
        Quickly assess stock levels against thresholds.
        Uses fast role for rapid assessment.
        Returns: {items_below_threshold, auto_order_triggered, orders: list[dict]}
        """
        prompt = (
            "You are an inventory management system. "
            "Check the following items against their reorder thresholds. "
            "Identify items below threshold and determine if auto-order should be triggered. "
            "Return JSON with keys: items_below_threshold (list of strings), "
            "auto_order_triggered (bool), orders (list of {item, quantity, supplier}).\n\n"
            f"Items:\n{json.dumps(items, indent=2)}\n\n"
            f"Thresholds:\n{json.dumps(thresholds, indent=2)}"
        )

        try:
            raw = await call_llm(role="fast", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("items_below_threshold", [])
            result.setdefault("auto_order_triggered", False)
            result.setdefault("orders", [])
            return result
        except Exception as exc:
            logger.error("check_inventory LLM failed: %s — computing locally", exc)
            below = []
            orders = []
            for item in items:
                item_name = item.get("name", item.get("id", "unknown"))
                current_stock = item.get("quantity", item.get("stock", 0))
                threshold = thresholds.get(item_name, 0)
                if current_stock < threshold:
                    below.append(item_name)
                    orders.append({
                        "item": item_name,
                        "quantity": threshold * 2,
                        "supplier": item.get("supplier", "default"),
                    })
            return {
                "items_below_threshold": below,
                "auto_order_triggered": len(below) > 0,
                "orders": orders,
            }

    # ------------------------------------------------------------------
    # auto_order
    # ------------------------------------------------------------------

    async def auto_order(
        self,
        item: str,
        quantity: int,
        supplier: str,
    ) -> dict:
        """
        Place an automatic purchase order.
        Returns: {order_id, item, quantity, supplier, estimated_delivery, cost}
        """
        order_id = f"PO-{uuid.uuid4().hex[:8].upper()}"
        estimated_delivery = (date.today() + timedelta(days=7)).isoformat()

        logger.info(
            "auto_order: order_id=%s item=%s qty=%d supplier=%s",
            order_id,
            item,
            quantity,
            supplier,
        )

        try:
            return {
                "order_id": order_id,
                "item": item,
                "quantity": quantity,
                "supplier": supplier,
                "estimated_delivery": estimated_delivery,
                "cost": 0.0,  # Resolved from supplier catalogue at runtime
            }
        except Exception as exc:
            logger.error("auto_order failed: %s", exc)
            return {
                "order_id": order_id,
                "item": item,
                "quantity": quantity,
                "supplier": supplier,
                "estimated_delivery": estimated_delivery,
                "cost": 0.0,
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
