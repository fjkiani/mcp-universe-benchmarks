# Local tests

Smoke MCP servers, tasks, and evaluators without paid agent runs.

```bash
python3 local_tests/run_all_tests.py
python3 local_tests/test_mcp_servers.py
python3 local_tests/test_tasks.py
python3 local_tests/test_evaluators.py
```

Full domain eval: `uv run alignerr_mcp validate --domain <name>`.
Results under `results/` are gitignored.
