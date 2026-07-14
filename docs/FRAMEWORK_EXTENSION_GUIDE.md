# Framework extension guide — CLI, servers, domains, CI/CD

How the **MCP benchmark stack** fits together, submodule pins, and how to **extend / test**.

## 1. Layers

| Layer | Location | Role |
|--------|----------|------|
| **Benchmark definitions** | `domains/<name>/` | `config.yaml`, `tasks/*.json`, `evaluators/` |
| **Runner & agents** | `lbx_mcp_universe_cli/` (submodule) | `alignerr_mcp`, LLM registry, ReAct agent |
| **Tool servers** | `lbx_mcp_universe_mcp_servers_mothership/servers/` (submodule) | Per-server packages |
| **CI** | `.github/workflows/` | Domain lint/validate, secret scan, mothership sync |
| **Fast feedback** | `local_tests/` | MCP/tool/task checks without a full agent run |

Domain configs use **`type: litellm`** for OpenAI-compatible / LiteLLM gateways.

## 2. Submodule pins

GitHub can show a submodule as “grey” when the pinned commit is **not** on the submodule’s **default branch**.

### Policy

- **`lbx_mcp_universe_cli`** — `origin/main`  
  After update: commit the new submodule SHA in this parent repo.
- **`lbx_mcp_universe_mcp_servers_mothership`** — `origin/feature/healthcare-servers` until those servers merge to upstream `main`  
  That branch = upstream `main` + healthcare servers (`twilio_hipaa`, `assemblyai`, `videosdk`, `nexhealth`).

`.gitmodules` sets `branch = …` for `git submodule update --remote`.

To clear grey pins: merge healthcare into upstream `main` (or your fork’s `main`) and repoint.

## 3. Extend

### Domain

```bash
uv run alignerr_mcp create-domain --name your_domain
```

Edit `config.yaml`, `tasks/*.json`, `evaluators/functions.py` (`@compare_func`). Patterns: `web_search`, `gitlab_mlops`.

### MCP servers

Change code **inside** the mothership submodule, commit there, then bump the parent submodule SHA.

```bash
uv run alignerr_mcp servers install <server_name>
```

## 4. Test

| Goal | Command |
|------|---------|
| Validate / run | `uv run alignerr_mcp validate --domain <name>` |
| Pass@k | `uv run alignerr_mcp validate --domain <name> --runs 3` |
| List / env | `uv run alignerr_mcp list`, `uv run alignerr_mcp env status` |
| Local smoke | `python3 local_tests/run_all_tests.py` |
| CI | `.github/workflows/ci.yml` on `domains/**` |

Private submodules may need `GH_ACCESS_TOKEN_WORKFLOW` in Actions secrets.

## 5. Workflows

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Domain lint + optional agent eval |
| `secret-scan.yml` | Block secret patterns |
| `sync-to-mother.yml` | Sync domains to aggregator repo (if enabled) |

## 6. Known gaps

1. `domains/base.py` — historical; file-based domains + CLI run path are authoritative.
2. Align remaining task fields to `TaskConfig` (`mcp_servers`, data in `question`).
3. Validate `governance_traps/config.yaml` against the multi-doc `spec:` schema.
4. If Alignerr submodule URLs are private/moved, fork and update `.gitmodules`.

## 7. Docs map

- [BENCHMARK_FRAMEWORK.md](../BENCHMARK_FRAMEWORK.md)
- [REPO_LAYOUT.md](../REPO_LAYOUT.md)
- [STRUCTURE_GUIDE.md](../STRUCTURE_GUIDE.md)
- [AGENTS.md](../AGENTS.md)
- [REPOSITORY_SECRETS_CHECKLIST.md](REPOSITORY_SECRETS_CHECKLIST.md)

**TL;DR:** Framework = CLI submodule + mothership submodule + `domains/` + CI.
