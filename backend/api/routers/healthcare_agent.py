"""
Healthcare Agent Router — AI-powered scheduling endpoints

POST /api/v1/agent/chat              — universal entry (any vertical)
POST /api/v1/agent/psychiatric       — psychiatric telehealth workflow
POST /api/v1/agent/dental            — dental office workflow
GET  /api/v1/agent/health            — sanity check
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()

from services.healthcare_agent_service import healthcare_agent

router = APIRouter(prefix="/api/v1/agent", tags=["Healthcare Agent"])


class AgentChatRequest(BaseModel):
    message: str
    vertical: Literal["psychiatric_telehealth", "dental", "general"] = "general"
    patient_id: str = "DEMO-001"
    patient_phone: str = "+15551234567"
    patient_name: str = "Patient"


@router.get("/health")
async def agent_health():
    """Quick sanity check — confirms agent service is alive and which APIs are configured."""
    return {
        "status": "alive",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "nexhealth_configured": bool(os.getenv("NEXHEALTH_API_KEY")),
        "twilio_configured": bool(os.getenv("TWILIO_ACCOUNT_SID")),
        "videosdk_configured": bool(os.getenv("VIDEOSDK_API_KEY")),
        "assemblyai_configured": bool(os.getenv("ASSEMBLYAI_API_KEY")),
        "mock_mode": os.getenv("DEMO_MOCK_MODE", "true").lower() == "true"
    }


@router.post("/chat")
async def agent_chat(request: AgentChatRequest):
    """
    Universal healthcare agent endpoint.

    Send patient's natural language message + vertical (psychiatric_telehealth | dental | general).
    Agent triages, checks availability, books, creates video room (if telehealth), sends SMS.

    Returns: message, actions taken (full trace), appointment ID, video link, sms_sent.
    """
    try:
        response = await healthcare_agent.process(
            patient_input=request.message,
            vertical=request.vertical,
            patient_id=request.patient_id,
            patient_phone=request.patient_phone,
            patient_name=request.patient_name
        )
        return response.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/psychiatric")
async def psychiatric_intake(request: AgentChatRequest):
    """
    Psychiatric telehealth workflow.

    Full journey: triage → check psychiatrist availability →
    book telehealth → create VideoSDK room → send SMS with join link.

    Emergency routing: If suicidal ideation/self-harm detected → 988 crisis line.
    """
    request.vertical = "psychiatric_telehealth"
    return await agent_chat(request)


@router.post("/dental")
async def dental_intake(request: AgentChatRequest):
    """
    Dental office workflow.

    Full journey: triage dental urgency → check dentist/oral surgeon availability →
    book in-person appointment → send SMS confirmation.

    Emergency routing: Spreading infection/facial trauma → ER redirect.
    """
    request.vertical = "dental"
    return await agent_chat(request)
