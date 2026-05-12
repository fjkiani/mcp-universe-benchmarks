"""Pydantic models for API responses"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class ServerStatus(BaseModel):
    """Server status model"""
    name: str
    status: str  # ready, testing, failed, pending
    structure: bool
    syntax: bool
    apiKeys: bool
    dependencies: bool
    testsPassed: int
    testsFailed: int
    tools: List[str]
    lastTested: Optional[str] = None


class SprintMetrics(BaseModel):
    """Sprint metrics model"""
    currentSprint: str
    passRate: float
    tasksCompleted: int
    tasksTotal: int
    serversTested: int
    serversTotal: int
    priorities: List[Dict[str, Any]] = []


class TaskStatus(BaseModel):
    """Task status model"""
    id: str
    name: str
    category: str
    status: str  # completed, in_progress, pending
    servers: List[str]
    passRate: Optional[float] = None
    lastTested: Optional[str] = None


class APIStatus(BaseModel):
    """API status from registry"""
    id: str
    name: str
    category: str
    status: str
    mcp_server: str
    endpoints: List[Dict[str, Any]]
    tests: Dict[str, int]
    frontend: Dict[str, Any]


class CentralAPIsResponse(BaseModel):
    """Response for /api/v1/central/apis"""
    timestamp: str
    summary: Dict[str, Any]
    apis: List[APIStatus]
    frontend_integration: Dict[str, Any]


class CentralTestsResponse(BaseModel):
    """Response for /api/v1/central/tests"""
    summary: Dict[str, Any]
    results: List[Dict[str, Any]]

