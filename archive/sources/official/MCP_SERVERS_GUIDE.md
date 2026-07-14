# MCP Servers Guide

Complete guide to using MCP servers in your benchmark domains.

## 📚 Table of Contents

- [What are MCP Servers?](#what-are-mcp-servers)
- [Listing Available Servers](#listing-available-servers)
- [Server Capabilities](#server-capabilities)
- [Installing Servers](#installing-servers)
- [Configuring API Keys](#configuring-api-keys)
- [Using Servers in Tasks](#using-servers-in-tasks)
- [Server Reference](#server-reference)
- [Troubleshooting](#troubleshooting)

---

## What are MCP Servers?

MCP (Model Context Protocol) servers are specialized services that provide AI agents with specific capabilities like:
- **Web search** (google_search)
- **Email operations** (email)
- **PDF generation** (pdf_generator)
- **Data processing** (google_sheets)
- **API access** (yahoo_finance, weather, etc.)
- And 20+ more...

Each server exposes **tools/functions** that agents can call to accomplish tasks.

---

## Listing Available Servers

### View All Servers

```bash
# List all available servers
uv run alignerr_mcp servers list

# List only installed servers
uv run alignerr_mcp servers list --installed

# List available (not installed) servers
uv run alignerr_mcp servers list --available
```

**Example output:**
```
┌─────────────────────┬───────────────┬────────────────────────────┐
│ Server              │ Status        │ Path                       │
├─────────────────────┼───────────────┼────────────────────────────┤
│ google_search       │ ✓ Installed   │ lbx_cli/.../servers/...    │
│ email               │ ○ Available   │ lbx_cli/.../servers/...    │
│ yahoo_finance       │ ○ Available   │ lbx_cli/.../servers/...    │
└─────────────────────┴───────────────┴────────────────────────────┘

Total: 26 servers
Installed: 1
Available: 25
```

---

## Server Capabilities

### View All Server Capabilities

```bash
# Show comprehensive overview of all servers
uv run alignerr_mcp servers capabilities
```

This displays:
- ✅ Server names
- ✅ Installation status
- ✅ Required API keys
- ✅ Available tools/functions
- ✅ Capabilities summary

**Example output:**
```
┌────────────────┬────────┬─────────────────────────┬──────────────────────────┐
│ Server         │ Status │ API Keys                │ Capabilities             │
├────────────────┼────────┼─────────────────────────┼──────────────────────────┤
│ google_search  │   ✓    │ SERP_API_KEY            │ • search                 │
│                │        │                         │ • web_search             │
├────────────────┼────────┼─────────────────────────┼──────────────────────────┤
│ email          │   ○    │ EMAIL_SMTP_SERVER       │ • send_email             │
│                │        │ EMAIL_SMTP_PORT         │ • read_inbox             │
│                │        │ EMAIL_USERNAME          │ • delete_email           │
├────────────────┼────────┼─────────────────────────┼──────────────────────────┤
│ yahoo_finance  │   ○    │ None required           │ • get_stock_price        │
│                │        │                         │ • get_historical_data    │
│                │        │                         │ • get_company_info       │
└────────────────┴────────┴─────────────────────────┴──────────────────────────┘
```

### View Specific Server Capabilities

```bash
# Show detailed capabilities for one server
uv run alignerr_mcp servers capabilities --server google_search

# Or use info command with --capabilities flag
uv run alignerr_mcp servers info google_search --capabilities
```

**Example output:**
```
Server: google_search

Required API Keys:
  • SERP_API_KEY (get from: serpapi.com)

┌─────────────────┬───────────────────────────────────────────────┐
│ Tool/Function   │ Description                                   │
├─────────────────┼───────────────────────────────────────────────┤
│ search          │ Perform Google search with query              │
│ web_search      │ Search web with advanced parameters           │
└─────────────────┴───────────────────────────────────────────────┘
```

### Server Information

```bash
# Get detailed information about a specific server
uv run alignerr_mcp servers info google_search
```

Shows:
- Installation status
- Required API keys with URLs
- Description
- Installation instructions
- Configuration help

---

## Installing Servers

### Install Single Server

```bash
# Install a specific server
uv run alignerr_mcp servers install google_search

# Force reinstall
uv run alignerr_mcp servers install google_search --force
```

### Install Multiple Servers

```bash
# Install all servers (not recommended - takes time)
uv run alignerr_mcp servers install all

# Or install them one by one as needed
uv run alignerr_mcp servers install google_search
uv run alignerr_mcp servers install yahoo_finance
uv run alignerr_mcp servers install email
```

### Uninstall Server

```bash
# Remove a server
uv run alignerr_mcp servers uninstall google_search
```

---

## Configuring API Keys

Many MCP servers require API keys to function. Here's how to configure them:

### Method 1: Using the CLI (Recommended)

```bash
# Interactive setup for all required keys
uv run alignerr_mcp env setup

# Setup specific category
uv run alignerr_mcp env setup --category llm

# Non-interactive mode
uv run alignerr_mcp env setup --no-interactive
```

**The CLI will:**
1. Detect which servers need API keys
2. Prompt you for each key
3. Save to `.env` file automatically
4. Validate the configuration

### Method 2: Manual .env File

Create or edit `.env` file in your project root:

```bash
# .env file
# Google Search (SerpAPI)
SERP_API_KEY=your_serpapi_key_here

# API Football
API_FOOTBALL_KEY=your_api_football_key_here

# Email Server
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# LLM Providers (for evaluation)
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx

# Financial Data
ALPHA_VANTAGE_KEY=your_key_here

# Add more as needed...
```

**Important:**
- ✅ **Never commit `.env` to git** (it's in `.gitignore` by default)
- ✅ Use environment variables in CI/CD (GitHub Secrets)
- ✅ Get free API keys from provider websites

### Method 3: Export Environment Variables

```bash
# Temporarily set for current session
export SERP_API_KEY=your_serpapi_key_here
export API_FOOTBALL_KEY=your_api_football_key_here

# Make permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export SERP_API_KEY=your_key' >> ~/.zshrc
source ~/.zshrc
```

### Check Configuration Status

```bash
# View which environment variables are configured
uv run alignerr_mcp env status

# Show required variables for all servers
uv run alignerr_mcp env show

# Show required variables for specific category
uv run alignerr_mcp env show --category llm
```

### Export Configuration Template

```bash
# Generate .env template with all possible keys
uv run alignerr_mcp env export

# Save to specific file
uv run alignerr_mcp env export --output .env.template
```

---

## Getting API Keys

### Common Server API Keys

| Server | API Key | Get From | Free Tier |
|--------|---------|----------|-----------|
| **google_search** | `SERP_API_KEY` | [serpapi.com](https://serpapi.com/) | 100 searches/month |
| **api_football** | `API_FOOTBALL_KEY` | [api-football.com](https://www.api-football.com/) | 100 requests/day |
| **openweather** | `OPENWEATHER_API_KEY` | [openweathermap.org](https://openweathermap.org/api) | 60 calls/min |
| **yahoo_finance** | None | N/A | Unlimited (public API) |
| **email** | SMTP credentials | Your email provider | Varies |
| **google_sheets** | `GOOGLE_CREDENTIALS_JSON` | [console.cloud.google.com](https://console.cloud.google.com/) | Free |
| **stripe_payments** | `STRIPE_API_KEY` | [stripe.com](https://stripe.com/docs/keys) | Test mode free |

### Steps to Get API Keys

#### Example: SerpAPI (for google_search)

1. Go to [serpapi.com](https://serpapi.com/)
2. Sign up for free account
3. Navigate to Dashboard → API Key
4. Copy your API key
5. Add to `.env`:
   ```bash
   SERP_API_KEY=your_key_here
   ```

#### Example: API Football

1. Go to [api-football.com](https://www.api-football.com/)
2. Sign up and choose free plan
3. Get API key from dashboard
4. Add to `.env`:
   ```bash
   API_FOOTBALL_KEY=your_key_here
   ```

#### Example: Google Sheets (OAuth)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Google Sheets API
4. Create service account credentials
5. Download JSON file
6. Save path in `.env`:
   ```bash
   GOOGLE_CREDENTIALS_JSON=/path/to/credentials.json
   ```

---

## Using Servers in Tasks

### Task Configuration

When creating tasks, specify which MCP servers to use:

```json
{
    "category": "web_search",
    "question": "Find the current CEO of Microsoft",
    "output_format": {
        "answer": "[CEO name]"
    },
    "use_specified_server": true,
    "mcp_servers": [
        {
            "name": "google-search"
        }
    ],
    "evaluators": [
        {
            "func": "raw",
            "op": "domain.evaluate_answer",
            "op_args": {
                "correct_answer": "Satya Nadella"
            }
        }
    ]
}
```

### Using Multiple Servers

```json
{
    "question": "Search for Apple stock price and send email summary",
    "mcp_servers": [
        {
            "name": "yahoo-finance"
        },
        {
            "name": "email"
        }
    ]
}
```

### Server Name Format

**In CLI:** Use underscore format
```bash
uv run alignerr_mcp servers install google_search
```

**In tasks:** Use hyphen format
```json
"mcp_servers": [{"name": "google-search"}]
```

---

## Seeding Server Data

Some servers may require initial data seeding or configuration.

### Servers That Need Seeding

#### file_storage
If using file_storage server, you may need to create initial directories:

```bash
# Create storage directory
mkdir -p ~/.mcp_storage

# Set environment variable
export MCP_STORAGE_PATH=~/.mcp_storage
```

#### email
For testing email server, you might want to use test data:

```bash
# Use a test SMTP server like MailHog or Mailtrap
export EMAIL_SMTP_SERVER=localhost
export EMAIL_SMTP_PORT=1025
export EMAIL_USERNAME=test@example.com
export EMAIL_PASSWORD=test
```

#### google_sheets
Initial sheet creation might be needed:

```python
# Create test spreadsheet (optional)
# The server can create sheets on-demand
```

#### invoicing / subscription_management
These may use in-memory or SQLite storage - no seeding needed for testing.

### Database-backed Servers

Some custom servers might use databases. Check server README:

```bash
# Example for a hypothetical database server
uv run alignerr_mcp servers info my_database_server

# Follow server-specific setup instructions
```

Most provided servers are **stateless** or use **in-memory storage** for simplicity.

---

## Server Reference

### Search & Information

- **google_search** - Web search via SerpAPI
- **wikipedia** - Wikipedia article retrieval
- **yahoo_finance** - Stock market data

### Communication

- **email** - Send and manage emails
- **sms_messaging** - SMS text messaging

### Document Processing

- **pdf_generator** - Create PDF documents
- **file_storage** - File management
- **image_processing** - Image manipulation

### Business Operations

- **invoicing** - Invoice generation
- **stripe_payments** - Payment processing
- **subscription_management** - Subscription handling
- **task_management** - Task tracking

### Data & Analytics

- **google_sheets** - Spreadsheet operations
- **stock_portfolio** - Portfolio management
- **crypto_intelligence** - Cryptocurrency data

### Utilities

- **calendar** - Calendar management
- **date** - Date/time operations
- **currency_converter** - Currency conversion
- **weather** - Weather information
- **url_shortener** - URL shortening

### Specialized

- **api_football** - Football/soccer data
- **flight_delay** - Flight information
- **blender** - 3D rendering (advanced)
- **receptionist_sim** - Receptionist simulation
- **it_support_desk** - IT ticketing system
- **echo** - Simple echo server (for testing)

---

## Troubleshooting

### Server Not Found

**Problem:**
```
Server not found: google_search
```

**Solutions:**
1. Check server name spelling
2. Verify submodules are initialized:
   ```bash
   git submodule update --init --recursive
   ```
3. Check server exists:
   ```bash
   ls lbx_mcp_universe_mcp_servers_mothership/servers/
   ```

### API Key Not Working

**Problem:**
```
Error: API_KEY not set in environment
```

**Solutions:**
1. Verify `.env` file exists and contains key
2. Check environment variable name (exact match required)
3. Restart terminal/shell after setting env vars
4. Verify API key is valid (test on provider website)
5. Check for typos or extra spaces in key

### Server Won't Install

**Problem:**
```
Installation failed for google_search
```

**Solutions:**
1. Update UV and Python:
   ```bash
   uv --version  # Should be recent
   python --version  # Should be 3.10+
   ```

2. Try force reinstall:
   ```bash
   uv run alignerr_mcp servers install google_search --force
   ```

3. Check dependencies:
   ```bash
   cd lbx_mcp_universe_mcp_servers_mothership/servers/google_search
   cat pyproject.toml  # Check requirements
   ```

4. Install manually:
   ```bash
   cd lbx_mcp_universe_mcp_servers_mothership/servers/google_search
   pip install -e .
   ```

### Server Not Responding

**Problem:**
Agent can't connect to MCP server

**Solutions:**
1. Verify server is installed:
   ```bash
   uv run alignerr_mcp servers list --installed
   ```

2. Test server independently:
   ```bash
   python -m google_search  # Replace with your server
   ```

3. Check logs for errors
4. Verify API keys are configured
5. Check network connectivity for API-dependent servers

### Rate Limiting

**Problem:**
```
HTTP 429: Too Many Requests
```

**Solutions:**
1. Check your API plan limits
2. Upgrade to higher tier if needed
3. Implement rate limiting in tasks
4. Use caching where applicable
5. Spread requests over time

### Missing Dependencies

**Problem:**
```
ModuleNotFoundError: No module named 'httpx'
```

**Solutions:**
1. Reinstall server:
   ```bash
   uv run alignerr_mcp servers install google_search --force
   ```

2. Install dependencies manually:
   ```bash
   pip install httpx requests python-dotenv mcp
   ```

3. Sync project dependencies:
   ```bash
   uv sync --all-extras
   ```

---

## Best Practices

### 1. Install Only What You Need

```bash
# Don't install all servers
# ❌ uv run alignerr_mcp servers install all

# Install specific servers for your domain
# ✅ uv run alignerr_mcp servers install google_search yahoo_finance
```

### 2. Secure Your API Keys

```bash
# ✅ Use .env file (git-ignored)
# ✅ Use environment variables
# ✅ Use GitHub Secrets for CI

# ❌ Never hardcode in code
# ❌ Never commit to git
# ❌ Never share in public
```

### 3. Test Servers Before Using

```bash
# Test server works
uv run alignerr_mcp servers info google_search --capabilities

# Verify API keys configured
uv run alignerr_mcp env status

# Test in simple task first
```

### 4. Monitor API Usage

- Track API calls in free tiers
- Set up billing alerts
- Cache results when possible
- Use mock servers for development

### 5. Document Server Requirements

In your domain README, specify:
```markdown
## Required MCP Servers

- **google_search**: For web search tasks
  - API Key: SERP_API_KEY
  - Get from: https://serpapi.com/
  - Free tier: 100 searches/month

- **yahoo_finance**: For stock data
  - No API key required
  - Free unlimited access
```

---

## Quick Reference

```bash
# List all servers
uv run alignerr_mcp servers list

# Show capabilities
uv run alignerr_mcp servers capabilities

# Install server
uv run alignerr_mcp servers install SERVER_NAME

# Configure API keys
uv run alignerr_mcp env setup

# Check configuration
uv run alignerr_mcp env status

# Get server details
uv run alignerr_mcp servers info SERVER_NAME --capabilities
```

---

## Support

**Need help with MCP servers?**
- 💬 Ask in Discord channel
- 📖 Check server README files in `lbx_mcp_universe_mcp_servers_mothership/servers/`
- 🐛 Report issues on GitHub

**Provider-specific help:**
- Check API provider documentation
- Contact API provider support
- Review rate limits and quotas

---

**Happy server configuration!** 🚀

