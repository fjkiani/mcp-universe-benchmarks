# Alignerr CLI

🎯 **Universal CLI for LBX MCP Universe Benchmarks**

A powerful command-line tool for managing, validating, and running MCP benchmark domains locally. Alignerr enables developers to run evaluations with parallel execution, pass@k validation, and comprehensive domain management.

## Features

- ✅ **Local Validation** - Run benchmark validations locally without external dependencies
- 🚀 **Parallel Execution** - Execute multiple domains in parallel for faster results
- 📊 **Pass@k Testing** - Validate benchmarks with multiple models and runs
- 🔄 **Domain Migration** - Migrate domains from legacy lbx-mcp-envs structure
- 📦 **Template Cloning** - Bootstrap new domain repositories quickly
- 🎨 **Rich Output** - Beautiful terminal output with progress bars and tables
- 📁 **Self-contained Domains** - Each domain is independent with config, tasks, and evaluators

## Installation

### From Source

```bash
cd lbx_mcp_universe_cli
pip install -e .
```

### Verify Installation

```bash
alignerr --help
```

## Quick Start

### 1. Migrate Domains from lbx-mcp-envs

If you have an existing lbx-mcp-envs installation:

```bash
# Migrate all domains
alignerr migrate --source /path/to/lbx-mcp-envs

# Migrate specific domains
alignerr migrate --source /path/to/lbx-mcp-envs --domains web_search,browser_automation
```

### 2. List Available Domains

```bash
# Simple list
alignerr list

# With details
alignerr list --details
```

### 3. Validate a Domain

```bash
# Validate single domain
alignerr validate --domain web_search

# Validate with specific model
alignerr validate --domain web_search --model openai/gpt-4o

# Validate all domains in parallel
alignerr validate --all --parallel 8
```

## Commands

### Server Management

#### `alignerr servers`

Manage MCP server installation and lifecycle.

```bash
# List all available servers with installation status
alignerr servers list

# List only installed servers
alignerr servers list --installed

# Install specific server
alignerr servers install google_search

# Install all servers
alignerr servers install all

# Force reinstall
alignerr servers install google_search --force

# Uninstall server
alignerr servers uninstall google_search

# Show server information
alignerr servers info google_search
```

**Sub-commands:**
- `list` - List available servers with status
- `install` - Install one or all servers
- `uninstall` - Remove installed server
- `info` - Show detailed server information

### Environment Management

#### `alignerr env`

Manage environment variables and API credentials.

```bash
# Show configuration status (what's set and what's missing)
alignerr env status

# Interactive setup of all environment variables
alignerr env setup

# Setup only LLM provider credentials
alignerr env setup --category llm

# Setup only MCP server credentials
alignerr env setup --category servers

# Show required variables and where to get them
alignerr env show

# Show only LLM variables
alignerr env show --category llm

# Export .env template file
alignerr env export

# Export to custom location
alignerr env export --output .env.example
```

**Sub-commands:**
- `status` - Show what's configured and what's missing
- `setup` - Interactive configuration wizard
- `show` - Display required variables with URLs
- `export` - Generate .env template file

**Environment Variables Managed:**

LLM Providers:
- `OPENAI_API_KEY` - OpenAI GPT models
- `ANTHROPIC_API_KEY` - Anthropic Claude models
- `GEMINI_API_KEY` - Google Gemini models
- `XAI_API_KEY` - xAI Grok models
- `MISTRAL_API_KEY` - Mistral models

MCP Servers:
- `SERP_API_KEY` - Google search
- `OPENWEATHER_API_KEY` - Weather data
- `GOOGLE_MAPS_API_KEY` - Maps functionality
- `GITHUB_PERSONAL_ACCESS_TOKEN` - GitHub operations
- `NOTION_API_KEY` - Notion integration
- `STRIPE_API_KEY` - Payment processing
- `TWILIO_ACCOUNT_SID` - SMS messaging
- `TWILIO_AUTH_TOKEN` - SMS messaging

### `alignerr validate`

Run domain validations locally with configurable parallel execution.

```bash
# Basic validation
alignerr validate --domain web_search

# With specific model
alignerr validate --domain web_search --model openai/gpt-4o

# Validate multiple domains in parallel
alignerr validate --all --parallel 8

# Pass@k validation with multiple models
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5

# With custom mcpuniverse path
alignerr validate --domain web_search \
  --mcpuniverse-path /path/to/lbx-mcp-envs

# Quiet mode (no callbacks)
alignerr validate --domain web_search --no-callbacks
```

**Options:**
- `--domain`, `-d` - Domain to validate
- `--all` - Validate all domains
- `--model`, `-m` - Model to use
- `--parallel`, `-p` - Number of parallel workers (default: 4)
- `--runs`, `-k` - Number of runs per model for pass@k (default: 1)
- `--models` - Comma-separated list of models for pass@k
- `--no-callbacks`, `-q` - Disable verbose output
- `--mcpuniverse-path` - Path to lbx-mcp-envs installation
- `--output-dir`, `-o` - Output directory for reports

### `alignerr migrate`

Migrate domains from lbx-mcp-envs to the new self-contained structure.

```bash
# Migrate all domains
alignerr migrate --source /path/to/lbx-mcp-envs

# Migrate specific domains
alignerr migrate --source /path/to/lbx-mcp-envs \
  --domains web_search,browser_automation

# Custom output directory
alignerr migrate --source /path/to/lbx-mcp-envs \
  --output ./my_domains/
```

**Options:**
- `--source`, `-s` - Path to lbx-mcp-envs repository (required)
- `--output`, `-o` - Output directory (default: ./domains/)
- `--domains`, `-d` - Comma-separated list of domains to migrate

### `alignerr clone`

Clone template repository to create a new domain repository.

```bash
# Basic clone
alignerr clone --name my-new-domain

# Clone to specific location
alignerr clone --name my-domain \
  --output ../lbx-mcp-domain-mydomain

# Clone with remote URL
alignerr clone --name my-domain \
  --remote git@github.com:org/lbx-mcp-domain-mydomain.git
```

**Options:**
- `--name`, `-n` - Name of the new repository (required)
- `--output`, `-o` - Output directory
- `--remote`, `-r` - Git remote URL

### `alignerr create-domain`

Create a new domain structure within a repository.

```bash
# Create new domain
alignerr create-domain --name financial_analysis

# Create in custom location
alignerr create-domain --name my_domain \
  --output ./custom_domains/

# Migrate from lbx-mcp-envs
alignerr create-domain --name web_search \
  --from-legacy /path/to/lbx-mcp-envs
```

**Options:**
- `--name`, `-n` - Domain name (required)
- `--output`, `-o` - Output directory (default: ./domains/)
- `--from-legacy` - Path to lbx-mcp-envs for migration

### `alignerr list`

List all available domains.

```bash
# Simple list
alignerr list

# With details
alignerr list --details
```

**Options:**
- `--details`, `-d` - Show detailed information

### `alignerr info`

Show detailed information about a domain or task.

```bash
# Show domain info
alignerr info --domain web_search

# Show task info
alignerr info --domain web_search --task task_0001
```

**Options:**
- `--domain`, `-d` - Domain name (required)
- `--task`, `-t` - Specific task ID

### `alignerr config`

Show current configuration.

```bash
alignerr config
```

## Domain Structure

Each domain is self-contained with the following structure:

```
domains/{domain}/
├── config.yaml              # Benchmark configuration
├── tasks/                   # Task definition files
│   ├── task_0001.json
│   ├── task_0002.json
│   └── ...
├── evaluators/              # Evaluation functions
│   ├── __init__.py
│   └── functions.py
└── README.md                # Domain documentation
```

### Config Format (`config.yaml`)

```yaml
kind: llm
spec:
  name: llm-1
  type: litellm
  config:
    model_name: openai/gpt-4o

---
kind: agent
spec:
  name: ReAct-agent
  type: react
  config:
    llm: llm-1
    instruction: You are an agent for domain tasks.
    max_iterations: 20
    summarize_tool_response: false

---
kind: benchmark
spec:
  description: Test agent for domain tasks.
  agent: ReAct-agent
  tasks:
    - tasks/task_0001.json
    - tasks/task_0002.json
```

### Task Format (`tasks/*.json`)

```json
{
    "category": "general",
    "question": "Task question or prompt",
    "output_format": {
        "answer": "[Expected format]"
    },
    "use_specified_server": true,
    "mcp_servers": [
        {
            "name": "example-server"
        }
    ],
    "evaluators": [
        {
            "func": "raw",
            "op": "domain_name.evaluation_function",
            "op_args": {
                "expected": "expected_value"
            }
        }
    ]
}
```

### Evaluators (`evaluators/functions.py`)

```python
"""Evaluation functions for domain."""

def llm_as_a_judge(question, correct_answer, agent_response, **kwargs):
    """Evaluate using LLM-based judgment."""
    # Implementation
    pass

def exact_match(expected, actual, **kwargs):
    """Simple exact match evaluation."""
    return str(expected).strip().lower() == str(actual).strip().lower()
```

## Configuration

Alignerr can be configured via environment variables:

```bash
export ALIGNERR_DOMAINS_ROOT=/path/to/domains
export ALIGNERR_MCPUNIVERSE_PATH=/path/to/lbx-mcp-envs
export ALIGNERR_OUTPUT_DIR=/path/to/reports
export ALIGNERR_DEFAULT_MODEL=openai/gpt-4o
export ALIGNERR_MAX_WORKERS=8
```

View current configuration:

```bash
alignerr config
```

## Parallel Execution

Alignerr supports parallel execution for faster validation:

```bash
# Run 8 domains in parallel
alignerr validate --all --parallel 8

# Default is 4 workers
alignerr validate --all
```

Parallel execution is managed intelligently:
- Uses asyncio for I/O-bound operations
- Thread pool for CPU-bound operations
- Configurable worker count
- Progress tracking with rich console output

## Pass@k Validation

Validate benchmarks with multiple models and runs to ensure quality:

```bash
# Run 3 times with default model (pass@3)
alignerr validate --domain web_search --runs 3

# Test with multiple models
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5

# Validation criteria:
# - Pass@k rate >= 10% and <= 80%
# - Zero score rate < 10%
```

## Reports

All validation runs generate comprehensive reports:

```
reports/
├── 20251013_143022__web_search__gpt_4o__report.yaml
├── 20251013_143022__summary.yaml
└── 20251013_143022__validation_report.yaml
```

Report formats:
- **YAML** - Structured data for programmatic processing
- **Markdown** - Human-readable summaries
- **Logs** - Detailed execution traces

## Integration with lbx-mcp-envs

Alignerr can work with or without lbx-mcp-envs:

1. **With mcpuniverse installed**: Uses the library directly
2. **With lbx-mcp-envs path**: Shells out to run.py
3. **Standalone**: Validates structure only

```bash
# Use installed mcpuniverse
alignerr validate --domain web_search

# Use lbx-mcp-envs installation
alignerr validate --domain web_search \
  --mcpuniverse-path /path/to/lbx-mcp-envs
```

## Development

### Adding a New Domain

```bash
# 1. Create domain structure
alignerr create-domain --name my_new_domain

# 2. Add task files to domains/my_new_domain/tasks/

# 3. Implement evaluators in domains/my_new_domain/evaluators/functions.py

# 4. Update config.yaml with task references

# 5. Validate
alignerr validate --domain my_new_domain
```

### Migrating from lbx-mcp-envs

```bash
# 1. Migrate all domains
alignerr migrate --source /path/to/lbx-mcp-envs

# 2. Review migrated domains
alignerr list --details

# 3. Validate
alignerr validate --all
```

## Examples

### Example 1: Basic Validation

```bash
# Validate single domain
alignerr validate --domain web_search --model openai/gpt-4o
```

### Example 2: Parallel Validation

```bash
# Validate all domains with 8 workers
alignerr validate --all --parallel 8 --model openai/gpt-4o
```

### Example 3: Pass@k Testing

```bash
# Test with multiple models, 3 runs each
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5
```

### Example 4: Complete Migration Workflow

```bash
# 1. Migrate from lbx-mcp-envs
alignerr migrate --source ../lbx-mcp-envs

# 2. List migrated domains
alignerr list --details

# 3. Validate specific domain
alignerr info --domain web_search
alignerr validate --domain web_search

# 4. Validate all domains
alignerr validate --all --parallel 8
```

## Troubleshooting

### Domain not found

```bash
# Check available domains
alignerr list

# Ensure domains directory exists
ls -la domains/
```

### mcpuniverse not found

```bash
# Install mcpuniverse or provide path
alignerr validate --domain web_search \
  --mcpuniverse-path /path/to/lbx-mcp-envs
```

### Migration fails

```bash
# Check source path
ls -la /path/to/lbx-mcp-envs/mcpuniverse/benchmark/configs/test/

# Migrate specific domains
alignerr migrate --source /path/to/lbx-mcp-envs \
  --domains web_search
```

## Architecture

```
lbx_mcp_universe_cli/
├── lbx_cli/
│   ├── commands/          # CLI commands
│   │   ├── validate.py    # Validation command
│   │   ├── clone.py       # Template cloning
│   │   ├── create.py      # Domain creation
│   │   ├── info.py        # List and info
│   │   └── migrate.py     # Migration utility
│   ├── core/              # Core functionality
│   │   ├── domain.py      # Domain models
│   │   ├── runner.py      # Benchmark runner
│   │   └── parallel.py    # Parallel execution
│   ├── utils/             # Utilities
│   │   ├── config.py      # Configuration
│   │   └── reports.py     # Report generation
│   └── main.py            # CLI entry point
├── pyproject.toml
└── README.md
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Your License Here]

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Check existing documentation
- Contact the development team

---

**Made with ❤️ by the LBX MCP Team**
