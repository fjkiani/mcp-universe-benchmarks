"""Video consultation management routes - Store and retrieve consultations"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database.session import get_db
from database.models import VideoConsultation, Appointment, Organization
from middleware.auth import get_current_user
from services.audit_service import log_audit
from uuid import UUID
from datetime import datetime

router = APIRouter(prefix="/api/v1/video/consultations", tags=["Video Consultations"])


class ConsultationCreate(BaseModel):
    appointment_id: Optional[str] = None
    room_id: str
    patient_id: Optional[str] = None
    provider_id: Optional[str] = None


class ConsultationUpdate(BaseModel):
    recording_url: Optional[str] = None
    recording_id: Optional[str] = None
    transcript_id: Optional[str] = None
    transcript_text: Optional[str] = None
    medical_entities: Optional[dict] = None
    ended_at: Optional[str] = None


class ConsultationResponse(BaseModel):
    id: str
    room_id: str
    appointment_id: Optional[str]
    recording_url: Optional[str]
    recording_id: Optional[str]
    transcript_id: Optional[str]
    transcript_text: Optional[str]
    medical_entities: Optional[dict]
    started_at: Optional[str]
    ended_at: Optional[str]
    duration_seconds: Optional[int]
    created_at: str

    class Config:
        from_attributes = True


@router.post("", response_model=ConsultationResponse, status_code=201)
async def create_consultation(
    consultation_data: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new video consultation record"""
    consultation = VideoConsultation(
        organization_id=current_user.organization_id,
        appointment_id=UUID(consultation_data.appointment_id) if consultation_data.appointment_id else None,
        room_id=consultation_data.room_id,
        started_at=datetime.utcnow()
    )
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="video_consultation.created",
        resource_type="VideoConsultation",
        resource_id=consultation.id,
        details={"room_id": consultation_data.room_id}
    )
    
    return consultation


@router.get("", response_model=List[ConsultationResponse])
async def list_consultations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    appointment_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List video consultations"""
    query = db.query(VideoConsultation).filter(
        VideoConsultation.organization_id == current_user.organization_id
    )
    
    if appointment_id:
        query = query.filter(VideoConsultation.appointment_id == appointment_id)
    
    consultations = query.order_by(VideoConsultation.created_at.desc()).offset(skip).limit(limit).all()
    return consultations


@router.get("/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation(
    consultation_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a video consultation by ID"""
    consultation = db.query(VideoConsultation).filter(
        VideoConsultation.id == consultation_id,
        VideoConsultation.organization_id == current_user.organization_id
    ).first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    return consultation


@router.put("/{consultation_id}", response_model=ConsultationResponse)
async def update_consultation(
    consultation_id: UUID,
    consultation_data: ConsultationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a video consultation (e.g., add transcription)"""
    consultation = db.query(VideoConsultation).filter(
        VideoConsultation.id == consultation_id,
        VideoConsultation.organization_id == current_user.organization_id
    ).first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    # Update fields
    if consultation_data.recording_url:
        consultation.recording_url = consultation_data.recording_url
    if consultation_data.recording_id:
        consultation.recording_id = consultation_data.recording_id
    if consultation_data.transcript_id:
        consultation.transcript_id = consultation_data.transcript_id
    if consultation_data.transcript_text:
        consultation.transcript_text = consultation_data.transcript_text
    if consultation_data.medical_entities:
        consultation.medical_entities = consultation_data.medical_entities
    if consultation_data.ended_at:
        consultation.ended_at = datetime.fromisoformat(consultation_data.ended_at)
        if consultation.started_at:
            duration = (consultation.ended_at - consultation.started_at).total_seconds()
            consultation.duration_seconds = int(duration)
    
    db.commit()
    db.refresh(consultation)
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="video_consultation.updated",
        resource_type="VideoConsultation",
        resource_id=consultation.id
    )
    
    return consultation




