# Command Name Updated: alignerr → alignerr_mcp

## Changes Made

The CLI has been updated to use **`alignerr_mcp`** as the primary command name, with **`alignerr`** kept as an alias for backward compatibility.

### Updated Files

#### 1. `pyproject.toml`

```toml
[project.scripts]
alignerr_mcp = "lbx_cli.main:app"  # Primary command
alignerr = "lbx_cli.main:app"      # Alias for backward compatibility
```

#### 2. `lbx_cli/main.py`

```python
app = typer.Typer(
    name="alignerr_mcp",  # Updated from "alignerr"
    help="🎯 Alignerr MCP - Universal CLI for LBX MCP Universe benchmarks",
    add_completion=False,
)
```

## Usage

Both command names work identically:

### Primary Command: alignerr_mcp

```bash
# Check help
alignerr_mcp --help

# Environment status
alignerr_mcp env status

# Server management
alignerr_mcp servers list

# Validate domains
alignerr_mcp validate --domain web_search

# All other commands
alignerr_mcp migrate --source ../lbx-mcp-envs
alignerr_mcp create-domain --name my_domain
alignerr_mcp list --details
```

### Alias: alignerr (for backward compatibility)

```bash
# Also works
alignerr --help
alignerr env status
alignerr validate --domain web_search
```

## Installation

After updating, reinstall the CLI:

### Using pip

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_cli
pip install -e .
```

### Using uv

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_cli
uv pip install -e .
```

### From template repository

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_template
uv sync
source .venv/bin/activate
alignerr_mcp --help
```

## Verification

Test that both commands work:

```bash
# Test primary command
alignerr_mcp --help
alignerr_mcp env status
alignerr_mcp servers list

# Test alias
alignerr --help
alignerr env status
```

Both should produce identical output.

## Documentation Updates Needed

The following documentation references should be updated (can be done gradually):

### Priority Updates
- ✅ `pyproject.toml` - Updated
- ✅ `lbx_cli/main.py` - Updated
- ⏳ README.md - Update examples
- ⏳ QUICKSTART.md - Update commands
- ⏳ EXAMPLES.md - Update examples

### Optional Updates
- Documentation files can show both forms: `alignerr_mcp` or `alignerr`
- Examples can use `alignerr_mcp` as primary with note about `alignerr` alias

## Command Reference (Updated)

All commands now use `alignerr_mcp` prefix:

```bash
# Domain Management
alignerr_mcp validate --domain <name>
alignerr_mcp migrate --source <path>
alignerr_mcp create-domain --name <name>
alignerr_mcp clone --name <name>
alignerr_mcp list --details
alignerr_mcp info --domain <name>

# Server Management
alignerr_mcp servers list
alignerr_mcp servers install <name>
alignerr_mcp servers uninstall <name>
alignerr_mcp servers info <name>

# Environment Management
alignerr_mcp env status
alignerr_mcp env setup
alignerr_mcp env show
alignerr_mcp env export

# Configuration
alignerr_mcp config
```

## Backward Compatibility

The `alignerr` alias ensures existing scripts and documentation continue to work:

```bash
# Old scripts still work
alignerr validate --domain web_search  ✅ Works

# New scripts use new name
alignerr_mcp validate --domain web_search  ✅ Works
```

## Why Both Names?

### alignerr_mcp (Primary)
- ✅ More descriptive
- ✅ Clearly indicates MCP functionality
- ✅ Distinguishes from other tools
- ✅ Professional naming

### alignerr (Alias)
- ✅ Shorter to type
- ✅ Backward compatibility
- ✅ Existing scripts work
- ✅ Documentation doesn't break

## Quick Reference Card

```bash
# Both work identically:

alignerr_mcp env status    ===    alignerr env status
alignerr_mcp servers list  ===    alignerr servers list
alignerr_mcp validate ...  ===    alignerr validate ...

# Use whichever you prefer!
```

## Installation Verification

After installation, verify both commands are available:

```bash
# Check which command you have
which alignerr_mcp
# Should show: /path/to/.venv/bin/alignerr_mcp or similar

which alignerr
# Should show: /path/to/.venv/bin/alignerr or similar

# Test both
alignerr_mcp --help
alignerr --help

# Both should show the same help text
```

## Summary

✅ **Primary command**: `alignerr_mcp`  
✅ **Alias**: `alignerr` (for convenience)  
✅ **Both work identically**  
✅ **No breaking changes**  
✅ **Updated in pyproject.toml and main.py**  

**Use either command - they're the same!** 🎉

---

**Recommended**: Use `alignerr_mcp` in new scripts and documentation  
**Compatible**: Existing `alignerr` usage continues to work

