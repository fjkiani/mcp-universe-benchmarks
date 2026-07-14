# API-Football MCP Server

A Model Context Protocol (MCP) server that provides access to comprehensive football data from [API-Football](https://www.api-football.com/). This server enables AI assistants to retrieve live scores, fixtures, standings, team information, player statistics, and betting odds.

## Features

- **Live Scores**: Real-time match data and scores
- **Fixtures**: Upcoming and past match schedules
- **Standings**: League tables and team rankings
- **Team Information**: Detailed team data and statistics
- **Player Information**: Player profiles and statistics
- **Search Functionality**: Search for teams and players
- **League Data**: Available leagues and competitions
- **Betting Odds**: Pre-match and live odds
- **Comprehensive Error Handling**: User-friendly error messages
- **Rate Limiting**: Respects API-Football rate limits

## Prerequisites

- Python 3.8+
- API-Football API key (get one at [api-football.com](https://www.api-football.com/))
- Required Python packages (see installation)

## Installation

1. Install the required dependencies:
```bash
pip install httpx click mcp
```

2. Set up your API key:
```bash
export API_FOOTBALL_KEY="your_api_key_here"
```

## Usage

### Starting the Server

```bash
# Using stdio transport (default)
python -m mcpuniverse.mcp.servers.api_football

# Using SSE transport
python -m mcpuniverse.mcp.servers.api_football --transport sse --port 8000
```

### Available Tools

#### 1. `get_livescores`
Get live football scores and match information.

**Parameters:**
- `league_id` (optional): Specific league ID to filter by
- `season` (optional): Season year to filter by

**Example:**
```python
await get_livescores(league_id=39, season=2024)
```

#### 2. `get_fixtures`
Get football fixtures (upcoming or past matches).

**Parameters:**
- `league_id` (optional): Specific league ID to filter by
- `season` (optional): Season year to filter by
- `team_id` (optional): Specific team ID to filter by
- `date` (optional): Date in YYYY-MM-DD format
- `next` (optional): Number of upcoming fixtures to get

**Example:**
```python
await get_fixtures(league_id=39, season=2024, next=5)
```

#### 3. `get_standings`
Get league standings/table.

**Parameters:**
- `league_id`: League ID to get standings for
- `season`: Season year

**Example:**
```python
await get_standings(league_id=39, season=2024)
```

#### 4. `get_team_info`
Get detailed information about a specific team.

**Parameters:**
- `team_id`: Team ID to get information for

**Example:**
```python
await get_team_info(team_id=33)
```

#### 5. `get_player_info`
Get detailed information about a specific player.

**Parameters:**
- `player_id`: Player ID to get information for

**Example:**
```python
await get_player_info(player_id=874)
```

#### 6. `search_teams`
Search for teams by name.

**Parameters:**
- `name`: Team name to search for
- `country` (optional): Country to filter by

**Example:**
```python
await search_teams(name="Manchester United")
```

#### 7. `search_players`
Search for players by name.

**Parameters:**
- `name`: Player name to search for
- `team_id` (optional): Team ID to filter by

**Example:**
```python
await search_players(name="Cristiano Ronaldo")
```

#### 8. `get_leagues`
Get available football leagues.

**Parameters:**
- `country` (optional): Country to filter by
- `season` (optional): Season year to filter by

**Example:**
```python
await get_leagues(country="England", season=2024)
```

#### 9. `get_odds`
Get betting odds for a specific fixture.

**Parameters:**
- `fixture_id`: Fixture ID to get odds for

**Example:**
```python
await get_odds(fixture_id=12345)
```

## API-Football Plan Limits

The server respects API-Football rate limits:

- **Free Plan**: 100 requests/day
- **Pro Plan**: 7,500 requests/day
- **Ultra Plan**: 75,000 requests/day
- **Mega Plan**: 150,000 requests/day

## Common League IDs

Here are some popular league IDs for reference:

- **Premier League**: 39
- **La Liga**: 140
- **Serie A**: 135
- **Bundesliga**: 78
- **Ligue 1**: 61
- **Champions League**: 2
- **Europa League**: 3
- **World Cup**: 1

## Error Handling

The server provides comprehensive error handling:

- **API Key Missing**: Clear message when API key is not set
- **HTTP Errors**: Proper handling of network issues
- **API Errors**: User-friendly error messages from API-Football
- **No Results**: Graceful handling when no data is found
- **Timeout**: 30-second timeout for requests

## Example Usage Scenarios

### Get Live Premier League Scores
```python
# Get all live Premier League matches
await get_livescores(league_id=39, season=2024)
```

### Get Upcoming Fixtures for a Team
```python
# Get next 5 fixtures for Manchester United (team_id=33)
await get_fixtures(team_id=33, next=5)
```

### Get League Standings
```python
# Get Premier League standings for 2024
await get_standings(league_id=39, season=2024)
```

### Search for a Player
```python
# Search for Messi
await search_players(name="Messi")
```

### Get Team Information
```python
# Get detailed info for Barcelona (team_id=529)
await get_team_info(team_id=529)
```

## Configuration

### Environment Variables

- `API_FOOTBALL_KEY`: Your API-Football API key (required)

### Server Options

- `--transport`: Transport type (`stdio` or `sse`)
- `--port`: Port for SSE transport (default: 8000)

## Troubleshooting

### Common Issues

1. **"API_FOOTBALL_KEY not set in environment"**
   - Make sure you've set the environment variable with your API key
   - Check that the API key is valid and active

2. **"No results found"**
   - Verify that the league/team/player IDs are correct
   - Check if the data exists for the specified season/date

3. **"HTTP error"**
   - Check your internet connection
   - Verify that API-Football service is available
   - Check if you've exceeded your rate limits

### Rate Limiting

If you hit rate limits, the server will return appropriate error messages. Consider upgrading your API-Football plan for higher limits.

## Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## License

This project is part of the mcpuniverse collection and follows the same licensing terms.

## Support

For API-Football specific issues, refer to the [API-Football documentation](https://www.api-football.com/documentation).

For MCP server issues, please check the server logs and error messages.
