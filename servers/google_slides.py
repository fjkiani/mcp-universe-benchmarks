"""Mock google-slides MCP server — presentation operations with mock data."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("google-slides")

_PRESENTATIONS = {
    "1goxT2tANy_fKy1H1GuK_6IZQ1dP_5G460KnYysTl26Q": {
        "title": "FAANG Companies Financial Analysis 2024",
        "slides": [{"slide_id": "slide_1", "layout": "TITLE", "title": "FAANG Analysis", "body": ""}],
    },
}


@mcp.tool()
async def get_presentation(presentation_id: str) -> str:
    """Get the content of a Google Slides presentation.

    Args:
        presentation_id: The presentation ID

    Returns:
        JSON with the presentation title and slides
    """
    if presentation_id in _PRESENTATIONS:
        pres = _PRESENTATIONS[presentation_id]
        return json.dumps({"presentation_id": presentation_id, "title": pres["title"], "slides": pres["slides"]}, indent=2)
    return json.dumps({"presentation_id": presentation_id, "title": "Untitled Presentation", "slides": []}, indent=2)


@mcp.tool()
async def create_slide(presentation_id: str, layout: str = "TITLE_AND_BODY", title: str = "", body: str = "") -> str:
    """Add a new slide to a presentation.

    Args:
        presentation_id: The presentation ID
        layout: Slide layout (TITLE, TITLE_AND_BODY, SECTION_HEADER, etc.)
        title: Slide title
        body: Slide body text

    Returns:
        JSON with the created slide ID
    """
    if presentation_id not in _PRESENTATIONS:
        _PRESENTATIONS[presentation_id] = {"title": "Untitled", "slides": []}
    slide_id = f"slide_{len(_PRESENTATIONS[presentation_id]['slides']) + 1}"
    slide = {"slide_id": slide_id, "layout": layout, "title": title, "body": body}
    _PRESENTATIONS[presentation_id]["slides"].append(slide)
    return json.dumps({"slide_id": slide_id, "slide": slide, "status": "created"}, indent=2)


@mcp.tool()
async def update_slide(presentation_id: str, slide_id: str, title: str = "", body: str = "") -> str:
    """Update an existing slide.

    Args:
        presentation_id: The presentation ID
        slide_id: The slide ID to update
        title: New slide title
        body: New slide body text

    Returns:
        JSON with the update result
    """
    if presentation_id not in _PRESENTATIONS:
        return json.dumps({"error": "Presentation not found"}, indent=2)
    for slide in _PRESENTATIONS[presentation_id]["slides"]:
        if slide["slide_id"] == slide_id:
            if title:
                slide["title"] = title
            if body:
                slide["body"] = body
            return json.dumps({"slide_id": slide_id, "status": "updated"}, indent=2)
    return json.dumps({"error": f"Slide {slide_id} not found"}, indent=2)


@mcp.tool()
async def create_presentation(title: str) -> str:
    """Create a new Google Slides presentation.

    Args:
        title: Presentation title

    Returns:
        JSON with the new presentation ID
    """
    pres_id = f"pres_{len(_PRESENTATIONS) + 1:06d}"
    _PRESENTATIONS[pres_id] = {"title": title, "slides": []}
    return json.dumps({"presentation_id": pres_id, "title": title, "status": "created"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
