"""Central workflow endpoints"""
from fastapi import APIRouter
from api.models import CentralAPIsResponse, CentralTestsResponse
from services.registry_service import RegistryService
from datetime import datetime

router = APIRouter()
registry_service = RegistryService()


@router.get("/apis", response_model=CentralAPIsResponse)
async def get_central_apis():
    """Get all APIs from central registry"""
    data = registry_service.read_frontend_data()
    
    # If frontend data exists, use it (it's already synced)
    if data.get("apis"):
        return CentralAPIsResponse(**data)
    
    # Otherwise, build from registry
    apis = registry_service.get_apis()
    summary = registry_service.get_summary()
    
    return CentralAPIsResponse(
        timestamp=datetime.now().isoformat(),
        summary=summary,
        apis=apis,
        frontend_integration={
            "total_showcases": len([a for a in apis if a.get("frontend", {}).get("integrated")]),
            "integrated_apis": len([a for a in apis if a.get("frontend", {}).get("integrated")]),
            "showcase_pages": [a.get("frontend", {}).get("showcase_page", "") for a in apis if a.get("frontend", {}).get("showcase_page")],
            "last_synced": None,
        }
    )


@router.get("/tests", response_model=CentralTestsResponse)
async def get_central_tests():
    """Get test results from central registry"""
    summary = registry_service.get_summary()
    apis = registry_service.get_apis()
    
    # Build test results
    results = []
    for api in apis:
        for endpoint in api.get("endpoints", []):
            results.append({
                "api": api["name"],
                "endpoint": endpoint.get("name", ""),
                "result": endpoint.get("test_result", "pending"),
                "last_test": endpoint.get("last_test"),
                "tested": endpoint.get("tested", False),
            })
    
    return CentralTestsResponse(
        summary=summary,
        results=results,
    )


@router.post("/sync")
async def trigger_sync():
    """Trigger frontend sync (runs frontend-sync.py)"""
    import subprocess
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent.parent
    sync_script = project_root / "central" / "frontend-sync.py"
    
    try:
        result = subprocess.run(
            ["python", str(sync_script)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "success": result.returncode == 0,
            "message": "Frontend sync completed",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Sync failed: {str(e)}",
        }

