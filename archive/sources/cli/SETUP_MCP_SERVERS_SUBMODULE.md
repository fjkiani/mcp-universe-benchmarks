# Setting Up MCP Servers as Git Submodule

## Current Setup

Currently, `lbx_cli/mcp_servers` is a **symlink** to `../lbx_mcp_servers` for local development.

## Converting to Git Submodule

Once `lbx_mcp_servers` is pushed to a remote repository, convert it to a proper git submodule:

### 1. Push MCP Servers to Remote

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_servers

# Add remote (replace with your actual URL)
git remote add origin git@github.com:YOUR_ORG/lbx_mcp_servers.git

# Push to remote
git push -u origin master
```

### 2. Remove Symlink in CLI

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_cli/lbx_cli
rm mcp_servers  # Remove symlink
```

### 3. Add as Submodule

```bash
cd /Users/manuaero/projects/mcp_arena/lbx_mcp_universe_cli

# Add as submodule
git submodule add git@github.com:YOUR_ORG/lbx_mcp_servers.git lbx_cli/mcp_servers

# Commit the submodule
git add .gitmodules lbx_cli/mcp_servers
git commit -m "Add MCP servers as git submodule"
```

### 4. Verify Submodule

```bash
# Check submodules
git submodule status

# Should show:
# <commit-hash> lbx_cli/mcp_servers (heads/master)
```

## For New Users

Once the submodule is set up, users clone with:

```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:YOUR_ORG/lbx_mcp_universe_cli.git

# Or if already cloned
cd lbx_mcp_universe_cli
git submodule update --init --recursive
```

## Updating Submodule

To get latest MCP server updates:

```bash
cd lbx_mcp_universe_cli
git submodule update --remote --merge
git add lbx_cli/mcp_servers
git commit -m "Update MCP servers"
```

## Current State (Local Development)

For now, with the symlink:

```bash
# MCP servers are accessible via symlink
ls lbx_cli/mcp_servers/

# Shows all 27 servers:
# google_search/
# weather/
# wikipedia/
# ... (24 more)
```

## Testing

```bash
# Test server access
cd lbx_cli/mcp_servers/google_search
python -m google_search

# Test imports
python -c "from lbx_cli.mcpuniverse.mcp.manager import MCPManager; print('✅ Works!')"
```

## Final Structure

```
lbx_mcp_universe_cli/
├── lbx_cli/
│   ├── commands/
│   ├── core/
│   ├── mcpuniverse/        # Embedded (192 files)
│   └── mcp_servers/        # Git submodule → lbx_mcp_servers
│       ├── google_search/
│       ├── weather/
│       └── ... (25 more)
└── .gitmodules             # Submodule configuration
```

Once remote repository is set up, the symlink will be replaced with a proper git submodule.

