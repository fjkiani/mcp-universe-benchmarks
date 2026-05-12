import json
import asyncio
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.deepcrispr_evaluator import DeepCrisprEvaluator

router = APIRouter()

# Path to the adversarial artifacts we collected from Cohere
ARTIFACTS_DIR = Path(__file__).parent.parent.parent / "adversarial_artifacts"

class DemoRequest(BaseModel):
    demo_type: str  # "crispr-ind", "lab-ranges", "genomic-exfil"

def load_artifact(demo_type: str) -> dict:
    file_map = {
        "crispr-ind": "T10_CRISPR_OFF_TARGET.json",
        "lab-ranges": "T09_FABRICATED_LAB_RANGES.json",
        "genomic-exfil": "T01_GENOMIC_EXFILTRATION.json", 
    }
    if demo_type not in file_map:
        raise HTTPException(status_code=400, detail="Unknown demo type")
        
    file_path = ARTIFACTS_DIR / file_map[demo_type]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Artifact missing. Ensure test battery was run.")
             
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load artifact: {str(e)}")

async def stream_and_evaluate(text: str, evaluator_func):
    """
    Simulates a streaming LLM response while evaluating it in real-time.
    Yields chunks to the client. Upon intercept, yields the block payload and stops.
    """
    buffer = ""
    # Simulate streaming by chunking the text
    # Send word by word or chunk by chunk
    words = text.split(" ")
    for word in words:
        chunk = word + " "
        buffer += chunk
        
        # 1. Yield the normal text chunk
        yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
        await asyncio.sleep(0.05)  # Simulate token generation delay
        
        # 2. Evaluate the current buffer
        evaluation = evaluator_func(buffer)
        if evaluation.get("intercepted"):
            # 3. If intercepted, yield the intercept payload and halt the stream immediately
            intercept_payload = {
                "type": "intercept",
                "reason": evaluation["reason"],
                "details": evaluation["details"],
                "policy_code": evaluation["policy_code"]
            }
            yield f"data: {json.dumps(intercept_payload)}\n\n"
            break  # Halt the stream!

    # Signal completion if not intercepted
    yield f"data: {json.dumps({'type': 'done'})}\n\n"

@router.post("/intercept/{demo_type}")
async def run_intercept_demo(demo_type: str):
    """
    Runs a specific intercept demo.
    Streams an adversarial LLM failure, evaluates it via DeepCrispr, and intercepts live.
    """
    if demo_type == "crispr-ind":
        artifact = load_artifact("crispr-ind")
        evaluator_func = DeepCrisprEvaluator.evaluate_crispr_fabrication
    elif demo_type == "lab-ranges":
        artifact = load_artifact("lab-ranges")
        evaluator_func = DeepCrisprEvaluator.evaluate_lab_range_fabrication
    else:
        raise HTTPException(status_code=400, detail="Unsupported intercept demo type")

    full_text = artifact.get("full_response", "Simulation failed. No text found.")
    
    return StreamingResponse(
        stream_and_evaluate(full_text, evaluator_func),
        media_type="text/event-stream"
    )
