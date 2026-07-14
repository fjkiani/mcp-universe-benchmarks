# Alignerr Examples

Practical examples for using Alignerr CLI.

## Basic Usage

### List Domains

```bash
# Simple list
alignerr list

# Output:
#   • web_search (50 tasks)
#   • browser_automation (30 tasks)
#   • financial_analysis (25 tasks)
```

### Get Domain Info

```bash
alignerr info --domain web_search

# Shows:
# - Description
# - Task count
# - Agent configuration
# - LLM configuration
# - First 10 tasks
```

### Get Task Info

```bash
alignerr info --domain web_search --task task_0001

# Shows:
# - Task question
# - Required MCP servers
# - Output format
# - Evaluators
```

## Validation Examples

### Single Domain Validation

```bash
# Basic validation
alignerr validate --domain web_search

# With specific model
alignerr validate --domain web_search --model openai/gpt-4o

# Quiet mode (no progress output)
alignerr validate --domain web_search --no-callbacks
```

### Multiple Domain Validation

```bash
# Validate all domains with 4 workers (default)
alignerr validate --all

# With 8 parallel workers
alignerr validate --all --parallel 8

# With specific model
alignerr validate --all --model anthropic/claude-3.5-sonnet
```

### Pass@k Validation

```bash
# Single model, 3 runs (pass@3)
alignerr validate --domain web_search --runs 3

# Multiple models (pass@3 for each)
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5

# Complex pass@k validation
alignerr validate --domain web_search \
  --runs 5 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5,google/gemini-2.0-flash \
  --no-callbacks
```

## Migration Examples

### Migrate All Domains

```bash
alignerr migrate --source /path/to/lbx-mcp-envs

# Output:
# Migrating 8 domain(s) from lbx-mcp-envs
# ✓ web_search (50 tasks)
# ✓ browser_automation (30 tasks)
# ✓ financial_analysis (25 tasks)
# ...
```

### Migrate Specific Domains

```bash
alignerr migrate \
  --source /path/to/lbx-mcp-envs \
  --domains web_search,browser_automation
```

### Migrate to Custom Location

```bash
alignerr migrate \
  --source /path/to/lbx-mcp-envs \
  --output ./custom_domains/
```

## Domain Creation Examples

### Create New Domain from Scratch

```bash
alignerr create-domain --name sentiment_analysis

# Creates:
# domains/sentiment_analysis/
# ├── config.yaml
# ├── tasks/
# │   └── task_0001.json
# ├── evaluators/
# │   ├── __init__.py
# │   └── functions.py
# └── README.md
```

### Create Domain from Legacy

```bash
alignerr create-domain \
  --name web_search \
  --from-legacy /path/to/lbx-mcp-envs

# Migrates specific domain with all tasks and evaluators
```

### Create in Custom Location

```bash
alignerr create-domain \
  --name my_domain \
  --output ./custom_location/domains/
```

## Template Cloning Examples

### Basic Template Clone

```bash
alignerr clone --name financial-tools

# Creates:
# ../lbx-mcp-domain-financial-tools/
# with complete repository structure
```

### Clone to Specific Location

```bash
alignerr clone \
  --name financial-tools \
  --output /path/to/repos/lbx-mcp-domain-financial-tools
```

### Clone with Remote URL

```bash
alignerr clone \
  --name financial-tools \
  --remote git@github.com:org/lbx-mcp-domain-financial-tools.git

# Automatically sets up git remote
```

## Workflow Examples

### Complete Migration Workflow

```bash
# 1. Migrate from lbx-mcp-envs
alignerr migrate --source /path/to/lbx-mcp-envs

# 2. List migrated domains
alignerr list --details

# 3. Get info about specific domain
alignerr info --domain web_search

# 4. Validate single domain
alignerr validate --domain web_search

# 5. Validate all domains
alignerr validate --all --parallel 8
```

### New Domain Development Workflow

```bash
# 1. Clone template for new repo
cd /path/to/repos
alignerr clone --name my-new-domain

# 2. Enter repo
cd lbx-mcp-domain-my-new-domain

# 3. Create domain
alignerr create-domain --name my_domain

# 4. Edit domain files
vim domains/my_domain/tasks/task_0001.json
vim domains/my_domain/evaluators/functions.py
vim domains/my_domain/config.yaml

# 5. Validate
alignerr validate --domain my_domain

# 6. Pass@k quality check
alignerr validate --domain my_domain \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5
```

### Quality Assurance Workflow

```bash
# 1. Run pass@k validation
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5

# 2. Review reports in reports/ directory

# 3. If pass rate is not in 10-80% range, adjust tasks

# 4. Re-validate
alignerr validate --domain web_search --runs 3
```

### Batch Validation Workflow

```bash
# 1. Create a domains list
DOMAINS="web_search,browser_automation,financial_analysis"

# 2. Validate each with pass@k
for domain in $(echo $DOMAINS | tr ',' ' '); do
  echo "Validating $domain..."
  alignerr validate --domain $domain \
    --runs 3 \
    --models openai/gpt-5,anthropic/claude-sonnet-4-5
done

# Or simply:
alignerr validate --all --parallel 8
```

## Advanced Examples

### Custom Configuration

```bash
# Set environment variables
export ALIGNERR_DOMAINS_ROOT=/custom/path/domains
export ALIGNERR_OUTPUT_DIR=/custom/path/reports
export ALIGNERR_MAX_WORKERS=16
export ALIGNERR_DEFAULT_MODEL=anthropic/claude-3.5-sonnet

# Run with custom config
alignerr validate --all
```

### Validation with Custom MCP Path

```bash
alignerr validate --domain web_search \
  --mcpuniverse-path /path/to/lbx-mcp-envs \
  --model openai/gpt-4o
```

### Parallel Validation with Different Models

```bash
# Validate different domains with different models in parallel
alignerr validate --all --parallel 8 &

# While that runs, start another with different model
alignerr validate --all \
  --parallel 8 \
  --model anthropic/claude-3.5-sonnet \
  --output-dir ./reports_claude/
```

## Output Examples

### Validation Output

```
🔧 Alignerr - Domain Validation Runner
════════════════════════════════════════════════════════════════
📊 Configuration:
   Domains: web_search
   Model: openai/gpt-4o
   Parallel Workers: 4
   Runs per model: 1
   Output: /Users/you/reports

🚀 Starting validation...

Running web_search with mcpuniverse directly...
🚀 Running benchmark: domains/web_search/config.yaml
📁 Logging to: reports/20251013_143022__web_search__gpt_4o__benchmark.log

[Task execution details...]

✅ Report generated successfully
📄 MCP Universe report: reports/20251013_143022__web_search__gpt_4o__mcp_universe_report.yaml
📋 Task summary: reports/20251013_143022__web_search__gpt_4o__task_summary.yaml

✓ web_search completed successfully

📁 Report saved: reports/20251013_143022__web_search__report.yaml
```

### Migration Output

```
Migrating 8 domain(s) from lbx-mcp-envs
Source: /path/to/lbx-mcp-envs
Output: ./domains

⠋ Migrating domains...
✓ web_search (50 tasks)
✓ browser_automation (30 tasks)
✓ financial_analysis (25 tasks)
✓ location_navigation (40 tasks)
✓ currency_converter (15 tasks)
✓ multi_server (10 tasks)
✓ repository_management (35 tasks)
⊘ blender already exists, skipping

════════════════════════════════════════════════════════════
MIGRATION SUMMARY
════════════════════════════════════════════════════════════
✓ Migrated: 7
⊘ Skipped: 1
✗ Failed: 0

Output directory: ./domains

✓ Migration completed successfully!

Next steps:
  1. Review migrated domains
  2. Validate domains: alignerr validate --all
```

## Tips and Tricks

### 1. Use Aliases

```bash
# Add to .bashrc or .zshrc
alias av='alignerr validate'
alias al='alignerr list'
alias ai='alignerr info'

# Usage
av --domain web_search
al --details
ai --domain web_search
```

### 2. Validate After Changes

```bash
# Watch for changes and validate
watch -n 60 'alignerr validate --domain my_domain'
```

### 3. Generate Reports Periodically

```bash
# Cron job for daily validation
0 2 * * * cd /path/to/domains && alignerr validate --all --parallel 8
```

### 4. Compare Models

```bash
# Validate with different models
alignerr validate --all --model openai/gpt-5 --output-dir ./reports_gpt5/
alignerr validate --all --model anthropic/claude-sonnet-4-5 --output-dir ./reports_claude/

# Compare reports
diff reports_gpt5/ reports_claude/
```

### 5. Debug Failed Tasks

```bash
# Get task info
alignerr info --domain web_search --task task_0042

# Validate with callbacks for detailed output
alignerr validate --domain web_search

# Check logs
tail -f reports/*__web_search__*__benchmark.log
```

## Common Issues and Solutions

### Issue: Domain not found

```bash
# Check available domains
alignerr list

# Check domains directory
ls -la domains/

# Verify domains root
alignerr config
```

### Issue: Validation fails

```bash
# Run with verbose output
alignerr validate --domain web_search

# Check task configuration
alignerr info --domain web_search --task task_0001

# Verify MCP servers are available
```

### Issue: Slow validation

```bash
# Increase parallel workers
alignerr validate --all --parallel 16

# Use quiet mode
alignerr validate --all --no-callbacks --parallel 16
```

