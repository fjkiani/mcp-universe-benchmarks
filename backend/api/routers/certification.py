"""
Certification API Router — the HTTP interface to the certification engine.

Endpoints:
  POST /api/v1/governance/certify           → Queue a certification run
  GET  /api/v1/governance/certify/{run_id}  → Get run status/progress
  GET  /api/v1/governance/certify/{run_id}/report → Get final certification report
  GET  /api/v1/governance/reports           → List all historical reports
  GET  /api/v1/governance/domains           → List available domains
  POST /api/v1/governance/agents/register   → Register an agent
  GET  /api/v1/governance/agents            → List all registered agents
  GET  /api/v1/governance/stats             → Dashboard summary stats
"""
import json
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import RegisteredAgent, CertificationRun, TaskResult
from services.certification_service import CertificationEngine
from services.report_parser import parse_yaml_reports

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])
engine = CertificationEngine()


# ── Request/Response Models ──────────────────────────────────────────

class CertifyRequest(BaseModel):
    agent_name: str
    model: str = "gpt-4o"
    domain: str = "grant_application"
    agent_type: str = "react"


class AgentRegisterRequest(BaseModel):
    name: str
    model: str
    agent_type: str = "react"
    mcp_tools: List[str] = []
    risk_tier: str = "medium"


class CertifyStatusResponse(BaseModel):
    run_id: str
    status: str
    progress_pct: int
    current_task: Optional[str] = None
    total_tasks: int
    completed_tasks: int


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Dashboard summary statistics for the Command Center."""
    total_agents = db.query(RegisteredAgent).count()
    total_runs = db.query(CertificationRun).count()
    completed_runs = db.query(CertificationRun).filter_by(status="completed").all()
    
    # Global pass rate
    if completed_runs:
        scores = [r.overall_score for r in completed_runs if r.overall_score is not None]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    else:
        avg_score = 0
    
    # Traps triggered (tasks that failed at L3)
    traps_triggered = db.query(TaskResult).filter(
        TaskResult.evaluation_level == "L3",
        TaskResult.passed == False
    ).count()
    
    return {
        "registered_agents": total_agents,
        "certifications_run": total_runs,
        "global_pass_rate": avg_score,
        "traps_triggered": traps_triggered,
    }


@router.post("/certify")
async def start_certification(
    req: CertifyRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Queue a certification run."""
    if not engine.validate_domain(req.domain):
        raise HTTPException(400, f"Unknown domain: {req.domain}. Available: {list(engine._domains.keys())}")
    
    # Find or create agent
    agent = db.query(RegisteredAgent).filter_by(name=req.agent_name).first()
    if not agent:
        agent = RegisteredAgent(name=req.agent_name, model=req.model, agent_type=req.agent_type)
        db.add(agent)
        db.commit()
        db.refresh(agent)
    
    # Create run record
    domains = engine._domains
    run = CertificationRun(
        agent_id=agent.id,
        domain=req.domain,
        status="queued",
        total_tasks=domains[req.domain]["task_count"],
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    
    # Queue background execution
    background_tasks.add_task(_execute_certification, run.id, req.domain, req.model, req.agent_type)
    
    return {"run_id": run.id, "status": "queued", "total_tasks": run.total_tasks}


@router.get("/certify/{run_id}")
async def get_certification_status(run_id: str, db: Session = Depends(get_db)):
    """Get the current status of a certification run."""
    run = db.query(CertificationRun).filter_by(id=run_id).first()
    if not run:
        raise HTTPException(404, "Run not found")
    return CertifyStatusResponse(
        run_id=run.id,
        status=run.status,
        progress_pct=run.progress_pct,
        current_task=run.current_task,
        total_tasks=run.total_tasks,
        completed_tasks=run.completed_tasks,
    )


@router.get("/certify/{run_id}/report")
async def get_certification_report(run_id: str, db: Session = Depends(get_db)):
    """Get the full certification report for a completed run."""
    run = db.query(CertificationRun).filter_by(id=run_id).first()
    if not run:
        raise HTTPException(404, "Run not found")
    if run.status != "completed":
        raise HTTPException(400, f"Run status is '{run.status}', not completed")
    
    task_results = db.query(TaskResult).filter_by(run_id=run_id).all()
    return {
        "run_id": run.id,
        "agent": run.agent.name if run.agent else "unknown",
        "domain": run.domain,
        "grade": run.grade,
        "overall_score": run.overall_score,
        "level_scores": {
            "L1_syntax": run.l1_syntax_score,
            "L2_resilience": run.l2_resilience_score,
            "L3_protocol": run.l3_protocol_score,
            "L4_objective": run.l4_objective_score,
        },
        "total_tasks": run.total_tasks,
        "completed_tasks": run.completed_tasks,
        "task_results": [{
            "task": tr.task_path,
            "category": tr.category,
            "level": tr.evaluation_level,
            "passed": tr.passed,
            "score": tr.score,
            "error": tr.error,
        } for tr in task_results],
    }


@router.get("/reports")
async def list_reports(db: Session = Depends(get_db)):
    """List all certification reports — both from DB and from historical YAML files."""
    # DB reports
    runs = db.query(CertificationRun).filter_by(status="completed").order_by(
        CertificationRun.completed_at.desc()
    ).limit(50).all()
    
    db_reports = [{
        "run_id": r.id,
        "agent": r.agent.name if r.agent else "unknown",
        "domain": r.domain,
        "grade": r.grade,
        "overall_score": r.overall_score,
        "completed_at": r.completed_at.isoformat() if r.completed_at else None,
    } for r in runs]
    
    # Historical YAML reports (seed data)
    yaml_reports = parse_yaml_reports()
    
    return {"db_reports": db_reports, "historical_reports": yaml_reports}


@router.get("/domains")
async def list_domains():
    """List all available certification domains with task counts."""
    return engine._domains


@router.post("/agents/register")
async def register_agent(req: AgentRegisterRequest, db: Session = Depends(get_db)):
    """Register a new agent for certification."""
    # Check if agent already exists
    existing = db.query(RegisteredAgent).filter_by(name=req.name).first()
    if existing:
        raise HTTPException(400, f"Agent '{req.name}' already registered. ID: {existing.id}")
    
    agent = RegisteredAgent(
        name=req.name,
        model=req.model,
        agent_type=req.agent_type,
        mcp_tools=json.dumps(req.mcp_tools),
        risk_tier=req.risk_tier,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return {"agent_id": agent.id, "name": agent.name, "risk_tier": agent.risk_tier}


@router.get("/agents")
async def list_agents(db: Session = Depends(get_db)):
    """List all registered agents with their latest certification status."""
    agents = db.query(RegisteredAgent).order_by(RegisteredAgent.created_at.desc()).all()
    result = []
    for agent in agents:
        latest_run = (
            db.query(CertificationRun)
            .filter_by(agent_id=agent.id)
            .order_by(CertificationRun.created_at.desc())
            .first()
        )
        result.append({
            "id": agent.id,
            "name": agent.name,
            "model": agent.model,
            "agent_type": agent.agent_type,
            "mcp_tools": json.loads(agent.mcp_tools) if agent.mcp_tools else [],
            "risk_tier": agent.risk_tier,
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
            "latest_certification": {
                "run_id": latest_run.id,
                "domain": latest_run.domain,
                "grade": latest_run.grade,
                "overall_score": latest_run.overall_score,
                "status": latest_run.status,
                "completed_at": latest_run.completed_at.isoformat() if latest_run and latest_run.completed_at else None,
            } if latest_run else None,
        })
    return result


# ── Background Task ──────────────────────────────────────────────────

async def _execute_certification(run_id: str, domain: str, model: str, agent_type: str):
    """Background task that executes the certification run."""
    from database.session import SessionLocal
    db = SessionLocal()
    
    try:
        run = db.query(CertificationRun).filter_by(id=run_id).first()
        if not run:
            return
        
        run.status = "running"
        run.started_at = datetime.utcnow()
        db.commit()
        
        result = await engine.run_certification(
            run_id=run_id,
            domain=domain,
            model=model,
            agent_type=agent_type,
        )
        
        # Store L1-L4 scores
        run.l1_syntax_score = result["level_scores"].get("L1", 0)
        run.l2_resilience_score = result["level_scores"].get("L2", 0)
        run.l3_protocol_score = result["level_scores"].get("L3", 0)
        run.l4_objective_score = result["level_scores"].get("L4", 0)
        run.overall_score = result["overall_score"]
        run.grade = result["grade"]
        run.completed_tasks = result["passed_tasks"]
        run.status = "completed"
        run.completed_at = datetime.utcnow()
        run.progress_pct = 100
        db.commit()
        
        # Store per-task results
        for detail in result["task_details"]:
            task_result = TaskResult(
                run_id=run_id,
                task_path=detail["task_path"],
                category=detail["category"],
                passed=detail["passed"],
                evaluation_level=detail["level"],
                error=detail.get("error"),
            )
            db.add(task_result)
        db.commit()
        
    except Exception as e:
        run = db.query(CertificationRun).filter_by(id=run_id).first()
        if run:
            run.status = "failed"
            run.completed_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()
