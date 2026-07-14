"""Mock google-sheets MCP server — spreadsheet operations with mock data."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("google-sheets")

_SPREADSHEETS = {
    "1HbEiG7d0tgZUS7phsD-A9hEJoEwTih0CsUhFXbnjhac": {
        "title": "Stock Tickers",
        "sheets": {
            "Sheet1": [["AAPL"], ["GOOGL"], ["MSFT"], ["AMZN"], ["META"]],
            "companies stocks": [],
        },
    },
}


@mcp.tool()
async def read_sheet(spreadsheet_id: str, sheet_name: str = "Sheet1", range: str = "") -> str:
    """Read data from a Google Sheets spreadsheet.

    Args:
        spreadsheet_id: The spreadsheet ID
        sheet_name: Name of the sheet/tab to read
        range: Optional cell range (e.g., 'A1:C10')

    Returns:
        JSON with the sheet data as a 2D array
    """
    if spreadsheet_id in _SPREADSHEETS:
        sheets = _SPREADSHEETS[spreadsheet_id]["sheets"]
        if sheet_name in sheets:
            return json.dumps({"spreadsheet_id": spreadsheet_id, "sheet_name": sheet_name, "values": sheets[sheet_name], "rows": len(sheets[sheet_name])}, indent=2)
    return json.dumps({"spreadsheet_id": spreadsheet_id, "sheet_name": sheet_name, "values": [["AAPL"], ["GOOGL"], ["MSFT"]], "rows": 3}, indent=2)


@mcp.tool()
async def write_sheet(spreadsheet_id: str, sheet_name: str, values: str, start_cell: str = "A1") -> str:
    """Write data to a Google Sheets spreadsheet.

    Args:
        spreadsheet_id: The spreadsheet ID
        sheet_name: Name of the sheet/tab to write to
        values: JSON string of 2D array of values to write
        start_cell: Starting cell (e.g., 'A1')

    Returns:
        JSON with the write result
    """
    try:
        data = json.loads(values) if isinstance(values, str) else values
    except json.JSONDecodeError:
        data = [[values]]

    if spreadsheet_id not in _SPREADSHEETS:
        _SPREADSHEETS[spreadsheet_id] = {"title": "New Spreadsheet", "sheets": {}}
    if sheet_name not in _SPREADSHEETS[spreadsheet_id]["sheets"]:
        _SPREADSHEETS[spreadsheet_id]["sheets"][sheet_name] = []
    _SPREADSHEETS[spreadsheet_id]["sheets"][sheet_name] = data

    return json.dumps({"spreadsheet_id": spreadsheet_id, "sheet_name": sheet_name, "rows_written": len(data), "status": "success"}, indent=2)


@mcp.tool()
async def create_sheet(spreadsheet_id: str, sheet_name: str) -> str:
    """Create a new sheet/tab in a spreadsheet.

    Args:
        spreadsheet_id: The spreadsheet ID
        sheet_name: Name for the new sheet

    Returns:
        JSON with the creation result
    """
    if spreadsheet_id not in _SPREADSHEETS:
        _SPREADSHEETS[spreadsheet_id] = {"title": "New Spreadsheet", "sheets": {}}
    _SPREADSHEETS[spreadsheet_id]["sheets"][sheet_name] = []
    return json.dumps({"spreadsheet_id": spreadsheet_id, "sheet_name": sheet_name, "status": "created"}, indent=2)


@mcp.tool()
async def get_spreadsheet_info(spreadsheet_id: str) -> str:
    """Get metadata about a spreadsheet.

    Args:
        spreadsheet_id: The spreadsheet ID

    Returns:
        JSON with spreadsheet title and sheet names
    """
    if spreadsheet_id in _SPREADSHEETS:
        sp = _SPREADSHEETS[spreadsheet_id]
        return json.dumps({"spreadsheet_id": spreadsheet_id, "title": sp["title"], "sheets": list(sp["sheets"].keys())}, indent=2)
    return json.dumps({"spreadsheet_id": spreadsheet_id, "title": "Untitled", "sheets": ["Sheet1"]}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
