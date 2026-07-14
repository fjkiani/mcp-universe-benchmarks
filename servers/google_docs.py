"""Mock google-docs MCP server — document operations with mock data."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("google-docs")

_DOCS = {
    "1AeA8CNVOYWYpUr1NYtw9aqyObRP_6CEGvS1BS7ZUZh4": {
        "title": "FAANG Analysis Document",
        "content": "This document contains analysis of FAANG companies (Facebook/Meta, Apple, Amazon, Netflix, Google). Initial content placeholder.",
    },
    "1hlaYYv7EdN2eEy0nvQR6pPWOuGFezE99": {
        "title": "Investment Analysis",
        "content": "Investment analysis document covering portfolio allocation, risk assessment, and performance metrics for Q4 2024.",
    },
}


@mcp.tool()
async def read_document(document_id: str) -> str:
    """Read the content of a Google Document.

    Args:
        document_id: The document ID

    Returns:
        JSON with the document title and content
    """
    if document_id in _DOCS:
        doc = _DOCS[document_id]
        return json.dumps({"document_id": document_id, "title": doc["title"], "content": doc["content"]}, indent=2)
    return json.dumps({"document_id": document_id, "title": "Untitled Document", "content": "This is a mock document with placeholder content."}, indent=2)


@mcp.tool()
async def update_document(document_id: str, content: str, title: str = "") -> str:
    """Update the content of a Google Document.

    Args:
        document_id: The document ID
        content: New content to set (or append)
        title: Optional new title

    Returns:
        JSON with the update result
    """
    if document_id not in _DOCS:
        _DOCS[document_id] = {"title": "Untitled", "content": ""}
    _DOCS[document_id]["content"] = content
    if title:
        _DOCS[document_id]["title"] = title
    return json.dumps({"document_id": document_id, "title": _DOCS[document_id]["title"], "status": "updated", "content_length": len(content)}, indent=2)


@mcp.tool()
async def create_document(title: str, content: str = "") -> str:
    """Create a new Google Document.

    Args:
        title: Document title
        content: Initial content

    Returns:
        JSON with the new document ID
    """
    doc_id = f"doc_{len(_DOCS) + 1:06d}"
    _DOCS[doc_id] = {"title": title, "content": content}
    return json.dumps({"document_id": doc_id, "title": title, "status": "created"}, indent=2)


@mcp.tool()
async def list_documents(folder_id: str = "") -> str:
    """List documents, optionally in a specific folder.

    Args:
        folder_id: Optional folder ID to filter by

    Returns:
        JSON array of document metadata
    """
    docs = [{"document_id": did, "title": d["title"]} for did, d in _DOCS.items()]
    return json.dumps({"documents": docs, "count": len(docs)}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
