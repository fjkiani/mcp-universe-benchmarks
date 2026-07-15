"""Fault injection for MCP tool calls (for tool-failure stress).

Wraps MCPServerManager.call_tool with a distribution over faults.
Compatible with `StressRunner`'s `tool_call_hook` signature:

    async def hook(server_manager, tool_name, tool_args) -> str: ...

Distribution (default):
    - 20% empty_string : return ""
    - 20% delay_3s     : sleep 3s then pass through
    - 20% malformed_json: return "{"partial": tru"
    - 20% simulated_500 : raise ToolCallError("HTTP 500 from upstream")
    - 20% passthrough   : normal call

Each fault emits its class in the returned string so the failure taxonomy
in stress.py can pick it up.
"""
from __future__ import annotations
import asyncio
import random
from typing import Optional


class FaultInjector:
    def __init__(
        self,
        seed: int = 0,
        weights: Optional[dict[str, float]] = None,
    ):
        self.rng = random.Random(seed)
        self.weights = weights or {
            "empty_string": 0.20,
            "delay_3s": 0.20,
            "malformed_json": 0.20,
            "simulated_500": 0.20,
            "passthrough": 0.20,
        }
        # Track what happened for the report
        self.log: list[dict] = []

    def _sample(self) -> str:
        r = self.rng.random()
        cum = 0.0
        for name, w in self.weights.items():
            cum += w
            if r <= cum:
                return name
        return "passthrough"

    async def hook(self, server_manager, tool_name: str, tool_args: dict) -> str:
        fault = self._sample()
        self.log.append({"tool": tool_name, "fault": fault})

        if fault == "empty_string":
            return ""

        if fault == "delay_3s":
            await asyncio.sleep(3)
            return await server_manager.call_tool(tool_name, tool_args)

        if fault == "malformed_json":
            return "{\"partial\": tru"  # deliberately truncated / invalid JSON

        if fault == "simulated_500":
            raise RuntimeError(
                f"Fault-injected 500 while calling tool '{tool_name}'"
            )

        # passthrough
        return await server_manager.call_tool(tool_name, tool_args)
