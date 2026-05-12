"""Audit logging service for HIPAA compliance"""
from sqlalchemy.orm import Session
from database.models import AuditLog
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from fastapi import Request

def log_audit(
    db: Session,
    user_id: UUID,
    organization_id: UUID,
    action: str,
    resource_type: str,
    resource_id: Optional[UUID] = None,
    patient_id: Optional[UUID] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """Log an audit event (synchronous for database operations)"""
    audit_entry = AuditLog(
        organization_id=organization_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        patient_id=patient_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details or {}
    )
    db.add(audit_entry)
    db.commit()


def get_client_ip(request: Request) -> Optional[str]:
    """Get client IP address from request"""
    if request.client:
        return request.client.host
    return None


def get_user_agent(request: Request) -> Optional[str]:
    """Get user agent from request"""
    return request.headers.get("user-agent")

