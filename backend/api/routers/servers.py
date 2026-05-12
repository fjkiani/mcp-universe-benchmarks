"""Server management endpoints - Internal Testing Only"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from api.models import ServerStatus
from services.sprint_service import SprintService
from services.server_test_service import ServerTestService

router = APIRouter()
sprint_service = SprintService()
server_test_service = ServerTestService()


@router.get("", response_model=List[ServerStatus])
async def list_servers():
    """List all MCP servers with internal test status"""
    servers = sprint_service.get_server_statuses()
    
    # Enhance with internal test results
    test_results = server_test_service.get_all_servers_status()
    
    for server in servers:
        server_name = server.get("name", "").lower().replace(" ", "_")
        if server_name in test_results.get("servers", {}):
            test_status = test_results["servers"][server_name]
            server["internal_test_status"] = {
                "structure": test_status.get("structure", {}).get("status", "unknown"),
                "api_connectivity": test_status.get("api_connectivity", {}).get("status", "not_tested"),
                "last_tested": test_results.get("timestamp")
            }
    
    return servers


@router.get("/{server_name}", response_model=ServerStatus)
async def get_server(server_name: str):
    """Get specific server status with internal test results"""
    server = sprint_service.get_server_status(server_name)
    if not server:
        raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
    
    # Add internal test results
    test_status = server_test_service.get_server_status(server_name)
    if test_status:
        server["internal_test_status"] = {
            "structure": test_status.get("structure", {}).get("status", "unknown"),
            "api_connectivity": test_status.get("api_connectivity", {}).get("status", "not_tested"),
            "tools_count": test_status.get("structure", {}).get("tools_count", 0),
            "errors": test_status.get("structure", {}).get("errors", [])
        }
    
    return server


@router.post("/test-all")
async def test_all_servers():
    """Run internal server tests for all servers (frontend source of truth)"""
    results = await server_test_service.test_all_servers()
    return {
        "message": "Internal server tests completed",
        "results": results,
        "note": "These are internal tests tracked in frontend. CI/CD runs end-to-end LLM tests separately."
    }


@router.post("/{server_name}/test")
async def test_server(server_name: str):
    """Run internal server test for specific server"""
    result = await server_test_service.test_server_structure(server_name)
    api_result = await server_test_service.test_server_api_connectivity(server_name)
    
    return {
        "server": server_name,
        "structure": result["structure"],
        "api_connectivity": api_result["api_connectivity"],
        "note": "Internal test - tracked in frontend. CI/CD runs end-to-end LLM tests separately."
    }

