"""Benchmark runner — executes tasks against LLM models with Pass@K scoring."""
import asyncio
import json
import os
import time
import inspect
import importlib.util
from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv

load_dotenv()


class BenchmarkRunner:
    """Run benchmark tasks against one or more LLM models."""

    def __init__(
        self,
        repo_root: Path,
        domain: str,
        models: list[str],
        runs_per_model: int = 1,
        concurrent_runs: int = 1,
        dry_run: bool = False,
    ):
        self.repo_root = repo_root
        self.domain = domain
        self.models = models
        self.runs_per_model = runs_per_model
        self.concurrent_runs = concurrent_runs
        self.dry_run = dry_run
        self.domain_dir = repo_root / "domains" / domain

    def _load_config(self) -> dict:
        with open(self.domain_dir / "config.yaml") as f:
            docs = list(yaml.safe_load_all(f))

        llms = {}
        agents = {}
        benchmarks = []
        for doc in docs:
            if not doc:
                continue
            kind = doc.get("kind", "")
            spec = doc.get("spec", doc)
            if kind == "llm":
                name = spec.get("name", "")
                llms[name] = spec
            elif kind == "agent":
                name = spec.get("name", "")
                agents[name] = spec
            elif kind == "benchmark":
                benchmarks.append(spec)
        return {"llms": llms, "agents": agents, "benchmarks": benchmarks}

    def _load_tasks(self, benchmark_spec: dict) -> list[dict]:
        tasks = []
        for task_path in benchmark_spec.get("tasks", []):
            full_path = self.domain_dir / task_path
            if full_path.exists():
                with open(full_path) as f:
                    task = json.load(f)
                task["_path"] = task_path
                tasks.append(task)
        return tasks

    def _load_evaluators(self) -> dict:
        eval_path = self.domain_dir / "evaluators" / "functions.py"
        if not eval_path.exists():
            return {}

        spec = importlib.util.spec_from_file_location(
            f"{self.domain}_evaluators", eval_path
        )
        module = importlib.util.module_from_spec(spec)

        scripts_path = str(self.repo_root / "scripts")
        if scripts_path not in __import__("sys").path:
            __import__("sys").path.insert(0, scripts_path)

        spec.loader.exec_module(module)

        evaluators = {}
        for name in dir(module):
            obj = getattr(module, name)
            if callable(obj) and hasattr(obj, "_evaluator_name"):
                evaluators[obj._evaluator_name] = obj
        return evaluators

    async def _run_evaluator(self, func, llm_response: Any, op_args: dict) -> tuple[bool, str]:
        """Run an evaluator function, normalizing across signature variants."""
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())

        try:
            if len(params) >= 3:
                result = await func(llm_response, op_args, op_args)
            elif len(params) == 1:
                result = await func(llm_response)
            elif any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in sig.parameters.values()):
                result = await func(llm_response, op_args)
            else:
                result = await func(llm_response, op_args)

            if isinstance(result, tuple) and len(result) == 2:
                return result
            return bool(result), str(result)
        except Exception as e:
            return False, f"Evaluator error: {e}"

    def run(self) -> dict:
        return asyncio.run(self._run_async())

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

                for task in tasks:
                    for run_id in range(self.runs_per_model):
                        result = await self._run_single_task(
                            model_slug, task, evaluators, instruction, max_iterations, run_id
                        )
                        all_results.append(result)

        pass_at_k = {}
        for model_slug in self.models:
            model_results = [r for r in all_results if r["model"] == model_slug]
            total = len(model_results)
            passed = sum(1 for r in model_results if r["passed"])
            pass_at_k[model_slug] = {
                "total": total,
                "passed": passed,
                "pass_rate": passed / total if total > 0 else 0.0,
            }

        return {
            "domain": self.domain,
            "models": self.models,
            "runs_per_model": self.runs_per_model,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "results": all_results,
            "pass_at_k": pass_at_k,
        }

    async def _run_single_task(
        self, model_slug: str, task: dict, evaluators: dict,
        instruction: str, max_iterations: int, run_id: int
    ) -> dict:
        from mcpbench.llm import call_llm
        from mcpbench.mcp_client import MCPServerManager

        task_path = task.get("_path", "")
        question = task.get("question", "")
        mcp_servers = task.get("mcp_servers", [])
        output_format = task.get("output_format", {})

        start_time = time.time()
        tool_calls = 0
        iterations = 0
        llm_response = ""
        error = None

        try:
            if self.dry_run:
                llm_response = json.dumps({"dry_run": True, "question": question[:100]})
            else:
                system_prompt = instruction
                if output_format:
                    system_prompt += f"\n\nReturn your answer as valid JSON matching this format:\n{json.dumps(output_format, indent=2)}"

                server_manager = MCPServerManager(self.repo_root)
                tools_schema = []

                if mcp_servers:
                    for server_entry in mcp_servers:
                        server_name = server_entry.get("name", server_entry) if isinstance(server_entry, dict) else server_entry
                        try:
                            await server_manager.start_server(server_name)
                        except Exception as e:
                            error = f"Failed to start server '{server_name}': {e}"

                    tools_schema = await server_manager.get_tools_schema()

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ]

                for iteration in range(max_iterations):
                    iterations += 1
                    response = await call_llm(
                        model_slug, messages, tools=tools_schema if tools_schema else None
                    )

                    if hasattr(response, "choices") and response.choices:
                        choice = response.choices[0]
                        msg = choice.message

                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            messages.append(msg.model_dump())
                            for tc in msg.tool_calls:
                                tool_calls += 1
                                tool_name = tc.function.name
                                tool_args = json.loads(tc.function.arguments)
                                try:
                                    result = await server_manager.call_tool(tool_name, tool_args)
                                except Exception as e:
                                    result = f"Error calling tool {tool_name}: {e}"
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tc.id,
                                    "content": str(result),
                                })
                        else:
                            llm_response = msg.content or ""
                            break
                    else:
                        llm_response = str(response)
                        break

                await server_manager.cleanup()

        except Exception as e:
            error = str(e)
            llm_response = ""

        latency = time.time() - start_time

        passed = False
        feedback = ""
        evaluator_name = ""

        for ev in task.get("evaluators", []):
            op = ev.get("op", "")
            op_args = ev.get("op_args", {})
            evaluator_name = op

            if op in evaluators:
                func = evaluators[op]
                passed, feedback = await self._run_evaluator(func, llm_response, op_args)
                if not passed:
                    break
            else:
                feedback = f"Evaluator '{op}' not found in domain evaluators"
                passed = False
                break

        return {
            "task": task_path,
            "model": model_slug,
            "run_id": run_id,
            "passed": passed,
            "evaluator": evaluator_name,
            "feedback": feedback,
            "tool_calls": tool_calls,
            "iterations": iterations,
            "latency_seconds": round(latency, 2),
            "error": error,
            "response_preview": llm_response[:200] if llm_response else "",
        }
