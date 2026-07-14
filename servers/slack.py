"""Mock slack MCP server — send messages to Slack channels."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("slack")

_MESSAGES = []


@mcp.tool()
async def send_message(channel: str, text: str) -> str:
    """Send a message to a Slack channel.

    Args:
        channel: Channel name (e.g., '#sales') or ID
        text: Message text

    Returns:
        JSON with the send result
    """
    msg_id = f"msg_{len(_MESSAGES) + 1:06d}"
    msg = {"id": msg_id, "channel": channel, "text": text, "timestamp": "2025-10-28T14:30:00Z", "status": "sent"}
    _MESSAGES.append(msg)
    return json.dumps({"message_id": msg_id, "channel": channel, "status": "sent"}, indent=2)


@mcp.tool()
async def send_welcome_message(channel: str, user_email: str, tier: str = "") -> str:
    """Send a welcome message to a new customer.

    Args:
        channel: Channel name
        user_email: Customer email
        tier: Subscription tier

    Returns:
        JSON with the send result
    """
    text = f"Welcome! Your {tier} subscription is now active. Email: {user_email}"
    msg_id = f"msg_{len(_MESSAGES) + 1:06d}"
    msg = {"id": msg_id, "channel": channel, "text": text, "timestamp": "2025-10-28T14:30:00Z", "status": "sent"}
    _MESSAGES.append(msg)
    return json.dumps({"message_id": msg_id, "channel": channel, "status": "sent", "text": text}, indent=2)


@mcp.tool()
async def list_messages(channel: str = "") -> str:
    """List messages, optionally filtered by channel.

    Args:
        channel: Channel name to filter by

    Returns:
        JSON array of messages
    """
    results = _MESSAGES
    if channel:
        results = [m for m in results if m["channel"] == channel]
    return json.dumps({"messages": results, "count": len(results)}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
