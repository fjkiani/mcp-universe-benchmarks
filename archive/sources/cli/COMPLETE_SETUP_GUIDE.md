# Complete Setup Guide for Alignerr CLI

## Overview

This guide walks you through the complete setup of Alignerr CLI, from installation to running your first validation.

---

## Step 1: Installation

### 1.1 Navigate to CLI Directory

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_cli
```

### 1.2 Install Dependencies

```bash
pip install -e .
```

This installs:
- ✅ CLI commands
- ✅ Embedded mcpuniverse (192 files)
- ✅ All LLM providers
- ✅ All MCP utilities
- ✅ All dependencies

**Expected output:**
```
Successfully installed alignerr-cli-0.1.0
```

### 1.3 Verify Installation

```bash
alignerr --help
```

You should see the main help menu with all available commands.

---

## Step 2: Environment Configuration

### 2.1 Check Current Status

```bash
alignerr env status
```

This shows which API keys are configured and which are missing.

### 2.2 Interactive Setup

```bash
alignerr env setup
```

This will guide you through setting up:
- LLM provider API keys (OpenAI, Anthropic, Gemini, etc.)
- MCP server credentials (SerpAPI, Weather API, etc.)

**Interactive prompts:**
```
OPENAI_API_KEY
  OpenAI API key for GPT models
  Required for: OpenAI LLM provider
  Get it at: https://platform.openai.com/api-keys
  Enter value for OPENAI_API_KEY: ********

ANTHROPIC_API_KEY
  Anthropic API key for Claude models
  Required for: Anthropic LLM provider
  Get it at: https://console.anthropic.com/
  Enter value for ANTHROPIC_API_KEY: ********
```

### 2.3 Setup Only LLM Providers (Minimal)

For quick start, setup only LLM providers:

```bash
alignerr env setup --category llm
```

This is sufficient for basic validation.

### 2.4 Load Environment Variables

```bash
# Load into current shell
source ~/.alignerr/.env

# Or add to your shell profile
echo "source ~/.alignerr/.env" >> ~/.bashrc
# or
echo "source ~/.alignerr/.env" >> ~/.zshrc
```

### 2.5 Verify Configuration

```bash
alignerr env status
```

Should now show configured items with ✓.

---

## Step 3: MCP Server Installation

### 3.1 List Available Servers

```bash
alignerr servers list
```

Shows all 27 available MCP servers.

### 3.2 Install Required Servers

For web_search domain, you need:

```bash
alignerr servers install google_search
```

For other domains, install as needed:

```bash
# Weather domain
alignerr servers install weather

# Wikipedia domain
alignerr servers install wikipedia

# Financial analysis
alignerr servers install yahoo_finance

# Or install all at once
alignerr servers install all
```

### 3.3 Verify Installation

```bash
alignerr servers list --installed
```

Shows only installed servers with ✓.

---

## Step 4: Migrate Domains (If Using lbx-mcp-envs)

### 4.1 Migrate All Domains

```bash
alignerr migrate --source /Users/manuaero/projects/mcp_arena/lbx-mcp-envs
```

This converts the convoluted test structure into clean, self-contained domains.

**Expected output:**
```
Migrating 8 domain(s) from lbx-mcp-envs
✓ web_search (50 tasks)
✓ browser_automation (30 tasks)
✓ financial_analysis (25 tasks)
...

MIGRATION SUMMARY
✓ Migrated: 8
⊘ Skipped: 0
✗ Failed: 0
```

### 4.2 Verify Migrated Domains

```bash
alignerr list --details
```

Should show all migrated domains with task counts.

---

## Step 5: Run Your First Validation

### 5.1 Check What You Have

```bash
# Check configuration
alignerr env status

# Check installed servers
alignerr servers list --installed

# Check available domains
alignerr list
```

### 5.2 Run Simple Validation

```bash
alignerr validate --domain web_search --model openai/gpt-4o
```

### 5.3 View Results

Reports are generated in `./reports/`:

```bash
ls -la reports/
```

You'll see:
- `*__report.yaml` - Detailed benchmark results
- `*__benchmark.log` - Execution logs

---

## Step 6: Advanced Usage

### 6.1 Parallel Validation

```bash
# Validate all domains with 8 workers
alignerr validate --all --parallel 8
```

### 6.2 Pass@k Validation

```bash
# Test with multiple models, 3 runs each
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5
```

### 6.3 Create New Domain

```bash
# Create new domain
alignerr create-domain --name sentiment_analysis

# Edit domain files
cd domains/sentiment_analysis
vim tasks/task_0001.json
vim evaluators/functions.py
vim config.yaml

# Validate
alignerr validate --domain sentiment_analysis
```

---

## Complete Workflow Example

### New Developer Setup

```bash
#!/bin/bash
# Complete setup script

echo "🚀 Setting up Alignerr CLI..."

# Step 1: Install CLI
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_cli
pip install -e .

# Step 2: Check environment status
echo "\n📊 Checking environment status..."
alignerr env status

# Step 3: Setup environment variables
echo "\n🔐 Setting up environment variables..."
alignerr env setup --category llm

# Step 4: Install core MCP servers
echo "\n📥 Installing MCP servers..."
alignerr servers install google_search
alignerr servers install weather
alignerr servers install wikipedia

# Step 5: Migrate domains (if you have lbx-mcp-envs)
echo "\n🔄 Migrating domains..."
alignerr migrate --source ../lbx-mcp-envs

# Step 6: List domains
echo "\n📋 Available domains:"
alignerr list --details

# Step 7: Verify everything is ready
echo "\n✅ Verification:"
alignerr env status
alignerr servers list --installed
alignerr config

echo "\n🎉 Setup complete!"
echo "\n📚 Try these commands:"
echo "  alignerr validate --domain web_search"
echo "  alignerr validate --all --parallel 8"
```

---

## Troubleshooting

### Issue: Module 'rich' not found

```bash
# Dependencies not installed
pip install -e . --force-reinstall
```

### Issue: Server installation fails

```bash
# Check server exists
alignerr servers list

# Try force reinstall
alignerr servers install google_search --force

# Check server path
ls lbx_cli/mcp_servers/servers/google_search/
```

### Issue: Environment variables not working

```bash
# Check status
alignerr env status

# Re-run setup
alignerr env setup

# Load into shell
source ~/.alignerr/.env

# Verify
echo $OPENAI_API_KEY
```

### Issue: Validation fails

```bash
# Check configuration
alignerr env status

# Check servers installed
alignerr servers list --installed

# Check domain exists
alignerr list

# Get domain info
alignerr info --domain web_search

# Run with verbose output
alignerr validate --domain web_search
```

---

## Quick Reference

### Essential Commands

```bash
# Installation
pip install -e .

# Environment
alignerr env status              # Check config
alignerr env setup               # Interactive setup
alignerr env show                # Show requirements

# Servers
alignerr servers list            # List all servers
alignerr servers install all     # Install all
alignerr servers install <name>  # Install specific

# Domains
alignerr list                    # List domains
alignerr info --domain <name>    # Domain details
alignerr migrate --source <path> # Migrate from legacy

# Validation
alignerr validate --domain <name>        # Single domain
alignerr validate --all --parallel 8     # All domains
alignerr validate --domain <name> --runs 3  # Pass@k

# Configuration
alignerr config                  # Show config
```

### Configuration Files

```bash
~/.alignerr/.env                 # Environment variables
~/.alignerr/config.json          # Alignerr config
./domains/                       # Domain definitions
./reports/                       # Validation reports
```

### Directory Structure

```bash
lbx_mcp_universe_cli/
├── lbx_cli/
│   ├── mcpuniverse/            # Embedded (192 files)
│   └── mcp_servers/            # Symlink to mothership
│       └── servers/            # 27 MCP servers
└── domains/                     # Your domains (after migration)
```

---

## Next Steps

After completing this guide:

1. ✅ CLI installed and working
2. ✅ Environment configured
3. ✅ Servers installed
4. ✅ Domains migrated
5. ✅ Ready to validate!

Try:
```bash
alignerr validate --domain web_search
```

For more examples, see [EXAMPLES.md](EXAMPLES.md)

---

**Setup Status**: ✅ **Complete!**

You're now ready to use Alignerr CLI for MCP benchmark validation! 🎉

