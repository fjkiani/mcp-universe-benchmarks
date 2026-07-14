# MCP Universe benchmarks

Monorepo for **MCP-backed agent benchmarks**. Domains live under `domains/`; execution is the CLI submodule; tools are the mothership submodule.

Guides: [BENCHMARK_FRAMEWORK.md](BENCHMARK_FRAMEWORK.md) · [STRUCTURE_GUIDE.md](STRUCTURE_GUIDE.md) · [AGENTS.md](AGENTS.md) · [docs/FRAMEWORK_EXTENSION_GUIDE.md](docs/FRAMEWORK_EXTENSION_GUIDE.md)

## Quick start

```bash
git submodule update --init --recursive
uv sync
cp .env.example .env   # fill keys for servers your domain uses

uv run alignerr_mcp --help
uv run alignerr_mcp list
```

## Domains

| Domain | Notes |
|--------|--------|
| [web_search](domains/web_search) | Reference implementation |
| [google_workspace](domains/google_workspace) / [google_slides](domains/google_slides) | Workspace + slides subset |
| [grant_application](domains/grant_application) | 55 tasks |
| [investments](domains/investments) | Portfolio/risk + local `mcp_servers/` |
| [identity_service](domains/identity_service) | 25 auth/security tasks |
| currency_converter, flight_delay, gitlab_mlops, governance_traps | Additional domains |

## Contribution

```bash
uv run alignerr_mcp create-domain --name {your-domain}
# implement under domains/{your-domain}/ following STRUCTURE_GUIDE.md
uv run alignerr_mcp validate --domain {your-domain}
uv run alignerr_mcp validate --domain {your-domain} --runs 3
```

PR branch: `domains/{your-domain}/v1`. CI runs domain lint/eval on `domains/**` changes.

> **Model failures are the goal.** This benchmark finds where models struggle.

## Best practices

- Test locally before push
- Keep submodules updated
- Never commit secrets
- Design hard tasks; verify expected outputs

## Troubleshooting

**CLI not found:** use `uv run alignerr_mcp …` and `uv sync --reinstall` if needed.

**Empty submodules:**

```bash
git submodule update --init --recursive
uv sync
```

**MCP server install:**

```bash
uv run alignerr_mcp servers install google_search
# or
uv pip install -e "lbx_mcp_universe_mcp_servers_mothership/servers/<server_name>"
```
