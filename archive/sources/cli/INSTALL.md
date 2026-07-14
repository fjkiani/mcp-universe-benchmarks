# Installation Guide

Quick installation guide for Alignerr CLI.

## Prerequisites

- Python 3.12 or higher
- pip or uv package manager

## Installation Steps

### 1. Navigate to CLI Directory

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_cli
```

### 2. Install in Development Mode

Using pip:

```bash
pip install -e .
```

Or using uv:

```bash
uv pip install -e .
```

### 3. Verify Installation

```bash
alignerr --help
```

You should see:

```
Usage: alignerr [OPTIONS] COMMAND [ARGS]...

  🎯 Alignerr - Universal CLI for LBX MCP Universe

  A powerful CLI tool for managing, validating, and running
  MCP benchmark domains locally...
```

## Quick Test

### List Available Commands

```bash
alignerr --help
```

### Check Configuration

```bash
alignerr config
```

### List Domains (will be empty initially)

```bash
alignerr list
```

## First Domain Setup

### Option 1: Migrate from lbx-mcp-envs

If you have lbx-mcp-envs installed:

```bash
alignerr migrate --source /path/to/lbx-mcp-envs
```

### Option 2: Create New Domain

```bash
alignerr create-domain --name test_domain
```

### Verify Domain Was Created

```bash
alignerr list
```

## Configuration

### Set Environment Variables (Optional)

```bash
export ALIGNERR_DOMAINS_ROOT=/path/to/domains
export ALIGNERR_MCPUNIVERSE_PATH=/path/to/lbx-mcp-envs
export ALIGNERR_DEFAULT_MODEL=openai/gpt-4o
export ALIGNERR_MAX_WORKERS=8
```

### Add to Shell Profile (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Alignerr Configuration
export ALIGNERR_DOMAINS_ROOT="$HOME/alignerr/domains"
export ALIGNERR_OUTPUT_DIR="$HOME/alignerr/reports"
export ALIGNERR_DEFAULT_MODEL="openai/gpt-4o"
export ALIGNERR_MAX_WORKERS=8

# Alignerr Aliases (optional)
alias av='alignerr validate'
alias al='alignerr list'
alias ai='alignerr info'
alias am='alignerr migrate'
```

Then reload:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

## Troubleshooting

### Command Not Found

If `alignerr` command is not found after installation:

```bash
# Check if package is installed
pip list | grep alignerr

# Reinstall
pip install -e . --force-reinstall

# Or check Python path
which python
python -m lbx_cli.main --help
```

### Import Errors

If you get import errors:

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Or install again
pip install -e .
```

### Permission Errors

If you get permission errors:

```bash
# Use user installation
pip install -e . --user

# Or use a virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Uninstallation

To uninstall:

```bash
pip uninstall alignerr-cli
```

## Next Steps

After installation:

1. Read the [Quick Start Guide](QUICKSTART.md)
2. Check out [Examples](EXAMPLES.md)
3. Read the full [README](README.md)

## Support

For issues:
- Check [Troubleshooting](#troubleshooting) section above
- Check the full [README](README.md)
- Create an issue in the repository

