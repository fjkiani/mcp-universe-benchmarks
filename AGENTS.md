# Agent instructions — mcp-universe-benchmarks

## What this repo is

File-based **MCP agent benchmarks** only. Canonical work product: `domains/`. Runner + tools: git submodules.

## Always prefer (signal)

- `domains/**/tasks/*.json`
- `domains/**/config.yaml`
- `domains/**/evaluators/*.py`
- `domains/**/README.md` (short)
- `STRUCTURE_GUIDE.md`
- `BENCHMARK_FRAMEWORK.md`
- `REPO_LAYOUT.md`
- `docs/FRAMEWORK_EXTENSION_GUIDE.md`
- `docs/REPOSITORY_SECRETS_CHECKLIST.md`
- Reference patterns: `domains/web_search/`, `domains/gitlab_mlops/`
- Submodules after `git submodule update --init --recursive`:
  - `lbx_mcp_universe_cli/`
  - `lbx_mcp_universe_mcp_servers_mothership/`

## Never cite or reintroduce (slop)

- Product apps: `frontend/`, `backend/`, `central/`, `datasets/`
- Docs: `archive/`, `docs/archive/`, `docs/healthcare-receptionist/`, `docs/development/`, `docs/architecture/`
- Names: `*STATUS*`, `*SUMMARY*`, `*COMPLETE*`, `*AUDIT*`, `*BREAKDOWN*`, `*PLAN*` (unless the user asks for that file)
- Deploy demos: root `Dockerfile`, `render*.yaml`, `setup_*frontend*`, `setup_*backend*`
- `.cursor/plans/`, sprint trees, landing-page copy

## How to extend a domain

1. Copy `domains/web_search` or `domains/gitlab_mlops`.
2. Match JSON schema + evaluator patterns exactly.
3. Keep README to purpose + `uv run alignerr_mcp validate --domain <name>`.
4. Validate before PR.
