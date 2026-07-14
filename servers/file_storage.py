"""Mock file-storage MCP server — store and retrieve files."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("file-storage")

_FILES = {}


@mcp.tool()
async def upload_file(filename: str, content: str, content_type: str = "text/plain") -> str:
    """Upload a file to storage.

    Args:
        filename: Name of the file
        content: File content as string
        content_type: MIME type

    Returns:
        JSON with the file ID and storage info
    """
    file_id = f"file_{len(_FILES) + 1:06d}"
    _FILES[file_id] = {"id": file_id, "filename": filename, "content": content, "content_type": content_type, "size": len(content.encode())}
    return json.dumps({"file_id": file_id, "filename": filename, "size": len(content.encode()), "status": "uploaded"}, indent=2)


@mcp.tool()
async def download_file(file_id: str) -> str:
    """Download a file from storage.

    Args:
        file_id: The file ID

    Returns:
        JSON with the file content
    """
    if file_id in _FILES:
        return json.dumps({"file": _FILES[file_id]}, indent=2)
    return json.dumps({"error": f"File {file_id} not found"}, indent=2)


@mcp.tool()
async def list_files() -> str:
    """List all stored files.

    Returns:
        JSON array of file metadata
    """
    files = [{"file_id": fid, "filename": f["filename"], "size": f["size"], "content_type": f["content_type"]} for fid, f in _FILES.items()]
    return json.dumps({"files": files, "count": len(files)}, indent=2)


@mcp.tool()
async def delete_file(file_id: str) -> str:
    """Delete a file from storage.

    Args:
        file_id: The file ID

    Returns:
        JSON with the deletion result
    """
    if file_id in _FILES:
        del _FILES[file_id]
        return json.dumps({"file_id": file_id, "status": "deleted"}, indent=2)
    return json.dumps({"error": f"File {file_id} not found"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
