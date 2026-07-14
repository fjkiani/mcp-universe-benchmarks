"""Mock stock-portfolio MCP server — re-exports the existing investments server.

The canonical implementation lives at domains/investments/mcp_servers/stock_portfolio/server.py
with captured real market data. This module provides a top-level entry point
so the server registry can launch it as `python -m servers.stock_portfolio`.
"""
import json
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("stock-portfolio")

# Load the captured real market data from the investments domain
_DATA_FILE = Path(__file__).parent.parent / "domains" / "investments" / "mcp_servers" / "stock_portfolio" / "stock_data.json"

with open(_DATA_FILE, 'r') as f:
    STOCK_DATA = json.load(f)

QUOTES = STOCK_DATA["quotes"]
OVERVIEWS = STOCK_DATA["overviews"]
DAILY_DATA = STOCK_DATA["daily_data"]


@mcp.tool()
async def get_stock_quote(symbol: str) -> str:
    """Get real-time stock quote (from captured data).

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "GOOGL")

    Returns:
        JSON with stock quote data
    """
    if symbol not in QUOTES:
        return json.dumps({"error": f"Stock symbol {symbol} not found in dataset"})
    quote_data = QUOTES[symbol].get("Global Quote", {})
    result = {
        "symbol": quote_data.get("01. symbol"),
        "price": float(quote_data.get("05. price", 0)),
        "change": float(quote_data.get("09. change", 0)),
        "change_percent": quote_data.get("10. change percent", "0%"),
        "volume": int(quote_data.get("06. volume", 0)),
        "latest_trading_day": quote_data.get("07. latest trading day"),
        "previous_close": float(quote_data.get("08. previous close", 0)),
        "open": float(quote_data.get("02. open", 0)),
        "high": float(quote_data.get("03. high", 0)),
        "low": float(quote_data.get("04. low", 0)),
    }
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_stock_daily(symbol: str) -> str:
    """Get daily time series data for a stock.

    Args:
        symbol: Stock ticker symbol

    Returns:
        JSON with daily price data
    """
    if symbol not in DAILY_DATA:
        return json.dumps({"error": f"Stock symbol {symbol} not found in dataset"})
    return json.dumps({"symbol": symbol, "daily_data": DAILY_DATA[symbol]}, indent=2)


@mcp.tool()
async def search_symbol(keywords: str) -> str:
    """Search for stock symbols by keyword.

    Args:
        keywords: Search keywords (e.g., "Apple", "Microsoft")

    Returns:
        JSON with matching symbols
    """
    results = []
    for sym, overview in OVERVIEWS.items():
        if keywords.lower() in sym.lower() or keywords.lower() in overview.get("Name", "").lower():
            results.append({"symbol": sym, "name": overview.get("Name", ""), "exchange": overview.get("Exchange", "")})
    return json.dumps({"results": results, "count": len(results)}, indent=2)


@mcp.tool()
async def get_company_overview(symbol: str) -> str:
    """Get company overview and fundamental data.

    Args:
        symbol: Stock ticker symbol

    Returns:
        JSON with company overview
    """
    if symbol not in OVERVIEWS:
        return json.dumps({"error": f"Stock symbol {symbol} not found in dataset"})
    return json.dumps({"symbol": symbol, "overview": OVERVIEWS[symbol]}, indent=2)


@mcp.tool()
async def calculate_portfolio_value(holdings: str) -> str:
    """Calculate total portfolio value with current prices.

    Args:
        holdings: JSON string array of {symbol, shares} objects

    Returns:
        JSON with portfolio value breakdown
    """
    try:
        holding_data = json.loads(holdings) if isinstance(holdings, str) else holdings
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid holdings JSON"}, indent=2)

    total_value = 0
    holdings_result = []
    for h in holding_data:
        symbol = h.get("symbol", "")
        shares = h.get("shares", 0)
        if symbol in QUOTES:
            price = float(QUOTES[symbol].get("Global Quote", {}).get("05. price", 0))
            value = price * shares
            total_value += value
            holdings_result.append({"symbol": symbol, "shares": shares, "price": price, "value": round(value, 2)})
    return json.dumps({"holdings": holdings_result, "total_value": round(total_value, 2), "count": len(holdings_result)}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
