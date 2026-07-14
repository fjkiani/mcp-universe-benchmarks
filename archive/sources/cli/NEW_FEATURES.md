# 🆕 New Features: Server & Environment Management

## Overview

Two powerful new command groups have been added to Alignerr CLI:

1. **`alignerr servers`** - Complete MCP server lifecycle management
2. **`alignerr env`** - Environment variable and credential management

---

## 🔌 Server Management Commands

### `alignerr servers list`

List all available MCP servers with installation status.

```bash
# List all servers
alignerr servers list

# List only installed
alignerr servers list --installed

# List all available
alignerr servers list --available
```

**Output:**
```
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Server             ┃ Status      ┃ Path                       ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ google_search      │ ✓ Installed │ lbx_cli/mcp_servers/...    │
│ weather            │ ○ Available │ lbx_cli/mcp_servers/...    │
│ wikipedia          │ ○ Available │ lbx_cli/mcp_servers/...    │
└────────────────────┴─────────────┴────────────────────────────┘

Total: 27 servers
Installed: 1
Available: 26
```

---

### `alignerr servers install`

Install one or all MCP servers.

```bash
# Install specific server
alignerr servers install google_search

# Install all servers at once
alignerr servers install all

# Force reinstall
alignerr servers install google_search --force
```

**What it does:**
1. Locates server in `lbx_cli/mcp_servers/servers/`
2. Runs `pip install -e <server_path>`
3. Verifies installation
4. Reports success/failure

**Output:**
```
Installing google_search...
✓ google_search installed successfully

Installation Summary
════════════════════════════════════════
Successful: 1
Failed: 0
```

---

### `alignerr servers uninstall`

Remove an installed server.

```bash
alignerr servers uninstall google_search
```

---

### `alignerr servers info`

Show detailed information about a server.

```bash
alignerr servers info google_search
```

**Output:**
```
╭─ Server: google_search ──────────────────────╮
│ google_search                                 │
│                                               │
│ Status: ✓ Installed                           │
│ Path: lbx_cli/mcp_servers/servers/google...  │
│                                               │
│ Description:                                  │
│ # Google Search MCP Server                    │
│                                               │
│ MCP server providing Google search...         │
╰───────────────────────────────────────────────╯

To install:
  alignerr servers install google_search

To run:
  python -m google_search
```

---

## 🔐 Environment Management Commands

### `alignerr env status`

**The most important new command** - shows what's configured and what's missing.

```bash
alignerr env status
```

**Output:**
```
╭─ Environment Configuration Status ─╮
│                                    │
╰────────────────────────────────────╯

LLM Providers:
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Variable           ┃ Status  ┃ Required For          ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ OPENAI_API_KEY     │ ✓ Set   │ OpenAI LLM provider   │
│ ANTHROPIC_API_KEY  │ ✓ Set   │ Anthropic LLM...      │
│ GEMINI_API_KEY     │ ✗ Not   │ Gemini LLM provider   │
│ XAI_API_KEY        │ ✗ Not   │ Grok LLM provider     │
│ MISTRAL_API_KEY    │ ✗ Not   │ Mistral LLM provider  │
└────────────────────┴─────────┴───────────────────────┘

MCP Server Credentials:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Variable                   ┃ Status  ┃ Required For     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ SERP_API_KEY               │ ✓ Set   │ google_search... │
│ OPENWEATHER_API_KEY        │ ✗ Not   │ weather server   │
│ GOOGLE_MAPS_API_KEY        │ ✗ Not   │ Google Maps...   │
│ GITHUB_PERSONAL_ACCESS_... │ ✗ Not   │ GitHub...        │
│ NOTION_API_KEY             │ ✗ Not   │ Notion...        │
│ STRIPE_API_KEY             │ ✗ Not   │ stripe_payments  │
│ TWILIO_ACCOUNT_SID         │ ✗ Not   │ sms_messaging    │
│ TWILIO_AUTH_TOKEN          │ ✗ Not   │ sms_messaging    │
└────────────────────────────┴─────────┴──────────────────┘

Summary:
  Configured: 2/13
  Missing: 11

Tip: Use 'alignerr env setup' to configure missing variables
```

**Benefits:**
- ✅ See at a glance what's configured
- ✅ Know exactly what's missing
- ✅ Understand what each variable is for
- ✅ Get help on next steps

---

### `alignerr env setup`

Interactive wizard for setting up environment variables.

```bash
# Setup all variables
alignerr env setup

# Setup only LLM providers
alignerr env setup --category llm

# Setup only MCP servers
alignerr env setup --category servers

# Non-interactive mode
alignerr env setup --no-interactive
```

**Interactive Flow:**
```
Environment Setup

Configuration will be saved to: ~/.alignerr/.env

LLM
──────────────────────────────────────────────────

OPENAI_API_KEY
  OpenAI API key for GPT models
  Required for: OpenAI LLM provider
  Get it at: https://platform.openai.com/api-keys
  Enter value for OPENAI_API_KEY: ********
  ✓ OPENAI_API_KEY updated

ANTHROPIC_API_KEY
  Anthropic API key for Claude models
  Required for: Anthropic LLM provider
  Get it at: https://console.anthropic.com/
  Current: sk-ant-api03-...
  Update ANTHROPIC_API_KEY? [y/N]: n

[... continues for all variables ...]

✓ Configuration saved to ~/.alignerr/.env

To use these variables:
  source ~/.alignerr/.env
  Or add to your shell profile (~/.bashrc or ~/.zshrc)
```

**Features:**
- ✅ Password-masked input (secure)
- ✅ Shows current values
- ✅ Option to skip/update existing
- ✅ Helpful links to get API keys
- ✅ Persistent storage
- ✅ Categorized (LLM vs Servers)

---

### `alignerr env show`

Display all required environment variables and where to get them.

```bash
# Show all
alignerr env show

# Show only LLM variables
alignerr env show --category llm

# Show only server variables
alignerr env show --category servers
```

**Output:**
```
LLM
════════════════════════════════════════════════════════════

OPENAI_API_KEY
  Description: OpenAI API key for GPT models
  Required for: OpenAI LLM provider
  Get it at: https://platform.openai.com/api-keys

ANTHROPIC_API_KEY
  Description: Anthropic API key for Claude models
  Required for: Anthropic LLM provider
  Get it at: https://console.anthropic.com/

[... continues for all variables ...]
```

**Use Case:** Reference guide when setting up manually

---

### `alignerr env export`

Export a template `.env` file for sharing with team.

```bash
# Export to default location (.env.example)
alignerr env export

# Export to custom file
alignerr env export --output team.env.template
```

**Generated File:**
```bash
# Alignerr Environment Variables Template
# Copy this file to .env and fill in your actual values

# LLM
# OpenAI API key for GPT models
# Get it at: https://platform.openai.com/api-keys
OPENAI_API_KEY=

# Anthropic API key for Claude models
# Get it at: https://console.anthropic.com/
ANTHROPIC_API_KEY=

[... all variables with comments ...]
```

**Use Case:** Share with team, check into git as .env.example

---

## 📋 Complete Workflow Examples

### New Developer Onboarding

```bash
# 1. Clone and install
git clone <repo>
cd lbx_mcp_universe_cli
pip install -e .

# 2. Check what's needed
alignerr env status
alignerr servers list

# 3. Interactive setup
alignerr env setup

# 4. Install servers
alignerr servers install all

# 5. Verify everything
alignerr env status
alignerr servers list --installed

# 6. Ready to go!
alignerr validate --domain web_search
```

### Before Running Validation

```bash
# Always check first
alignerr env status
alignerr servers list --installed

# Install missing servers
alignerr servers install google_search

# Then validate
alignerr validate --domain web_search
```

### Team Setup

```bash
# Team lead exports template
alignerr env export --output .env.example
git add .env.example
git commit -m "Add environment template"
git push

# Team members clone and setup
git clone <repo>
cd lbx_mcp_universe_cli
pip install -e .
cp .env.example .env
# Edit .env with actual API keys
alignerr env status  # Verify
alignerr servers install all
```

### CI/CD Pipeline

```bash
#!/bin/bash
# CI setup script

# Check configuration
alignerr env status || exit 1

# Verify required vars are set
if [ -z "$OPENAI_API_KEY" ]; then
  echo "OPENAI_API_KEY not set"
  exit 1
fi

# Install servers
alignerr servers install all

# Run validations
alignerr validate --all --parallel 8 --no-callbacks
```

---

## 🎯 Environment Variables Managed

### LLM Providers (5 variables)

| Variable | Provider | Get API Key |
|----------|----------|-------------|
| `OPENAI_API_KEY` | OpenAI GPT | https://platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | Anthropic Claude | https://console.anthropic.com/ |
| `GEMINI_API_KEY` | Google Gemini | https://makersuite.google.com/app/apikey |
| `XAI_API_KEY` | xAI Grok | https://x.ai/ |
| `MISTRAL_API_KEY` | Mistral | https://console.mistral.ai/ |

### MCP Server Credentials (8 variables)

| Variable | Service | Get API Key |
|----------|---------|-------------|
| `SERP_API_KEY` | Google Search | https://serpapi.com/ |
| `OPENWEATHER_API_KEY` | Weather Data | https://openweathermap.org/api |
| `GOOGLE_MAPS_API_KEY` | Google Maps | https://console.cloud.google.com/google/maps-apis/credentials |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub | https://github.com/settings/tokens |
| `NOTION_API_KEY` | Notion | https://developers.notion.com/ |
| `STRIPE_API_KEY` | Stripe Payments | https://dashboard.stripe.com/apikeys |
| `TWILIO_ACCOUNT_SID` | Twilio SMS | https://console.twilio.com/ |
| `TWILIO_AUTH_TOKEN` | Twilio SMS | https://console.twilio.com/ |

---

## 🎨 Command Examples

### Server Management

```bash
# Discovery
alignerr servers list
# Output: Table showing all 27 servers with status

# Installation
alignerr servers install google_search weather wikipedia
# Output: Progress and success/failure for each

# Bulk Install
alignerr servers install all
# Output: Installs all 27 servers with progress

# Check Installation
alignerr servers list --installed
# Output: Only shows installed servers

# Server Details
alignerr servers info google_search
# Output: Description, status, installation commands
```

### Environment Management

```bash
# Status Check (Most Useful!)
alignerr env status
# Output: Tables showing what's set and what's missing

# Interactive Setup
alignerr env setup
# Output: Guided wizard with prompts for each variable

# Quick LLM Setup
alignerr env setup --category llm
# Output: Only prompts for LLM provider keys

# Reference Guide
alignerr env show
# Output: All variables with descriptions and URLs

# Team Template
alignerr env export --output .env.example
# Output: Template file with comments
```

---

## 💡 Use Cases

### Use Case 1: "What do I need to get started?"

```bash
alignerr env status
```

Instantly shows:
- Which LLM providers you can use
- Which MCP servers you can use
- What's missing
- Percentage configured

### Use Case 2: "Install everything I need"

```bash
# Check what's needed
alignerr env status

# Setup environment
alignerr env setup --category llm

# Install all servers
alignerr servers install all

# Verify
alignerr env status
alignerr servers list --installed
```

### Use Case 3: "Which servers are available?"

```bash
alignerr servers list
```

Shows all 27 servers with installation status.

### Use Case 4: "Help new team member setup"

```bash
# 1. Create template
alignerr env export --output .env.example

# 2. Team member copies and edits
cp .env.example .env
vim .env  # Add real API keys

# 3. Verify setup
alignerr env status

# 4. Install servers
alignerr servers install all
```

---

## 🔍 Status Command Details

### What Gets Checked

#### LLM Providers
- ✅ OPENAI_API_KEY
- ✅ ANTHROPIC_API_KEY
- ✅ GEMINI_API_KEY
- ✅ XAI_API_KEY
- ✅ MISTRAL_API_KEY

#### MCP Servers
- ✅ SERP_API_KEY (google_search)
- ✅ OPENWEATHER_API_KEY (weather)
- ✅ GOOGLE_MAPS_API_KEY (maps)
- ✅ GITHUB_PERSONAL_ACCESS_TOKEN (github)
- ✅ NOTION_API_KEY (notion)
- ✅ STRIPE_API_KEY (stripe_payments)
- ✅ TWILIO_ACCOUNT_SID (sms_messaging)
- ✅ TWILIO_AUTH_TOKEN (sms_messaging)

### Status Indicators

- **✓ Set** (Green) - Variable is configured
- **✗ Not Set** (Red) - Variable is missing

### Summary Metrics

- **Configured:** Count of set variables
- **Missing:** Count of unset variables
- **Percentage:** Configuration completeness

---

## 📂 Configuration Storage

### Location

```
~/.alignerr/
├── .env              # Environment variables
└── config.json       # CLI configuration
```

### .env File Structure

```bash
# Alignerr Environment Configuration
# Generated by alignerr env setup

# LLM
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=...
XAI_API_KEY=...
MISTRAL_API_KEY=...

# SERVERS
SERP_API_KEY=...
OPENWEATHER_API_KEY=...
GOOGLE_MAPS_API_KEY=...
GITHUB_PERSONAL_ACCESS_TOKEN=...
NOTION_API_KEY=...
STRIPE_API_KEY=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
```

### Loading Variables

```bash
# Load in current shell
source ~/.alignerr/.env

# Or add to shell profile
echo "source ~/.alignerr/.env" >> ~/.bashrc
```

---

## 🎯 Integration with Existing Commands

### Before Validation

```bash
# Check everything is ready
alignerr env status           # Check API keys
alignerr servers list --installed  # Check servers
alignerr list                # Check domains

# Then validate
alignerr validate --domain web_search
```

### Before Migration

```bash
# Ensure environment is ready
alignerr env setup --category llm

# Then migrate
alignerr migrate --source ../lbx-mcp-envs
```

---

## 🚀 Benefits

### For Users

✅ **Visibility** - Know exactly what's configured  
✅ **Guidance** - Links to get API keys  
✅ **Simplicity** - One command to setup everything  
✅ **Safety** - Password-masked input  
✅ **Persistence** - Configuration saved automatically  

### For Teams

✅ **Onboarding** - Easy new developer setup  
✅ **Templates** - Share .env.example  
✅ **Consistency** - Everyone has same setup  
✅ **Documentation** - Self-documenting via status command  

### For DevOps

✅ **CI/CD Ready** - Check configuration status  
✅ **Automation** - Non-interactive mode  
✅ **Validation** - Verify before running  
✅ **Visibility** - Know what's missing  

---

## 📊 Command Comparison

### Old Way (Manual)

```bash
# Had to manually:
1. Read documentation to find what variables needed
2. Create .env file manually
3. Add each variable one by one
4. No way to know what's missing
5. No way to see status
6. Hope everything works
```

### New Way (Alignerr)

```bash
# Simple workflow:
1. alignerr env status        # See what's needed
2. alignerr env setup         # Interactive wizard
3. alignerr env status        # Verify configured
4. alignerr servers install all  # Install servers
5. alignerr validate ...      # Run with confidence
```

---

## 🔧 Technical Details

### Files Created

1. **`lbx_cli/commands/servers.py`** (290 lines)
   - Server lifecycle management
   - Installation logic
   - Status checking
   - Server information display

2. **`lbx_cli/commands/env.py`** (300 lines)
   - Environment variable definitions
   - Interactive setup wizard
   - Status reporting
   - Template export

3. **Updated `lbx_cli/main.py`** (+70 lines)
   - Integrated new command groups
   - Added sub-apps for servers and env

### Environment Variable Registry

Centralized registry in `env.py`:

```python
ENV_REQUIREMENTS = {
    "llm": {
        "OPENAI_API_KEY": {
            "description": "...",
            "required_for": ["..."],
            "get_url": "...",
        },
        # ... more LLM variables
    },
    "servers": {
        "SERP_API_KEY": {
            "description": "...",
            "required_for": ["..."],
            "get_url": "...",
        },
        # ... more server variables
    },
}
```

**Benefits:**
- Single source of truth
- Easy to extend
- Self-documenting
- Categorized

---

## ✅ Quick Reference

### Essential Commands

```bash
# Check Status (Most Important!)
alignerr env status

# Setup Everything
alignerr env setup

# Install Servers
alignerr servers install all

# List What's Available
alignerr servers list
alignerr list

# Get Help
alignerr servers --help
alignerr env --help
```

### Before Validation Checklist

```bash
✓ alignerr env status              # All required vars set?
✓ alignerr servers list --installed # Required servers installed?
✓ alignerr list                    # Domain exists?
✓ alignerr validate --domain <name> # Run validation
```

---

## 🎊 Summary

Two powerful new command groups:

**1. `alignerr servers`** - Server Management
- list, install, uninstall, info
- Manages all 27 MCP servers
- Visual status indicators
- Batch operations

**2. `alignerr env`** - Environment Management
- status, setup, show, export
- Manages 13 environment variables
- Interactive wizard
- Status dashboard

**Result:** Complete visibility and control over configuration!

---

**Try it now:**
```bash
alignerr env status
alignerr servers list
```

🎉 **Makes setup and configuration easy!**

