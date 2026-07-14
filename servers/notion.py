"""Mock notion MCP server — Notion page operations."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notion")

_PAGES = {
    "page_001": {"id": "page_001", "title": "2025 NBA Draft Picks", "content": "1. Cooper Flagg (F, Duke) - Pick #1 to Dallas\n2. Dylan Harper (G, Rutgers) - Pick #2 to San Antonio\n...\n16. Noah Essugo (F, Creighton) - Pick #16", "parent": "database_001"},
    "page_002": {"id": "page_002", "title": "Lionel Messi Inter Miami Stats", "content": "Messi 2024 MLS Stats: 20 goals, 10 assists in 19 appearances. Inter Miami record with Messi: 12W-2L-5D.", "parent": "database_001"},
    "page_003": {"id": "page_003", "title": "LMM Performance Benchmarks", "content": "GPT-4o: MMLU 88.7%, GSM8K 94.5%\nGemini 2.5 Pro: MMLU 90.1%, GSM8K 95.2%\nClaude 3.5 Sonnet: MMLU 88.3%, GSM8K 93.1%", "parent": "database_001"},
}


@mcp.tool()
async def search_pages(query: str = "") -> str:
    """Search Notion pages by title or content.

    Args:
        query: Search query

    Returns:
        JSON array of matching pages
    """
    results = list(_PAGES.values())
    if query:
        q = query.lower()
        results = [p for p in results if q in p["title"].lower() or q in p["content"].lower()]
    return json.dumps({"pages": [{"id": p["id"], "title": p["title"]} for p in results], "count": len(results)}, indent=2)


@mcp.tool()
async def get_page(page_id: str) -> str:
    """Get a Notion page by ID.

    Args:
        page_id: The page ID

    Returns:
        JSON with the page content
    """
    if page_id in _PAGES:
        return json.dumps({"page": _PAGES[page_id]}, indent=2)
    return json.dumps({"error": f"Page {page_id} not found"}, indent=2)


@mcp.tool()
async def create_page(title: str, content: str = "", parent_id: str = "") -> str:
    """Create a new Notion page.

    Args:
        title: Page title
        content: Page content
        parent_id: Parent page or database ID

    Returns:
        JSON with the created page ID
    """
    page_id = f"page_{len(_PAGES) + 1:03d}"
    _PAGES[page_id] = {"id": page_id, "title": title, "content": content, "parent": parent_id}
    return json.dumps({"page_id": page_id, "title": title, "status": "created"}, indent=2)


@mcp.tool()
async def update_page(page_id: str, title: str = "", content: str = "") -> str:
    """Update a Notion page.

    Args:
        page_id: The page ID
        title: New title (optional)
        content: New content (optional)

    Returns:
        JSON with the update result
    """
    if page_id not in _PAGES:
        return json.dumps({"error": f"Page {page_id} not found"}, indent=2)
    if title:
        _PAGES[page_id]["title"] = title
    if content:
        _PAGES[page_id]["content"] = content
    return json.dumps({"page_id": page_id, "status": "updated"}, indent=2)


@mcp.tool()
async def compare_page_text(page_id: str, expected_text: str) -> str:
    """Compare a page's text content against expected text.

    Args:
        page_id: The page ID
        expected_text: Expected text content to compare against

    Returns:
        JSON with comparison result
    """
    if page_id not in _PAGES:
        return json.dumps({"error": f"Page {page_id} not found"}, indent=2)
    actual = _PAGES[page_id]["content"]
    match = expected_text.lower() in actual.lower()
    return json.dumps({"page_id": page_id, "match": match, "actual_length": len(actual), "expected_length": len(expected_text)}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
