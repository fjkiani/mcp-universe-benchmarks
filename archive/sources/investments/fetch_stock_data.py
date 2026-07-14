#!/usr/bin/env python3
"""
Fetch real stock data from Alpha Vantage to use for mock server.
This will capture actual market data for the 6 stocks used in investment tasks.
"""
import json
import httpx
import asyncio
from datetime import datetime

ALPHA_VANTAGE_API_KEY = "0F77498K6RPO3D58"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"

# Stocks used in investment tasks
STOCKS = ["AAPL", "GOOGL", "MSFT", "TSLA", "JPM", "JNJ"]

async def fetch_stock_quote(symbol: str):
    """Fetch real-time quote."""
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(ALPHA_VANTAGE_API_URL, params=params, timeout=30.0)
        data = response.json()
        return {symbol: data}

async def fetch_company_overview(symbol: str):
    """Fetch company fundamentals."""
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(ALPHA_VANTAGE_API_URL, params=params, timeout=30.0)
        data = response.json()
        return {symbol: data}

async def fetch_daily_data(symbol: str):
    """Fetch daily historical data."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",  # Last 100 days
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(ALPHA_VANTAGE_API_URL, params=params, timeout=30.0)
        data = response.json()
        return {symbol: data}

async def fetch_all_data():
    """Fetch all data for all stocks."""
    print(f"🔍 Fetching data for {len(STOCKS)} stocks from Alpha Vantage...")
    print(f"📅 Timestamp: {datetime.now().isoformat()}\n")
    
    all_data = {
        "metadata": {
            "fetched_at": datetime.now().isoformat(),
            "api_provider": "Alpha Vantage",
            "stocks": STOCKS
        },
        "quotes": {},
        "overviews": {},
        "daily_data": {}
    }
    
    for i, symbol in enumerate(STOCKS, 1):
        print(f"[{i}/{len(STOCKS)}] Fetching {symbol}...")
        
        # Fetch quote
        print(f"  → Real-time quote...")
        quote_data = await fetch_stock_quote(symbol)
        all_data["quotes"].update(quote_data)
        await asyncio.sleep(12)  # Alpha Vantage: 5 calls/min free tier
        
        # Fetch overview
        print(f"  → Company overview...")
        overview_data = await fetch_company_overview(symbol)
        all_data["overviews"].update(overview_data)
        await asyncio.sleep(12)
        
        # Fetch daily data
        print(f"  → Daily historical data...")
        daily_data = await fetch_daily_data(symbol)
        all_data["daily_data"].update(daily_data)
        await asyncio.sleep(12)
        
        print(f"  ✅ {symbol} complete\n")
    
    # Save to file
    output_file = "stock_data_snapshot.json"
    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\n✅ ALL DATA FETCHED!")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 Total stocks: {len(STOCKS)}")
    print(f"💾 File size: {len(json.dumps(all_data)) / 1024:.1f} KB")
    
    # Print summary
    print("\n📈 DATA SUMMARY:")
    for symbol in STOCKS:
        quote = all_data["quotes"].get(symbol, {}).get("Global Quote", {})
        overview = all_data["overviews"].get(symbol, {})
        
        price = quote.get("05. price", "N/A")
        company_name = overview.get("Name", "N/A")
        sector = overview.get("Sector", "N/A")
        
        print(f"  • {symbol}: {company_name} - ${price} ({sector})")

if __name__ == "__main__":
    asyncio.run(fetch_all_data())

