# Adapted from SafeRL-Lab/cheetahclaws agent.py (Apache-2.0)
# Modifications: OpenRouter provider, benchmark permission gates, phase tracking,
#   degradation detection, no REPL/runtime/quota/circuit_breaker dependencies.
"""Kairos Execution Engine — Plan→Act→Observe→Refine loop for ZOA skill execution."""
from __future__ import annotations

import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Generator, Optional

from .compaction import maybe_compact, estimate_tokens, get_context_limit, compact_messages, sanitize_history
from .permission_gate import SkillMeta, check as _gate_check, requires_human_approval
from .providers import stream, AssistantTurn, TextChunk, ThinkingChunk, model_for_phase
from .tool_registry import get_tool_schemas, get_tool, execute_tool

logger = logging.getLogger(__name__)

__all__ = [
    "KairosEngine", "KairosState", "KairosResult",
    "PhaseChange", "PermissionViolation",
    "TextChunk", "ThinkingChunk",
    "ToolStart", "ToolEnd", "TurnDone", "PermissionRequest",
]


# ── Event types ───────────────────────────────────────────────────────────────

@dataclass
class ToolStart:
    name: str
    inputs: dict


@dataclass
class ToolEnd:
    name: str
    result: str
    permitted: bool = True


@dataclass
class TurnDone:
    input_tokens: int
    output_tokens: int


@dataclass
class PermissionRequest:
    description: str
    granted: bool = False


@dataclass
class PhaseChange:
    """Emitted when the state machine transitions to a new phase."""
    phase: str  # planning | acting | observing | refining | done | failed


@dataclass
class PermissionViolation:
    """Emitted when a tool call is blocked by the permission gate."""
    tool_name: str
    reason: str
    benchmark_score: float = 0.0


# ── State ─────────────────────────────────────────────────────────────────────

@dataclass
class KairosState:
    """Mutable execution state for a single Kairos run."""
    messages: list = field(default_factory=list)
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    turn_count: int = 0
    # Kairos-specific
    skill_id: str = ""
    run_id: str = ""
    phase: str = "idle"
    tool_calls_made: int = 0
    tool_calls_timed_out: int = 0
    permission_violations: list = field(default_factory=list)
    max_turns: int = 20


@dataclass
class KairosResult:
    """Final result after the Kairos loop completes."""
    run_id: str
    success: bool
    final_text: str
    turns: int
    tool_calls_made: int
    violations: list
    degraded: bool = False
    error: Optional[str] = None

    @property
    def timeout_rate(self) -> float:
        return 0.0  # populated by engine after run


# ── System prompt builder ─────────────────────────────────────────────────────

def _build_system_prompt(skill_id: str, goal: str, skill_meta: SkillMeta, memory_summary: str) -> str:
    gate_info = (
        f"L1={skill_meta.l1_score:.0f} L2={skill_meta.l2_score:.0f} "
        f"L3={skill_meta.l3_score:.0f} L4={skill_meta.l4_score:.1f}"
    )
    aggressive = "AGGRESSIVE CHAINING ENABLED (L3≥80)" if skill_meta.l3_score >= 80 else "STANDARD GATING"
    permitted = ", ".join(skill_meta.permitted_tools) if skill_meta.permitted_tools else "all registered tools"

    prompt = f"""You are Kairos, a Zeta-grade execution engine running skill '{skill_id}'.

GOAL: {goal}

BENCHMARK PROFILE: {gate_info} | {aggressive}
PERMITTED TOOLS: {permitted}

EXECUTION PROTOCOL:
1. PLAN: Break the goal into concrete tool calls. Think step by step.
2. ACT: Execute tools one at a time (or in parallel if safe).
3. OBSERVE: Analyze each tool result before proceeding.
4. REFINE: If the goal is not yet met, loop back to plan with new context.
5. DONE: When the goal is fully achieved, output a clear summary.

RULES:
- Only call tools in your permitted list. Attempting blocked tools wastes turns.
- If a tool returns an error, diagnose it and try an alternative approach.
- Do not hallucinate tool results. If a tool fails, report the real error.
- Max turns: {20}. Be efficient.
"""
    if memory_summary:
        prompt += f"\n{memory_summary}\n"
    return prompt


# ── Main engine ───────────────────────────────────────────────────────────────

class KairosEngine:
    """Kairos execution engine. Call run() to get a generator of events."""

    def __init__(self, skill_meta: SkillMeta, config: dict):
        self.skill_meta = skill_meta
        self.config = config

    def run(
        self,
        goal: str,
        state: KairosState,
        memory_summary: str = "",
        cancel_check=None,
    ) -> Generator:
        """Execute the Plan→Act→Observe→Refine loop.

        Yields: PhaseChange | TextChunk | ThinkingChunk | ToolStart | ToolEnd |
                PermissionRequest | PermissionViolation | TurnDone
        """
        system_prompt = _build_system_prompt(
            state.skill_id, goal, self.skill_meta, memory_summary
        )

        # Append initial user message
        state.messages.append({"role": "user", "content": goal})

        # Phase: planning
        state.phase = "planning"
        yield PhaseChange("planning")

        while True:
            if cancel_check and cancel_check():
                state.phase = "failed"
                yield PhaseChange("failed")
                return

            if state.turn_count >= state.max_turns:
                state.phase = "failed"
                yield PhaseChange("failed")
                yield TextChunk(f"\n[Kairos: max turns ({state.max_turns}) reached]\n")
                return

            state.turn_count += 1
            assistant_turn: Optional[AssistantTurn] = None

            # Compact context if needed
            try:
                maybe_compact(state, self.config)
            except Exception as e:
                logger.warning(f"Kairos compaction failed: {e}")

            # Sanitize history (enforce tool_calls ↔ tool-response pairing)
            state.messages = sanitize_history(state.messages)

            # Determine model for current phase
            model = model_for_phase(state.phase)
            run_config = {**self.config, "model": model}

            # Stream from OpenRouter
            max_retries = 3
            for attempt in range(max_retries + 1):
                try:
                    for event in stream(
                        model=model,
                        system=system_prompt,
                        messages=state.messages,
                        tool_schemas=get_tool_schemas(),
                        config=run_config,
                    ):
                        if isinstance(event, (TextChunk, ThinkingChunk)):
                            yield event
                        elif isinstance(event, AssistantTurn):
                            assistant_turn = event
                    break  # success

                except Exception as e:
                    if attempt >= max_retries:
                        state.phase = "failed"
                        yield PhaseChange("failed")
                        yield TextChunk(f"\n[Kairos: API failed after {max_retries} retries: {e}]\n")
                        return
                    backoff = min(2 ** (attempt + 1), 30)
                    yield TextChunk(f"\n[Kairos: retry {attempt+1}/{max_retries} in {backoff}s: {e}]\n")
                    time.sleep(backoff)

            if assistant_turn is None:
                state.phase = "failed"
                yield PhaseChange("failed")
                return

            # Record assistant turn
            state.messages.append({
                "role": "assistant",
                "content": assistant_turn.text,
                "tool_calls": assistant_turn.tool_calls,
            })
            state.total_input_tokens += assistant_turn.in_tokens
            state.total_output_tokens += assistant_turn.out_tokens
            yield TurnDone(assistant_turn.in_tokens, assistant_turn.out_tokens)

            # No tool calls → done
            if not assistant_turn.tool_calls:
                state.phase = "done"
                yield PhaseChange("done")
                return

            # Phase: acting
            state.phase = "acting"
            yield PhaseChange("acting")

            tool_calls = assistant_turn.tool_calls

            # ── Permission check (sequential) ──────────────────────────────
            permissions: dict[str, bool] = {}
            for tc in tool_calls:
                permitted, violation_reason = _gate_check(tc, self.skill_meta)

                if not permitted:
                    # Hard block — log violation
                    violation = PermissionViolation(
                        tool_name=tc.get("name", ""),
                        reason=violation_reason or "blocked by permission gate",
                        benchmark_score=self.skill_meta.l4_score,
                    )
                    state.permission_violations.append({
                        "tool": tc.get("name", ""),
                        "reason": violation_reason,
                        "turn": state.turn_count,
                    })
                    yield violation
                    permissions[tc["id"]] = False
                elif requires_human_approval(tc, self.skill_meta):
                    # Soft gate — yield PermissionRequest, wait for grant
                    req = PermissionRequest(description=_permission_desc(tc))
                    yield req
                    permissions[tc["id"]] = req.granted
                else:
                    permissions[tc["id"]] = True

            # ── Parallel vs sequential batching ───────────────────────────
            aggressive = self.skill_meta.l3_score >= 80.0
            parallel_batch = []
            sequential_batch = []

            for tc in tool_calls:
                if not permissions[tc["id"]]:
                    sequential_batch.append(tc)
                    continue
                tdef = get_tool(tc["name"])
                if tdef and (tdef.concurrent_safe or aggressive) and len(tool_calls) > 1:
                    parallel_batch.append(tc)
                else:
                    sequential_batch.append(tc)

            def _exec_one(tc):
                tid = tc["id"]
                if not permissions[tid]:
                    return tc, "Denied: blocked by Kairos permission gate", False
                result = execute_tool(tc["name"], tc["input"], run_config)
                # Track timeouts
                if "timed out" in result.lower():
                    state.tool_calls_timed_out += 1
                state.tool_calls_made += 1
                return tc, result, True

            results_ordered = []

            if parallel_batch:
                for tc in parallel_batch:
                    yield ToolStart(tc["name"], tc["input"])
                with ThreadPoolExecutor(max_workers=min(len(parallel_batch), 8)) as pool:
                    futures = {pool.submit(_exec_one, tc): tc for tc in parallel_batch}
                    for future in futures:
                        tc, result, permitted = future.result()
                        results_ordered.append((tc, result, permitted))

            for tc in sequential_batch:
                yield ToolStart(tc["name"], tc["input"])
                tc, result, permitted = _exec_one(tc)
                results_ordered.append((tc, result, permitted))

            # Yield results + append to messages
            for tc, result, permitted in results_ordered:
                yield ToolEnd(tc["name"], result, permitted)
                state.messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "name": tc["name"],
                    "content": result,
                })

            # Phase: observing
            state.phase = "observing"
            yield PhaseChange("observing")

            # Phase: refining (will loop back to top of while)
            state.phase = "refining"
            yield PhaseChange("refining")


def build_result(state: KairosState, final_text: str, error: Optional[str] = None) -> KairosResult:
    """Build a KairosResult from a completed KairosState."""
    timeout_rate = (
        state.tool_calls_timed_out / state.tool_calls_made
        if state.tool_calls_made > 0 else 0.0
    )
    degraded = timeout_rate > 0.3 or len(state.permission_violations) > 3

    return KairosResult(
        run_id=state.run_id,
        success=state.phase == "done" and error is None,
        final_text=final_text,
        turns=state.turn_count,
        tool_calls_made=state.tool_calls_made,
        violations=state.permission_violations,
        degraded=degraded,
        error=error,
    )


def _permission_desc(tc: dict) -> str:
    name = tc.get("name", "")
    inp = tc.get("input", {})
    return f"{name}({list(inp.values())[:1]})"
