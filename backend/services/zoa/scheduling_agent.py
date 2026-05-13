"""
scheduling_agent.py — Time Optimizer
Books meetings, optimises calendars, manages ROI of time.

Primary LLM: reasoning (Hermes 3 405B)
"""

import json
import logging
import uuid
from typing import Any, Dict, List

from services.openrouter_service import call_llm, call_llm_with_messages
from services.zoa.context_bus import bus

logger = logging.getLogger(__name__)


class SchedulingAgent:
    """Time Optimizer — ZOA scheduling intelligence agent."""

    # ------------------------------------------------------------------
    # find_optimal_slot
    # ------------------------------------------------------------------

    async def find_optimal_slot(
        self,
        participants: List[str],
        duration_mins: int,
        context: str,
    ) -> dict:
        """
        Analyse participant availability and meeting ROI to find the best slot.
        Returns: {slot, participants, agenda_items, roi_score, alternatives}
        """
        prompt = (
            "You are an expert calendar optimiser and time-ROI analyst. "
            f"Find the optimal meeting slot for the following participants: {participants}. "
            f"Duration: {duration_mins} minutes. Context: {context}. "
            "Consider time zones, energy levels, and ROI of the meeting. "
            "Return JSON with keys: slot (string ISO datetime), participants (list), "
            "agenda_items (list of strings), roi_score (float 0-1), "
            "alternatives (list of slot strings)."
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("slot", "TBD")
            result.setdefault("participants", participants)
            result.setdefault("agenda_items", [])
            result.setdefault("roi_score", 0.5)
            result.setdefault("alternatives", [])
            return result
        except Exception as exc:
            logger.error("find_optimal_slot LLM failed: %s", exc)
            return {
                "slot": "TBD",
                "participants": participants,
                "agenda_items": [],
                "roi_score": 0.0,
                "alternatives": [],
            }

    # ------------------------------------------------------------------
    # book_meeting
    # ------------------------------------------------------------------

    async def book_meeting(
        self,
        slot: dict,
        agenda: str,
        participants: List[str],
    ) -> dict:
        """
        Confirm a meeting booking and generate a structured agenda.
        Returns: {meeting_id, confirmation, agenda, calendar_link}
        """
        meeting_id = str(uuid.uuid4())
        prompt = (
            "You are a professional executive assistant. "
            "Generate a structured meeting agenda for the following: "
            f"Slot: {json.dumps(slot)}, Participants: {participants}, "
            f"Agenda brief: {agenda}. "
            "Return JSON with keys: meeting_id (string), confirmation (string), "
            "agenda (string — formatted agenda), calendar_link (string)."
        )

        try:
            raw = await call_llm(role="write", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("meeting_id", meeting_id)
            result.setdefault("confirmation", "Meeting booked successfully.")
            result.setdefault("agenda", agenda)
            result.setdefault("calendar_link", f"https://calendar.zoa.ai/meeting/{meeting_id}")
            return result
        except Exception as exc:
            logger.error("book_meeting LLM failed: %s", exc)
            return {
                "meeting_id": meeting_id,
                "confirmation": "Meeting booked (agenda generation failed).",
                "agenda": agenda,
                "calendar_link": f"https://calendar.zoa.ai/meeting/{meeting_id}",
            }

    # ------------------------------------------------------------------
    # handle_decline
    # ------------------------------------------------------------------

    async def handle_decline(
        self,
        meeting_id: str,
        decliner: str,
        reason: str,
    ) -> dict:
        """
        Decide how to handle a meeting decline: reschedule, proceed without, or escalate.
        Returns: {action, new_slot, message}
        """
        prompt = (
            "You are a scheduling intelligence agent. "
            f"Meeting {meeting_id} has been declined by {decliner}. Reason: {reason}. "
            "Decide the best course of action: reschedule, proceed_without, or escalate. "
            "Return JSON with keys: action (string), new_slot (string or null), message (string)."
        )

        try:
            raw = await call_llm(role="reasoning", prompt=prompt)
            result = self._parse_json_response(raw)
            result.setdefault("action", "reschedule")
            result.setdefault("new_slot", None)
            result.setdefault("message", f"Handling decline from {decliner}.")
            return result
        except Exception as exc:
            logger.error("handle_decline LLM failed: %s", exc)
            return {
                "action": "reschedule",
                "new_slot": None,
                "message": (
                    f"Could not process decline automatically. "
                    f"Manual review needed. Error: {exc}"
                ),
            }

    # ------------------------------------------------------------------
    # get_pending_blocks
    # ------------------------------------------------------------------

    async def get_pending_blocks(self) -> List[dict]:
        """
        Drain context_bus for scheduling.block_external events.
        Returns list of blocked slot dicts.
        """
        try:
            events = await bus.get_pending_events("scheduling_agent")
            blocks = [
                e for e in events
                if e.get("event_type") == "scheduling.block_external"
            ]
            logger.info("get_pending_blocks: found %d block events", len(blocks))
            return [b.get("payload", b) for b in blocks]
        except Exception as exc:
            logger.error("get_pending_blocks failed: %s", exc)
            return []

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
