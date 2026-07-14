# Flight Delay Prediction MCP Server

An MCP (Model Control Protocol) server that predicts flight delays using the official FlightRadar24 API. This server analyzes historical flight data to estimate delay probabilities and provides actionable recommendations for travelers.

## Features

- **Flight Number Delay Prediction**: Get delay probability for specific flights (e.g., "AA100")
- **Route-Based Analysis**: Analyze delays for specific airline routes
- **Airport Delay Statistics**: Check current delay conditions at airports
- **Historical Data Analysis**: Uses up to 14 days of historical flight data
- **Real-time API Integration**: Connects to official FlightRadar24 REST API

## Installation

### Prerequisites

- Python 3.8+
- FlightRadar24 API key (get from [https://fr24api.flightradar24.com](https://fr24api.flightradar24.com))

### Setup

1. **Install dependencies** (httpx is required):
```bash
pip install httpx click mcp
```

2. **Set your API key**:
```bash
export FLIGHTRADAR24_API_KEY="your-api-key-here"
```

Or add to `.env` file:
```
FLIGHTRADAR24_API_KEY=your-api-key-here
```

3. **Run the server**:
```bash
python -m mcpuniverse.mcp.servers.flight_delay
```

## Available Tools

### 1. predict_flight_delay_by_number

Predicts delay probability for a specific flight number.

**Parameters:**
- `flight_number` (string): Flight number (e.g., "AA100", "BA123")

**Example:**
```json
{
  "tool": "predict_flight_delay_by_number",
  "arguments": {
    "flight_number": "AA100"
  }
}
```

**Response:**
```json
{
  "flight_number": "AA100",
  "airline": "American Airlines",
  "delay_probability": 35.5,
  "confidence": "high",
  "recommendation": "Moderate delay risk. Consider arriving early.",
  "data_source": "FlightRadar24 Official API"
}
```

### 2. predict_flight_delay_by_route

Analyzes delay probability for a specific route.

**Parameters:**
- `airline` (string): Airline code (e.g., "AA", "BA", "DL")
- `departure_airport` (string): Departure airport code (e.g., "JFK", "LAX")
- `arrival_airport` (string): Arrival airport code (e.g., "LHR", "CDG")
- `date` (string, optional): Date in YYYY-MM-DD format

**Example:**
```json
{
  "tool": "predict_flight_delay_by_route",
  "arguments": {
    "airline": "AA",
    "departure_airport": "JFK",
    "arrival_airport": "LAX"
  }
}
```

**Response:**
```json
{
  "route": {
    "airline": "AA",
    "from": "JFK",
    "to": "LAX",
    "date": "2025-01-15"
  },
  "delay_prediction": {
    "probability": 28.7,
    "confidence": "high",
    "total_flights": 14,
    "delayed_flights": 4,
    "average_delay_minutes": 35.5
  },
  "recommendation": "This route has low to moderate delay risk."
}
```

### 3. get_airport_delay_stats

Get current delay statistics for an airport.

**Parameters:**
- `airport_code` (string): Airport IATA code (e.g., "JFK", "LAX", "ORD")

**Example:**
```json
{
  "tool": "get_airport_delay_stats",
  "arguments": {
    "airport_code": "JFK"
  }
}
```

**Response:**
```json
{
  "airport": "JFK",
  "current_status": "Moderate delays",
  "delay_statistics": {
    "average_departure_delay": 18.5,
    "average_arrival_delay": 22.3,
    "on_time_percentage": 72.5
  },
  "time_period": "Last 24 hours"
}
```

## API Endpoints Used

This server uses the following FlightRadar24 API endpoints:

- **Airlines**: `GET /api/static/airlines/{ICAO}/light`
- **Live Flights**: `GET /api/live/flight-positions/light`
- **Historic Flights**: `GET /api/historic/flight-positions/full?timestamp={ts}&flight={flight}`

## Configuration

### MCP Server Registration

Add to `mcpuniverse/mcp/configs/server_list.json`:

```json
{
  "flight-delay": {
    "stdio": {
      "command": "python3",
      "args": ["-m", "mcpuniverse.mcp.servers.flight_delay"]
    },
    "sse": {
      "command": "python3",
      "args": [
        "-m", "mcpuniverse.mcp.servers.flight_delay",
        "--transport", "sse",
        "--port", "{{PORT}}"
      ]
    }
  }
}
```

### Agent Configuration

Example agent using this server:

```yaml
kind: llm
spec:
  name: llm-1
  type: litellm
  config:
    model_name: openai/gpt-4o-mini

---
kind: agent
spec:
  name: FlightDelayAgent
  type: react
  config:
    llm: llm-1
    instruction: |
      You are a flight delay prediction assistant.
      Help travelers understand flight delay risks and provide recommendations.
    servers:
      - name: flight-delay

---
kind: benchmark
spec:
  description: Test flight delay predictions
  agent: FlightDelayAgent
  tasks:
    - flight_delay/tasks/flight_delay_by_number.json
```

## Testing

Run the test benchmark:

```bash
uv run python run.py one mcpuniverse/benchmark/configs/flight_delay/flight_delay_benchmark.yaml --no-callbacks
```

## Delay Calculation Logic

The server calculates delay probability using:

1. **Historical Data Collection**: Fetches flight data for the last 14 days
2. **Delay Detection**: Flags flights delayed more than 15 minutes
3. **Probability Calculation**: `(delayed_flights / total_flights) × 100`
4. **Confidence Scoring**:
   - **High**: 10+ historical flights
   - **Medium**: 5-9 historical flights
   - **Low**: <5 historical flights

## Limitations & Future Enhancements

### Current Limitations

- Historical analysis requires multiple API calls (one per day)
- Some endpoints return simulated data when real data unavailable
- Airport statistics are simulated (requires additional API access)

### Planned Enhancements

1. **Caching**: Add Redis caching for historical data
2. **Real Airport Stats**: Integrate live airport delay feeds
3. **Weather Integration**: Include weather data in predictions
4. **ML Model**: Train model on historical patterns
5. **Route Optimization**: Suggest alternative flights with better on-time records

## References

- **Official FlightRadar24 API Docs**: [https://fr24api.flightradar24.com/docs](https://fr24api.flightradar24.com/docs)
- **Official MCP Server**: [@flightradar24/fr24api-mcp](https://www.npmjs.com/package/@flightradar24/fr24api-mcp)
- **GitHub**: [github.com/Flightradar24/fr24api-mcp](https://github.com/Flightradar24/fr24api-mcp)

## License

This MCP server is part of the MCP-Universe framework.

## Support

For issues or questions:
- Create an issue in the MCP-Universe repository
- Check FlightRadar24 API documentation for API-related issues
