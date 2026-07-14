"""Mock date MCP server — provides current time and date calculations."""
import json
from datetime import datetime, timedelta, timezone
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("date")

_MOCK_NOW = datetime(2025, 10, 28, 14, 30, 0, tzinfo=timezone.utc)


@mcp.tool()
async def get_current_time() -> str:
    """Get the current timestamp in ISO 8601 format.

    Returns:
        JSON with the current UTC timestamp
    """
    return json.dumps({"timestamp": _MOCK_NOW.isoformat(), "timezone": "UTC", "date": _MOCK_NOW.strftime("%Y-%m-%d"), "time": _MOCK_NOW.strftime("%H:%M:%S")}, indent=2)


@mcp.tool()
async def get_current_date() -> str:
    """Get the current date.

    Returns:
        JSON with the current date
    """
    return json.dumps({"date": _MOCK_NOW.strftime("%Y-%m-%d"), "day_of_week": _MOCK_NOW.strftime("%A"), "timezone": "UTC"}, indent=2)


@mcp.tool()
async def calculate_time_difference(start_time: str, end_time: str) -> str:
    """Calculate the difference between two timestamps.

    Args:
        start_time: Start timestamp in ISO 8601 format
        end_time: End timestamp in ISO 8601 format

    Returns:
        JSON with the time difference in various units
    """
    try:
        start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        diff = end - start
        return json.dumps({
            "start": start_time, "end": end_time,
            "seconds": int(diff.total_seconds()),
            "minutes": int(diff.total_seconds() / 60),
            "hours": round(diff.total_seconds() / 3600, 2),
            "days": round(diff.total_seconds() / 86400, 2),
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def add_time(timestamp: str, duration_minutes: int = 0, duration_hours: int = 0, duration_days: int = 0) -> str:
    """Add a duration to a timestamp.

    Args:
        timestamp: Base timestamp in ISO 8601 format
        duration_minutes: Minutes to add
        duration_hours: Hours to add
        duration_days: Days to add

    Returns:
        JSON with the resulting timestamp
    """
    try:
        base = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        result = base + timedelta(minutes=duration_minutes, hours=duration_hours, days=duration_days)
        return json.dumps({"original": timestamp, "result": result.isoformat(), "added": {"minutes": duration_minutes, "hours": duration_hours, "days": duration_days}}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
