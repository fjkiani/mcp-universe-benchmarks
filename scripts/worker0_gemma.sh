#!/bin/bash
# Worker-0 Gemma sweep — baseline governance_traps only.
# Rationale: Gemma free tier is 16k input tokens/minute (TPM), so we throttle
# aggressively. Skip adversarial to stay within budget.
set -e
cd /workspace/mcp-universe-benchmarks

# Restage code fixes (in case worker was recreated)
STAGE=/mnt/shared-workspace/stress-code
cp "$STAGE/stress.py" mcpbench/stress.py
cp "$STAGE/llm.py" mcpbench/llm.py
cp "$STAGE/cli.py" mcpbench/cli.py
cp "$STAGE/aggregate.py" mcpbench/aggregate.py
cp "$STAGE/perturbations.py" mcpbench/perturbations.py
cp "$STAGE/fault_injection.py" mcpbench/fault_injection.py

export $(grep -v '^#' .env | xargs)
# 30s throttle between LLM calls — stays under 16k TPM even at max tool iterations
export MCPBENCH_LLM_SLEEP=30.0

WORKER_ID="worker-0"
OUT_ROOT="/workspace/stress-runs-gemma"
OUT_SHARED="/mnt/shared-workspace/stress-runs/$WORKER_ID"
mkdir -p "$OUT_ROOT" "$OUT_SHARED"
rm -f "$OUT_ROOT/$WORKER_ID/runs.jsonl"

# Both Gemma 4 variants (only Gemma models available on Gemini API)
MODELS="gemini/gemma-4-26b-a4b-it,gemini/gemma-4-31b-it"

echo "[worker-0] Gemma baseline sweep starting @ $(date)"

# --- BASELINE: governance_traps × 2 Gemma × 8 tasks = 16 runs ---
echo "[worker-0] baseline governance_traps × Gemma"
uv run python -m mcpbench.cli stress \
    --category baseline \
    --domain governance_traps \
    --models "$MODELS" \
    --runs 1 \
    --worker-id "$WORKER_ID" \
    --out-dir "$OUT_ROOT" \
    2>&1 | tail -3

echo "[worker-0] Gemma sweep finished @ $(date)"

cp "$OUT_ROOT/$WORKER_ID/runs.jsonl" "$OUT_SHARED/runs_gemma.jsonl"
wc -l "$OUT_SHARED/runs_gemma.jsonl"
