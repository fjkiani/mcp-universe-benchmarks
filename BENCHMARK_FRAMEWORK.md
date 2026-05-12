# MCP Universe — benchmark framework

This repository is the **benchmark template**: file-based domains, MCP tool servers, validation CLI, and CI. Treat everything under `domains/` as the **single canonical place** for benchmark definitions (including GitLab MLOps, investments, grant workflows, reference `web_search`, etc.).

## What is “core” vs optional product code

| Area | Path | Role |
|------|------|------|
| **Domains** | `domains/` | Tasks (JSON), `config.yaml`, evaluators — the benchmark |
| **CLI** | `lbx_mcp_universe_cli/` (submodule) | `alignerr_mcp`, validation, agents, LLM registry |
| **MCP servers** | `lbx_mcp_universe_mcp_servers_mothership/servers/` (submodule) | Tool implementations |
| **Registry & sync** | `central/` | API registry, test runner, frontend data sync |
| **Tests** | `tests/`, `local_tests/` | API, MCP, local fixtures |
| **Optional apps** | `frontend/`, `backend/` | Dashboards, demo UX — **not required** to run benchmarks |

Optional product and go-to-market docs live alongside this tree (for example `docs/healthcare-receptionist/`) but are **out of the critical path** for `uv run alignerr_mcp validate`.

## Reproducible workflow

1. `git submodule update --init --recursive`
2. `uv sync`
3. `cp .env.example .env` and fill keys for the MCP servers your domain uses
4. `uv run alignerr_mcp validate --domain <name>`

Domain configs use **`type: litellm`** for OpenAI-compatible / LiteLLM gateways. The bundled CLI submodule may still use legacy environment variable names for that integration; see `.env.example` and submodule docs.

## Git remotes (worktrees / forks)

Extra remotes may exist for historical domain repos (e.g. investments, grant application). **This template repo is the integration copy**: prefer merging domain work into `domains/<name>/` here rather than maintaining parallel trees.

## For the next maintainer

- Reference domain: `domains/web_search/`
- Structured evaluators pattern: `domains/gitlab_mlops/`
- Server discovery expects the mothership submodule layout documented in `STRUCTURE_GUIDE.md`
- **Extend / test / CI / submodule pins (including GitHub “grey” submodules):** [docs/FRAMEWORK_EXTENSION_GUIDE.md](docs/FRAMEWORK_EXTENSION_GUIDE.md)
- Remove transient IDE or chat-export folders before committing; they are ignored via `.gitignore` / `.cursorignore`

## Submodules (summary)

- ** CLI:** pin to **`main`** — validation, linter, agent runner.
- **Mothership:** pin follows **`feature/healthcare-servers`** until those servers merge to upstream `main`; see extension guide for why and how to fork if you want default-branch-only pins.
