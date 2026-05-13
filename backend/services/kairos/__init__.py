"""Kairos Execution Engine — CheetahClaws-derived agent loop for ZOA skill execution.

Adapted from SafeRL-Lab/cheetahclaws (Apache-2.0).
Modifications: OpenRouter provider, benchmark-driven permission gates,
Postgres-backed memory, ZOA skill tool registration.
"""
from .engine import KairosEngine, KairosState, KairosResult, PhaseChange, PermissionViolation
from .permission_gate import SkillMeta

__all__ = [
    "KairosEngine", "KairosState", "KairosResult",
    "SkillMeta", "PhaseChange", "PermissionViolation",
]
