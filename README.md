# MCP Universe Benchmarks

Monorepo for **MCP-backed agent benchmarks**. Domains live under `domains/`; the CLI runner is `mcpbench`; mock MCP servers are in `servers/`.

Guides: [BENCHMARK_FRAMEWORK.md](BENCHMARK_FRAMEWORK.md) · [STRUCTURE_GUIDE.md](STRUCTURE_GUIDE.md) · [AGENTS.md](AGENTS.md) · [docs/FRAMEWORK_EXTENSION_GUIDE.md](docs/FRAMEWORK_EXTENSION_GUIDE.md)

## Quick start

```bash
uv sync
cp .env.example .env   # fill keys for servers your domain uses

python -m mcpbench validate --all
python -m mcpbench list-models
python -m mcpbench run --domain investments --models openrouter/openai/gpt-oss-20b:free
```

## Domains

| Domain | Tasks | Notes |
|--------|-------|-------|
| [web_search](domains/web_search) | 55 | Reference implementation |
| [grant_application](domains/grant_application) | 55 | Multi-step reasoning |
| [identity_service](domains/identity_service) | 25 | Auth/security workflows |
| [investments](domains/investments) | 15 | Portfolio/risk + captured market data |
| [governance_traps](domains/governance_traps) | 8 | Compliance trap detection |
| [gitlab_mlops](domains/gitlab_mlops) | 6 | GitLab project operations |
| [google_workspace](domains/google_workspace) | 6 | Docs + sheets tasks |
| [google_slides](domains/google_slides) | 3 | Slides tasks |
| [currency_converter](domains/currency_converter) | 1 | Currency conversion |
| [flight_delay](domains/flight_delay) | 1 | Flight delay prediction |

## CLI commands

```bash
python -m mcpbench validate --domain <name>     # validate one domain
python -m mcpbench validate --all               # validate all domains
python -m mcpbench list-models                  # list available models
python -m mcpbench run --domain <name> --models <slug> [--runs N] [--dry-run]
```

## Mock MCP servers

18 servers in `servers/`, launched as subprocesses via stdio:

google-search, fetch, calendar, task-management, google-sheets, google-docs,
google-slides, date, pdf-generator, gitlab, email, file-storage, notion,
currency-converter, flight-delay, stripe, slack, stock-portfolio

Registry: `servers/registry.yaml`

## Contribution

```bash
# Create a new domain
cp -r domains/web_search domains/{your-domain}
# implement tasks, config.yaml, evaluators
python -m mcpbench validate --domain {your-domain}
```

PR branch: `domains/{your-domain}/v1`. CI runs validation on `domains/**` changes.

> **Model failures are the goal.** This benchmark finds where models struggle.

## Best practices

- Test locally before push
- Never commit secrets
- Design hard tasks; verify expected outputs
