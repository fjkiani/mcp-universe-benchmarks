"""Mock stripe MCP server — payment processing operations."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("stripe")

_CUSTOMERS = {}
_PAYMENTS = {}


@mcp.tool()
async def verify_payment(payment_intent_id: str) -> str:
    """Verify a Stripe payment intent.

    Args:
        payment_intent_id: The payment intent ID (e.g., 'pi_3Oabc123')

    Returns:
        JSON with payment verification result
    """
    return json.dumps({
        "payment_intent_id": payment_intent_id,
        "status": "succeeded",
        "amount": 999900,
        "currency": "usd",
        "verified": True,
    }, indent=2)


@mcp.tool()
async def update_customer_tier(customer_email: str, tier: str) -> str:
    """Update a customer's subscription tier.

    Args:
        customer_email: Customer email address
        tier: New tier ('enterprise', 'pro', 'starter')

    Returns:
        JSON with the update result
    """
    _CUSTOMERS[customer_email] = {"email": customer_email, "tier": tier, "updated_at": "2025-10-28T14:30:00Z"}
    return json.dumps({"customer_email": customer_email, "tier": tier, "status": "updated"}, indent=2)


@mcp.tool()
async def get_customer(customer_email: str) -> str:
    """Get customer information.

    Args:
        customer_email: Customer email address

    Returns:
        JSON with customer details
    """
    if customer_email in _CUSTOMERS:
        return json.dumps({"customer": _CUSTOMERS[customer_email]}, indent=2)
    return json.dumps({"customer": {"email": customer_email, "tier": "free", "status": "new"}}, indent=2)


@mcp.tool()
async def process_refund(payment_intent_id: str, amount: int = 0, reason: str = "") -> str:
    """Process a refund for a payment.

    Args:
        payment_intent_id: The payment intent ID
        amount: Refund amount in cents (0 = full refund)
        reason: Refund reason

    Returns:
        JSON with the refund result
    """
    return json.dumps({"payment_intent_id": payment_intent_id, "refund_amount": amount, "reason": reason, "status": "refunded"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
