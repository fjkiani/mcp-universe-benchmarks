"""MCP server lifecycle management — spawn, connect, call tools, teardown."""
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

import yaml
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPServerManager:
    """Manages MCP server subprocesses and client sessions."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.registry_path = repo_root / "servers" / "registry.yaml"
        self._sessions: dict[str, ClientSession] = {}
        self._contexts: dict[str, Any] = {}
        self._tools_cache: dict[str, list] = {}
        self._registry = None

    def _load_registry(self) -> dict:
        if self._registry is not None:
            return self._registry
        if not self.registry_path.exists():
            self._registry = {}
            return self._registry
        with open(self.registry_path) as f:
            self._registry = yaml.safe_load(f) or {}
        return self._registry

    async def start_server(self, server_name: str) -> None:
        """Start an MCP server as a subprocess and connect a client session."""
        if server_name in self._sessions:
            return

        registry = self._load_registry()
        server_config = registry.get("servers", {}).get(server_name)

        if not server_config:
            raise ValueError(f"Server '{server_name}' not found in registry.yaml")

        command = server_config.get("command", f"python -m servers.{server_name.replace('-', '_')}")
        parts = command.split()

        params = StdioServerParameters(
            command=parts[0],
            args=parts[1:],
            env={**os.environ, "PYTHONPATH": str(self.repo_root)},
        )

        ctx = stdio_client(params)
        read, write = await ctx.__aenter__()
        self._contexts[server_name] = ctx

        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()

        self._sessions[server_name] = session

        tools_result = await session.list_tools()
        self._tools_cache[server_name] = tools_result.tools

    async def get_tools_schema(self) -> list[dict]:
        """Get OpenAI-compatible tool schemas from all started servers."""
        schemas = []
        for server_name, tools in self._tools_cache.items():
            for tool in tools:
                schema = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema if isinstance(tool.inputSchema, dict) else {},
                    }
                }
                schemas.append(schema)
        return schemas

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Call a tool on the appropriate server."""
        for server_name, session in self._sessions.items():
            tools = self._tools_cache.get(server_name, [])
            tool_names = [t.name for t in tools]
            if tool_name in tool_names:
                result = await session.call_tool(tool_name, arguments)
                if result.content:
                    return result.content[0].text if hasattr(result.content[0], "text") else str(result.content[0])
                return str(result)
        raise ValueError(f"Tool '{tool_name}' not found in any started server")

    async def cleanup(self) -> None:
        """Clean up all server sessions and subprocesses."""
        for server_name, session in self._sessions.items():
            try:
                await session.__aexit__(None, None, None)
            except Exception:
                pass

        for server_name, ctx in self._contexts.items():
            try:
                await ctx.__aexit__(None, None, None)
            except Exception:
                pass

        self._sessions.clear()
        self._contexts.clear()
        self._tools_cache.clear()
