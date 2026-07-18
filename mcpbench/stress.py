"""StressRunner — extends BenchmarkRunner with rich per-run telemetry.

Captures for every run:
    - per-tool-call latency + name + status
    - token usage (prompt/completion/total, when provider returns it)
    - finish_reason (stop / tool_calls / length / content_filter / ...)
    - failure_class classification
    - perturbation_id + worker_id + run_index
    - error type + full traceback

Writes JSONL to <out_dir>/runs.jsonl (append), one record per run.
Intended to run in-process on the assigned worker.
"""
import asyncio
import concurrent.futures
import inspect
import json
import os
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Callable, Optional

from mcpbench.runner import BenchmarkRunner
from mcpbench.mcp_client import MCPServerManager


async def _shielded_cleanup(server_manager: "MCPServerManager"):
    """Run MCP teardown in its own task so its CancelledError is absorbed."""
    try:
        await server_manager.cleanup()
    except Exception:
        pass


# -------- Failure taxonomy --------
FAILURE_CLASSES = {
    "none",             # passed cleanly
    "wrong_answer",     # ran to completion but evaluator returned False
    "tool_error",       # server returned an error / raised while calling a tool
    "rate_limit",       # provider returned 429 / RateLimitError
    "timeout",          # provider or task timeout
    "loop_max_iter",    # hit max_iterations without producing a final answer
    "parse_error",      # LLM returned malformed json / could not parse args
    "refusal",          # LLM refused / said it can't do the task
    "hallucination",    # answered without calling required tool
    "judge_disagree",   # LLM-judge said wrong (currently unused, hook only)
    "subprocess_crash", # MCP server subprocess died mid-run
    "start_failure",    # a required MCP server could not be started
    "unknown_error",    # anything else
}


def classify_failure(
    passed: bool,
    error: Optional[str],
    iterations: int,
    max_iterations: int,
    tool_calls: int,
    required_tools: bool,
    llm_response: str,
) -> str:
    if passed:
        return "none"
    if error:
        e = error.lower()
        if "ratelimit" in e or "rate limit" in e or "429" in e or "too many requests" in e:
            return "rate_limit"
        if "timeout" in e or "timed out" in e:
            return "timeout"
        if "failed to start server" in e:
            return "start_failure"
        if "brokenpipeerror" in e or "connection" in e and "reset" in e:
            return "subprocess_crash"
        if "expecting value" in e or "json" in e and ("decode" in e or "parse" in e):
            return "parse_error"
        if "error calling tool" in e:
            return "tool_error"
        return "unknown_error"
    if iterations >= max_iterations:
        return "loop_max_iter"
    if required_tools and tool_calls == 0:
        return "hallucination"
    low = (llm_response or "").lower()
    if any(w in low for w in ("i can't", "i cannot", "i'm sorry, but", "as an ai", "unable to")):
        return "refusal"
    return "wrong_answer"


class StressRunner(BenchmarkRunner):
    """Runs a benchmark and emits a rich JSONL record per run."""

    def __init__(
        self,
        *args,
        out_path: Path,
        worker_id: str = "worker-0",
        category: str = "baseline",
        perturbation_id: str = "baseline",
        tool_call_hook: Optional[Callable] = None,
        task_filter: Optional[Callable[[dict], bool]] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.out_path = Path(out_path)
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        self.worker_id = worker_id
        self.category = category
        self.perturbation_id = perturbation_id
        self.tool_call_hook = tool_call_hook
        self.task_filter = task_filter

    # ------- override _run_single_task to gather rich telemetry ------
    async def _run_single_task(
        self, model_slug: str, task: dict, evaluators: dict,
        instruction: str, max_iterations: int, run_id: int
    ) -> dict:
        from mcpbench.llm import call_llm

        task_path = task.get("_path", "")
        question = task.get("question", "")
        mcp_servers = task.get("mcp_servers", [])
        output_format = task.get("output_format", {})

        start_time = time.time()
        tool_calls = 0
        iterations = 0
        llm_response = ""
        error: Optional[str] = None
        traceback_str: Optional[str] = None
        per_tool_calls: list[dict] = []
        finish_reason: Optional[str] = None
        token_usage: dict = {"prompt": 0, "completion": 0, "total": 0}

        server_manager = MCPServerManager(self.repo_root)
        try:
            if self.dry_run:
                llm_response = json.dumps({"dry_run": True, "question": question[:100]})
            else:
                system_prompt = instruction
                if output_format:
                    system_prompt += (
                        "\n\nReturn your answer as valid JSON matching this format:\n"
                        + json.dumps(output_format, indent=2)
                    )

                tools_schema: list = []
                started_any = False
                if mcp_servers:
                    for server_entry in mcp_servers:
                        server_name = (
                            server_entry.get("name", server_entry)
                            if isinstance(server_entry, dict) else server_entry
                        )
                        try:
                            await server_manager.start_server(server_name)
                            started_any = True
                        except Exception as e:
                            if error is None:
                                error = f"Failed to start server '{server_name}': {e}"
                    if started_any:
                        tools_schema = await server_manager.get_tools_schema()

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ]

                for _ in range(max_iterations):
                    iterations += 1
                    try:
                        response = await call_llm(
                            model_slug, messages,
                            tools=tools_schema if tools_schema else None
                        )
                    except Exception as e:
                        error = f"LLM error: {type(e).__name__}: {e}"
                        traceback_str = traceback.format_exc()
                        break

                    # accumulate token usage
                    try:
                        usage = getattr(response, "usage", None)
                        if usage:
                            token_usage["prompt"] += getattr(usage, "prompt_tokens", 0) or 0
                            token_usage["completion"] += getattr(usage, "completion_tokens", 0) or 0
                            token_usage["total"] += getattr(usage, "total_tokens", 0) or 0
                    except Exception:
                        pass

                    if not (hasattr(response, "choices") and response.choices):
                        llm_response = str(response)
                        break

                    choice = response.choices[0]
                    finish_reason = getattr(choice, "finish_reason", None) or finish_reason
                    msg = choice.message

                    # Snapshot best-effort answer BEFORE going into tool branch —
                    # so if we hit iteration cap, we retain the last content/reasoning.
                    _cand = (
                        (msg.content or "").strip()
                        or (getattr(msg, "reasoning_content", None) or "").strip()
                    )
                    if _cand:
                        llm_response = _cand

                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        messages.append(msg.model_dump())
                        for tc in msg.tool_calls:
                            tool_calls += 1
                            tool_name = tc.function.name
                            call_start = time.time()
                            call_status = "ok"
                            call_err: Optional[str] = None
                            try:
                                tool_args = json.loads(tc.function.arguments)
                            except Exception as e:
                                tool_args = {}
                                call_status = "arg_parse_error"
                                call_err = str(e)

                            try:
                                if self.tool_call_hook is not None:
                                    result = await self.tool_call_hook(
                                        server_manager, tool_name, tool_args
                                    )
                                else:
                                    result = await server_manager.call_tool(tool_name, tool_args)
                            except Exception as e:
                                result = f"Error calling tool {tool_name}: {e}"
                                call_status = "call_error"
                                call_err = str(e)

                            per_tool_calls.append({
                                "name": tool_name,
                                "latency_ms": int((time.time() - call_start) * 1000),
                                "status": call_status,
                                "error": call_err,
                            })
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "content": str(result),
                            })
                    else:
                        # Fall back to reasoning_content for reasoning-style
                        # models (Gemma 4 via Gemini API, o1-style OpenAI, etc.)
                        # whose final answer stays in reasoning_content when
                        # max_tokens budget is consumed during thinking.
                        llm_response = (
                            (msg.content or "").strip()
                            or (getattr(msg, "reasoning_content", None) or "").strip()
                            or ""
                        )
                        break
        except asyncio.CancelledError:
            error = "CancelledError (likely MCP anyio cleanup)"
            traceback_str = traceback.format_exc()
        except Exception as e:
            error = f"{type(e).__name__}: {e}"
            traceback_str = traceback.format_exc()
        finally:
            # Fire-and-forget cleanup — deliberately NOT awaited so the
            # anyio TaskGroup inside stdio_client.__aexit__ cannot cancel
            # the parent task (which would cascade-cancel every subsequent
            # start_server call). The Python interpreter shutdown / OS
            # will reap the MCP subprocesses; each subprocess is short-lived.
            try:
                asyncio.ensure_future(_shielded_cleanup(server_manager))
            except Exception:
                pass

        latency = time.time() - start_time

        # ---------- evaluators ----------
        passed = False
        feedback = ""
        evaluator_name = ""
        # Fast path: if the LLM/runtime raised an error, the run cannot
        # legitimately pass. Skip evaluators entirely to avoid the "empty
        # llm_response is treated as a valid answer" false-positive we saw
        # on inverse_compliance_trap_001 in governance_traps.
        if error:
            passed = False
            feedback = f"skipped evaluator: error occurred ({error[:80]})"
            evaluator_name = ""
        else:
            for ev in task.get("evaluators", []):
                op = ev.get("op", "")
                op_args = ev.get("op_args", {})
                evaluator_name = op
                if op in evaluators:
                    func = evaluators[op]
                    try:
                        passed, feedback = await self._run_evaluator(func, llm_response, op_args)
                    except Exception as e:
                        passed = False
                        feedback = f"evaluator exception: {e}"
                    if not passed:
                        break
                else:
                    feedback = f"Evaluator '{op}' not found in domain evaluators"
                    passed = False
                    break

        required_tools = bool(mcp_servers)
        failure_class = classify_failure(
            passed=passed,
            error=error,
            iterations=iterations,
            max_iterations=max_iterations,
            tool_calls=tool_calls,
            required_tools=required_tools,
            llm_response=llm_response,
        )

        record = {
            "worker_id": self.worker_id,
            "category": self.category,
            "perturbation_id": self.perturbation_id,
            "task": task_path,
            "domain": self.domain,
            "model": model_slug,
            "run_id": run_id,
            "passed": passed,
            "failure_class": failure_class,
            "evaluator": evaluator_name,
            "feedback": feedback[:400] if feedback else "",
            "iterations": iterations,
            "max_iterations": max_iterations,
            "tool_calls": tool_calls,
            "per_tool_calls": per_tool_calls,
            "finish_reason": finish_reason,
            "token_usage": token_usage,
            "latency_seconds": round(latency, 3),
            "latency_ms": int(latency * 1000),
            "error": error,
            "traceback": traceback_str,
            "response_preview": (llm_response[:200] if llm_response else ""),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        # append JSONL immediately for checkpoint safety
        with open(self.out_path, "a") as f:
            f.write(json.dumps(record) + "\n")

        return record

    def _run_single_task_isolated(
        self, model_slug, task, evaluators, instruction, max_iterations, run_id
    ) -> dict:
        """Runs one task in a brand-new event loop. This isolates the
        anyio TaskGroup cancel scope inside MCP stdio_client cleanup,
        so a bad cleanup can't cascade-cancel the next task."""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(
                self._run_single_task(
                    model_slug, task, evaluators,
                    instruction, max_iterations, run_id,
                )
            )
        finally:
            try:
                # Drain any lingering tasks so loop.close() is clean
                pending = asyncio.all_tasks(loop)
                for t in pending:
                    t.cancel()
                if pending:
                    loop.run_until_complete(
                        asyncio.gather(*pending, return_exceptions=True)
                    )
            except Exception:
                pass
            try:
                loop.close()
            except Exception:
                pass

    # override _run_async to honour task_filter
    async def _run_async(self) -> dict:
        config = self._load_config()
        evaluators = self._load_evaluators()

        all_results = []
        for model_slug in self.models:
            for bm_spec in config["benchmarks"]:
                agent_name = bm_spec.get("agent", "")
                agent_spec = config["agents"].get(agent_name, {})
                instruction = agent_spec.get("config", {}).get("instruction", "")
                max_iterations = agent_spec.get("config", {}).get("max_iterations", 20)

                tasks = self._load_tasks(bm_spec)
                if self.task_filter is not None:
                    tasks = [t for t in tasks if self.task_filter(t)]

                for task in tasks:
                    for run_id in range(self.runs_per_model):
                        # Run each task in a fresh event loop on a worker
                        # thread. This isolates the anyio cancel scope of
                        # MCP stdio_client cleanup — if it cancels, only
                        # this thread's loop dies, not our outer loop.
                        result = await asyncio.get_event_loop().run_in_executor(
                            None,
                            self._run_single_task_isolated,
                            model_slug, task, evaluators,
                            instruction, max_iterations, run_id,
                        )
                        all_results.append(result)

        pass_by_model = {}
        for model_slug in self.models:
            rs = [r for r in all_results if r["model"] == model_slug]
            passed = sum(1 for r in rs if r["passed"])
            pass_by_model[model_slug] = {
                "total": len(rs),
                "passed": passed,
                "pass_rate": passed / len(rs) if rs else 0.0,
            }

        return {
            "worker_id": self.worker_id,
            "category": self.category,
            "domain": self.domain,
            "models": self.models,
            "runs_per_model": self.runs_per_model,
            "results": all_results,
            "pass_by_model": pass_by_model,
            "runs_jsonl": str(self.out_path),
        }
