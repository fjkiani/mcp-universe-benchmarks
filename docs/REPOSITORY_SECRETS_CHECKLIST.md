# Repository secrets checklist (names only)

Use GitHub Actions → Secrets (or your vault). **Do not commit real values.**

### LLM / gateway (as needed by domain configs and benchmark runs)

- `OPENROUTER_API_KEY` — OpenRouter free + paid models
- `GROQ_API_KEY` — Groq-hosted models
- `GEMINI_API_KEY` — Google Gemini models
- `OPENAI_API_KEY` — OpenAI models
- `ANTHROPIC_API_KEY` — Anthropic models

### MCP servers (domain-dependent)

- Search: `SERP_API_KEY`
- Google Workspace: service account file (local path; do not commit keys)
- GitHub/GitLab domains: `GITHUB_TOKEN`
- Finance: `ALPHA_VANTAGE_API_KEY`

### Git

- `GITHUB_TOKEN` — push commits to remote

Copy values into local `.env` from `.env.example`. Never paste secrets into tracked files.
