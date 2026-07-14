# Framework extension guide — CLI, servers, domains, CI/CD

How the **MCP benchmark stack** fits together and how to **extend / test**.

## 1. Layers

| Layer | Location | Role |
|--------|----------|------|
| **Benchmark definitions** | `domains/<name>/` | `config.yaml`, `tasks/*.json`, `evaluators/` |
| **Runner & agents** | `mcpbench/` | `python -m mcpbench` — CLI, LLM registry, ReAct agent, Pass@K |
| **Tool servers** | `servers/` | 18 mock FastMCP servers (stdio transport) |
| **Validator** | `scripts/validate.py` | AST-based domain structure validation |
| **Compat shim** | `scripts/eval_compat.py` | `compare_func`/`eval_func` decorators |
| **CI** | `.github/workflows/` | Domain validation, secret scan |
| **Fast feedback** | `local_tests/` | MCP/tool/task checks without a full agent run |

Domain configs use **`type: litellm`** for LiteLLM-routed models. Supported providers: OpenRouter, Groq, Google Gemini, OpenAI, Anthropic.

## 2. Model routing

Models are routed via LiteLLM. The registry lives at `mcpbench/models.yaml` with 17 verified model slugs. Free-tier models are available through OpenRouter.

```bash
python -m mcpbench list-models
```

To add a model, append to `mcpbench/models.yaml` with the correct LiteLLM provider prefix.

## 3. Extend

### Domain

```bash
cp -r domains/web_search domains/your_domain
```

Edit `config.yaml`, `tasks/*.json`, `evaluators/functions.py` (`@compare_func`). Patterns: `web_search`, `gitlab_mlops`.

### MCP servers

Add a new server in `servers/your_server.py` following the FastMCP pattern, then register it in `servers/registry.yaml`:

```yaml
servers:
  your-server:
    command: "python -m servers.your_server"
    description: "Your server description"
```

## 4. Test

| Goal | Command |
|------|---------|
| Validate one domain | `python -m mcpbench validate --domain <name>` |
| Validate all domains | `python -m mcpbench validate --all` |
| List models | `python -m mcpbench list-models` |
| Run benchmark | `python -m mcpbench run --domain <name> --models <slug>` |
| Pass@K | `python -m mcpbench run --domain <name> --models <slug> --runs 3` |
| Dry run | `python -m mcpbench run --domain <name> --models <slug> --dry-run` |
| Local smoke | `python3 local_tests/run_all_tests.py` |
| CI | `.github/workflows/ci.yml` on `domains/**` |

## 5. Workflows

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Domain validation + optional benchmark run |
| `secret-scan.yml` | Block secret patterns |

## 6. Evaluator signatures

The runner normalizes 4 evaluator calling conventions:

1. `(llm_response, expected_values, op_args)` — 3+ params
2. `(llm_response)` — single param
3. `(llm_response, *args, **kwargs)` — variadic, `args[1]` = op_args
4. `(llm_response, op_args)` — 2 params

All evaluators must return `Tuple[bool, str]` (passed, feedback).

## 7. Docs map

- [BENCHMARK_FRAMEWORK.md](../BENCHMARK_FRAMEWORK.md)
- [REPO_LAYOUT.md](../REPO_LAYOUT.md)
- [STRUCTURE_GUIDE.md](../STRUCTURE_GUIDE.md)
- [AGENTS.md](../AGENTS.md)
- [REPOSITORY_SECRETS_CHECKLIST.md](REPOSITORY_SECRETS_CHECKLIST.md)
