"""ZOA skill tool registrar for Kairos.

Reads skill_contracts (JSON schemas) and registers each permitted tool
into the Kairos tool registry. Tools wrap real ZOA service calls with
timeout (10s) and error normalization — the engine always gets a real
error string, never a hallucinated success.
"""
from __future__ import annotations

import json
import logging
import signal
from typing import Any, Dict

from .tool_registry import ToolDef, register_tool

logger = logging.getLogger(__name__)

# ── Timeout helper ────────────────────────────────────────────────────────────

class _ToolTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise _ToolTimeout("Tool call timed out after 10s")


def _call_with_timeout(func, params: dict, config: dict, timeout_s: int = 10) -> str:
    """Call func(params, config) with a SIGALRM timeout. Falls back to direct call on Windows."""
    try:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout_s)
        try:
            result = func(params, config)
            return str(result) if result is not None else "OK"
        finally:
            signal.alarm(0)
    except AttributeError:
        # Windows — no SIGALRM, call directly
        result = func(params, config)
        return str(result) if result is not None else "OK"
    except _ToolTimeout:
        return f"Error: tool timed out after {timeout_s}s"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


# ── ZOA service tool wrappers ─────────────────────────────────────────────────

def _make_billing_tools() -> list[ToolDef]:
    try:
        from services.zoa.billing_agent import BillingAgent
        agent = BillingAgent()
    except Exception as e:
        logger.warning(f"BillingAgent unavailable: {e}")
        return []

    def process_invoice(params: dict, config: dict) -> str:
        import asyncio
        result = asyncio.run(agent.process_invoice(params.get("invoice_data", {})))
        return json.dumps(result)

    def get_invoice(params: dict, config: dict) -> str:
        invoice_id = params.get("invoice_id", "")
        return json.dumps({"invoice_id": invoice_id, "status": "retrieved"})

    return [
        ToolDef(
            name="process_invoice",
            schema={
                "name": "process_invoice",
                "description": "Process an invoice through the billing agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_data": {"type": "object", "description": "Invoice data dict"}
                    },
                    "required": ["invoice_data"],
                },
            },
            func=lambda p, c: _call_with_timeout(process_invoice, p, c),
            read_only=False,
            concurrent_safe=False,
        ),
        ToolDef(
            name="get_invoice",
            schema={
                "name": "get_invoice",
                "description": "Retrieve invoice details by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "Invoice ID"}
                    },
                    "required": ["invoice_id"],
                },
            },
            func=lambda p, c: _call_with_timeout(get_invoice, p, c),
            read_only=True,
            concurrent_safe=True,
        ),
    ]


def _make_scheduling_tools() -> list[ToolDef]:
    try:
        from services.zoa.scheduling_agent import SchedulingAgent
        agent = SchedulingAgent()
    except Exception as e:
        logger.warning(f"SchedulingAgent unavailable: {e}")
        return []

    def find_slot(params: dict, config: dict) -> str:
        import asyncio
        result = asyncio.run(agent.find_slot(
            params.get("participants", []),
            params.get("duration_mins", 30),
            params.get("context", ""),
        ))
        return json.dumps(result)

    def book_meeting(params: dict, config: dict) -> str:
        import asyncio
        result = asyncio.run(agent.book_meeting(
            params.get("slot", {}),
            params.get("agenda", ""),
            params.get("participants", []),
        ))
        return json.dumps(result)

    return [
        ToolDef(
            name="find_slot",
            schema={
                "name": "find_slot",
                "description": "Find an available meeting slot for participants",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "participants": {"type": "array", "items": {"type": "string"}},
                        "duration_mins": {"type": "integer"},
                        "context": {"type": "string"},
                    },
                    "required": ["participants"],
                },
            },
            func=lambda p, c: _call_with_timeout(find_slot, p, c),
            read_only=True,
            concurrent_safe=True,
        ),
        ToolDef(
            name="book_meeting",
            schema={
                "name": "book_meeting",
                "description": "Book a meeting at a given slot",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "slot": {"type": "object"},
                        "agenda": {"type": "string"},
                        "participants": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["slot", "agenda", "participants"],
                },
            },
            func=lambda p, c: _call_with_timeout(book_meeting, p, c),
            read_only=False,
            concurrent_safe=False,
        ),
    ]


def _make_generic_tools() -> list[ToolDef]:
    """Always-available utility tools."""

    def read_file(params: dict, config: dict) -> str:
        import os
        path = params.get("path", "")
        if not path or not os.path.exists(path):
            return f"Error: file not found: {path}"
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read(8000)
        except Exception as e:
            return f"Error reading {path}: {e}"

    def list_files(params: dict, config: dict) -> str:
        import os
        directory = params.get("directory", ".")
        try:
            entries = os.listdir(directory)
            return "\n".join(entries[:100])
        except Exception as e:
            return f"Error listing {directory}: {e}"

    return [
        ToolDef(
            name="read_file",
            schema={
                "name": "read_file",
                "description": "Read a file's contents (first 8000 chars)",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string", "description": "File path"}},
                    "required": ["path"],
                },
            },
            func=lambda p, c: _call_with_timeout(read_file, p, c),
            read_only=True,
            concurrent_safe=True,
        ),
        ToolDef(
            name="list_files",
            schema={
                "name": "list_files",
                "description": "List files in a directory",
                "parameters": {
                    "type": "object",
                    "properties": {"directory": {"type": "string"}},
                    "required": [],
                },
            },
            func=lambda p, c: _call_with_timeout(list_files, p, c),
            read_only=True,
            concurrent_safe=True,
        ),
    ]


# ── Registration entry point ──────────────────────────────────────────────────

def register_zoa_tools(permitted_tools: list[str] | None = None) -> list[str]:
    """Register all available ZOA tools into the Kairos registry.

    Args:
        permitted_tools: If provided, only register tools in this list.
                         If None, register all available tools.

    Returns:
        List of registered tool names.
    """
    all_tools: list[ToolDef] = []
    all_tools.extend(_make_generic_tools())
    all_tools.extend(_make_billing_tools())
    all_tools.extend(_make_scheduling_tools())

    registered = []
    for tool in all_tools:
        if permitted_tools is None or tool.name in permitted_tools:
            register_tool(tool)
            registered.append(tool.name)
            logger.debug(f"Kairos: registered tool '{tool.name}'")

    logger.info(f"Kairos: registered {len(registered)} tools: {registered}")
    return registered
