"""Sprint metrics endpoints"""
from fastapi import APIRouter
from api.models import SprintMetrics
from services.sprint_service import SprintService

router = APIRouter()
sprint_service = SprintService()


@router.get("/metrics", response_model=SprintMetrics)
async def get_sprint_metrics():
    """Get sprint metrics"""
    return sprint_service.get_metrics()


@router.get("/progress")
async def get_sprint_progress():
    """Get detailed sprint progress"""
    metrics = sprint_service.get_metrics()
    sprint_status = sprint_service.get_sprint_status()
    test_results = sprint_service.get_test_results()
    
    # Get milestones based on sprint status
    milestones = []
    
    if sprint_status["sprint1Complete"]:
        milestones.append({"id": "sprint1-foundation", "name": "Sprint 1: Foundation & Testing", "status": "completed"})
    
    if sprint_status["sprint2Complete"]:
        milestones.append({"id": "sprint2-nexhealth", "name": "Sprint 2: NexHealth Integration", "status": "completed"})
    elif sprint_status["sprint1Complete"]:
        milestones.append({"id": "sprint2-nexhealth", "name": "Sprint 2: NexHealth Integration", "status": "in_progress"})
    
    if metrics["tasksCompleted"] >= 40:
        milestones.append({"id": "sprint3-expansion", "name": "Sprint 3: Task Expansion", "status": "completed"})
    elif sprint_status["sprint2Complete"]:
        milestones.append({"id": "sprint3-expansion", "name": "Sprint 3: Task Expansion", "status": "pending"})
    
    return {
        "metrics": metrics,
        "sprintStatus": sprint_status,
        "testResults": {
            "tasks": test_results.get("tests", {}).get("tasks", {}).get("summary", {}),
            "servers": test_results.get("tests", {}).get("mcp_servers", {}).get("summary", {}),
        },
        "timeline": metrics["currentSprint"],
        "milestones": milestones,
        "blockers": [],
        "lastUpdated": metrics.get("lastUpdated"),
    }

