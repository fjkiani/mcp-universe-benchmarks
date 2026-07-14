"""Mock fetch MCP server — returns deterministic page content."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fetch")

_MOCK_PAGES = {
    "https://example.com/nsf-career-2025": {
        "title": "NSF CAREER Program 2025",
        "content": "The NSF CAREER program offers awards of $500,000 over 5 years for early-career faculty. Eligibility: tenure-track, within 7 years of PhD. Deadline: July 2025.",
    },
    "https://example.com/nih-r01-2025": {
        "title": "NIH R01 Guidelines 2025",
        "content": "NIH R01 grants support up to $500K direct costs per year. Modular budget applies above $500K. Salary cap: $221,900. F&A rate negotiated by institution.",
    },
    "https://example.com/doe-ecrp-2025": {
        "title": "DOE Early Career Research Program 2025",
        "content": "DOE ECRP provides $500K/year for 5 years. Eligibility: untenured, within 10 years of PhD. Must be employed at DOE national lab or university.",
    },
}


@mcp.tool()
async def fetch_url(url: str) -> str:
    """Fetch the content of a web page.

    Args:
        url: The URL to fetch

    Returns:
        JSON with title and content of the page
    """
    if url in _MOCK_PAGES:
        page = _MOCK_PAGES[url]
        return json.dumps({"url": url, "title": page["title"], "content": page["content"], "status": 200}, indent=2)
    return json.dumps({
        "url": url,
        "title": "Mock Page",
        "content": f"This is mock content for {url}. The page discusses relevant information for the query.",
        "status": 200,
    }, indent=2)


@mcp.tool()
async def fetch_markdown(url: str) -> str:
    """Fetch a web page and return it as markdown.

    Args:
        url: The URL to fetch

    Returns:
        Markdown-formatted page content
    """
    if url in _MOCK_PAGES:
        page = _MOCK_PAGES[url]
        return json.dumps({"url": url, "markdown": f"# {page['title']}\n\n{page['content']}", "status": 200}, indent=2)
    return json.dumps({
        "url": url,
        "markdown": f"# Mock Page\n\nThis is mock markdown content for {url}.",
        "status": 200,
    }, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
