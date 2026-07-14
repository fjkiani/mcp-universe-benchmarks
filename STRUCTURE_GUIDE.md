# Structure Guide

Visual guide to understanding the repository structure and where everything goes.

## Repository Layout

```
mcp-universe-benchmarks/
│
├── Documentation Files
│   ├── README.md                     Start here — quick start + commands
│   ├── STRUCTURE_GUIDE.md            This file
│   ├── BENCHMARK_FRAMEWORK.md        Framework overview
│   ├── REPO_LAYOUT.md                Compact layout reference
│   └── AGENTS.md                     Agent coding instructions
│
├── Domain Implementations (canonical benchmark surface)
│   └── domains/
│       ├── web_search/               Reference implementation
│       │   ├── config.yaml           Benchmark configuration
│       │   ├── README.md             Domain documentation
│       │   ├── tasks/                Task definitions (JSON)
│       │   └── evaluators/           Evaluation logic
│       ├── grant_application/        55 tasks
│       ├── identity_service/         25 tasks
│       ├── investments/              15 tasks
│       └── ... (7 more domains)
│
├── CLI Package (mcpbench/)
│   ├── cli.py                        Typer CLI (validate, run, list-models)
│   ├── runner.py                     BenchmarkRunner (ReAct loop, Pass@K)
│   ├── llm.py                        LiteLLM wrapper (async completion + tools)
│   ├── judge.py                      LLM-as-judge
│   ├── mcp_client.py                 MCP server lifecycle manager
│   ├── models.py + models.yaml       Model registry (17 models)
│   └── __main__.py                   python -m mcpbench entry
│
├── Mock MCP Servers (servers/)
│   ├── registry.yaml                 Server name → launch command mapping
│   ├── google_search.py              18 servers, FastMCP-based, stdio
│   ├── fetch.py
│   ├── calendar.py
│   └── ... (15 more)
│
├── Scripts
│   ├── validate.py                   AST-based domain validator
│   └── eval_compat.py               compare_func/eval_func decorators
│
├── CI/CD
│   └── .github/workflows/
│       ├── ci.yml                    Validates PRs + optional benchmark run
│       └── secret-scan.yml           Prevents secret leaks
│
├── pyproject.toml                    Python project config (mcpbench entry point)
├── uv.lock                           Dependency lock file
├── .env.example                      Template for API keys
└── .gitignore
```

## Where to Put Your Files

### Creating a New Domain

```
domains/your_domain/
├── config.yaml                      Required: benchmark config
├── README.md                        Required: documentation
├── tasks/                           Required: task files
│   ├── category_task_0001.json
│   └── ...
└── evaluators/                      Required: evaluation logic
    ├── __init__.py
    └── functions.py
```

### File Naming Conventions

**Task files:** `{category}_task_{number}.json` (4-digit zero-padded)

Examples:
- `email_send_task_0001.json`
- `multi-server_task_0001.json`

**Evaluator functions:** `@compare_func(name="{domain}.{function_name}")`

Examples:
- `@compare_func(name="web_search.llm_as_a_judge")`
- `@compare_func(name="investments.validate_stock_research")`

## config.yaml Template

```yaml
kind: llm
spec:
  name: llm-1
  type: litellm
  config:
    model_name: openai/gpt-4o

---
kind: llm
spec:
  name: llm-evaluator
  type: litellm
  config:
    model_name: openai/gpt-4o-mini

---
kind: agent
spec:
  name: ReAct-agent
  type: react
  config:
    llm: llm-1
    instruction: |
      You are an AI agent specialized in [your domain].
    max_iterations: 20
    summarize_tool_response: false

---
kind: benchmark
spec:
  description: Your domain benchmark
  agent: ReAct-agent
  tasks:
    - tasks/category_task_0001.json
    # ... list all task files
```

## Task File Template

```json
{
    "category": "your_category",
    "question": "Clear, specific question or instruction",
    "output_format": {
        "field1": "expected format"
    },
    "use_specified_server": true,
    "mcp_servers": [
        {"name": "server_name"}
    ],
    "evaluators": [
        {
            "func": "raw",
            "op": "your_domain.evaluator_function",
            "op_args": {
                "correct_answer": "ground truth"
            }
        }
    ]
}
```

## Evaluator Template

```python
try:
    from lbx_cli.mcpuniverse.evaluator.functions import compare_func  # live pipeline
except ImportError:
    from scripts.eval_compat import compare_func  # in-repo fallback
from typing import Tuple


@compare_func(name="your_domain.your_evaluator")
async def your_evaluator(llm_response, *args, **kwargs) -> Tuple[bool, str]:
    """Evaluate if the agent's response is correct."""
    _, values = args
    correct_answer = values.get('correct_answer')
    response_text = str(llm_response).lower()

    if "expected" in response_text:
        return True, "Task completed successfully"
    else:
        return False, "Task failed"
```

## Finding Things

| Looking for | Location |
|-------------|----------|
| Reference domain | `domains/web_search/` |
| Task examples | `domains/web_search/tasks/` |
| Evaluator examples | `domains/web_search/evaluators/` |
| CLI source code | `mcpbench/` |
| MCP servers | `servers/` |
| Model registry | `mcpbench/models.yaml` |
| CI configuration | `.github/workflows/ci.yml` |
| Validator | `scripts/validate.py` |

## Validation

```bash
python -m mcpbench validate --domain your_domain
python -m mcpbench validate --all
```

## Checklist

- Domain directory exists: `domains/your_domain/`
- `config.yaml` is valid YAML with at least 2 LLMs
- `tasks/` directory with JSON files
- All task files have `evaluators` field
- `evaluators/functions.py` with `@compare_func` decorators
- Evaluator names match task `op` fields
- No secrets committed
