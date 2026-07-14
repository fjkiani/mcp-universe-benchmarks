# Web Search (reference domain)

Reference implementation for MCP search + fetch benchmarks.

| | |
|--|--|
| Tasks | `tasks/*.json` |
| Config | `config.yaml` |
| Evaluators | `evaluators/functions.py` |
| Servers | google-search, fetch |

```bash
python -m mcpbench validate --domain web_search
```

Copy this domain’s structure when creating new domains. Formats: `STRUCTURE_GUIDE.md`.
