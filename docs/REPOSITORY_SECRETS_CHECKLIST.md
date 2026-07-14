# Repository secrets checklist (names only)

Use GitHub Actions → Secrets (or your vault). **Do not commit real values.**

### CI / submodules

- `GH_ACCESS_TOKEN_WORKFLOW` — checkout private Alignerr submodules in Actions

### LLM / gateway (as needed by domain configs)

- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `OPENROUTER_API_KEY` / `LABELBOX_API_KEY`
- Other model keys only if your `config.yaml` references them

### MCP servers (domain-dependent)

- Search: `SERP_API_KEY`
- Google Workspace: service account file (local path; do not commit keys)
- GitHub/GitLab domains: `GITHUB_PERSONAL_ACCESS_TOKEN`
- Finance: `EXCHANGERATE_API_KEY`, `ALPHA_VANTAGE_API_KEY`

Copy values into local `.env` from `.env.example`. Never paste secrets into tracked files.
