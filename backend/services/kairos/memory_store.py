"""Postgres-backed memory store for Kairos agents.

Adapts the CheetahClaws memory/store.py API (Apache-2.0) to SQLAlchemy.
Same public interface: save_memory, search_memory, load_index, touch_last_used.
Storage: agent_memories table (skill_id, tenant_id, name, description, type,
         content, confidence, source, last_used_at, conflict_group).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Column, String, Float, Date, DateTime, Text
from sqlalchemy.orm import Session

from database.models import Base
from database.session import SessionLocal


def _uuid() -> str:
    return str(uuid.uuid4())


# ── SQLAlchemy model ──────────────────────────────────────────────────────────

class AgentMemory(Base):
    """Per-skill, per-tenant agent memory entry."""
    __tablename__ = "agent_memories"

    id = Column(String(36), primary_key=True, default=_uuid)
    skill_id = Column(String(255), nullable=False, index=True)
    tenant_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    type = Column(String(50), default="project")
    content = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    source = Column(String(50), default="model")
    last_used_at = Column(Date, nullable=True)
    conflict_group = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)


# ── Data class (mirrors CheetahClaws MemoryEntry) ─────────────────────────────

@dataclass
class MemoryEntry:
    name: str
    description: str
    type: str
    content: str
    skill_id: str = ""
    tenant_id: str = ""
    confidence: float = 1.0
    source: str = "model"
    last_used_at: str = ""
    conflict_group: str = ""
    db_id: str = ""


# ── Core operations ───────────────────────────────────────────────────────────

def save_memory(entry: MemoryEntry, skill_id: str, tenant_id: str) -> None:
    """Upsert a memory entry (match on skill_id + tenant_id + name)."""
    db: Session = SessionLocal()
    try:
        existing = (
            db.query(AgentMemory)
            .filter_by(skill_id=skill_id, tenant_id=tenant_id, name=entry.name)
            .first()
        )
        if existing:
            existing.description = entry.description
            existing.type = entry.type
            existing.content = entry.content
            existing.confidence = entry.confidence
            existing.source = entry.source
            existing.conflict_group = entry.conflict_group
        else:
            db.add(AgentMemory(
                id=_uuid(),
                skill_id=skill_id,
                tenant_id=tenant_id,
                name=entry.name,
                description=entry.description,
                type=entry.type,
                content=entry.content,
                confidence=entry.confidence,
                source=entry.source,
                conflict_group=entry.conflict_group,
            ))
        db.commit()
    finally:
        db.close()


def delete_memory(name: str, skill_id: str, tenant_id: str) -> None:
    """Delete a memory entry by name."""
    db: Session = SessionLocal()
    try:
        db.query(AgentMemory).filter_by(
            skill_id=skill_id, tenant_id=tenant_id, name=name
        ).delete()
        db.commit()
    finally:
        db.close()


def load_index(skill_id: str, tenant_id: str) -> list[MemoryEntry]:
    """Return all memory entries for a skill+tenant, sorted by name."""
    db: Session = SessionLocal()
    try:
        rows = (
            db.query(AgentMemory)
            .filter_by(skill_id=skill_id, tenant_id=tenant_id)
            .order_by(AgentMemory.name)
            .all()
        )
        return [_row_to_entry(r) for r in rows]
    finally:
        db.close()


def search_memory(query: str, skill_id: str, tenant_id: str) -> list[MemoryEntry]:
    """Case-insensitive keyword search on name + description + content."""
    q = query.lower()
    results = []
    for entry in load_index(skill_id, tenant_id):
        haystack = f"{entry.name} {entry.description} {entry.content}".lower()
        if q in haystack:
            results.append(entry)
    return results


def touch_last_used(db_id: str) -> None:
    """Update last_used_at to today for a memory entry."""
    db: Session = SessionLocal()
    try:
        row = db.query(AgentMemory).filter_by(id=db_id).first()
        if row:
            today = date.today()
            if row.last_used_at != today:
                row.last_used_at = today
                db.commit()
    finally:
        db.close()


def get_index_summary(skill_id: str, tenant_id: str) -> str:
    """Return a markdown summary of all memories for injection into system prompt."""
    entries = load_index(skill_id, tenant_id)
    if not entries:
        return ""
    lines = [f"- [{e.name}] {e.description}" for e in entries]
    return "## Agent Memory\n" + "\n".join(lines)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _row_to_entry(row: AgentMemory) -> MemoryEntry:
    return MemoryEntry(
        name=row.name,
        description=row.description or "",
        type=row.type or "project",
        content=row.content,
        skill_id=row.skill_id,
        tenant_id=row.tenant_id,
        confidence=row.confidence or 1.0,
        source=row.source or "model",
        last_used_at=str(row.last_used_at) if row.last_used_at else "",
        conflict_group=row.conflict_group or "",
        db_id=row.id,
    )
