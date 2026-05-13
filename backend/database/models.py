"""Database models for Healthcare Receptionist OS

Uses SQLite-compatible types for local development.
In production (PostgreSQL), swap to:
  - UUID(as_uuid=True) for id columns
  - JSONB for JSON columns
  - INET for IP address columns
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


def _uuid():
    return str(uuid.uuid4())


Base = declarative_base()


class Organization(Base):
    """Organization/Practice model"""
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=_uuid)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    patients = relationship("Patient", back_populates="organization", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="organization", cascade="all, delete-orphan")


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="staff")  # admin, provider, staff
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="users")
    appointments_as_provider = relationship(
        "Appointment",
        foreign_keys="Appointment.provider_id",
        back_populates="provider"
    )


class Patient(Base):
    """Patient model with FHIR resource storage"""
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True, default=_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    mrn = Column(String(50), nullable=False, index=True)  # Medical Record Number
    fhir_resource = Column(Text, nullable=False, default="{}")   # JSON stored as Text in SQLite
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    organization = relationship("Organization", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    messages = relationship("Message", back_populates="patient")


class Appointment(Base):
    """Appointment model"""
    __tablename__ = "appointments"

    id = Column(String(36), primary_key=True, default=_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    provider_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    fhir_resource = Column(Text, nullable=False, default="{}")   # JSON as Text
    status = Column(String(20), nullable=False, default="scheduled")
    start_time = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    provider = relationship("User", foreign_keys=[provider_id], back_populates="appointments_as_provider")
    video_consultation = relationship("VideoConsultation", back_populates="appointment", uselist=False)


class VideoConsultation(Base):
    """Video consultation model"""
    __tablename__ = "video_consultations"

    id = Column(String(36), primary_key=True, default=_uuid)
    organization_id = Column(String(36), nullable=True)
    appointment_id = Column(String(36), ForeignKey("appointments.id"), nullable=True)
    room_id = Column(String(255), nullable=False, index=True)
    recording_url = Column(Text)
    recording_id = Column(String(255))
    transcript_id = Column(String(255))
    transcript_text = Column(Text)
    medical_entities = Column(Text)   # JSON as Text
    ai_analysis = Column(Text)        # JSON as Text
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="video_consultation")


class Message(Base):
    """HIPAA-compliant SMS message model"""
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=_uuid)
    organization_id = Column(String(36), nullable=True)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=True)
    thread_id = Column(String(36), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    message_text = Column(Text, nullable=False)
    phi_detected = Column(Boolean, default=False)
    phi_filtered = Column(Boolean, default=False)
    phi_types = Column(Text)   # JSON as Text
    direction = Column(String(10), nullable=False, default="outbound")
    message_sid = Column(String(255))
    status = Column(String(20), default="sent")
    sent_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="messages")


class AuditLog(Base):
    """HIPAA-compliant audit log (immutable)"""
    __tablename__ = "audit_log"

    id = Column(String(36), primary_key=True, default=_uuid)
    organization_id = Column(String(36), nullable=True)
    user_id = Column(String(36), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(String(36))
    patient_id = Column(String(36), index=True)
    ip_address = Column(String(45))   # IPv4/IPv6 as String
    user_agent = Column(String(500))
    details = Column(Text)   # JSON as Text
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


# ══════════════════════════════════════════════════════════════════════
# GOVERNANCE ENGINE MODELS (Agent Certification / UL for AI)
# ══════════════════════════════════════════════════════════════════════

class RegisteredAgent(Base):
    """An AI agent registered for certification testing"""
    __tablename__ = "registered_agents"

    id = Column(String(36), primary_key=True, default=_uuid)
    name = Column(String(255), nullable=False, index=True)
    model = Column(String(100), nullable=False)          # "gpt-4o", "claude-3.5-sonnet"
    agent_type = Column(String(50), default="react")     # matches CLI agent types
    endpoint_url = Column(String(500), nullable=True)    # external agent endpoint (V2)
    mcp_tools = Column(Text, default="[]")               # JSON array of declared tools
    risk_tier = Column(String(20), default="medium")     # low/medium/high/critical
    created_at = Column(DateTime, default=datetime.utcnow)

    certification_runs = relationship("CertificationRun", back_populates="agent")


class CertificationRun(Base):
    """A single certification execution against an agent"""
    __tablename__ = "certification_runs"

    id = Column(String(36), primary_key=True, default=_uuid)
    agent_id = Column(String(36), ForeignKey("registered_agents.id"), nullable=False)
    domain = Column(String(100), nullable=False)         # "grant_application", "web_search"
    status = Column(String(20), default="queued")        # queued/running/completed/failed
    progress_pct = Column(Integer, default=0)
    current_task = Column(String(255), nullable=True)
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)

    # L1-L4 hierarchical scores (populated after completion)
    l1_syntax_score = Column(Integer, nullable=True)     # 0-100
    l2_resilience_score = Column(Integer, nullable=True)
    l3_protocol_score = Column(Integer, nullable=True)
    l4_objective_score = Column(Integer, nullable=True)
    overall_score = Column(Integer, nullable=True)
    grade = Column(String(20), nullable=True)            # CERTIFIED/CONDITIONAL/FAILED/INCONCLUSIVE

    config_snapshot = Column(Text, default="{}")         # JSON snapshot of config.yaml used
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    agent = relationship("RegisteredAgent", back_populates="certification_runs")
    task_results = relationship("TaskResult", back_populates="certification_run")


class TaskResult(Base):
    """Individual task result within a certification run"""
    __tablename__ = "task_results"

    id = Column(String(36), primary_key=True, default=_uuid)
    run_id = Column(String(36), ForeignKey("certification_runs.id"), nullable=False)
    task_path = Column(String(500), nullable=False)      # "tasks/edge_case_task_0050.json"
    category = Column(String(50))                         # "edge_cases", "multi_server"
    passed = Column(Boolean, nullable=True)
    score = Column(Integer, nullable=True)                # 0-100
    evaluation_level = Column(String(10))                 # "L1", "L2", "L3", "L4"
    agent_response = Column(Text)                         # raw agent output
    evaluator_output = Column(Text)                       # JSON of EvaluationResult
    trace_id = Column(String(36))                         # links to trace records
    tool_calls_made = Column(Text, default="[]")          # JSON array of tool calls
    tool_calls_expected = Column(Text, default="[]")      # from task config mcp_servers
    error = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    certification_run = relationship("CertificationRun", back_populates="task_results")


# ══════════════════════════════════════════════════════════════════════
# KAIROS MEMORY MODELS
# ══════════════════════════════════════════════════════════════════════

class AgentMemory(Base):
    """Persistent memory entries for Kairos execution runs.

    Stores key facts, tool results, and context summaries that the
    Kairos engine should recall across skill invocations.
    """
    __tablename__ = "agent_memories"

    id = Column(String(36), primary_key=True, default=_uuid)
    skill_id = Column(String(255), nullable=False, index=True)
    run_id = Column(String(36), nullable=True, index=True)       # which run created this
    memory_type = Column(String(50), nullable=False, default="fact")  # fact | summary | tool_result | error
    content = Column(Text, nullable=False)                        # the memory text
    importance = Column(Integer, default=5)                       # 1-10 relevance score
    tags = Column(Text, default="[]")                             # JSON array of string tags
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
