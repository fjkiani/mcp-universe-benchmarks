# Central Workflow - API & Test Management

**Purpose:** One central place to manage APIs, tests, and frontend integration

## Quick Start

```bash
# 1. Run tests
python central/test-runner.py

# 2. Sync to frontend
python central/frontend-sync.py

# 3. View showcase
cd frontend && npm run dev
# Open http://localhost:3000/showcase
```

## Files

- `api-registry.yaml` - Single source of truth for all APIs
- `test-runner.py` - Automated test runner
- `frontend-sync.py` - Frontend sync script
- `api-manager.py` - API connection manager (coming soon)

## Workflow

1. **Build API** → Register in `api-registry.yaml`
2. **Write Tests** → Create in `tests/api/`
3. **Run Tests** → `python central/test-runner.py`
4. **Sync Frontend** → `python central/frontend-sync.py`
5. **View Showcase** → Frontend shows real status

## Documentation

See `CENTRAL_WORKFLOW.md` for complete documentation.

