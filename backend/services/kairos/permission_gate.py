"""Benchmark-score-driven permission gate for Kairos skill execution.

Gate rules (applied in order):
  1. Tool not in skill_meta.permitted_tools → BLOCK + log violation
  2. l4_score < 6.0 → BLOCK all tools (skill not certified)
  3. l2_score < 60  → BLOCK write/mutating tools (force human-in-loop)
  4. l3_score >= 80 → ALLOW aggressive chaining (all tools auto-approved)
  5. Default: ALLOW read-only, ASK for write/bash
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

_READ_ONLY_TOOLS = frozenset({
    "read_file", "list_files", "search_files", "get_skill_info",
    "get_tenant_info", "get_schedule", "get_invoice", "get_employee",
    "get_contract", "get_regulation", "check_inventory",
})

_WRITE_TOOLS = frozenset({
    "write_file", "bash", "send_email", "create_invoice", "update_invoice",
    "book_meeting", "cancel_meeting", "process_payment", "update_employee",
    "create_purchase_order", "update_inventory", "send_notification",
    "call_webhook", "call_api",
})


@dataclass
class SkillMeta:
    """Benchmark metadata for a deployed skill."""
    skill_id: str
    l1_score: float = 0.0
    l2_score: float = 0.0
    l3_score: float = 0.0
    l4_score: float = 0.0
    permitted_tools: list = field(default_factory=list)


def check(tc: dict, skill_meta: SkillMeta) -> tuple[bool, Optional[str]]:
    """Evaluate whether a tool call is permitted.

    Returns:
        (permitted: bool, violation_reason: str | None)
    """
    tool_name = tc.get("name", "")

    # Rule 1: explicit allowlist
    if skill_meta.permitted_tools and tool_name not in skill_meta.permitted_tools:
        return False, (
            f"Tool '{tool_name}' not in skill's permitted_tools allowlist "
            f"(permitted: {skill_meta.permitted_tools})"
        )

    # Rule 2: L4 certification gate
    if skill_meta.l4_score < 6.0:
        return False, (
            f"Skill '{skill_meta.skill_id}' L4={skill_meta.l4_score:.1f} < 6.0 — "
            "not certified for execution. Re-benchmark via Archon."
        )

    # Rule 3: Low L2 resilience — block write tools
    if skill_meta.l2_score < 60.0 and tool_name in _WRITE_TOOLS:
        return False, (
            f"Skill '{skill_meta.skill_id}' L2={skill_meta.l2_score:.1f} < 60 — "
            f"write tool '{tool_name}' requires human approval."
        )

    # Rule 4: High L3 — allow everything
    if skill_meta.l3_score >= 80.0:
        return True, None

    # Rule 5: default
    return True, None


def requires_human_approval(tc: dict, skill_meta: SkillMeta) -> bool:
    """Return True if this permitted tool call still needs explicit human approval."""
    if skill_meta.l3_score >= 80.0:
        return False
    return tc.get("name", "") in _WRITE_TOOLS


def is_aggressive_chaining_allowed(skill_meta: SkillMeta) -> bool:
    return skill_meta.l3_score >= 80.0
