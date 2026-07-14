# MCP Universe — Benchmark Framework

This repository is the **benchmark suite**: file-based domains, mock MCP tool servers, a validation + execution CLI, and CI. Everything under `domains/` is the canonical benchmark surface.

| Area | Path | Role |
|------|------|------|
| **Domains** | `domains/` | Tasks (JSON), `config.yaml`, evaluators |
| **CLI** | `mcpbench/` | `python -m mcpbench` — validation, model listing, benchmark runs |
| **MCP servers** | `servers/` | 18 mock FastMCP servers (stdio transport) |
| **Validator** | `scripts/validate.py` | AST-based domain structure validation |
| **Compat shim** | `scripts/eval_compat.py` | `compare_func`/`eval_func` decorators for in-repo evaluators |
| **Local tests** | `local_tests/` | Fast evaluator / server smoke tests |
| **CI** | `.github/workflows/` | Domain validation, secret scan |

## Workflow

1. `uv sync`
2. `cp .env.example .env` — fill API keys for the models and MCP servers your domain uses
3. `python -m mcpbench validate --domain <name>`
4. `python -m mcpbench run --domain <name> --models <slug>`

Domain configs use **`type: litellm`** for LiteLLM-routed models. Supported providers: OpenRouter, Groq, Google Gemini, OpenAI, Anthropic. See `mcpbench/models.yaml` for the full model registry.

## Model routing

Models are routed via LiteLLM. Free-tier models are available through OpenRouter:

```bash
python -m mcpbench list-models          # list all registered models
python -m mcpbench run --domain web_search \
  --models openrouter/openai/gpt-oss-20b:free
```

## Maintainer notes

- Reference domain: `domains/web_search/`
- Structured evaluators: `domains/gitlab_mlops/`
- Evaluator signatures vary by domain — the runner normalizes 4 calling conventions
- Extend / CI: [docs/FRAMEWORK_EXTENSION_GUIDE.md](docs/FRAMEWORK_EXTENSION_GUIDE.md)
- Agent allowlist: [AGENTS.md](AGENTS.md)
