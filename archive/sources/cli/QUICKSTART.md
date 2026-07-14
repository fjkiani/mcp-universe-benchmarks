# Alignerr Quick Start Guide

Get started with Alignerr in 5 minutes!

## Installation

```bash
cd lbx_mcp_universe_cli
pip install -e .
```

## First Steps

### 1. Check Environment Status

```bash
alignerr env status
```

See what API keys are configured and what's missing.

### 2. Setup Environment (Interactive)

```bash
# Setup all environment variables
alignerr env setup

# Or just LLM providers for quick start
alignerr env setup --category llm
```

Guided wizard walks you through entering API keys.

### 3. Install MCP Servers

```bash
# List available servers
alignerr servers list

# Install specific servers
alignerr servers install google_search
alignerr servers install weather

# Or install all
alignerr servers install all
```

### 4. Migrate Existing Domains (if you have lbx-mcp-envs)

```bash
alignerr migrate --source /path/to/lbx-mcp-envs
```

This creates clean, self-contained domains in `./domains/`

### 5. List Your Domains

```bash
alignerr list --details
```

### 6. Run Your First Validation

```bash
# Single domain
alignerr validate --domain web_search

# With specific model
alignerr validate --domain web_search --model openai/gpt-4o
```

### 7. View Results

Reports are saved in `./reports/` with timestamps:

```
reports/
├── 20251013_143022__web_search__gpt_4o__report.yaml
└── 20251013_143022__web_search__gpt_4o__benchmark.log
```

## Common Workflows

### Complete Setup

```bash
# 1. Install CLI
pip install -e .

# 2. Setup environment
alignerr env setup --category llm

# 3. Install servers
alignerr servers install all

# 4. Migrate domains
alignerr migrate --source ../lbx-mcp-envs

# 5. Validate
alignerr validate --all --parallel 8
```

### Check Configuration Status

```bash
# Check environment
alignerr env status

# Check servers
alignerr servers list --installed

# Check config
alignerr config
```

### Validate All Domains (Fast)

```bash
alignerr validate --all --parallel 8
```

### Pass@k Quality Testing

```bash
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5
```

### Create New Domain

```bash
# Create from scratch
alignerr create-domain --name my_domain

# Or migrate from legacy
alignerr create-domain --name my_domain \
  --from-legacy /path/to/lbx-mcp-envs
```

## Domain Structure

```
domains/web_search/
├── config.yaml              # Benchmark config
├── tasks/                   # 50 task files
│   ├── task_0001.json
│   └── ...
├── evaluators/              # Evaluation logic
│   ├── __init__.py
│   └── functions.py
└── README.md
```

## Configuration

Set via environment variables:

```bash
export ALIGNERR_DOMAINS_ROOT=./domains
export ALIGNERR_MCPUNIVERSE_PATH=/path/to/lbx-mcp-envs
export ALIGNERR_DEFAULT_MODEL=openai/gpt-4o
export ALIGNERR_MAX_WORKERS=8
```

Or check current config:

```bash
alignerr config
```

## Next Steps

- Read the full [README.md](README.md)
- Create custom domains
- Run pass@k validation
- Generate reports

## Need Help?

```bash
alignerr --help
alignerr validate --help
alignerr create-domain --help
```

Happy validating! 🎯

