# UV Setup Guide for Template Repository

## Overview

This template repository is configured to use **UV** (modern Python package manager) for dependency management. Running `uv sync` will automatically install:

✅ **Alignerr CLI** (from git submodule)  
✅ **All CLI dependencies** (including embedded mcpuniverse)  
✅ **Template dependencies**  
✅ **Development tools**  

## Quick Start with UV

### 1. Clone Template with Submodules

```bash
git clone --recurse-submodules https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_mcp_servers_mothership
git clone --recurse-submodules https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_cli
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

### 2. Install Everything with UV

```bash
uv sync
```

This single command:
1. Creates virtual environment (`.venv`)
2. Installs Alignerr CLI from `lbx_mcp_universe_cli/` submodule
3. Installs all CLI dependencies (192 embedded mcpuniverse files + deps)
4. Installs template dependencies
5. Installs development tools (pytest, black, etc.)

### 3. Activate Environment

```bash
source .venv/bin/activate
```

### 4. Verify Installation

```bash
# CLI should be available
alignerr --help

# Check what's installed
alignerr env status
alignerr servers list
```

## How It Works

### pyproject.toml Configuration

The template's `pyproject.toml` includes:

```toml
[project]
dependencies = [
    "alignerr-cli",  # CLI from submodule
    # ... other deps
]

[tool.uv.sources]
alignerr-cli = { path = "lbx_mcp_universe_cli", editable = true }
```

**Key Points:**
- ✅ `alignerr-cli` listed in dependencies
- ✅ `[tool.uv.sources]` points to submodule path
- ✅ `editable = true` allows development

### Dependency Resolution

When you run `uv sync`:

```
1. UV reads pyproject.toml
   ↓
2. Sees alignerr-cli dependency
   ↓
3. Checks [tool.uv.sources]
   ↓
4. Finds path to lbx_mcp_universe_cli/ submodule
   ↓
5. Installs CLI in editable mode
   ↓
6. Reads CLI's pyproject.toml
   ↓
7. Installs all CLI dependencies:
   - Embedded mcpuniverse dependencies
   - LLM providers (OpenAI, Anthropic, etc.)
   - MCP utilities
   - Rich, Typer, etc.
   ↓
8. Installs template dependencies
   ↓
9. Creates/updates uv.lock
```

## Complete Setup Workflow

### New Developer Onboarding

```bash
# 1. Clone with submodules
git clone --recurse-submodules <repo-url>
cd lbx_mcp_universe_template

# 2. Install everything with UV
uv sync

# 3. Activate environment
source .venv/bin/activate

# 4. Setup environment variables
alignerr env setup --category llm

# 5. Install MCP servers
alignerr servers install google_search

# 6. Validate reference example
alignerr validate --domain web_search

# ✅ Ready to develop!
```

### Benefits of UV Approach

✅ **Single Command** - `uv sync` does everything  
✅ **Fast** - UV is extremely fast  
✅ **Reproducible** - `uv.lock` ensures consistency  
✅ **Submodule Support** - Installs from git submodule  
✅ **Editable Install** - CLI changes reflected immediately  
✅ **Virtual Environment** - Automatic `.venv` creation  

## Alternative: Manual Installation

If you prefer not to use UV:

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install CLI from submodule
cd lbx_mcp_universe_cli
pip install -e .
cd ..

# 3. Install template dependencies
pip install -e .

# 4. Install dev dependencies
pip install pytest pytest-asyncio black
```

## Updating Dependencies

### Update CLI

```bash
# Update CLI submodule to latest
git submodule update --remote --merge

# Sync dependencies
uv sync
```

### Update Template Dependencies

```bash
# Edit pyproject.toml
# Then sync
uv sync
```

### Update Lock File

```bash
# After changing dependencies
uv lock

# Then sync
uv sync
```

## Development Workflow

### Making Changes to CLI

Since CLI is installed in editable mode:

```bash
# Edit CLI code
cd lbx_mcp_universe_cli
vim lbx_cli/commands/validate.py

# Changes are immediately available
alignerr validate --help  # Shows updated help

# No need to reinstall!
```

### Adding New Domain

```bash
# Create new domain
alignerr create-domain --name my_domain

# Develop domain
cd domains/my_domain
# Edit tasks, evaluators, config

# Test
alignerr validate --domain my_domain
```

## Project Structure with UV

```
lbx_mcp_universe_template/
├── pyproject.toml              # ✅ Configured for UV
├── uv.lock                     # ✅ Dependency lock file
├── .venv/                      # ✅ Virtual environment (created by UV)
│
├── lbx_mcp_universe_cli/       # Git submodule
│   └── [CLI code]              # Installed in editable mode
│
├── domains/                    # Your domains
│   ├── web_search/             # Reference example
│   └── [your domains]/
│
└── .github/
    └── workflows/
        └── ci.yml              # Can use: uv sync && alignerr validate
```

## CI/CD with UV

### GitHub Actions

```yaml
name: Validate Domains

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive  # Important!
      
      - uses: astral-sh/setup-uv@v1
      
      - name: Install dependencies
        run: uv sync
      
      - name: Setup environment
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          source .venv/bin/activate
          alignerr env status
      
      - name: Install servers
        run: |
          source .venv/bin/activate
          alignerr servers install all
      
      - name: Validate domains
        run: |
          source .venv/bin/activate
          alignerr validate --all --parallel 8
```

## Troubleshooting

### Submodule Not Found

```bash
# Initialize submodules
git submodule update --init --recursive

# Then sync
uv sync
```

### UV Not Found

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### Dependency Conflicts

```bash
# Force reinstall
uv sync --reinstall

# Or clear cache
uv cache clean
uv sync
```

### CLI Not in PATH

```bash
# Ensure venv is activated
source .venv/bin/activate

# Check installation
which alignerr

# Should show: .venv/bin/alignerr
```

## Commands Reference

```bash
# Install/sync everything
uv sync

# Update dependencies
uv sync --upgrade

# Install with dev dependencies
uv sync --extra dev

# Reinstall everything
uv sync --reinstall

# Show installed packages
uv pip list

# Lock dependencies
uv lock

# Export requirements
uv pip compile pyproject.toml -o requirements.txt
```

## Best Practices

### 1. Always Use Submodules

```bash
# Clone with submodules
git clone --recurse-submodules <repo>

# Or initialize after clone
git submodule update --init --recursive
```

### 2. Keep Lock File Updated

```bash
# After changing pyproject.toml
uv lock

# Commit uv.lock
git add uv.lock
git commit -m "Update dependencies"
```

### 3. Use Virtual Environment

```bash
# Always activate before working
source .venv/bin/activate

# Or use uv run
uv run alignerr validate --domain web_search
```

### 4. Update Regularly

```bash
# Update CLI submodule
git submodule update --remote --merge

# Sync dependencies
uv sync
```

## Migration from pip

If you're used to pip:

| pip command | uv equivalent |
|-------------|---------------|
| `pip install -e .` | `uv sync` |
| `pip install package` | `uv add package` |
| `pip install -r requirements.txt` | `uv sync` |
| `pip list` | `uv pip list` |
| `pip freeze` | `uv pip freeze` |

## Summary

✅ **Single Command Setup** - `uv sync` installs everything  
✅ **Submodule Support** - CLI installed from submodule  
✅ **Editable Mode** - CLI changes reflected immediately  
✅ **Fast** - UV is extremely fast  
✅ **Reproducible** - Lock file ensures consistency  
✅ **Simple** - No manual CLI installation needed  

**Just run:** `uv sync` and you're ready to go! 🚀

---

**Next Steps:**
1. Clone template: `git clone --recurse-submodules <repo>`
2. Sync: `uv sync`
3. Activate: `source .venv/bin/activate`
4. Use: `alignerr validate --domain web_search`

