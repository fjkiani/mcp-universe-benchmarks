# Framework extension guide — CLI, servers, domains, CI/CD

This document explains how the **MCP benchmark stack** fits together, why **Git submodule pins** sometimes look “grey” or “superseded” on GitHub, and how to **extend, test**, and track **known gaps**.

## 1. What “full framework” means here

| Layer | Location | Role |
|--------|----------|------|
| **Benchmark definitions** | `domains/<name>/` | `config.yaml`, `tasks/*.json`, `evaluators/` |
| **Runner & agents** | `lbx_mcp_universe_cli/` (submodule) | `alignerr_mcp`, `MCPRunner`, LLM registry, ReAct agent |
| **Tool servers** | `lbx_mcp_universe_mcp_servers_mothership/servers/` (submodule) | Per-server `server.py`, `pyproject.toml`, configs |
| **Registry & automation** | `central/` | API registry YAML, frontend sync, test-runner helpers |
| **CI/CD** | `.github/workflows/` | Domain lint/validate on PRs, secret scan, optional deploy/sync |
| **Fast feedback** | `local_tests/` | MCP/tool/task checks without a full benchmark run |

The **upstream template** was built around **file-based domains** discovered by the CLI, **MCP** for tools, and **YAML multi-doc** `config.yaml` for LLM + agent + benchmark specs. Domain configs in this repo standardize on **`type: litellm`** for OpenAI-compatible / LiteLLM gateways; the CLI submodule still implements that via a shared proxy client class—see submodule `lbx_cli/mcpuniverse/llm/`.

## 2. Submodule pins and GitHub “grey / superseded”

GitHub shows a submodule commit as unusual or “behind” the default branch when:

- The pinned commit is **not** on the submodule repo’s **default branch** (e.g. `main`), or  
- The default branch has **moved forward** and no longer contains that exact history display.

### Current policy in this repo

- **`lbx_mcp_universe_cli`** — track **`origin/main`**.  
  Keeps the runner, linter, and validation path aligned with upstream.  
  After updates: `cd lbx_mcp_universe_cli && git checkout main && git pull origin main`, then in the **parent** repo: `git add lbx_mcp_universe_cli`.

- **`lbx_mcp_universe_mcp_servers_mothership`** — track **`origin/feature/healthcare-servers`** until healthcare servers are merged to upstream `main`.  
  That branch **includes** upstream `main` **plus** the four healthcare-oriented servers (`twilio_hipaa`, `assemblyai`, `videosdk`, `nexhealth`). Pinning only `main` would **drop** those directories until the upstream PR lands.

`.gitmodules` sets `branch = ...` so `git submodule update --remote` updates to the right line of development.

### Making pins look “clean” on GitHub

1. **Wait for upstream** to merge `feature/healthcare-servers` into `main`, then repoint the mothership submodule to `main` and run `git submodule update --init --recursive`.  
2. **Or fork** `lbx_mcp_universe_mcp_servers_mothership` under your org, merge the healthcare branch into **your fork’s `main`**, and change this repo’s `.gitmodules` `url` to the fork—then the pinned SHA can sit on the default branch of **your** fork.

## 3. How to extend the framework

### Add a domain

```bash
uv run alignerr_mcp create-domain --name your_domain
```

Then edit:

- `domains/your_domain/config.yaml` — `kind: llm`, `kind: agent`, `kind: benchmark`
- `domains/your_domain/tasks/*.json` — `question`, `output_format`, `mcp_servers`, `use_specified_server`, `evaluators`
- `domains/your_domain/evaluators/functions.py` — `@compare_func(name="your_domain.fn")` and reference those names from task JSON

**References:** `domains/web_search` (breadth), `domains/gitlab_mlops` (structured evaluators / error types).

### Add or change MCP servers

Work happens in the **mothership submodule** under `servers/<server_name>/`. After changes, commit **inside the submodule**, then commit the **parent** repo with the updated submodule SHA.

Install into the UV env when needed:

```bash
uv run alignerr_mcp servers install <server_name>
```

### Central registry and dashboard data

- `central/api-registry.yaml` — registry source of truth for many automations  
- `python central/frontend-sync.py` — refreshes frontend-facing JSON (e.g. `frontend/src/data/api-status.json`) when wired in your environment  
- `python central/test-runner.py` — exercise APIs/tests as set up in your pipeline

## 4. How to test

| Goal | Command / path |
|------|----------------|
| Validate structure & run benchmark | `uv run alignerr_mcp validate --domain <name>` |
| Pass@k / stress | `uv run alignerr_mcp validate --domain <name> --runs 3` (and parallel flags as needed) |
| Domain list / env | `uv run alignerr_mcp list`, `uv run alignerr_mcp env status` |
| Local MCP/task/evaluator checks | `local_tests/README.md`, `local_tests/run_all_tests.py` |
| CI | `.github/workflows/ci.yml` on PRs touching `domains/**` |

**CI note:** `ci.yml` uses `submodules: recursive` and may require `GH_ACCESS_TOKEN_WORKFLOW` (or equivalent) for **private** submodule hosts—verify repository secrets if CI checkout fails.

## 5. CI/CD workflows (this repo)

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Domain lint + optional expensive agent eval on PR / `workflow_dispatch` |
| `secret-scan.yml` | Block obvious secret patterns |
| `sync-to-mother.yml` | Sync conventions to aggregator “mothership” monorepo (if enabled) |
| `governance-deploy.yml` | Deployment path for governance/demo API (see workflow file for triggers) |

## 6. Known gaps / follow-ups (for agents extending this)

These are **intentional backlog hints**, not blockers for a minimal domain.

1. **`domains/base.py` (`BaseDomain`)** — Present historically; **file-based** domains + CLI `Domain` class are what actually run. Align or remove `BaseDomain` to avoid confusion.  
2. **`investments` tasks** — Some tasks used legacy fields (`required_mcp_servers`, embedded `input`); align with `TaskConfig` (`mcp_servers`, data in `question`). See `.cursor/plans/move-investments-domain-to-template-c35175ea.plan.md`.  
3. **`governance_traps/config.yaml`** — Validate against the same multi-doc `spec:` schema as other domains (`kind: llm` with `spec:` blocks).  
4. **Healthcare vs benchmark split** — `frontend/`, `backend/`, and `docs/healthcare-receptionist/` are **product/demo** surfaces; they do not need to ship for `alignerr_mcp validate` to work.  
5. **Submodule upstream access** — If `https://github.com/Alignerr-Code-Labeling/...` is private or moved, fork and update `.gitmodules` URLs so clones remain reproducible.  
6. **TypeScript / mixed JS** — Frontend and some `mcp-client` paths mix `.js`/`.tsx`; `tsc` may report missing `.d.ts` until types are added or paths consolidated.

## 7. Single source docs map

- [BENCHMARK_FRAMEWORK.md](../BENCHMARK_FRAMEWORK.md) — core vs optional apps, quick mental model  
- [REPO_LAYOUT.md](../REPO_LAYOUT.md) — directory map  
- [STRUCTURE_GUIDE.md](../STRUCTURE_GUIDE.md) — where files go  
- [PROJECT_AUDIT.md](../PROJECT_AUDIT.md) — audit and domain inventory  
- [docs/REPOSITORY_SECRETS_CHECKLIST.md](REPOSITORY_SECRETS_CHECKLIST.md) — secret **names** only (never commit values)

---

**TL;DR:** The framework **is** the CLI submodule + mothership submodule + `domains/` + CI. GitHub may grey a mothership SHA while it sits on **`feature/healthcare-servers`**; that is expected until it lands on upstream `main` or you repoint to a fork whose default branch includes those commits.
