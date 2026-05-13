"""ZOA-W Writing Overlord — FastAPI router mounted at /api/v1/writing."""

import asyncio
import logging
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.writing.outline_agent import OutlineAgent
from services.writing.draft_agent import DraftAgent
from services.writing.critique_agent import CritiqueAgent
from services.writing.refine_agent import RefineAgent
from services.writing.publish_agent import PublishAgent
from services.writing.writing_pipeline import create_run, get_run, run_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(tags=["writing"])

# Shared agent instances (stateless — safe to reuse)
_outline_agent = OutlineAgent()
_draft_agent = DraftAgent()
_critique_agent = CritiqueAgent()
_refine_agent = RefineAgent()
_publish_agent = PublishAgent()


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class PipelineRunRequest(BaseModel):
    topic: str = Field(..., min_length=1, description="Topic to write about")
    tone: str = Field(
        ...,
        description="Writing tone: zeta_warlord | professional | technical | satirical",
    )
    platform: str = Field(
        ...,
        description="Target platform: medium | linkedin | blog | cold_email",
    )
    max_loops: Optional[int] = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum critique-refine loops before publishing",
    )


class OutlineRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    tone: str = Field(...)


class DraftRequest(BaseModel):
    outline: dict[str, Any] = Field(...)
    tone: str = Field(...)


class CritiqueRequest(BaseModel):
    draft: str = Field(..., min_length=1)
    tone: str = Field(...)


class RefineRequest(BaseModel):
    draft: str = Field(..., min_length=1)
    critique: dict[str, Any] = Field(...)
    tone: str = Field(...)


class PublishRequest(BaseModel):
    content: str = Field(..., min_length=1)
    platform: str = Field(...)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/health")
async def writing_health() -> dict:
    """Health check for the writing service."""
    return {
        "status": "ok",
        "service": "ZOA-W Writing Overlord",
        "agents": ["outline", "draft", "critique", "refine", "publish"],
        "tones": ["zeta_warlord", "professional", "technical", "satirical"],
        "platforms": ["medium", "linkedin", "blog", "cold_email"],
    }


@router.post("/pipeline/run")
async def pipeline_run(request: PipelineRunRequest) -> dict:
    """Start a full 5-agent writing pipeline asynchronously.

    Returns immediately with a run_id. Poll /pipeline/{run_id} for status.
    """
    try:
        run_id = create_run(request.topic, request.tone, request.platform)
        asyncio.create_task(
            run_pipeline(
                run_id=run_id,
                topic=request.topic,
                tone=request.tone,
                target_platform=request.platform,
                max_critique_loops=request.max_loops or 3,
            )
        )
        logger.info(
            "Pipeline started: run_id=%s topic=%r tone=%r platform=%r",
            run_id,
            request.topic,
            request.tone,
            request.platform,
        )
        return {"run_id": run_id, "status": "pending"}
    except Exception as exc:
        logger.error("pipeline_run error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/pipeline/{run_id}")
async def pipeline_status(run_id: str) -> dict:
    """Poll the status of a running or completed pipeline."""
    try:
        run = get_run(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail=f"Run {run_id!r} not found")
        return run
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("pipeline_status error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/outline")
async def outline(request: OutlineRequest) -> dict:
    """Generate a battle-plan outline for a topic and tone."""
    try:
        result = await _outline_agent.generate(topic=request.topic, tone=request.tone)
        return result
    except Exception as exc:
        logger.error("outline endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/draft")
async def draft(request: DraftRequest) -> dict:
    """Write a full draft from an outline."""
    try:
        result = await _draft_agent.write(outline=request.outline, tone=request.tone)
        return result
    except Exception as exc:
        logger.error("draft endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/critique")
async def critique(request: CritiqueRequest) -> dict:
    """Evaluate a draft against the 5-dimension rubric."""
    try:
        result = await _critique_agent.evaluate(draft=request.draft, tone=request.tone)
        return result
    except Exception as exc:
        logger.error("critique endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/refine")
async def refine(request: RefineRequest) -> dict:
    """Apply critique fixes and return a strengthened draft."""
    try:
        result = await _refine_agent.improve(
            draft=request.draft,
            critique=request.critique,
            tone=request.tone,
        )
        return result
    except Exception as exc:
        logger.error("refine endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/publish")
async def publish(request: PublishRequest) -> dict:
    """Format content for a target publishing platform."""
    try:
        result = await _publish_agent.format(
            content=request.content,
            platform=request.platform,
        )
        return result
    except Exception as exc:
        logger.error("publish endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
