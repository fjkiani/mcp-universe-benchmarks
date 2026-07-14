"""Mock pdf-generator MCP server — generates mock PDF documents."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pdf-generator")

_PDFS = {}


@mcp.tool()
async def generate_pdf(title: str, content: str, format: str = "letter") -> str:
    """Generate a PDF document from text content.

    Args:
        title: Document title
        content: Text content for the PDF body
        format: Page format ('letter', 'a4', 'legal')

    Returns:
        JSON with the generated PDF metadata
    """
    pdf_id = f"pdf_{len(_PDFS) + 1:06d}"
    pdf = {"id": pdf_id, "title": title, "content": content, "format": format, "pages": max(1, len(content) // 3000 + 1), "size_bytes": len(content.encode()) + 1024}
    _PDFS[pdf_id] = pdf
    return json.dumps({"pdf_id": pdf_id, "title": title, "pages": pdf["pages"], "format": format, "status": "generated"}, indent=2)


@mcp.tool()
async def generate_structured_pdf(title: str, sections: str) -> str:
    """Generate a PDF with structured sections.

    Args:
        title: Document title
        sections: JSON string array of {heading, content} objects

    Returns:
        JSON with the generated PDF metadata
    """
    try:
        section_data = json.loads(sections) if isinstance(sections, str) else sections
    except json.JSONDecodeError:
        section_data = [{"heading": "Content", "content": str(sections)}]

    total_content = sum(len(s.get("content", "")) for s in section_data)
    pdf_id = f"pdf_{len(_PDFS) + 1:06d}"
    pdf = {"id": pdf_id, "title": title, "sections": section_data, "pages": max(1, total_content // 3000 + 1), "status": "generated"}
    _PDFS[pdf_id] = pdf
    return json.dumps({"pdf_id": pdf_id, "title": title, "sections_count": len(section_data), "pages": pdf["pages"], "status": "generated"}, indent=2)


@mcp.tool()
async def get_pdf_info(pdf_id: str) -> str:
    """Get metadata about a generated PDF.

    Args:
        pdf_id: The PDF ID

    Returns:
        JSON with PDF metadata
    """
    if pdf_id in _PDFS:
        return json.dumps({"pdf": _PDFS[pdf_id]}, indent=2)
    return json.dumps({"error": f"PDF {pdf_id} not found"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
