# Agent instructions — mcp-universe-benchmarks

## What this repo is

File-based **MCP agent benchmarks**. Canonical work product is under `domains/`. CLI and MCP tool servers live in **git submodules**.

## Always prefer (signal)

- `domains/**/tasks/*.json`
- `domains/**/config.yaml`
- `domains/**/evaluators/*.py`
- `domains/**/README.md` (short domain notes only)
- `STRUCTURE_GUIDE.md`
- `BENCHMARK_FRAMEWORK.md`
- `REPO_LAYOUT.md`
- `docs/FRAMEWORK_EXTENSION_GUIDE.md`
- `docs/REPOSITORY_SECRETS_CHECKLIST.md`
- Reference patterns: `domains/web_search/`, `domains/gitlab_mlops/`
- Submodules (after `git submodule update --init --recursive`):
  - `lbx_mcp_universe_cli/`
  - `lbx_mcp_universe_mcp_servers_mothership/`

## Never cite or imitate (slop)

- Anything named `*STATUS*`, `*SUMMARY*`, `*COMPLETE*`, `*AUDIT*`, `*BREAKDOWN*`, `*PLAN*` unless the user names that file
- `archive/`, `docs/archive/`, `docs/healthcare-receptionist/`, `docs/development/`, `docs/architecture/`
- `.cursor/plans/`, sprint deliverable trees
- Product-marketing / landing-page copy
- Committed run artifacts under `local_tests/results/`

## How to extend a domain

1. Copy structure from `domains/web_search` or `domains/gitlab_mlops`.
2. Match existing JSON schema and evaluator patterns exactly.
3. Keep domain README short (purpose + how to validate). No proposal/status novels.
4. Validate: `uv run alignerr_mcp validate --domain <name>`

## Optional surfaces

`frontend/` and `backend/` are product demos — out of the critical path for `alignerr_mcp validate`. Touch them only when asked.
