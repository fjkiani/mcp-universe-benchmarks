"""
Identity Agent Router — FastAPI endpoints for identity security engine

POST /api/v1/identity/agent/chat          — Live identity agent
POST /api/v1/identity/agent/benchmark/run — Run full benchmark suite
GET  /api/v1/identity/agent/benchmark/latest — Latest benchmark results
GET  /api/v1/identity/agent/health        — Health check
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Literal, Optional, List, Dict, Any
import os
import asyncio
from datetime import datetime, timezone

from services.identity import identity_agent, benchmark_runner
from services.threat_detection_engine import (
    threat_engine,
    generate_audit_event_with_hash,
    detect_audit_chain_break,
)



router = APIRouter(prefix="/api/v1/identity", tags=["Identity Agent"])

# In-memory store for latest benchmark run (swap for DB in prod)
_latest_benchmark: Optional[Dict[str, Any]] = None


class IdentityChatRequest(BaseModel):
    message: str
    vertical: Literal["mfa_auth", "rbac_check", "compliance_audit"] = "mfa_auth"
    scenario_context: Optional[dict] = None


class BenchmarkRequest(BaseModel):
    task_ids: Optional[List[str]] = None  # None = run all


@router.get("/agent/health")
async def identity_health():
    """Health check — confirms identity engine status."""
    return {
        "status": "alive",
        "engine": "identity_agent_v1",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "benchmark_tasks": len(benchmark_runner.BENCHMARK_TASKS),
        "verticals": ["mfa_auth", "rbac_check", "compliance_audit"],
        "features": ["mfa_evaluation", "rbac_engine", "compliance_audit", "autonomous_remediation", "benchmark_runner"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.post("/agent/chat")
async def identity_chat(request: IdentityChatRequest):
    """
    Live identity security agent with threat pre-scan.

    Every request is first screened through the 6-tier ThreatDetectionEngine.
    CRITICAL threats are blocked. HIGH threats are flagged in the response.
    Clean requests proceed to the identity agent for full evaluation.
    """
    try:
        # ── Threat Pre-Scan ──────────────────────────────────────────
        # Build scan payload from whatever context is available
        scan_payload = {}
        ctx = request.scenario_context or {}

        if ctx.get("jwt_token"):
            scan_payload["jwt_token"] = ctx["jwt_token"]
        if ctx.get("user_id"):
            scan_payload["mfa_push_user_id"] = ctx["user_id"]
        if ctx.get("ip") and ctx.get("username"):
            scan_payload["ip"] = ctx["ip"]
            scan_payload["username"] = ctx["username"]
            scan_payload["login_success"] = ctx.get("credentials_valid", True)
        if ctx.get("redirect_uri"):
            scan_payload["redirect_uri"] = ctx["redirect_uri"]
            scan_payload["registered_domains"] = ctx.get("registered_domains", [])
        if ctx.get("token_scopes"):
            scan_payload["token_scopes"] = ctx["token_scopes"]
            scan_payload["requested_resource"] = ctx.get("resource", "")
        if ctx.get("username"):
            scan_payload["username"] = str(ctx["username"])

        threat_scan_result = None
        if scan_payload:
            threat_scan_result = threat_engine.scan_request(scan_payload)

            # Hard block on CRITICAL threats
            if threat_scan_result.get("recommended_action") == "BLOCK_AND_ALERT":
                return {
                    "message": (
                        f"🚨 REQUEST BLOCKED — {threat_scan_result['threats_found']} CRITICAL threat(s) detected. "
                        f"Action: {threat_scan_result['recommended_action']}. "
                        f"Threats: {', '.join(t['attack_class'] for t in threat_scan_result['threats'])}."
                    ),
                    "vertical": request.vertical,
                    "auth_status": "denied",
                    "access_granted": False,
                    "risk_level": "CRITICAL",
                    "risk_score": 100,
                    "threat_scan": threat_scan_result,
                    "actions": [],
                    "mfa_required": False,
                    "applied_roles": [],
                    "event_log": [],
                    "remediation_applied": False,
                }

        # ── Agent Processing ──────────────────────────────────────────
        response = await identity_agent.process(
            user_request=request.message,
            vertical=request.vertical,
            scenario_context=request.scenario_context
        )
        result = response.model_dump()

        # Attach threat scan results to every response for transparency
        if threat_scan_result:
            result["threat_scan"] = threat_scan_result

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/agent/benchmark/run")
async def run_benchmark(request: BenchmarkRequest, background_tasks: BackgroundTasks):
    """
    Run the identity benchmark suite.
    Executes all 15 tasks (auth + RBAC + compliance), scores each, returns full report.
    """
    global _latest_benchmark
    try:
        run = await benchmark_runner.run_benchmark(task_ids=request.task_ids)
        _latest_benchmark = run.model_dump()
        return _latest_benchmark
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/benchmark/latest")
async def get_latest_benchmark():
    """Return the most recent benchmark run results."""
    global _latest_benchmark
    if _latest_benchmark is None:
        # Auto-run on first request for demo
        run = await benchmark_runner.run_benchmark()
        _latest_benchmark = run.model_dump()
    return _latest_benchmark


@router.get("/agent/benchmark/tasks")
async def list_benchmark_tasks():
    """List all benchmark tasks with metadata (no results)."""
    return {
        "total": len(benchmark_runner.BENCHMARK_TASKS),
        "tasks": [
            {
                "id": t["id"],
                "category": t["category"],
                "complexity": t["complexity"],
                "request": t["request"][:80] + "...",
                "vertical": t["scenario"].get("vertical", "unknown")
            }
            for t in benchmark_runner.BENCHMARK_TASKS
        ]
    }


@router.post("/threat/scan")
async def threat_scan(request: dict):
    """
    Run the full 6-tier threat detection engine against any identity request.

    Feed it any combination of:
      - jwt_token           → T1: alg:none, RS256→HS256 confusion
      - token_id + ip       → T2: refresh token replay
      - redirect_uri        → T2: OAuth subdomain hijack
      - submitted_fields    → T3: mass assignment / privilege escalation
      - requesting_user_id  → T3: IDOR attempt
      - username / email    → T4: CRLF log injection
      - token_scopes        → T5: scope creep
      - ip + login_success  → T5: credential stuffing
      - mfa_push_user_id    → T6: MFA fatigue bombing

    Returns: threat list, severities, mitigations, recommended action.
    """
    try:
        result = threat_engine.scan_request(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/threat/audit/seal")
async def seal_audit_event(event: dict, previous_hash: Optional[str] = None):
    """Seal an audit event into the tamper-evident hash chain."""
    try:
        sealed = generate_audit_event_with_hash(event, previous_hash)
        return sealed
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/threat/audit/verify")
async def verify_audit_chain(events: List[dict]):
    """Verify the integrity of an audit event hash chain."""
    try:
        result = detect_audit_chain_break(events)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

