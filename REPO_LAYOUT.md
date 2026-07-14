# Repository layout

```
.
├── domains/                         # Benchmark definitions (canonical)
│   ├── */tasks/*.json
│   ├── */config.yaml
│   └── */evaluators/
├── mcpbench/                        # CLI package (validate, run, list-models)
│   ├── cli.py                       # Typer CLI entry point
│   ├── runner.py                    # BenchmarkRunner (ReAct loop, Pass@K)
│   ├── llm.py                       # LiteLLM wrapper
│   ├── judge.py                     # LLM-as-judge
│   ├── mcp_client.py                # MCP server lifecycle manager
│   ├── models.py + models.yaml      # Model registry (17 models)
│   └── __main__.py                  # python -m mcpbench entry
├── servers/                         # 18 mock MCP servers (FastMCP, stdio)
│   ├── registry.yaml                # Server name → launch command mapping
│   └── *.py                         # One file per server
├── scripts/                         # Validator + compat shim
│   ├── validate.py                  # AST-based domain validation
│   └── eval_compat.py              # compare_func/eval_func decorators
├── local_tests/                     # Smoke tests (results/ gitignored)
├── AGENTS.md
├── BENCHMARK_FRAMEWORK.md
├── STRUCTURE_GUIDE.md
├── docs/                            # Extension guide + secrets checklist
├── .github/workflows/               # CI, secret-scan
├── .env.example
└── pyproject.toml / uv.lock
```

If it is not consumed by `mcpbench` or domain JSON/YAML, it does not belong in this repo.
