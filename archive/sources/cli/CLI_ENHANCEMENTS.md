# CLI Enhancements: Server Management & Environment Setup

## New Features Added

### 1. MCP Server Management (`alignerr servers`)

Complete server lifecycle management commands:

#### Commands

```bash
# List all available servers
alignerr servers list

# List only installed servers
alignerr servers list --installed

# Show all available servers
alignerr servers list --available

# Install a specific server
alignerr servers install google_search

# Install all servers
alignerr servers install all

# Force reinstall
alignerr servers install google_search --force

# Uninstall a server
alignerr servers uninstall google_search

# Show server information
alignerr servers info google_search
```

#### Features

✅ **List Servers** - View all available servers with installation status  
✅ **Install Servers** - Install individual or all servers  
✅ **Force Reinstall** - Reinstall if needed  
✅ **Uninstall** - Remove installed servers  
✅ **Server Info** - View details about specific servers  
✅ **Status Indicators** - Visual indication of installed vs available  

---

### 2. Environment Variable Management (`alignerr env`)

Easy configuration management for API keys and credentials:

#### Commands

```bash
# Show configuration status
alignerr env status

# Interactive setup of all variables
alignerr env setup

# Setup only LLM providers
alignerr env setup --category llm

# Setup only MCP servers
alignerr env setup --category servers

# Show required variables and where to get them
alignerr env show

# Show only LLM variables
alignerr env show --category llm

# Export template .env file
alignerr env export

# Export to custom location
alignerr env export --output my.env
```

#### Features

✅ **Status Dashboard** - See what's configured and what's missing  
✅ **Interactive Setup** - Guided configuration with prompts  
✅ **Categorized** - Separate LLM and Server credentials  
✅ **Helpful Links** - URLs to get API keys  
✅ **Template Export** - Generate .env.example files  
✅ **Secure Input** - Password-masked input for sensitive data  

---

## Environment Variables Tracked

### LLM Providers

| Variable | Description | Get It At |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | https://platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude models | https://console.anthropic.com/ |
| `GEMINI_API_KEY` | Google Gemini API key | https://makersuite.google.com/app/apikey |
| `XAI_API_KEY` | xAI API key for Grok models | https://x.ai/ |
| `MISTRAL_API_KEY` | Mistral API key | https://console.mistral.ai/ |

### MCP Server Credentials

| Variable | Description | Get It At |
|----------|-------------|-----------|
| `SERP_API_KEY` | SerpAPI key for Google search | https://serpapi.com/ |
| `OPENWEATHER_API_KEY` | OpenWeather API key | https://openweathermap.org/api |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | https://console.cloud.google.com/google/maps-apis/credentials |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub Personal Access Token | https://github.com/settings/tokens |
| `NOTION_API_KEY` | Notion Integration Token | https://developers.notion.com/ |
| `STRIPE_API_KEY` | Stripe API key | https://dashboard.stripe.com/apikeys |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | https://console.twilio.com/ |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | https://console.twilio.com/ |

---

## Usage Examples

### Complete Setup Workflow

```bash
# 1. Check what's configured
alignerr env status

# Output:
# ╭─ Environment Configuration Status ─╮
# │                                    │
# ╰────────────────────────────────────╯
#
# LLM Providers:
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Variable           ┃ Status ┃ Required For        ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
# │ OPENAI_API_KEY     │ ✓ Set  │ OpenAI LLM provider │
# │ ANTHROPIC_API_KEY  │ ✗ Not Set │ Anthropic LLM provider │
# └────────────────────┴────────┴─────────────────────┘

# 2. Setup missing variables
alignerr env setup --category llm

# 3. List available servers
alignerr servers list

# 4. Install needed servers
alignerr servers install google_search
alignerr servers install weather
alignerr servers install wikipedia

# Or install all at once
alignerr servers install all

# 5. Check installed servers
alignerr servers list --installed

# 6. Verify configuration
alignerr env status
```

### Quick Server Installation

```bash
# Install specific servers for a domain
alignerr servers install google_search
alignerr servers install fetch

# Then validate the domain
alignerr validate --domain web_search
```

### Environment Setup

```bash
# See what variables are needed
alignerr env show

# Interactive setup
alignerr env setup

# Prompts like:
# OPENAI_API_KEY
#   OpenAI API key for GPT models
#   Required for: OpenAI LLM provider
#   Get it at: https://platform.openai.com/api-keys
#   Enter value for OPENAI_API_KEY: ********

# Setup only servers
alignerr env setup --category servers

# Export template for team
alignerr env export --output .env.example
git add .env.example
git commit -m "Add environment template"
```

---

## Configuration Storage

### Location

Environment variables are stored in:
```
~/.alignerr/.env
```

### Usage

Load variables in your shell:

```bash
# Bash/Zsh
source ~/.alignerr/.env

# Or add to your shell profile
echo "source ~/.alignerr/.env" >> ~/.bashrc
# or
echo "source ~/.alignerr/.env" >> ~/.zshrc
```

---

## Integration with Validation

The CLI automatically checks for required environment variables when running validations:

```bash
# Before validation, check status
alignerr env status

# Install required servers
alignerr servers install google_search

# Run validation
alignerr validate --domain web_search
```

---

## Server Installation Details

### What Happens During Installation

1. **Locates Server** - Finds server in `lbx_cli/mcp_servers/servers/`
2. **Checks pyproject.toml** - Validates server structure
3. **Pip Install** - Runs `pip install -e <server_path>`
4. **Verifies** - Checks installation success
5. **Reports** - Shows success/failure

### Server Package Names

Servers are installed with standardized names:
- `google_search` → `lbx-mcp-google-search`
- `weather` → `lbx-mcp-weather`
- `yahoo_finance` → `lbx-mcp-yahoo-finance`

---

## Status Command Details

### What It Shows

```bash
alignerr env status
```

Displays:
1. **LLM Providers Table**
   - All LLM provider variables
   - Configuration status (✓ Set / ✗ Not Set)
   - What they're required for

2. **MCP Server Credentials Table**
   - All server credential variables
   - Configuration status
   - Which servers need them

3. **Summary**
   - Total variables configured
   - Total variables missing
   - Percentage configured

### Example Output

```
╭─ Environment Configuration Status ─╮
│                                    │
╰────────────────────────────────────╯

LLM Providers:
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Variable           ┃ Status  ┃ Required For        ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ OPENAI_API_KEY     │ ✓ Set   │ OpenAI LLM provider │
│ ANTHROPIC_API_KEY  │ ✓ Set   │ Anthropic LLM..     │
│ GEMINI_API_KEY     │ ✗ Not   │ Gemini LLM provider │
│ XAI_API_KEY        │ ✗ Not   │ Grok LLM provider   │
│ MISTRAL_API_KEY    │ ✗ Not   │ Mistral LLM..       │
└────────────────────┴─────────┴─────────────────────┘

MCP Server Credentials:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Variable                   ┃ Status  ┃ Required For     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ SERP_API_KEY               │ ✓ Set   │ google_search..  │
│ OPENWEATHER_API_KEY        │ ✗ Not   │ weather server   │
│ GOOGLE_MAPS_API_KEY        │ ✗ Not   │ Google Maps..    │
│ GITHUB_PERSONAL_ACCESS_..  │ ✗ Not   │ GitHub..         │
│ NOTION_API_KEY             │ ✗ Not   │ Notion..         │
│ STRIPE_API_KEY             │ ✗ Not   │ stripe_payments  │
│ TWILIO_ACCOUNT_SID         │ ✗ Not   │ sms_messaging    │
│ TWILIO_AUTH_TOKEN          │ ✗ Not   │ sms_messaging    │
└────────────────────────────┴─────────┴──────────────────┘

Summary:
  Configured: 2/13
  Missing: 11

Tip: Use 'alignerr env setup' to configure missing variables
```

---

## Benefits

### For Users

✅ **Easy Discovery** - See all available servers  
✅ **Simple Installation** - One command to install  
✅ **Configuration Help** - Guided setup with links  
✅ **Status Visibility** - Know what's configured  
✅ **Quick Setup** - Interactive prompts for credentials  

### For Development

✅ **Standardized** - Consistent approach across all servers  
✅ **Documented** - Built-in help for each variable  
✅ **Automated** - No manual environment file editing  
✅ **Trackable** - Know exactly what's needed  
✅ **Shareable** - Export templates for teams  

---

## Integration Examples

### CI/CD Pipeline

```bash
#!/bin/bash
# Setup script for CI

# Check configuration status
alignerr env status

# Install required servers
alignerr servers install all

# Run validations
alignerr validate --all --parallel 8
```

### Development Setup

```bash
#!/bin/bash
# New developer setup

echo "Setting up Alignerr CLI..."

# Install CLI
pip install -e .

# Show what's needed
alignerr env show

# Interactive setup
alignerr env setup

# Install commonly used servers
alignerr servers install google_search
alignerr servers install weather
alignerr servers install wikipedia

# Verify setup
alignerr env status
alignerr servers list --installed

echo "Setup complete! Try: alignerr validate --domain web_search"
```

---

## Command Reference

### Server Commands

| Command | Description |
|---------|-------------|
| `alignerr servers list` | List all servers with status |
| `alignerr servers list --installed` | List only installed |
| `alignerr servers list --available` | List all available |
| `alignerr servers install <name>` | Install specific server |
| `alignerr servers install all` | Install all servers |
| `alignerr servers install <name> --force` | Force reinstall |
| `alignerr servers uninstall <name>` | Uninstall server |
| `alignerr servers info <name>` | Show server details |

### Environment Commands

| Command | Description |
|---------|-------------|
| `alignerr env status` | Show configuration status |
| `alignerr env setup` | Interactive setup (all) |
| `alignerr env setup --category llm` | Setup LLM providers only |
| `alignerr env setup --category servers` | Setup servers only |
| `alignerr env show` | Show required variables |
| `alignerr env show --category llm` | Show LLM variables |
| `alignerr env export` | Export .env.example |
| `alignerr env export --output <file>` | Export to custom file |

---

## Files Created

1. **`lbx_cli/commands/servers.py`** (290 lines)
   - Server management commands
   - Installation logic
   - Status checking

2. **`lbx_cli/commands/env.py`** (300 lines)
   - Environment variable management
   - Interactive setup
   - Status reporting

3. **`lbx_cli/main.py`** (updated)
   - Integrated new commands
   - Added sub-apps for servers and env

4. **`CLI_ENHANCEMENTS.md`** (this file)
   - Complete documentation

---

## Next Steps

1. **Try the new commands:**
   ```bash
   alignerr env status
   alignerr servers list
   ```

2. **Setup your environment:**
   ```bash
   alignerr env setup
   ```

3. **Install servers:**
   ```bash
   alignerr servers install all
   ```

4. **Validate domains:**
   ```bash
   alignerr validate --domain web_search
   ```

---

**Status**: ✅ **Complete and Ready to Use!**

The CLI now provides comprehensive server management and environment configuration! 🎉

