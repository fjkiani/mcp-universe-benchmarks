"""Appointment management routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.session import get_db
from database.models import Appointment, Patient, User
from middleware.auth import get_current_user
from services.audit_service import log_audit
from services.mcp_client_service import mcp_client_service
from uuid import UUID
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/appointments", tags=["Appointments"])


class AppointmentCreate(BaseModel):
    patient_id: str
    provider_id: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    reason: Optional[str] = None
    appointment_type: Optional[str] = "general"


class AppointmentUpdate(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: str
    patient_id: str
    provider_id: str
    fhir_resource: dict
    status: str
    start_time: str
    end_time: str
    notes: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


def create_fhir_appointment(
    appointment_id: str,
    patient_id: str,
    provider_id: str,
    start_time: datetime,
    end_time: datetime,
    status: str = "scheduled"
) -> dict:
    """Create FHIR Appointment resource"""
    return {
        "resourceType": "Appointment",
        "id": appointment_id,
        "status": status,
        "serviceType": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/service-type",
                "code": "general"
            }]
        }],
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "participant": [
            {
                "actor": {
                    "reference": f"Patient/{patient_id}"
                },
                "status": "accepted"
            },
            {
                "actor": {
                    "reference": f"Practitioner/{provider_id}"
                },
                "status": "accepted"
            }
        ]
    }


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new appointment"""
    # Validate patient
    patient = db.query(Patient).filter(
        Patient.id == appointment_data.patient_id,
        Patient.organization_id == current_user.organization_id,
        Patient.deleted_at.is_(None)
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Validate provider
    provider = db.query(User).filter(
        User.id == appointment_data.provider_id,
        User.organization_id == current_user.organization_id,
        User.is_active == True
    ).first()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    
    # Parse date and time
    start_time = datetime.fromisoformat(f"{appointment_data.date}T{appointment_data.time}:00")
    end_time = start_time + timedelta(minutes=30)  # Default 30-minute appointment
    
    # Check provider availability (call NexHealth MCP if available)
    try:
        availability = await mcp_client_service.call_tool(
            "nexhealth",
            "check_provider_availability",
            {
                "provider_id": appointment_data.provider_id,
                "start_date": appointment_data.date,
                "end_date": appointment_data.date,
                "appointment_type": appointment_data.appointment_type
            }
        )
        # If mock mode, availability will return mock data
    except Exception:
        # If MCP call fails, proceed anyway (for demo/mock mode)
        pass
    
    # Create FHIR resource
    fhir_resource = create_fhir_appointment(
        str(UUID()),
        str(patient.id),
        str(provider.id),
        start_time,
        end_time
    )
    
    # Create appointment
    appointment = Appointment(
        organization_id=current_user.organization_id,
        patient_id=patient.id,
        provider_id=provider.id,
        fhir_resource=fhir_resource,
        status="scheduled",
        start_time=start_time,
        end_time=end_time,
        notes=appointment_data.reason
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    # Try to book in NexHealth (if available)
    try:
        await mcp_client_service.call_tool(
            "nexhealth",
            "book_appointment",
            {
                "provider_id": appointment_data.provider_id,
                "patient_id": appointment_data.patient_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "appointment_type": appointment_data.appointment_type,
                "notes": appointment_data.reason or ""
            }
        )
    except Exception:
        # If booking fails, appointment is still created locally
        pass
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="appointment.created",
        resource_type="Appointment",
        resource_id=appointment.id,
        patient_id=patient.id,
        details={"provider_id": str(provider.id), "start_time": start_time.isoformat()}
    )
    
    return appointment


@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    patient_id: Optional[str] = Query(None),
    provider_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List appointments with filters"""
    query = db.query(Appointment).filter(
        Appointment.organization_id == current_user.organization_id
    )
    
    if start_date:
        query = query.filter(Appointment.start_time >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Appointment.start_time <= datetime.fromisoformat(end_date))
    if status:
        query = query.filter(Appointment.status == status)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if provider_id:
        query = query.filter(Appointment.provider_id == provider_id)
    
    appointments = query.order_by(Appointment.start_time.asc()).offset(skip).limit(limit).all()
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get an appointment by ID"""
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.organization_id == current_user.organization_id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: UUID,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an appointment"""
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.organization_id == current_user.organization_id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Update fields
    if appointment_data.date and appointment_data.time:
        start_time = datetime.fromisoformat(f"{appointment_data.date}T{appointment_data.time}:00")
        appointment.start_time = start_time
        appointment.end_time = start_time + timedelta(minutes=30)
    
    if appointment_data.status:
        appointment.status = appointment_data.status
    
    if appointment_data.reason:
        appointment.notes = appointment_data.reason
    
    if appointment_data.notes:
        appointment.notes = appointment_data.notes
    
    appointment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(appointment)
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="appointment.updated",
        resource_type="Appointment",
        resource_id=appointment.id,
        patient_id=appointment.patient_id
    )
    
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cancel an appointment"""
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.organization_id == current_user.organization_id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Update status to cancelled
    appointment.status = "cancelled"
    appointment.updated_at = datetime.utcnow()
    db.commit()
    
    # Try to cancel in NexHealth
    try:
        await mcp_client_service.call_tool(
            "nexhealth",
            "cancel_appointment",
            {
                "appointment_id": str(appointment_id)
            }
        )
    except Exception:
        pass
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="appointment.cancelled",
        resource_type="Appointment",
        resource_id=appointment.id,
        patient_id=appointment.patient_id
    )
    
    return None

