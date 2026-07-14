# Source map — consolidated into mcp-universe-benchmarks

| Local folder | Origin remote | What landed here |
|---|---|---|
| `lbx_mcp_universe_template-main` | already tracked `benchmarks` remote | Base monorepo (GitHub main is newer; used as foundation) |
| `lbx_mcp_universe_cli` | Alignerr submodule | Kept as git submodule `lbx_mcp_universe_cli` (docs-only snapshot under `archive/sources/cli`) |
| `lbx_mcp_universe_mcp_servers_mothership` | Alignerr submodule | Kept as git submodule (docs-only archive: `archive/sources/mothership`) |
| `lbx_mcp_universe_identity_service` | Alignerr domain repo | `domains/identity_service/` (was missing from monorepo) |
| `lbx_mcp_universe_identity_service_packaged` | packaging drop (no .git) | Identical domain + `PACKAGING_REPORT.md` → archive |
| `lbx_mcp_universe_demo` | Alignerr demo | Domains already present; identity_service identical to identity repo |
| `lbx_mcp_universe_grant_application` | Alignerr grant domain | Preferred `domains/grant_application/` (55 tasks incl. 0051–0055) |
| `lbx_official` | Alignerr template @ grant v1 | Docs archived; early 10-task grant superseded; `domains/google_slides/` retained |
| `lbx_template_official` | Alignerr @ phase2a | Grant docs variants archived under `archive/sources/` |
| `lbx_mcp_universe_investments` | Alignerr investments | Preferred `domains/investments/` (+ `mcp_servers/`, embedded-input task fixes) |
| `lbx_template_pr26` | Alignerr investments phase2 PR | Maintainer notes archived; task set superseded by investments repo |

## Deliberate non-copies
- Nested empty/partial submodule checkouts inside domain repos
- `.venv`, `node_modules`, `__pycache__`, `.env`, large SpecStory noise
- Duplicate template scaffolding (`pyproject.toml`/`uv.lock` per domain fork)
