"""Mock stock portfolio MCP server using captured real market data.

This server uses a snapshot of real Alpha Vantage data (captured Oct 25, 2025)
to provide deterministic responses for benchmark evaluation.
"""
import json
import os
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("stock-portfolio")

# Load captured real market data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "stock_data.json")

with open(DATA_FILE, 'r') as f:
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
    try:
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
            "low": float(quote_data.get("04. low", 0))
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def get_stock_daily(symbol: str, outputsize: str = "compact") -> str:
    """Get daily time series data for a stock (from captured data).
    
    Args:
        symbol: Stock ticker symbol
        outputsize: "compact" (last 100 data points) or "full" (20+ years)
        
    Returns:
        JSON with daily price data
    """
    try:
        if symbol not in DAILY_DATA:
            return json.dumps({"error": f"Stock symbol {symbol} not found in dataset"})
        
        time_series_data = DAILY_DATA[symbol].get("Time Series (Daily)", {})
        
        # Get last 10 days (or all if less than 10)
        daily_data = []
        for date, values in list(time_series_data.items())[:10]:
            daily_data.append({
                "date": date,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            })
        
        result = {
            "symbol": symbol,
            "daily_data": daily_data,
            "count": len(daily_data)
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def search_symbol(keywords: str) -> str:
    """Search for stock symbols (from captured data).
    
    Args:
        keywords: Search keywords (company name or symbol)
        
    Returns:
        JSON with matching symbols
    """
    try:
        keywords_lower = keywords.lower()
        matches = []
        
        for symbol, overview_data in OVERVIEWS.items():
            name = overview_data.get("Name", "").lower()
            if keywords_lower in symbol.lower() or keywords_lower in name:
                matches.append({
                    "symbol": symbol,
                    "name": overview_data.get("Name"),
                    "type": "Equity",
                    "region": "United States",
                    "currency": "USD"
                })
        
        result = {
            "matches": matches,
            "count": len(matches)
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def get_company_overview(symbol: str) -> str:
    """Get company overview and fundamental data (from captured data).
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        JSON with company overview
    """
    try:
        if symbol not in OVERVIEWS:
            return json.dumps({"error": f"Company {symbol} not found in dataset"})
        
        data = OVERVIEWS[symbol]
        
        result = {
            "symbol": data.get("Symbol"),
            "name": data.get("Name"),
            "description": data.get("Description"),
            "sector": data.get("Sector"),
            "industry": data.get("Industry"),
            "market_cap": data.get("MarketCapitalization"),
            "pe_ratio": data.get("PERatio"),
            "dividend_yield": data.get("DividendYield"),
            "52_week_high": data.get("52WeekHigh"),
            "52_week_low": data.get("52WeekLow"),
            "analyst_target_price": data.get("AnalystTargetPrice"),
            "revenue_ttm": data.get("RevenueTTM"),
            "profit_margin": data.get("ProfitMargin")
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def calculate_portfolio_value(holdings: list) -> str:
    """Calculate total portfolio value with current prices.
    
    Args:
        holdings: List of holdings with symbol and shares (e.g., [{"symbol": "AAPL", "shares": 10}])
        
    Returns:
        JSON with portfolio valuation
    """
    try:
        total_value = 0
        holdings_data = []
        
        for holding in holdings:
            symbol = holding.get("symbol")
            shares = float(holding.get("shares", 0))
            
            if symbol not in QUOTES:
                continue
            
            quote_data = QUOTES[symbol].get("Global Quote", {})
            price = float(quote_data.get("05. price", 0))
            value = price * shares
            
            total_value += value
            
            holdings_data.append({
                "symbol": symbol,
                "shares": shares,
                "price": price,
                "value": value,
                "change_percent": quote_data.get("10. change percent", "0%")
            })
        
        result = {
            "holdings": holdings_data,
            "total_value": round(total_value, 2),
            "count": len(holdings_data)
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


def main():
    """Run the Mock Stock Portfolio MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()

