# Repository layout

```
.
├── domains/                    # Benchmark definitions (canonical)
│   ├── */tasks/*.json
│   ├── */config.yaml
│   └── */evaluators/
├── AGENTS.md                   # AI allowlist — prefer domains, ignore slop
├── BENCHMARK_FRAMEWORK.md
├── STRUCTURE_GUIDE.md
├── lbx_mcp_universe_cli/       # Submodule — CLI & runner
├── lbx_mcp_universe_mcp_servers_mothership/  # Submodule — MCP servers
├── central/                    # Registry / sync helpers
├── tests/, local_tests/
├── frontend/, backend/         # Optional product demos
├── docs/                       # Lean guides only (see docs/README.md)
├── .github/workflows/
└── pyproject.toml / uv.lock
```

**Rule of thumb:** If it is not consumed by `alignerr_mcp` or domain JSON/YAML, treat it as documentation or product code, not the benchmark kernel.
