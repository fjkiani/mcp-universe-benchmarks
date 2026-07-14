# Repository layout

```
.
├── domains/                         # Benchmark definitions (canonical)
│   ├── */tasks/*.json
│   ├── */config.yaml
│   └── */evaluators/
├── AGENTS.md
├── BENCHMARK_FRAMEWORK.md
├── STRUCTURE_GUIDE.md
├── lbx_mcp_universe_cli/            # Submodule — CLI
├── lbx_mcp_universe_mcp_servers_mothership/  # Submodule — MCP servers
├── local_tests/                     # Smoke tests (results/ gitignored)
├── docs/                            # Extension guide + secrets checklist
├── .github/workflows/               # CI, secret-scan, mothership sync
├── .env.example
└── pyproject.toml / uv.lock
```

If it is not consumed by `alignerr_mcp` or domain JSON/YAML, it does not belong in this repo.
