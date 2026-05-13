"""
ZOA Context Bus — in-memory async event bus for cross-agent triggers.

Pre-wired trigger rules:
  billing.payment_overdue    → payroll.hold_commission
  billing.fraud_detected     → compliance.alert
  compliance.audit_triggered → scheduling.block_external
  hr.performance_flag        → payroll.review_compensation
"""

import asyncio
import logging
import time
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)

# Cross-agent trigger rules: source event → list of downstream events to fire
TRIGGER_RULES: dict[str, list[str]] = {
    "billing.payment_overdue": ["payroll.hold_commission"],
    "billing.fraud_detected": ["compliance.alert"],
    "compliance.audit_triggered": ["scheduling.block_external"],
    "hr.performance_flag": ["payroll.review_compensation"],
}


class EventBus:
    """
    Simple in-memory async pub/sub event bus.

    Usage:
        await bus.publish("billing.payment_overdue", {"invoice_id": "INV-001", "amount": 5000})
        queue = await bus.subscribe("payroll.hold_commission")
        event = await queue.get()
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)
        self._agent_queues: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._event_log: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

    async def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        """Publish an event to all subscribers and apply trigger rules."""
        event = {
            "event_type": event_type,
            "payload": payload,
            "timestamp": time.time(),
        }

        async with self._lock:
            self._event_log.append(event)
            if len(self._event_log) > 500:
                self._event_log = self._event_log[-500:]

            # Notify direct subscribers
            for queue in self._subscribers.get(event_type, []):
                try:
                    queue.put_nowait(event)
                except asyncio.QueueFull:
                    logger.warning(f"[bus] Queue full for {event_type}, dropping")

            # Route to agent polling queues
            agent_id = event_type.split(".")[0]
            self._agent_queues[agent_id].append(event)
            self._agent_queues["dashboard"].append(event)

            # Apply trigger rules
            for downstream_type in TRIGGER_RULES.get(event_type, []):
                downstream_event = {
                    "event_type": downstream_type,
                    "payload": {**payload, "_triggered_by": event_type},
                    "timestamp": time.time(),
                }
                logger.info(f"[bus] Trigger: {event_type} → {downstream_type}")
                self._event_log.append(downstream_event)

                for queue in self._subscribers.get(downstream_type, []):
                    try:
                        queue.put_nowait(downstream_event)
                    except asyncio.QueueFull:
                        pass

                target_agent = downstream_type.split(".")[0]
                self._agent_queues[target_agent].append(downstream_event)
                self._agent_queues["dashboard"].append(downstream_event)

        logger.info(f"[bus] Published: {event_type} | keys={list(payload.keys())}")

    async def subscribe(self, event_type: str) -> asyncio.Queue:
        """Subscribe to an event type. Returns a queue that receives matching events."""
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        async with self._lock:
            self._subscribers[event_type].append(queue)
        return queue

    async def get_pending_events(self, agent_id: str) -> list[dict[str, Any]]:
        """Drain and return all pending events for a given agent_id (consume-once)."""
        async with self._lock:
            events = list(self._agent_queues.get(agent_id, []))
            self._agent_queues[agent_id] = []
        return events

    async def get_recent_events(self, limit: int = 20) -> list[dict[str, Any]]:
        """Return the most recent events from the log (non-destructive)."""
        async with self._lock:
            return list(self._event_log[-limit:])

    def get_trigger_rules(self) -> dict[str, list[str]]:
        """Return the configured trigger rules."""
        return dict(TRIGGER_RULES)


# Singleton — import this everywhere
bus = EventBus()
