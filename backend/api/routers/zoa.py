"""
ZOA Agent Suite Router
======================
Exposes all 6 ZOA autonomous business agents via REST endpoints.

Agents:
  Billing      — invoice processing, payment chasing, fraud detection
  Scheduling   — slot finding, meeting booking, decline handling
  Payroll      — payroll calculation, anomaly detection, commission holds
  HR           — resume screening, performance reviews, exit processing
  Procurement  — receipt scanning, supplier negotiation, inventory checks
  Compliance   — regulation interpretation, audit docs, risk assessment

Endpoints are grouped by agent prefix under /zoa/<agent>/<action>.
All POST endpoints accept a Pydantic request model and return a dict.
Cross-agent events are accessible via the context bus at /zoa/events/{agent_id}.
"""

import logging
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

# ─── Agent singletons ─────────────────────────────────────────────────────────
from services.zoa.billing_agent import BillingAgent
from services.zoa.scheduling_agent import SchedulingAgent
from services.zoa.payroll_agent import PayrollAgent
from services.zoa.hr_agent import HRAgent
from services.zoa.procurement_agent import ProcurementAgent
from services.zoa.compliance_agent import ComplianceAgent
from services.zoa.context_bus import bus

billing_agent = BillingAgent()
scheduling_agent = SchedulingAgent()
payroll_agent = PayrollAgent()
hr_agent = HRAgent()
procurement_agent = ProcurementAgent()
compliance_agent = ComplianceAgent()


# ─── Billing Models ───────────────────────────────────────────────────────────

class ProcessInvoiceRequest(BaseModel):
    invoice_data: dict


class ChasePaymentRequest(BaseModel):
    invoice_id: str
    days_overdue: int
    client_name: str


class DetectFraudRequest(BaseModel):
    invoice_data: dict


class GenerateInvoiceRequest(BaseModel):
    contract_data: dict


# ─── Scheduling Models ────────────────────────────────────────────────────────

class FindSlotRequest(BaseModel):
    participants: list[str]
    duration_mins: int
    context: str


class BookMeetingRequest(BaseModel):
    slot: dict
    agenda: str
    participants: list[str]


class HandleDeclineRequest(BaseModel):
    meeting_id: str
    decliner: str
    reason: str


# ─── Payroll Models ───────────────────────────────────────────────────────────

class CalculatePayrollRequest(BaseModel):
    employees: list[dict]
    period: str


class DetectAnomalyRequest(BaseModel):
    employee_id: str
    metrics: dict


class HoldCommissionRequest(BaseModel):
    employee_id: str
    reason: str


class ReviewCompensationRequest(BaseModel):
    employee_id: str
    performance_data: dict


# ─── HR Models ────────────────────────────────────────────────────────────────

class ScreenResumeRequest(BaseModel):
    resume_text: str
    role_requirements: dict


class PerformanceReviewRequest(BaseModel):
    employee_id: str
    metrics: dict
    period: str


class ProcessExitRequest(BaseModel):
    employee_id: str
    reason: str


class FlagPerformanceRequest(BaseModel):
    employee_id: str
    issue: str


# ─── Procurement Models ───────────────────────────────────────────────────────

class ScanReceiptRequest(BaseModel):
    receipt_data: str


class NegotiateSupplierRequest(BaseModel):
    supplier: str
    current_terms: dict
    market_data: dict


class CheckInventoryRequest(BaseModel):
    items: list[dict]
    thresholds: dict


class AutoOrderRequest(BaseModel):
    item: str
    quantity: int
    supplier: str


# ─── Compliance Models ────────────────────────────────────────────────────────

class InterpretRegulationRequest(BaseModel):
    regulation_text: str
    business_context: str


class GenerateAuditDocRequest(BaseModel):
    audit_type: str
    data: dict


class AssessRiskRequest(BaseModel):
    operation: str
    jurisdiction: str
    data: dict


class HandleAlertRequest(BaseModel):
    alert_type: str
    details: dict


# ─── Health & Context Bus ─────────────────────────────────────────────────────

@router.get("/zoa/health")
async def zoa_health() -> dict:
    """Returns operational status of all ZOA agents."""
    return {
        "status": "operational",
        "agents": ["billing", "scheduling", "payroll", "hr", "procurement", "compliance"],
    }


@router.get("/zoa/events/{agent_id}")
async def get_pending_events(agent_id: str) -> dict:
    """Returns pending cross-agent events for the given agent from the context bus."""
    try:
        result = await bus.get_pending_events(agent_id)
        return result
    except Exception as exc:
        logger.exception("Error fetching events for agent %s", agent_id)
        raise HTTPException(status_code=500, detail=str(exc))


# ─── Billing Endpoints ────────────────────────────────────────────────────────

@router.post("/zoa/billing/process-invoice")
async def process_invoice(req: ProcessInvoiceRequest) -> dict:
    """Process an incoming invoice through the billing agent."""
    try:
        result = await billing_agent.process_invoice(req.invoice_data)
        return result
    except Exception as exc:
        logger.exception("Error in process_invoice")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/billing/chase-payment")
async def chase_payment(req: ChasePaymentRequest) -> dict:
    """Chase an overdue payment for a given invoice."""
    try:
        result = await billing_agent.chase_payment(req.invoice_id, req.days_overdue, req.client_name)
        return result
    except Exception as exc:
        logger.exception("Error in chase_payment")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/billing/detect-fraud")
async def detect_fraud(req: DetectFraudRequest) -> dict:
    """Run fraud detection on invoice data."""
    try:
        result = await billing_agent.detect_fraud(req.invoice_data)
        return result
    except Exception as exc:
        logger.exception("Error in detect_fraud")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/billing/generate-invoice")
async def generate_invoice(req: GenerateInvoiceRequest) -> dict:
    """Generate a new invoice from contract data."""
    try:
        result = await billing_agent.generate_invoice(req.contract_data)
        return result
    except Exception as exc:
        logger.exception("Error in generate_invoice")
        raise HTTPException(status_code=500, detail=str(exc))


# ─── Scheduling Endpoints ─────────────────────────────────────────────────────

@router.post("/zoa/scheduling/find-slot")
async def find_slot(req: FindSlotRequest) -> dict:
    """Find an optimal meeting slot for the given participants."""
    try:
        result = await scheduling_agent.find_optimal_slot(req.participants, req.duration_mins, req.context)
        return result
    except Exception as exc:
        logger.exception("Error in find_optimal_slot")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/scheduling/book")
async def book_meeting(req: BookMeetingRequest) -> dict:
    """Book a meeting at the specified slot."""
    try:
        result = await scheduling_agent.book_meeting(req.slot, req.agenda, req.participants)
        return result
    except Exception as exc:
        logger.exception("Error in book_meeting")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/scheduling/handle-decline")
async def handle_decline(req: HandleDeclineRequest) -> dict:
    """Handle a meeting decline and reschedule if needed."""
    try:
        result = await scheduling_agent.handle_decline(req.meeting_id, req.decliner, req.reason)
        return result
    except Exception as exc:
        logger.exception("Error in handle_decline")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/zoa/scheduling/pending-blocks")
async def get_pending_blocks() -> dict:
    """Return all pending scheduling blocks awaiting resolution."""
    try:
        result = await scheduling_agent.get_pending_blocks()
        return result
    except Exception as exc:
        logger.exception("Error in get_pending_blocks")
        raise HTTPException(status_code=500, detail=str(exc))


# ─── Payroll Endpoints ────────────────────────────────────────────────────────

@router.post("/zoa/payroll/calculate")
async def calculate_payroll(req: CalculatePayrollRequest) -> dict:
    """Calculate payroll for a list of employees for the given period."""
    try:
        result = await payroll_agent.calculate_payroll(req.employees, req.period)
        return result
    except Exception as exc:
        logger.exception("Error in calculate_payroll")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/payroll/detect-anomaly")
async def detect_anomaly(req: DetectAnomalyRequest) -> dict:
    """Detect payroll anomalies for a specific employee."""
    try:
        result = await payroll_agent.detect_anomaly(req.employee_id, req.metrics)
        return result
    except Exception as exc:
        logger.exception("Error in detect_anomaly")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/payroll/hold-commission")
async def hold_commission(req: HoldCommissionRequest) -> dict:
    """Place a hold on an employee's commission."""
    try:
        result = await payroll_agent.hold_commission(req.employee_id, req.reason)
        return result
    except Exception as exc:
        logger.exception("Error in hold_commission")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/payroll/review-compensation")
async def review_compensation(req: ReviewCompensationRequest) -> dict:
    """Review and adjust compensation based on performance data."""
    try:
        result = await payroll_agent.review_compensation(req.employee_id, req.performance_data)
        return result
    except Exception as exc:
        logger.exception("Error in review_compensation")
        raise HTTPException(status_code=500, detail=str(exc))


# ─── HR Endpoints ─────────────────────────────────────────────────────────────

@router.post("/zoa/hr/screen-resume")
async def screen_resume(req: ScreenResumeRequest) -> dict:
    """Screen a candidate resume against role requirements."""
    try:
        result = await hr_agent.screen_resume(req.resume_text, req.role_requirements)
        return result
    except Exception as exc:
        logger.exception("Error in screen_resume")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/hr/performance-review")
async def performance_review(req: PerformanceReviewRequest) -> dict:
    """Conduct a performance review for an employee."""
    try:
        result = await hr_agent.conduct_performance_review(req.employee_id, req.metrics, req.period)
        return result
    except Exception as exc:
        logger.exception("Error in conduct_performance_review")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/hr/process-exit")
async def process_exit(req: ProcessExitRequest) -> dict:
    """Process an employee exit/offboarding."""
    try:
        result = await hr_agent.process_exit(req.employee_id, req.reason)
        return result
    except Exception as exc:
        logger.exception("Error in process_exit")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/hr/flag-performance")
async def flag_performance(req: FlagPerformanceRequest) -> dict:
    """Flag a performance issue for an employee."""
    try:
        result = await hr_agent.flag_performance(req.employee_id, req.issue)
        return result
    except Exception as exc:
        logger.exception("Error in flag_performance")
        raise HTTPException(status_code=500, detail=str(exc))


# ─── Procurement Endpoints ────────────────────────────────────────────────────

@router.post("/zoa/procurement/scan-receipt")
async def scan_receipt(req: ScanReceiptRequest) -> dict:
    """Scan and parse a procurement receipt."""
    try:
        result = await procurement_agent.scan_receipt(req.receipt_data)
        return result
    except Exception as exc:
        logger.exception("Error in scan_receipt")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/procurement/negotiate")
async def negotiate_supplier(req: NegotiateSupplierRequest) -> dict:
    """Negotiate supplier terms using market data."""
    try:
        result = await procurement_agent.negotiate_supplier(req.supplier, req.current_terms, req.market_data)
        return result
    except Exception as exc:
        logger.exception("Error in negotiate_supplier")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/procurement/check-inventory")
async def check_inventory(req: CheckInventoryRequest) -> dict:
    """Check inventory levels against defined thresholds."""
    try:
        result = await procurement_agent.check_inventory(req.items, req.thresholds)
        return result
    except Exception as exc:
        logger.exception("Error in check_inventory")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/procurement/auto-order")
async def auto_order(req: AutoOrderRequest) -> dict:
    """Automatically place an order for a given item and quantity."""
    try:
        result = await procurement_agent.auto_order(req.item, req.quantity, req.supplier)
        return result
    except Exception as exc:
        logger.exception("Error in auto_order")
        raise HTTPException(status_code=500, detail=str(exc))


# ─── Compliance Endpoints ─────────────────────────────────────────────────────

@router.post("/zoa/compliance/interpret")
async def interpret_regulation(req: InterpretRegulationRequest) -> dict:
    """Interpret a regulation in the context of the business."""
    try:
        result = await compliance_agent.interpret_regulation(req.regulation_text, req.business_context)
        return result
    except Exception as exc:
        logger.exception("Error in interpret_regulation")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/compliance/audit-doc")
async def generate_audit_doc(req: GenerateAuditDocRequest) -> dict:
    """Generate audit documentation for a given audit type."""
    try:
        result = await compliance_agent.generate_audit_doc(req.audit_type, req.data)
        return result
    except Exception as exc:
        logger.exception("Error in generate_audit_doc")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/compliance/assess-risk")
async def assess_risk(req: AssessRiskRequest) -> dict:
    """Assess regulatory risk for an operation in a given jurisdiction."""
    try:
        result = await compliance_agent.assess_risk(req.operation, req.jurisdiction, req.data)
        return result
    except Exception as exc:
        logger.exception("Error in assess_risk")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/zoa/compliance/handle-alert")
async def handle_alert(req: HandleAlertRequest) -> dict:
    """Handle a compliance alert with the given details."""
    try:
        result = await compliance_agent.handle_alert(req.alert_type, req.details)
        return result
    except Exception as exc:
        logger.exception("Error in handle_alert")
        raise HTTPException(status_code=500, detail=str(exc))


# ══════════════════════════════════════════════════════════════════════
# KAIROS EXECUTION ENGINE ENDPOINTS
# ══════════════════════════════════════════════════════════════════════
#
# POST /zoa/kairos/run          — start a Kairos run, returns run_id
# GET  /zoa/kairos/run/{id}     — poll run status + result
# GET  /zoa/kairos/run/{id}/stream — SSE event stream (with replay)
#
# Runs execute in a BackgroundTask thread. Events are buffered in
# _KAIROS_RUNS (in-memory, acceptable for alpha). SSE clients that
# connect after the run completes receive the full buffered event log.
# ══════════════════════════════════════════════════════════════════════

import asyncio
import json as _json
import threading
import time as _time
import uuid as _uuid
from typing import Any

from fastapi import Request
from fastapi.responses import StreamingResponse

from services.kairos import KairosEngine, KairosState, KairosResult
from services.kairos.permission_gate import SkillMeta
from services.kairos.engine import build_result
from services.kairos.providers import TextChunk, ThinkingChunk
from services.kairos.engine import (
    PhaseChange, PermissionViolation, ToolStart, ToolEnd, TurnDone, PermissionRequest
)

# ── In-memory run store ───────────────────────────────────────────────────────
# { run_id: { "status": str, "events": list[str], "result": dict|None, "lock": threading.Lock } }
_KAIROS_RUNS: dict[str, dict] = {}
_RUNS_LOCK = threading.Lock()


def _new_run_record() -> dict:
    return {
        "status": "running",   # running | done | failed
        "events": [],          # SSE-formatted strings buffered for replay
        "result": None,
        "lock": threading.Lock(),
    }


def _push_event(run_id: str, event_type: str, data: Any) -> None:
    """Serialize an event to SSE format and append to the run buffer."""
    payload = _json.dumps({"type": event_type, "data": data})
    sse_line = f"event: {event_type}\ndata: {payload}\n\n"
    with _KAIROS_RUNS[run_id]["lock"]:
        _KAIROS_RUNS[run_id]["events"].append(sse_line)


def _event_to_dict(event) -> tuple[str, Any]:
    """Convert a Kairos event object to (event_type, data_dict)."""
    if isinstance(event, PhaseChange):
        return "phase_change", {"phase": event.phase}
    if isinstance(event, TextChunk):
        return "text_chunk", {"text": event.text}
    if isinstance(event, ThinkingChunk):
        return "thinking_chunk", {"text": event.text}
    if isinstance(event, ToolStart):
        return "tool_start", {"name": event.name, "inputs": event.inputs}
    if isinstance(event, ToolEnd):
        return "tool_end", {"name": event.name, "result": event.result, "permitted": event.permitted}
    if isinstance(event, TurnDone):
        return "turn_done", {"input_tokens": event.input_tokens, "output_tokens": event.output_tokens}
    if isinstance(event, PermissionViolation):
        return "permission_violation", {
            "tool_name": event.tool_name,
            "reason": event.reason,
            "benchmark_score": event.benchmark_score,
        }
    if isinstance(event, PermissionRequest):
        return "permission_request", {"description": event.description, "granted": event.granted}
    return "unknown", {"repr": str(event)}


def _run_kairos_thread(run_id: str, engine: KairosEngine, goal: str, state: KairosState) -> None:
    """Execute the Kairos loop in a background thread, buffering all events."""
    final_text = ""
    error = None
    try:
        for event in engine.run(goal=goal, state=state):
            event_type, data = _event_to_dict(event)
            _push_event(run_id, event_type, data)
            if event_type == "text_chunk":
                final_text += data.get("text", "")
    except Exception as exc:
        error = str(exc)
        logger.exception("Kairos run %s failed: %s", run_id, exc)

    result = build_result(state, final_text, error)
    result_dict = {
        "run_id": result.run_id,
        "success": result.success,
        "final_text": result.final_text,
        "turns": result.turns,
        "tool_calls_made": result.tool_calls_made,
        "violations": result.violations,
        "degraded": result.degraded,
        "error": result.error,
    }

    with _KAIROS_RUNS[run_id]["lock"]:
        _KAIROS_RUNS[run_id]["result"] = result_dict
        _KAIROS_RUNS[run_id]["status"] = "done" if result.success else "failed"

    # Push terminal event so SSE clients know the stream is complete
    _push_event(run_id, "run_complete", result_dict)


# ── Pydantic models ───────────────────────────────────────────────────────────

class KairosRunRequest(BaseModel):
    skill_id: str
    goal: str
    # Benchmark scores — used by permission gate
    l1_score: float = 0.0
    l2_score: float = 0.0
    l3_score: float = 0.0
    l4_score: float = 0.0
    permitted_tools: list[str] = []
    allowlisted_tools: list[str] = []
    max_turns: int = 20
    memory_summary: str = ""


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/zoa/kairos/run")
async def kairos_start_run(req: KairosRunRequest, background_tasks: BackgroundTasks) -> dict:
    """Start a Kairos execution run. Returns run_id immediately.

    The run executes asynchronously. Poll GET /zoa/kairos/run/{id} for status,
    or stream events via GET /zoa/kairos/run/{id}/stream.
    """
    run_id = str(_uuid.uuid4())

    skill_meta = SkillMeta(
        skill_id=req.skill_id,
        l1_score=req.l1_score,
        l2_score=req.l2_score,
        l3_score=req.l3_score,
        l4_score=req.l4_score,
        permitted_tools=req.permitted_tools,
        allowlisted_tools=req.allowlisted_tools,
    )

    config = {}  # openrouter_api_key resolved from env inside providers.py

    engine = KairosEngine(skill_meta=skill_meta, config=config)

    state = KairosState(
        skill_id=req.skill_id,
        run_id=run_id,
        max_turns=req.max_turns,
    )

    with _RUNS_LOCK:
        _KAIROS_RUNS[run_id] = _new_run_record()

    # Run in a background thread (engine.run() is a sync generator)
    background_tasks.add_task(
        _run_kairos_thread, run_id, engine, req.goal, state
    )

    return {"run_id": run_id, "status": "running"}


@router.get("/zoa/kairos/run/{run_id}")
async def kairos_get_run(run_id: str) -> dict:
    """Poll the status and result of a Kairos run."""
    record = _KAIROS_RUNS.get(run_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")
    with record["lock"]:
        return {
            "run_id": run_id,
            "status": record["status"],
            "event_count": len(record["events"]),
            "result": record["result"],
        }


@router.get("/zoa/kairos/run/{run_id}/stream")
async def kairos_stream_run(run_id: str, request: Request):
    """SSE event stream for a Kairos run.

    Replays all buffered events from the start, then streams new events
    as they arrive. Clients that connect after the run completes receive
    the full event log including the terminal run_complete event.
    """
    record = _KAIROS_RUNS.get(run_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")

    async def event_generator():
        sent = 0
        while True:
            if await request.is_disconnected():
                break

            with record["lock"]:
                events = record["events"]
                new_events = events[sent:]
                status = record["status"]

            for sse_line in new_events:
                yield sse_line
            sent += len(new_events)

            if status in ("done", "failed") and sent >= len(record["events"]):
                break

            await asyncio.sleep(0.1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/zoa/kairos/runs")
async def kairos_list_runs() -> dict:
    """List all in-memory Kairos runs (run_id, status, event_count)."""
    with _RUNS_LOCK:
        runs = [
            {
                "run_id": rid,
                "status": rec["status"],
                "event_count": len(rec["events"]),
            }
            for rid, rec in _KAIROS_RUNS.items()
        ]
    return {"runs": runs, "total": len(runs)}
