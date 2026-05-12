"""Task management endpoints"""
from fastapi import APIRouter, HTTPException
from api.models import TaskStatus
from pathlib import Path
import json
from typing import List, Dict, Any
from datetime import datetime


router = APIRouter()


def get_task_files() -> List[Path]:
    """Get all task JSON files"""
    project_root = Path(__file__).parent.parent.parent.parent
    tasks_dir = project_root / "domains" / "healthcare_receptionist" / "tasks"
    
    if not tasks_dir.exists():
        return []
    
    return list(tasks_dir.glob("*.json"))


@router.get("", response_model=List[TaskStatus])
async def list_tasks():
    """List all tasks"""
    task_files = get_task_files()
    tasks = []
    
    # Get test results if available
    project_root = Path(__file__).parent.parent.parent.parent
    local_tests_dir = project_root / "local_tests" / "results"
    test_results = {}
    
    if local_tests_dir.exists():
        test_files = sorted(local_tests_dir.glob("test_results_*.json"), reverse=True)
        if test_files:
            try:
                with open(test_files[0], 'r') as f:
                    test_results = json.load(f)
            except:
                pass
    
    task_results = test_results.get("tests", {}).get("tasks", {}).get("results", [])
    task_status_map = {r.get("task"): r.get("status") for r in task_results}
    
    for task_file in task_files:
        try:
            with open(task_file, 'r') as f:
                task_data = json.load(f)
            
            task_id = task_file.stem
            mcp_servers = task_data.get("mcp_servers", [])
            server_names = [s.get("name") if isinstance(s, dict) else s for s in mcp_servers]
            
            # Determine status
            task_status = task_status_map.get(task_id, "pending")
            if task_status == "valid":
                status = "completed"
            elif task_status == "warning":
                status = "in_progress"
            elif task_status == "error":
                status = "failed"
            else:
                status = "pending"
            
            # Check if uses NexHealth
            uses_nexhealth = "nexhealth" in server_names
            
            task = TaskStatus(
                id=task_id,
                name=task_data.get("category", task_id).replace("_", " ").title(),
                category=task_data.get("category", "unknown"),
                status=status,
                servers=server_names,
                passRate=100.0 if task_status == "valid" else None,
                lastTested=datetime.now().isoformat() if task_status == "valid" else None,
            )
            tasks.append(task)
        except Exception as e:
            # Skip invalid task files
            continue
    
    return tasks


@router.get("/{task_id}", response_model=Dict[str, Any])
async def get_task(task_id: str):
    """Get specific task details"""
    project_root = Path(__file__).parent.parent.parent.parent
    task_file = project_root / "domains" / "healthcare_receptionist" / "tasks" / f"{task_id}.json"
    
    if not task_file.exists():
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    
    try:
        with open(task_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading task: {str(e)}")


@router.get("/{task_id}/status", response_model=Dict[str, Any])
async def get_task_status(task_id: str):
    """Get task status"""
    task = await get_task(task_id)
    
    # Get test results if available
    project_root = Path(__file__).parent.parent.parent.parent
    local_tests_dir = project_root / "local_tests" / "results"
    test_results = {}
    
    if local_tests_dir.exists():
        test_files = sorted(local_tests_dir.glob("test_results_*.json"), reverse=True)
        if test_files:
            try:
                with open(test_files[0], 'r') as f:
                    test_results = json.load(f)
            except:
                pass
    
    # Find task in test results
    task_results = test_results.get("tests", {}).get("tasks", {}).get("results", [])
    task_result = next((r for r in task_results if r.get("task") == task_id), None)
    
    task_status = task_result.get("status", "pending") if task_result else "pending"
    if task_status == "valid":
        status = "completed"
        pass_rate = 100.0
    elif task_status == "warning":
        status = "in_progress"
        pass_rate = None
    elif task_status == "error":
        status = "failed"
        pass_rate = 0.0
    else:
        status = "pending"
        pass_rate = None
    
    return {
        "id": task_id,
        "status": status,
        "lastTested": datetime.now().isoformat() if task_result else None,
        "passRate": pass_rate,
        "completed": status == "completed",
        "testResult": task_result,
    }

