"""Mock task-management MCP server — stores sessions and audit records."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("task-management")

_STORE = {}


@mcp.tool()
async def create_task(title: str, description: str = "", assignee: str = "", status: str = "pending") -> str:
    """Create a new task.

    Args:
        title: Task title
        description: Task description
        assignee: Person assigned to the task
        status: Initial status (default 'pending')

    Returns:
        JSON with the created task ID
    """
    task_id = f"task_{len(_STORE) + 1:04d}"
    task = {"id": task_id, "title": title, "description": description, "assignee": assignee, "status": status}
    _STORE[task_id] = task
    return json.dumps({"task_id": task_id, "task": task, "status": "created"}, indent=2)


@mcp.tool()
async def get_task(task_id: str) -> str:
    """Get a task by ID.

    Args:
        task_id: The task ID

    Returns:
        JSON with the task details
    """
    if task_id in _STORE:
        return json.dumps({"task": _STORE[task_id]}, indent=2)
    return json.dumps({"error": f"Task {task_id} not found"}, indent=2)


@mcp.tool()
async def update_task(task_id: str, status: str = "", assignee: str = "", description: str = "") -> str:
    """Update an existing task.

    Args:
        task_id: The task ID to update
        status: New status
        assignee: New assignee
        description: New description

    Returns:
        JSON with the updated task
    """
    if task_id not in _STORE:
        return json.dumps({"error": f"Task {task_id} not found"}, indent=2)
    if status:
        _STORE[task_id]["status"] = status
    if assignee:
        _STORE[task_id]["assignee"] = assignee
    if description:
        _STORE[task_id]["description"] = description
    return json.dumps({"task": _STORE[task_id], "status": "updated"}, indent=2)


@mcp.tool()
async def store_session(user_id: str, session_token: str, timestamp: str, expiry: str = "", metadata: str = "") -> str:
    """Store a user session record.

    Args:
        user_id: User identifier
        session_token: Session token string
        timestamp: Creation timestamp
        expiry: Session expiry timestamp
        metadata: Additional metadata as JSON string

    Returns:
        JSON with the stored session ID
    """
    session_id = f"sess_{len(_STORE) + 1:04d}"
    session = {"id": session_id, "user_id": user_id, "session_token": session_token, "timestamp": timestamp, "expiry": expiry, "metadata": metadata}
    _STORE[session_id] = session
    return json.dumps({"session_id": session_id, "session": session, "status": "stored"}, indent=2)


@mcp.tool()
async def get_session(session_id: str) -> str:
    """Retrieve a stored session by ID.

    Args:
        session_id: The session ID

    Returns:
        JSON with the session details
    """
    if session_id in _STORE:
        return json.dumps({"session": _STORE[session_id]}, indent=2)
    return json.dumps({"error": f"Session {session_id} not found"}, indent=2)


@mcp.tool()
async def list_tasks(status: str = "") -> str:
    """List all tasks, optionally filtered by status.

    Args:
        status: Filter by status

    Returns:
        JSON array of tasks
    """
    results = [v for v in _STORE.values() if "title" in v]
    if status:
        results = [t for t in results if t.get("status") == status]
    return json.dumps({"tasks": results, "count": len(results)}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
