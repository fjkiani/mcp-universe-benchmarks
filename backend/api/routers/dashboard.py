"""Dashboard routes"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from pydantic import BaseModel
from typing import List, Optional
from database.session import get_db
from database.models import Patient, Appointment, VideoConsultation, Message, User
from middleware.auth import get_current_user
from datetime import datetime, timedelta
from uuid import UUID

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


class DashboardOverview(BaseModel):
    total_patients: int
    total_appointments: int
    upcoming_appointments: int
    completed_consultations: int
    total_messages: int
    active_users: int


class RecentActivity(BaseModel):
    id: str
    type: str  # patient, appointment, consultation, message
    action: str
    description: str
    timestamp: str
    user_name: Optional[str] = None


class UpcomingAppointment(BaseModel):
    id: str
    patient_name: str
    provider_name: str
    start_time: str
    status: str


@router.get("/overview", response_model=DashboardOverview)
async def get_overview(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get dashboard overview metrics"""
    org_id = current_user.organization_id
    
    # Total patients
    total_patients = db.query(Patient).filter(
        Patient.organization_id == org_id,
        Patient.deleted_at.is_(None)
    ).count()
    
    # Total appointments
    total_appointments = db.query(Appointment).filter(
        Appointment.organization_id == org_id
    ).count()
    
    # Upcoming appointments (next 7 days)
    upcoming_start = datetime.utcnow()
    upcoming_end = datetime.utcnow() + timedelta(days=7)
    upcoming_appointments = db.query(Appointment).filter(
        Appointment.organization_id == org_id,
        Appointment.start_time >= upcoming_start,
        Appointment.start_time <= upcoming_end,
        Appointment.status == "scheduled"
    ).count()
    
    # Completed consultations
    completed_consultations = db.query(VideoConsultation).filter(
        VideoConsultation.organization_id == org_id,
        VideoConsultation.ended_at.isnot(None)
    ).count()
    
    # Total messages
    total_messages = db.query(Message).filter(
        Message.organization_id == org_id
    ).count()
    
    # Active users
    active_users = db.query(User).filter(
        User.organization_id == org_id,
        User.is_active == True
    ).count()
    
    return {
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "upcoming_appointments": upcoming_appointments,
        "completed_consultations": completed_consultations,
        "total_messages": total_messages,
        "active_users": active_users
    }


@router.get("/appointments/upcoming", response_model=List[UpcomingAppointment])
async def get_upcoming_appointments(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get upcoming appointments"""
    appointments = db.query(Appointment).filter(
        Appointment.organization_id == current_user.organization_id,
        Appointment.start_time >= datetime.utcnow(),
        Appointment.status == "scheduled"
    ).order_by(Appointment.start_time.asc()).limit(limit).all()
    
    results = []
    for apt in appointments:
        # Get patient name from FHIR
        patient_name = "Unknown"
        if apt.patient and apt.patient.fhir_resource:
            name = apt.patient.fhir_resource.get("name", [{}])[0]
            given = name.get("given", [""])[0]
            family = name.get("family", "")
            patient_name = f"{given} {family}".strip()
        
        # Get provider name
        provider_name = "Unknown"
        if apt.provider:
            provider_name = f"{apt.provider.first_name or ''} {apt.provider.last_name or ''}".strip() or apt.provider.email
        
        results.append({
            "id": str(apt.id),
            "patient_name": patient_name,
            "provider_name": provider_name,
            "start_time": apt.start_time.isoformat(),
            "status": apt.status
        })
    
    return results


@router.get("/activity", response_model=List[RecentActivity])
async def get_recent_activity(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get recent activity from audit log"""
    from database.models import AuditLog
    
    activities = db.query(AuditLog).filter(
        AuditLog.organization_id == current_user.organization_id
    ).order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    results = []
    for activity in activities:
        # Determine type from resource_type
        activity_type = activity.resource_type.lower()
        
        # Get user name
        user_name = None
        if activity.user_id:
            user = db.query(User).filter(User.id == activity.user_id).first()
            if user:
                user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.email
        
        # Create description
        description = f"{activity.action.replace('_', ' ').title()}"
        if activity.patient_id:
            description += f" for patient"
        
        results.append({
            "id": str(activity.id),
            "type": activity_type,
            "action": activity.action,
            "description": description,
            "timestamp": activity.created_at.isoformat(),
            "user_name": user_name
        })
    
    return results




