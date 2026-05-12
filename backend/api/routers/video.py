"""Video consultation routes - Modular endpoints for telehealth"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import VideoConsultation
from middleware.auth import get_current_user
from services.mcp_client_service import mcp_client_service
from services.audit_service import log_audit
from services.telehealth_analysis_service import analyze_transcript
from datetime import datetime
from uuid import UUID
import json

router = APIRouter(prefix="/api/v1/video", tags=["Video Consultations"])


class TokenRequest(BaseModel):
    room_id: str
    participant_name: str
    participant_role: str = "participant"  # participant, moderator, viewer


class RecordingRequest(BaseModel):
    room_id: str
    recording_id: Optional[str] = None


class TranscriptionRequest(BaseModel):
    room_id: str
    recording_id: str


async def call_mcp_tool(server_name: str, tool_name: str, arguments: dict) -> dict:
    """Helper to call MCP tool and handle responses"""
    try:
        result = await mcp_client_service.call_tool(server_name, tool_name, arguments)
        
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                result = {"response": result}
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling MCP tool: {str(e)}")


@router.post("/generate-token")
async def generate_token(request: TokenRequest):
    """
    Generate VideoSDK token for joining a room
    
    Returns:
    {
      "success": true,
      "token": "eyJhbGc...",
      "join_link": "https://...",
      "expires_in": 3600
    }
    """
    try:
        result = await call_mcp_tool(
            "videosdk",
            "generate_token",
            {
                "room_id": request.room_id,
                "participant_name": request.participant_name,
                "participant_role": request.participant_role
            }
        )
        
        return {
            "success": True,
            "token": result.get("token", ""),
            "join_link": result.get("join_link", ""),
            "expires_in": result.get("expires_in", 3600),
            "room_id": request.room_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating token: {str(e)}")


@router.post("/recordings/start")
async def start_recording(
    request: RecordingRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Start recording a video consultation and create/update consultation record
    
    Returns:
    {
      "success": true,
      "recording_id": "rec_xxx",
      "status": "recording",
      "consultation_id": "uuid"
    }
    """
    try:
        # Start recording via VideoSDK (REAL API if keys configured)
        result = await call_mcp_tool(
            "videosdk",
            "start_recording",
            {
                "room_id": request.room_id,
                "recording_format": "mp4"
            }
        )
        
        recording_id = result.get("recording_id", "")
        
        # Find or create consultation record
        consultation = db.query(VideoConsultation).filter(
            VideoConsultation.room_id == request.room_id,
            VideoConsultation.organization_id == current_user.organization_id
        ).first()
        
        if not consultation:
            consultation = VideoConsultation(
                organization_id=current_user.organization_id,
                room_id=request.room_id,
                started_at=datetime.utcnow()
            )
            db.add(consultation)
        
        consultation.recording_id = recording_id
        db.commit()
        db.refresh(consultation)
        
        return {
            "success": True,
            "recording_id": recording_id,
            "status": "recording",
            "room_id": request.room_id,
            "consultation_id": str(consultation.id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting recording: {str(e)}")


@router.post("/recordings/stop")
async def stop_recording(request: RecordingRequest):
    """
    Stop recording and get download URL
    
    Returns:
    {
      "success": true,
      "recording_url": "https://...",
      "download_url": "https://...",
      "status": "stopped"
    }
    """
    try:
        if not request.recording_id:
            raise HTTPException(status_code=400, detail="recording_id is required")
        
        result = await call_mcp_tool(
            "videosdk",
            "stop_recording",
            {
                "room_id": request.room_id,
                "recording_id": request.recording_id
            }
        )
        
        return {
            "success": True,
            "recording_url": result.get("recording_url") or result.get("download_url", ""),
            "download_url": result.get("download_url", ""),
            "status": "stopped",
            "room_id": request.room_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping recording: {str(e)}")


@router.get("/recordings/{recording_id}/status")
async def get_recording_status(recording_id: str, room_id: str):
    """
    Get recording status
    
    Returns:
    {
      "success": true,
      "status": "recording" | "stopped" | "processing",
      "recording_url": "https://..." (if available)
    }
    """
    try:
        result = await call_mcp_tool(
            "videosdk",
            "get_recording_status",
            {
                "room_id": room_id,
                "recording_id": recording_id
            }
        )
        
        return {
            "success": True,
            "status": result.get("status", "unknown"),
            "recording_url": result.get("recording_url", ""),
            "recording_id": recording_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recording status: {str(e)}")


@router.post("/transcribe-recording")
async def transcribe_recording(
    request: TranscriptionRequest,
    db: Session = Depends(get_db)
):
    """
    Transcribe a video recording using AssemblyAI and STORE in database
    
    Input:
    {
      "room_id": "room_xxx",
      "recording_id": "rec_xxx"
    }
    
    Returns:
    {
      "success": true,
      "recording_url": "https://...",
      "transcription": "...",
      "medical_entities": {...},
      "confidence": 0.933,
      "consultation_id": "uuid",
      "stored": true
    }
    """
    try:
        # 1. Get recording URL
        stop_result = await call_mcp_tool(
            "videosdk",
            "stop_recording",
            {
                "room_id": request.room_id,
                "recording_id": request.recording_id
            }
        )
        
        recording_url = stop_result.get("recording_url") or stop_result.get("download_url")
        if not recording_url:
            raise HTTPException(status_code=400, detail="No recording URL available")
        
        # 2. Transcribe with AssemblyAI (REAL API if keys configured)
        transcription_result = await call_mcp_tool(
            "assemblyai",
            "transcribe_medical",
            {
                "audio_url": recording_url,
                "redact_pii": True,
                "speaker_labels": True
            }
        )
        
        transcription_text = transcription_result.get("transcript", "")
        medical_entities = transcription_result.get("medical_entities", {})
        transcript_id = transcription_result.get("transcript_id", "")
        confidence = transcription_result.get("confidence", 0.933)
        
        # 2.5 AI Telehealth Post-Visit Analysis
        ai_analysis = await analyze_transcript(
            transcript=transcription_text,
            patient_name="Patient",  # In a prod system, fetch from Appointment/User
            provider_name="Dr. Smith"
        )
        
        # 3. Find or create consultation record
        consultation = db.query(VideoConsultation).filter(
            VideoConsultation.room_id == request.room_id,
            VideoConsultation.organization_id == "demo_org"
        ).first()
        
        if not consultation:
            # Create new consultation record
            consultation = VideoConsultation(
                organization_id="demo_org",
                room_id=request.room_id,
                started_at=datetime.utcnow()
            )
            db.add(consultation)
        
        # 4. Update consultation with transcription data & analysis
        consultation.recording_url = recording_url
        consultation.recording_id = request.recording_id
        consultation.transcript_id = transcript_id
        consultation.transcript_text = transcription_text
        consultation.medical_entities = json.dumps(medical_entities)
        consultation.ai_analysis = json.dumps(ai_analysis) if ai_analysis else None
        consultation.ended_at = datetime.utcnow()
        
        if consultation.started_at:
            duration = (consultation.ended_at - consultation.started_at).total_seconds()
            consultation.duration_seconds = int(duration)
        
        db.commit()
        db.refresh(consultation)
        
        # 5. Audit log
        log_audit(
            db=db,
            user_id="demo_user",
            organization_id="demo_org",
            action="video_consultation.transcribed",
            resource_type="VideoConsultation",
            resource_id=consultation.id,
            details=json.dumps({
                "transcript_id": transcript_id,
                "confidence": confidence,
                "recording_url": recording_url
            })
        )
        
        return {
            "success": True,
            "recording_url": recording_url,
            "transcription": transcription_text,
            "medical_entities": medical_entities,
            "ai_analysis": ai_analysis,
            "confidence": confidence,
            "transcript_id": transcript_id,
            "consultation_id": str(consultation.id),
            "stored": True,
            "message": "Transcription and AI Clinical Analysis completed and stored in database"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing recording: {str(e)}")

