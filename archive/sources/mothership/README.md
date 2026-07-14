# LBX MCP Servers

Collection of Model Context Protocol (MCP) servers for the LBX MCP Universe ecosystem.

## Overview

This repository contains **27 isolated MCP server implementations** that provide various capabilities for AI agents, from web search and weather data to financial analysis and task management.

## Architecture

Each MCP server is **completely isolated** in its own subdirectory with:
- ✅ Independent `pyproject.toml` for dependencies
- ✅ Self-contained implementation
- ✅ Dedicated README with usage instructions
- ✅ Test files where applicable
- ✅ Server configuration

## Available Servers

### Information & Search
- **google_search** - Google search functionality via SerpAPI
- **wikipedia** - Wikipedia article search and retrieval
- **weather** - Weather data and forecasts

### Financial Services
- **yahoo_finance** - Stock market data and analysis
- **yfinance** - Alternative finance data provider
- **currency_converter** - Currency conversion services
- **stock_portfolio** - Portfolio management and tracking
- **stripe_payments** - Payment processing via Stripe
- **invoicing** - Invoice generation and management
- **subscription_management** - Subscription billing management

### Communication
- **email** - Email sending and management
- **sms_messaging** - SMS messaging via Twilio
- **receptionist_sim** - Receptionist simulation with intent classification

### Productivity
- **task_management** - Task tracking and management
- **calendar** - Calendar and scheduling
- **google_sheets** - Google Sheets integration
- **file_storage** - File storage and management

### Development & Tools
- **echo** - Simple echo server for testing
- **date** - Date and time utilities
- **url_shortener** - URL shortening service
- **pdf_generator** - PDF document generation
- **image_processing** - Image manipulation and processing

### Specialized Services
- **api_football** - Football/soccer data API
- **flight_delay** - Flight delay information
- **blender** - Blender 3D integration
- **crypto_intelligence** - Cryptocurrency data and analysis
- **it_support_desk** - IT support ticket management
- **mcp-server-box** - Box file storage integration

## Directory Structure

```
lbx_mcp_universe_mcp_servers_mothership/
├── README.md                    # This file
├── CONTRIBUTING.md              # Contribution guidelines
├── .gitignore                   # Git ignore rules
│
└── servers/                     # All MCP servers
    ├── google_search/           # Each server in isolation
│   ├── pyproject.toml          # Server-specific dependencies
│   ├── README.md               # Server documentation
│   ├── server.py               # Main server implementation
│   ├── __init__.py             # Package init
│   ├── __main__.py             # CLI entry point
│   └── test_server.py          # Tests (optional)
│
    ├── weather/
    │   ├── pyproject.toml
    │   ├── README.md
    │   ├── server.py
    │   ├── __init__.py
    │   └── __main__.py
    │
    └── [... 25 more servers]
```

## Installation

### Install All Servers

```bash
# Clone the repository
git clone <repo-url> lbx_mcp_servers
cd lbx_mcp_servers

# Install all servers (from root)
./install_all.sh
```

### Install Specific Server

```bash
cd lbx_mcp_universe_mcp_servers_mothership/servers/google_search
pip install -e .
```

### Use as Git Submodule

This repository is designed to be used as a git submodule in other projects:

```bash
# In your project
git submodule add <repo-url> mcp_servers
git submodule update --init --recursive

# Update servers
git submodule update --remote --merge
```

## Usage

### Running a Server

Each server can be run independently:

```bash
# Method 1: Using python module
cd google_search
python -m google_search

# Method 2: Using server entry point
cd google_search
python server.py

# Method 3: If installed
google-search-server
```

### Server Configuration

Servers are configured via:
1. Environment variables (`.env` files)
2. Configuration files in each server directory
3. Command-line arguments

Example `.env`:
```bash
# For google_search server
SERP_API_KEY=your_api_key_here

# For weather server
OPENWEATHER_API_KEY=your_api_key_here
```

## Development

### Adding a New Server

1. Create a new directory for your server in servers/
2. Add required files:
   ```bash
   cd servers
   mkdir my_new_server
   cd my_new_server
   touch pyproject.toml README.md server.py __init__.py __main__.py
   ```

3. Implement your server in `server.py`
4. Add dependencies to `pyproject.toml`
5. Document usage in `README.md`
6. Test your server
7. Submit a pull request

### Server Template

Use the template structure:

```
my_server/
├── pyproject.toml          # Dependencies
├── README.md               # Documentation
├── server.py               # Main implementation
├── __init__.py             # Package init
├── __main__.py             # CLI entry
└── test_server.py          # Tests (optional)
```

### Testing

```bash
# Test specific server
cd google_search
pytest test_server.py

# Test all servers
./test_all.sh
```

## Integration with Alignerr CLI

This repository is integrated with the Alignerr CLI as a git submodule:

```bash
# In alignerr CLI
cd lbx_mcp_universe_cli
git submodule add <repo-url> lbx_cli/mcp_servers

# Servers are then available to the CLI
alignerr validate --domain google_search
```

## Server Standards

All servers must follow these standards:

### 1. Isolation
- Each server is completely independent
- No shared code between servers
- Own dependencies in `pyproject.toml`

### 2. Structure
- Standard file layout (pyproject.toml, README, server.py, etc.)
- Clear documentation
- Proper error handling

### 3. Configuration
- Environment variable support
- `.env` file support
- Sensible defaults

### 4. Testing
- Unit tests where applicable
- Integration test examples
- Test data in `tests/` subdirectory

### 5. Documentation
- Clear README with:
  - Purpose and description
  - Installation instructions
  - Configuration options
  - Usage examples
  - API documentation

## API Keys and Credentials

Many servers require API keys. See individual server READMEs for specific requirements:

- **google_search**: SERP_API_KEY
- **weather**: OPENWEATHER_API_KEY
- **gmail**: Google OAuth credentials
- **stripe_payments**: STRIPE_API_KEY
- **sms_messaging**: TWILIO credentials
- And more...

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-new-server`
3. Add your server following the structure above
4. Test thoroughly
5. Submit a pull request

## License

[Your License Here]

## Support

For issues or questions:
- Check individual server READMEs
- Create an issue in this repository
- Contact the maintainers

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Made with ❤️ for the LBX MCP Universe**

