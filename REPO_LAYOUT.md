# Repository layout

```
.
├── domains/                    # All benchmark domains (single project surface)
├── lbx_mcp_universe_cli/       # Submodule — CLI & benchmark runner
├── lbx_mcp_universe_mcp_servers_mothership/   # Submodule — MCP servers
├── central/                    # Registry, sync, test runner helpers
├── tests/                      # Repository test suites
├── local_tests/                # Fast local tests / fixtures
├── frontend/                   # Optional React dashboard (product)
├── backend/                    # Optional API / services (product)
├── docs/                       # Deep dives; healthcare receptionist docs = product-facing
├── .github/workflows/          # CI, secret scan, sync
├── pyproject.toml / uv.lock    # Python env for CLI usage
└── BENCHMARK_FRAMEWORK.md      # How to run and extend benchmarks
```

**Rule of thumb:** If it is not consumed by `alignerr_mcp` or domain JSON/YAML, treat it as documentation or product code, not the benchmark kernel.
