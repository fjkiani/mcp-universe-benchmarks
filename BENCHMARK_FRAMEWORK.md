# MCP Universe — benchmark framework

This repository is the **benchmark template**: file-based domains, MCP tool servers, validation CLI, and CI. Everything under `domains/` is the canonical benchmark surface.

| Area | Path | Role |
|------|------|------|
| **Domains** | `domains/` | Tasks (JSON), `config.yaml`, evaluators |
| **CLI** | `lbx_mcp_universe_cli/` (submodule) | `alignerr_mcp`, validation, agents |
| **MCP servers** | `lbx_mcp_universe_mcp_servers_mothership/` (submodule) | Tool implementations |
| **Local tests** | `local_tests/` | Fast evaluator / server smoke tests |
| **CI** | `.github/workflows/` | Domain validate, secret scan, mothership sync |

## Workflow

1. `git submodule update --init --recursive`
2. `uv sync`
3. `cp .env.example .env` — fill keys for the MCP servers your domain uses
4. `uv run alignerr_mcp validate --domain <name>`

Domain configs use **`type: litellm`** for OpenAI-compatible / LiteLLM gateways. See `.env.example`.

## Maintainer notes

- Reference domain: `domains/web_search/`
- Structured evaluators: `domains/gitlab_mlops/`
- Extend / CI / submodule pins: [docs/FRAMEWORK_EXTENSION_GUIDE.md](docs/FRAMEWORK_EXTENSION_GUIDE.md)
- Agent allowlist: [AGENTS.md](AGENTS.md)

## Submodules

- **CLI:** `main`
- **Mothership:** `feature/healthcare-servers` until healthcare servers land on upstream `main` (see extension guide)
