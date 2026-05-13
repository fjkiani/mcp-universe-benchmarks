# Adapted from SafeRL-Lab/cheetahclaws (Apache-2.0)
# Modifications: max_output default 16000, list_registered() added, scoped imports
"""Tool plugin registry for Kairos — ported from CheetahClaws tool_registry.py."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

@dataclass
class ToolDef:
    name: str
    schema: Dict[str, Any]
    func: Callable[[Dict[str, Any], Dict[str, Any]], str]
    read_only: bool = False
    concurrent_safe: bool = False

_registry: Dict[str, ToolDef] = {}

def register_tool(tool_def: ToolDef) -> None:
    _registry[tool_def.name] = tool_def

def get_tool(name: str) -> Optional[ToolDef]:
    return _registry.get(name)

def get_all_tools() -> List[ToolDef]:
    return list(_registry.values())

def get_tool_schemas() -> List[Dict[str, Any]]:
    return [t.schema for t in _registry.values()]

def execute_tool(name: str, params: Dict[str, Any], config: Dict[str, Any], max_output: int = 16_000) -> str:
    tool = get_tool(name)
    if tool is None:
        return f"Error: tool '{name}' not found in Kairos registry."
    try:
        result = tool.func(params, config)
    except Exception as e:
        return f"Error executing {name}: {type(e).__name__}: {e}"
    if not isinstance(result, str):
        result = str(result)
    if len(result) > max_output:
        first_half = max_output // 2
        last_quarter = max_output // 4
        truncated = len(result) - first_half - last_quarter
        result = (result[:first_half] + f"\n[... {truncated} chars truncated ...]\n" + result[-last_quarter:])
    return result

def clear_registry() -> None:
    _registry.clear()

def list_registered() -> List[str]:
    return list(_registry.keys())
