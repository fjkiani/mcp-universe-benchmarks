"""ZOA-W Writing Pipeline — orchestrates the 5-agent writing workflow."""

import asyncio
import logging
import time
import uuid
from typing import Any

from services.writing.outline_agent import OutlineAgent
from services.writing.draft_agent import DraftAgent
from services.writing.critique_agent import CritiqueAgent
from services.writing.refine_agent import RefineAgent
from services.writing.publish_agent import PublishAgent

# In-memory pipeline store (same pattern as benchmark store)
_pipeline_store: dict[str, dict[str, Any]] = {}
MAX_STORE = 200

outline_agent = OutlineAgent()
draft_agent = DraftAgent()
critique_agent = CritiqueAgent()
refine_agent = RefineAgent()
publish_agent = PublishAgent()


async def run_pipeline(
    run_id: str,
    topic: str,
    tone: str,
    target_platform: str,
    max_critique_loops: int = 3,
) -> dict:
    """Full 5-agent writing pipeline with critique loop."""
    store = _pipeline_store[run_id]
    store["status"] = "running"
    store["stage"] = "outline"

    try:
        # Stage 1: Outline
        outline = await outline_agent.generate(topic, tone)
        store["outline"] = outline
        store["stage"] = "draft"

        # Stage 2: Draft
        draft_result = await draft_agent.write(outline, tone)
        draft = draft_result.get("content", "")
        store["draft"] = draft_result
        store["stage"] = "critique"

        # Stage 3-4: Critique + Refine loop
        loops_taken = 0
        critique: dict[str, Any] = {}
        for i in range(max_critique_loops):
            critique = await critique_agent.evaluate(draft, tone)
            store["critique"] = critique
            store["critique_score"] = critique.get("score", 0)
            loops_taken = i + 1

            if critique.get("score", 0) >= 8:
                break

            store["stage"] = "refine"
            store["refine_loop"] = i + 1
            refine_result = await refine_agent.improve(draft, critique, tone)
            draft = refine_result.get("content", draft)
            store["refined_draft"] = refine_result
            store["stage"] = "critique"

        # Stage 5: Publish
        store["stage"] = "publish"
        published = await publish_agent.format(draft, target_platform)

        store.update(
            {
                "status": "completed",
                "stage": "done",
                "published": published,
                "loops_taken": loops_taken,
                "final_score": critique.get("score", 0),
                "completed_at": time.time(),
            }
        )
        return store

    except Exception as exc:
        store.update({"status": "failed", "error": str(exc)})
        logging.getLogger("writing_pipeline").error("Pipeline %s failed: %s", run_id, exc)
        return store


def create_run(topic: str, tone: str, platform: str) -> str:
    """Create a new pipeline run entry and return its run_id."""
    run_id = str(uuid.uuid4())
    _pipeline_store[run_id] = {
        "run_id": run_id,
        "topic": topic,
        "tone": tone,
        "platform": platform,
        "status": "pending",
        "stage": "queued",
        "created_at": time.time(),
    }
    if len(_pipeline_store) > MAX_STORE:
        oldest = sorted(
            _pipeline_store.keys(),
            key=lambda k: _pipeline_store[k].get("created_at", 0),
        )
        for k in oldest[:50]:
            del _pipeline_store[k]
    return run_id


def get_run(run_id: str) -> dict | None:
    """Retrieve a pipeline run by ID, or None if not found."""
    return _pipeline_store.get(run_id)
