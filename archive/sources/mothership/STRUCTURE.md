# MCP Servers Mothership - Repository Structure

## Overview

This repository contains all MCP servers for the LBX MCP Universe ecosystem, organized in a clean `servers/` subdirectory structure.

## Directory Structure

```
lbx_mcp_universe_mcp_servers_mothership/
├── README.md                           # Main documentation
├── CONTRIBUTING.md                     # Contributing guidelines
├── STRUCTURE.md                        # This file
├── .gitignore                         # Git ignore rules
├── create_pyproject.sh                # Utility script
│
└── servers/                           # All MCP servers
    ├── google_search/                 # Information & Search
    │   ├── pyproject.toml
    │   ├── README.md
    │   ├── server.py
    │   ├── __init__.py
    │   └── __main__.py
    ├── weather/
    ├── wikipedia/
    │
    ├── yahoo_finance/                 # Financial Services
    ├── currency_converter/
    ├── stock_portfolio/
    ├── stripe_payments/
    ├── invoicing/
    ├── subscription_management/
    ├── crypto_intelligence/
    │
    ├── email/                         # Communication
    ├── sms_messaging/
    ├── receptionist_sim/
    │
    ├── task_management/               # Productivity
    ├── calendar/
    ├── google_sheets/
    ├── file_storage/
    ├── url_shortener/
    │
    ├── echo/                          # Development & Tools
    ├── date/
    ├── pdf_generator/
    ├── image_processing/
    ├── blender/
    ├── it_support_desk/
    │
    ├── api_football/                  # Specialized Services
    ├── flight_delay/
    └── mcp-server-box/
```

## Benefits of servers/ Subdirectory

### 1. Clean Root Directory
- Documentation files at root level
- Easy to find README, CONTRIBUTING, etc.
- No clutter from 27 server directories

### 2. Clear Organization
- All servers in one place (`servers/`)
- Easy to discover and browse
- Logical grouping

### 3. Scalability
- Can add more directories (e.g., `tests/`, `docs/`, `scripts/`)
- Room for future organization
- Clean separation of concerns

### 4. Standard Practice
- Follows common repository patterns
- Similar to how many projects organize modules
- Professional structure

## Server Categories

### Information & Search (3 servers)
```
servers/google_search/
servers/wikipedia/
servers/weather/
```

### Financial Services (7 servers)
```
servers/yahoo_finance/
servers/currency_converter/
servers/stock_portfolio/
servers/stripe_payments/
servers/invoicing/
servers/subscription_management/
servers/crypto_intelligence/
```

### Communication (3 servers)
```
servers/email/
servers/sms_messaging/
servers/receptionist_sim/
```

### Productivity (5 servers)
```
servers/task_management/
servers/calendar/
servers/google_sheets/
servers/file_storage/
servers/url_shortener/
```

### Development & Tools (6 servers)
```
servers/echo/
servers/date/
servers/pdf_generator/
servers/image_processing/
servers/blender/
servers/it_support_desk/
```

### Specialized Services (3 servers)
```
servers/api_football/
servers/flight_delay/
servers/mcp-server-box/
```

## Usage

### Navigate to a Server

```bash
cd lbx_mcp_universe_mcp_servers_mothership/servers/google_search
```

### Install a Server

```bash
cd servers/google_search
pip install -e .
```

### Run a Server

```bash
cd servers/google_search
python -m google_search
```

### List All Servers

```bash
ls servers/
```

## Adding a New Server

### 1. Create in servers/ directory

```bash
cd servers
mkdir my_new_server
cd my_new_server
```

### 2. Add required files

```bash
touch pyproject.toml
touch README.md
touch server.py
touch __init__.py
touch __main__.py
```

### 3. Follow the template

See `CONTRIBUTING.md` for detailed instructions.

## Integration with CLI

The Alignerr CLI accesses servers via:

```
lbx_cli/mcp_servers → ../../lbx_mcp_universe_mcp_servers_mothership
```

The CLI will automatically discover servers in the `servers/` subdirectory.

## File Counts

```
Root Level:
  - 4 documentation files
  - 2 utility files

servers/ directory:
  - 27 server directories
  - ~120 total files
  - ~11,000 lines of code
```

## Navigation Tips

### List all servers
```bash
ls servers/
```

### Find specific server
```bash
find servers/ -name "google_search"
```

### Count servers
```bash
ls servers/ | wc -l
```

### Search in server code
```bash
grep -r "search" servers/google_search/
```

## Future Expansions

The structure allows for easy addition of:

```
lbx_mcp_universe_mcp_servers_mothership/
├── servers/          # MCP servers
├── tests/            # Shared tests (future)
├── docs/             # Extended documentation (future)
├── scripts/          # Utility scripts (future)
└── templates/        # Server templates (future)
```

## Commit History

- Initial commit: All servers added
- Reorganization: Moved to servers/ subdirectory
- Documentation: Updated to reflect structure

---

**Structure Status**: ✅ **Organized and Clean**

All 27 MCP servers are properly organized in the `servers/` subdirectory!

