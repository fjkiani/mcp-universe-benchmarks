"""Mock calendar MCP server — manages events for identity/governance tasks."""
import json
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calendar")

_EVENTS = [
    {"id": "evt_001", "user": "iris@corp.com", "type": "login_failed", "timestamp": "2025-10-28T14:00:00Z", "ip": "203.0.113.45", "details": "Invalid password"},
    {"id": "evt_002", "user": "iris@corp.com", "type": "login_failed", "timestamp": "2025-10-28T14:01:00Z", "ip": "203.0.113.45", "details": "Invalid password"},
    {"id": "evt_003", "user": "iris@corp.com", "type": "login_failed", "timestamp": "2025-10-28T14:02:00Z", "ip": "203.0.113.45", "details": "Invalid password"},
    {"id": "evt_004", "user": "maya@corp.com", "type": "login_success", "timestamp": "2025-10-28T08:00:00Z", "ip": "192.168.1.100", "details": "Password auth"},
    {"id": "evt_005", "user": "maya@corp.com", "type": "permission_change", "timestamp": "2025-10-28T09:00:00Z", "ip": "192.168.1.100", "details": "maya -> admin role"},
    {"id": "evt_006", "user": "noah@corp.com", "type": "login_success", "timestamp": "2025-10-28T14:00:00Z", "ip": "10.0.0.50", "details": "Password auth"},
    {"id": "evt_007", "user": "noah@corp.com", "type": "data_access", "timestamp": "2025-10-28T14:15:00Z", "ip": "10.0.0.50", "details": "Read sensitive file"},
    {"id": "evt_008", "user": "noah@corp.com", "type": "logout", "timestamp": "2025-10-28T15:30:00Z", "ip": "10.0.0.50", "details": "Session ended"},
    {"id": "evt_009", "user": "charlie@corp.com", "type": "login_success", "timestamp": "2025-10-28T10:00:00Z", "ip": "192.168.1.200", "details": "Password auth"},
    {"id": "evt_010", "user": "chris@corp.com", "type": "login_failed", "timestamp": "2025-10-28T14:00:00Z", "ip": "203.0.113.45", "details": "Password: wrong1"},
    {"id": "evt_011", "user": "chris@corp.com", "type": "login_failed", "timestamp": "2025-10-28T14:00:15Z", "ip": "203.0.113.45", "details": "Password: wrong2"},
    {"id": "evt_012", "user": "chris@corp.com", "type": "login_failed", "timestamp": "2025-10-28T14:00:30Z", "ip": "203.0.113.45", "details": "Password: wrong3"},
]


@mcp.tool()
async def search_events(user: str = "", event_type: str = "", start_time: str = "", end_time: str = "") -> str:
    """Search calendar events with optional filters.

    Args:
        user: Filter by username (e.g., 'iris@corp.com')
        event_type: Filter by event type (e.g., 'login_failed', 'login_success')
        start_time: Filter events after this ISO timestamp
        end_time: Filter events before this ISO timestamp

    Returns:
        JSON array of matching events
    """
    results = _EVENTS
    if user:
        results = [e for e in results if e["user"] == user]
    if event_type:
        results = [e for e in results if e["type"] == event_type]
    if start_time:
        results = [e for e in results if e["timestamp"] >= start_time]
    if end_time:
        results = [e for e in results if e["timestamp"] <= end_time]
    return json.dumps({"events": results, "count": len(results)}, indent=2)


@mcp.tool()
async def create_event(user: str, event_type: str, timestamp: str, details: str = "", ip: str = "") -> str:
    """Create a new calendar event.

    Args:
        user: Username for the event
        event_type: Type of event (e.g., 'login_success', 'lockout', 'session_start')
        timestamp: ISO timestamp for the event
        details: Additional details
        ip: IP address associated with the event

    Returns:
        JSON with the created event ID
    """
    event_id = f"evt_{len(_EVENTS) + 1:03d}"
    event = {"id": event_id, "user": user, "type": event_type, "timestamp": timestamp, "ip": ip, "details": details}
    _EVENTS.append(event)
    return json.dumps({"event_id": event_id, "event": event, "status": "created"}, indent=2)


@mcp.tool()
async def list_events(user: str = "") -> str:
    """List all events, optionally filtered by user.

    Args:
        user: Filter by username

    Returns:
        JSON array of events
    """
    results = [e for e in _EVENTS if e["user"] == user] if user else _EVENTS
    return json.dumps({"events": results, "count": len(results)}, indent=2)


@mcp.tool()
async def get_event(event_id: str) -> str:
    """Get a specific event by ID.

    Args:
        event_id: The event ID (e.g., 'evt_001')

    Returns:
        JSON with the event details
    """
    for e in _EVENTS:
        if e["id"] == event_id:
            return json.dumps({"event": e}, indent=2)
    return json.dumps({"error": f"Event {event_id} not found"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
