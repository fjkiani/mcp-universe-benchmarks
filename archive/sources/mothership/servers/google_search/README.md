# Google Search MCP Server

MCP server providing Google search capabilities via SerpAPI.

## Features

- Web search with customizable parameters
- Rich snippet extraction
- Related searches
- Knowledge graph results
- News and images search

## Installation

```bash
cd google_search
pip install -e .
```

## Configuration

Set your SerpAPI key:

```bash
export SERP_API_KEY=your_api_key_here
```

Or create a `.env` file:
```
SERP_API_KEY=your_api_key_here
```

Get your API key from: https://serpapi.com/

## Usage

### Run the server

```bash
python -m google_search
```

### Available Tools

- `google-search` - Perform Google search with query

## Example

```python
# Search for information
result = await google_search("Python programming tutorials")
```

## Dependencies

- `mcp>=1.9.4` - MCP protocol support
- `requests>=2.32.0` - HTTP requests
- `python-dotenv>=1.0.0` - Environment configuration

## License

BSD 3-Clause

