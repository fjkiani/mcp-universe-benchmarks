"""
Identity Data Models
────────────────────
All Pydantic models used across the identity engine.
"""
from typing import Optional, List, Dict
from pydantic import BaseModel


class ActionTrace(BaseModel):
    """Single tool call in the agent's action chain."""
    tool: str
    args: dict
    result: dict
    success: bool
    latency_ms: Optional[int] = None


class IdentityAgentResponse(BaseModel):
    """Structured response from the identity agent."""
    message: str
    vertical: str
    actions: List[ActionTrace] = []

    # Auth specific
    auth_status: Optional[str] = None       # granted | denied | mfa_required | locked
    session_token: Optional[str] = None
    session_expiry: Optional[str] = None
    mfa_required: bool = False

    # RBAC specific
    access_granted: Optional[bool] = None
    applied_roles: List[str] = []
    permission_breakdown: Optional[dict] = None

    # Audit specific
    anomaly_detected: Optional[bool] = None
    compliance_status: Optional[str] = None # compliant | non_compliant | review_required
    event_log: List[dict] = []

    # Remediation
    remediation_suggested: Optional[str] = None
    remediation_applied: bool = False

    # Risk
    risk_score: Optional[int] = None        # 0–100
    risk_level: Optional[str] = None        # LOW | MEDIUM | HIGH | CRITICAL

    # Threat pre-scan (attached by router, not agent)
    threat_scan: Optional[dict] = None

    error: Optional[str] = None


class BenchmarkResult(BaseModel):
    """Result for a single benchmark task."""
    task_id: str
    category: str
    passed: bool
    score: float        # 0.0 – 1.0
    reason: str
    latency_ms: int
    response: dict


class BenchmarkRun(BaseModel):
    """Aggregated results for a full benchmark run."""
    run_id: str
    timestamp: str
    total_tasks: int
    passed: int
    failed: int
    pass_rate: float
    by_category: Dict[str, dict]
    results: List[BenchmarkResult]
    risk_summary: str
