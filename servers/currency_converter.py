"""Mock currency-converter MCP server — currency conversion with fixed rates."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("currency-converter")

_RATES = {
    "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 149.50, "CAD": 1.36, "AUD": 1.52, "CHF": 0.88, "CNY": 7.24, "INR": 83.30},
    "EUR": {"USD": 1.087, "GBP": 0.86, "JPY": 162.50, "CAD": 1.48, "AUD": 1.65, "CHF": 0.96, "CNY": 7.87, "INR": 90.50},
    "GBP": {"USD": 1.266, "EUR": 1.163, "JPY": 189.00, "CAD": 1.72, "AUD": 1.92, "CHF": 1.11, "CNY": 9.16, "INR": 105.40},
}


@mcp.tool()
async def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another.

    Args:
        amount: The amount to convert
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')

    Returns:
        JSON with the converted amount and exchange rate
    """
    from_c = from_currency.upper()
    to_c = to_currency.upper()

    if from_c == to_c:
        return json.dumps({"amount": amount, "from": from_c, "to": to_c, "converted_amount": amount, "rate": 1.0}, indent=2)

    if from_c in _RATES and to_c in _RATES[from_c]:
        rate = _RATES[from_c][to_c]
    elif to_c in _RATES and from_c in _RATES[to_c]:
        rate = 1.0 / _RATES[to_c][from_c]
    else:
        rate = 1.0

    converted = round(amount * rate, 2)
    return json.dumps({"amount": amount, "from": from_c, "to": to_c, "converted_amount": converted, "rate": rate}, indent=2)


@mcp.tool()
async def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Get the exchange rate between two currencies.

    Args:
        from_currency: Source currency code
        to_currency: Target currency code

    Returns:
        JSON with the exchange rate
    """
    from_c = from_currency.upper()
    to_c = to_currency.upper()
    if from_c in _RATES and to_c in _RATES[from_c]:
        rate = _RATES[from_c][to_c]
    elif to_c in _RATES and from_c in _RATES[to_c]:
        rate = 1.0 / _RATES[to_c][from_c]
    else:
        rate = 1.0
    return json.dumps({"from": from_c, "to": to_c, "rate": rate}, indent=2)


@mcp.tool()
async def list_currencies() -> str:
    """List all supported currencies.

    Returns:
        JSON array of supported currency codes
    """
    currencies = set()
    for from_c, rates in _RATES.items():
        currencies.add(from_c)
        for to_c in rates:
            currencies.add(to_c)
    return json.dumps({"currencies": sorted(currencies), "count": len(currencies)}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
