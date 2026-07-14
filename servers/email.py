"""Mock email MCP server — send and search emails."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("email")

_EMAILS = [
    {"id": "email_001", "from": "po@nsf.gov", "to": "researcher@university.edu", "subject": "RE: NSF CAREER eligibility question", "body": "Thank you for your question. The 7-year eligibility window is calculated from your PhD conferral date. Extensions may be granted for qualifying circumstances.", "date": "2025-01-15"},
    {"id": "email_002", "from": "grants@nih.gov", "to": "researcher@university.edu", "subject": "NIH R01 budget clarification", "body": "The modular budget threshold is $500K direct costs per year. Above this, detailed budget is required. Salary cap applies to all personnel.", "date": "2025-02-01"},
]


@mcp.tool()
async def send_email(to: str, subject: str, body: str, cc: str = "") -> str:
    """Send an email.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        cc: CC recipients (comma-separated)

    Returns:
        JSON with the send result
    """
    email_id = f"email_{len(_EMAILS) + 1:03d}"
    email = {"id": email_id, "to": to, "subject": subject, "body": body, "cc": cc, "status": "sent", "date": "2025-10-28"}
    _EMAILS.append(email)
    return json.dumps({"email_id": email_id, "status": "sent", "to": to, "subject": subject}, indent=2)


@mcp.tool()
async def search_emails(query: str = "", folder: str = "inbox") -> str:
    """Search emails by keyword.

    Args:
        query: Search query
        folder: Email folder ('inbox', 'sent', 'drafts')

    Returns:
        JSON array of matching emails
    """
    results = _EMAILS
    if query:
        q = query.lower()
        results = [e for e in results if q in e.get("subject", "").lower() or q in e.get("body", "").lower()]
    return json.dumps({"emails": results, "count": len(results)}, indent=2)


@mcp.tool()
async def get_email(email_id: str) -> str:
    """Get a specific email by ID.

    Args:
        email_id: The email ID

    Returns:
        JSON with the email details
    """
    for e in _EMAILS:
        if e["id"] == email_id:
            return json.dumps({"email": e}, indent=2)
    return json.dumps({"error": f"Email {email_id} not found"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
