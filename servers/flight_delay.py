"""Mock flight-delay MCP server — flight delay probability predictions."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("flight-delay")

_FLIGHTS = {
    "AAL100": {"flight_number": "AAL100", "airline": "American Airlines", "origin": "JFK", "destination": "LAX", "scheduled_departure": "2025-10-28T10:00:00Z", "delay_probability": 0.35, "delay_minutes": 22, "status": "on_time", "weather": "clear", "temperature": 72},
    "UAL200": {"flight_number": "UAL200", "airline": "United Airlines", "origin": "SFO", "destination": "ORD", "scheduled_departure": "2025-10-28T14:00:00Z", "delay_probability": 0.65, "delay_minutes": 45, "status": "delayed", "weather": "rain", "temperature": 58},
    "DAL300": {"flight_number": "DAL300", "airline": "Delta Air Lines", "origin": "ATL", "destination": "DFW", "scheduled_departure": "2025-10-28T16:30:00Z", "delay_probability": 0.15, "delay_minutes": 5, "status": "on_time", "weather": "clear", "temperature": 80},
}


@mcp.tool()
async def get_flight_delay_probability(flight_number: str) -> str:
    """Get the delay probability for a specific flight.

    Args:
        flight_number: Flight number (e.g., 'AAL100')

    Returns:
        JSON with delay probability and flight details
    """
    fn = flight_number.upper()
    if fn in _FLIGHTS:
        flight = _FLIGHTS[fn]
        return json.dumps({
            "flight_number": flight["flight_number"],
            "airline": flight["airline"],
            "origin": flight["origin"],
            "destination": flight["destination"],
            "scheduled_departure": flight["scheduled_departure"],
            "delay_probability": flight["delay_probability"],
            "delay_minutes": flight["delay_minutes"],
            "status": flight["status"],
            "weather": flight["weather"],
            "temperature": flight["temperature"],
        }, indent=2)
    return json.dumps({"error": f"Flight {flight_number} not found", "flight_number": flight_number}, indent=2)


@mcp.tool()
async def get_flight_info(flight_number: str) -> str:
    """Get general information about a flight.

    Args:
        flight_number: Flight number (e.g., 'AAL100')

    Returns:
        JSON with flight information
    """
    fn = flight_number.upper()
    if fn in _FLIGHTS:
        return json.dumps({"flight": _FLIGHTS[fn]}, indent=2)
    return json.dumps({"error": f"Flight {flight_number} not found"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
