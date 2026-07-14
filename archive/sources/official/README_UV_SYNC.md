# Single Command Setup with UV Sync

## Overview

This template repository is configured so that **a single `uv sync` command** installs everything you need:

✅ Alignerr CLI (from git submodule)  
✅ All CLI dependencies (embedded mcpuniverse, LLM providers, etc.)  
✅ Template dependencies  
✅ Development tools  

## Quick Start

```bash
# 1. Clone with submodules
git clone --recurse-submodules <your-repo-url>
cd lbx_mcp_universe_template

# 2. One command to install everything
uv sync

# 3. Activate environment
source .venv/bin/activate

# 4. Verify
alignerr --help
alignerr env status

# ✅ Ready to use!
```

## What Gets Installed

When you run `uv sync`:

### 1. Alignerr CLI (from submodule)
- Source: `lbx_mcp_universe_cli/` (git submodule)
- Mode: Editable installation
- Result: `alignerr` command available

### 2. Embedded MCPUniverse (192 files)
- Agents, LLMs, MCP system
- Benchmark runner
- Evaluators, tracers
- Workflows, callbacks
- All automatically included with CLI

### 3. All Dependencies
- LLM providers: OpenAI, Anthropic, Gemini, Mistral, xAI
- MCP utilities: mcp>=1.9.4, httpx, anyio
- CLI tools: typer, rich, click
- Core libraries: pydantic, pyyaml, requests
- Google services, Playwright, yfinance, etc.

### 4. Development Tools (with --extra dev)
- pytest, pytest-asyncio
- black (code formatter)

## Configuration

The magic happens in `pyproject.toml`:

```toml
[project]
dependencies = [
    "alignerr-cli",  # Declares CLI as dependency
    # ... other deps
]

[tool.uv.sources]
# Tells UV to install CLI from submodule path
alignerr-cli = { path = "lbx_mcp_universe_cli", editable = true }
```

**Key Features:**
- `path = "lbx_mcp_universe_cli"` - Points to submodule
- `editable = true` - Installs in development mode
- UV automatically handles the submodule

## Step-by-Step Workflow

### First Time Setup

```bash
# Clone repository
git clone --recurse-submodules <repo-url>
cd lbx_mcp_universe_template

# Install everything (this may take 1-2 minutes)
uv sync

# Activate virtual environment
source .venv/bin/activate

# Verify CLI is installed
alignerr --version
alignerr --help

# Check environment
alignerr env status

# Setup API keys
alignerr env setup --category llm

# Install MCP servers
alignerr servers install google_search

# Validate reference example
alignerr validate --domain web_search
```

### Daily Development

```bash
# Activate environment
source .venv/bin/activate

# Work on your domain
cd domains/my_domain
vim tasks/task_0001.json

# Validate
alignerr validate --domain my_domain

# Update CLI if needed
git submodule update --remote --merge
uv sync
```

## Benefits

### ✅ Single Command Installation

**Before:**
```bash
# Multiple steps
cd lbx_mcp_universe_cli
pip install -e .
cd ..
pip install -e .
pip install pytest black
```

**After:**
```bash
# One step!
uv sync
```

### ✅ Reproducible Builds

`uv.lock` ensures everyone gets the same dependencies:

```bash
# First developer
uv sync
# Creates uv.lock

# Second developer
git pull
uv sync
# Gets exact same versions from uv.lock
```

### ✅ Fast Installation

UV is **10-100x faster** than pip:

```
pip install:  60-120 seconds
uv sync:      5-10 seconds
```

### ✅ Automatic Submodule Handling

UV understands the submodule relationship:

```bash
# UV automatically:
1. Finds lbx_mcp_universe_cli/ submodule
2. Reads its pyproject.toml
3. Installs it in editable mode
4. Installs all its dependencies
5. Makes alignerr command available
```

## Advanced Usage

### Install with Development Tools

```bash
uv sync --extra dev
```

Installs: pytest, pytest-asyncio, black

### Update All Dependencies

```bash
uv sync --upgrade
```

Updates all packages to latest compatible versions.

### Reinstall Everything

```bash
uv sync --reinstall
```

Useful if something went wrong.

### Run Commands Without Activating

```bash
# Use uv run to execute in venv
uv run alignerr validate --domain web_search

# No need to activate!
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Validate

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
      
      - uses: astral-sh/setup-uv@v1
      
      - name: Install dependencies
        run: uv sync
      
      - name: Validate domains
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          source .venv/bin/activate
          alignerr validate --all --parallel 8
```

**Benefits:**
- Fast CI builds
- Reproducible
- Single command

## Submodule Management

### Initialize Submodules

If not cloned with `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

### Update CLI Submodule

```bash
# Get latest CLI
git submodule update --remote --merge

# Sync dependencies (in case CLI deps changed)
uv sync

# Commit updated submodule
git add lbx_mcp_universe_cli
git commit -m "Update CLI to latest"
```

### Check Submodule Status

```bash
git submodule status
# Should show: <commit> lbx_mcp_universe_cli (heads/main)
```

## Troubleshooting

### Submodule Empty

```bash
# Submodule not initialized
git submodule update --init --recursive

# Then sync
uv sync
```

### UV Command Not Found

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### alignerr Command Not Found

```bash
# Ensure venv is activated
source .venv/bin/activate

# Or use uv run
uv run alignerr --help

# If still not found, reinstall
uv sync --reinstall
```

### Import Errors

```bash
# Reinstall with force
uv sync --reinstall

# Or manually install CLI
cd lbx_mcp_universe_cli
pip install -e .
```

## Comparison: pip vs UV

| Aspect | pip | UV |
|--------|-----|-----|
| Install Speed | 60-120s | 5-10s |
| Lock File | requirements.txt | uv.lock |
| Submodule Support | Manual | Automatic |
| Reproducibility | Good | Excellent |
| Venv Creation | Manual | Automatic |

## Files Involved

```
lbx_mcp_universe_template/
├── pyproject.toml          # Defines dependencies & UV sources
├── uv.lock                 # Lock file (auto-generated)
├── .venv/                  # Virtual environment (auto-created)
│
├── lbx_mcp_universe_cli/   # Git submodule
│   ├── pyproject.toml      # CLI dependencies
│   └── lbx_cli/            # CLI code
│       ├── mcpuniverse/    # Embedded (192 files)
│       └── mcp_servers/    # Symlink to mothership
│
└── domains/                # Your domains
    └── web_search/         # Reference example
```

## What UV Sync Does

```
$ uv sync

1. ✅ Creates .venv/ if not exists
2. ✅ Reads pyproject.toml
3. ✅ Finds alignerr-cli dependency
4. ✅ Checks [tool.uv.sources] for path
5. ✅ Installs CLI from lbx_mcp_universe_cli/ (editable)
6. ✅ Reads CLI's pyproject.toml
7. ✅ Installs all CLI dependencies:
   - Embedded mcpuniverse dependencies
   - LLM providers
   - MCP utilities
   - Rich, Typer, etc.
8. ✅ Installs template dependencies
9. ✅ Creates/updates uv.lock
10. ✅ Makes alignerr command available

Total time: ~5-10 seconds
```

## Best Practices

### 1. Always Clone with Submodules

```bash
git clone --recurse-submodules <repo>
```

### 2. Use UV Sync After Pulling

```bash
git pull
git submodule update --remote --merge
uv sync  # Ensure dependencies up to date
```

### 3. Commit Lock File

```bash
git add uv.lock
git commit -m "Update dependencies"
```

### 4. Use uv run for Scripts

```bash
# Instead of activating, use uv run
uv run alignerr validate --domain web_search
```

## Summary

✅ **One Command**: `uv sync` does everything  
✅ **Fast**: 10-100x faster than pip  
✅ **Simple**: No manual CLI installation  
✅ **Reproducible**: Lock file ensures consistency  
✅ **Automatic**: Handles submodules automatically  
✅ **CI/CD Ready**: Perfect for GitHub Actions  

**Just run `uv sync` and start developing!** 🚀

---

**Installation:**
```bash
git clone --recurse-submodules <repo>
cd lbx_mcp_universe_template
uv sync
source .venv/bin/activate
alignerr --help
```

Done! 🎉

