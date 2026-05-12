# TASK 001: GitLab Server Structure

**Agent:** Backend Specialist  
**Status:** TODO  
**Priority:** P1 (Blocker for P2)  
**Estimated Time:** 4 hours

---

## 📋 Task Definition

Create the basic directory structure and configuration files for the GitLab MCP server.

---

## 🎯 Inputs

**Why These References?**
- `nexhealth` and `twilio_hipaa` are **custom servers we built** (similar to what we're building)
- They have **multiple tools** (nexhealth: 6 tools, twilio_hipaa: 5 tools) - similar to GitLab's 8 tools
- They use **real API integrations** (httpx, env vars) - same pattern we need
- They have **complete file structure** (all 6 required files)

**Alternative Simple References (if you want simpler examples):**
- `calendar/` - Simpler, but good for basic structure
- `task_management/` - Also simpler, good for structure

**Required Files to Review:**
1. `lbx_mcp_universe_mcp_servers_mothership/servers/nexhealth/` - **Primary reference** (custom server, multiple tools)
2. `lbx_mcp_universe_mcp_servers_mothership/servers/twilio_hipaa/` - **Secondary reference** (custom server, API integration)
3. `.cursor/rules/gitlab-mlops/MASTER.md` - Requirements

**What to Look For:**
- File structure: `pyproject.toml`, `server.py`, `server_config.json`, `__init__.py`, `__main__.py`, `README.md`
- FastMCP setup: `mcp = FastMCP("server_name")`
- Environment variable pattern: `os.getenv("API_KEY")`
- Basic imports: `httpx`, `json`, `os`

**Required Information:**
- Server name: `gitlab`
- Dependencies: `httpx`, `python-dotenv`, `fastmcp`
- API endpoint: `https://gitlab.com/api/v4`

---

## 📤 Outputs (Deliverables)

Create these files in `lbx_mcp_universe_mcp_servers_mothership/servers/gitlab/`:

### 1. `pyproject.toml`
```toml
[project]
name = "gitlab-mcp-server"
version = "1.0.0"
description = "GitLab MCP server for project management and MLOps automation"
requires-python = ">=3.9"
dependencies = [
    "httpx>=0.24.0",
    "python-dotenv>=1.0.0",
    "fastmcp>=0.2.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0"
]
```

### 2. `__init__.py`
```python
"""GitLab MCP Server - Project management and MLOps automation"""
__version__ = "1.0.0"
```

### 3. `__main__.py`
```python
"""Entry point for GitLab MCP server"""
import asyncio
from .server import mcp

if __name__ == "__main__":
    asyncio.run(mcp.run())
```

### 4. `server_config.json`
```json
{
  "name": "gitlab",
  "version": "1.0.0",
  "description": "GitLab MCP server for project management and MLOps automation",
  "capabilities": [
    "project_management",
    "merge_requests",
    "issues",
    "pipelines",
    "releases"
  ],
  "environment_variables": {
    "GITLAB_URL": {
      "required": false,
      "default": "https://gitlab.com",
      "description": "GitLab instance URL"
    },
    "GITLAB_TOKEN": {
      "required": true,
      "description": "GitLab Personal Access Token"
    }
  }
}
```

### 5. `README.md`
```markdown
# GitLab MCP Server

MCP server for GitLab project management and MLOps automation.

## Setup

1. Install dependencies:
```bash
uv pip install -e .
```

2. Set environment variables:
```bash
export GITLAB_URL="https://gitlab.com"  # Optional, defaults to gitlab.com
export GITLAB_TOKEN="glpat-xxxxx"       # Required
```

3. Test connection:
```bash
python -m servers.gitlab
```

## Capabilities

- Project management (create, update, list)
- Merge requests (create, update, assign reviewers)
- Issues (create, update, link)
- Pipelines (status, logs, retry)
- Releases (create, update)

## API Documentation

- GitLab REST API: https://docs.gitlab.com/ee/api/
- GitLab GraphQL API: https://docs.gitlab.com/ee/api/graphql/
```

### 6. `server.py` (Stub)
```python
"""GitLab MCP Server - Module 1: GitLab Orchestrator"""
from mcp.server.fastmcp import FastMCP
import httpx
import os
import json

mcp = FastMCP("gitlab")

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

# Module 1: GitLab Orchestrator (8 tools)
# Tools will be added by TASK 002-009

if __name__ == "__main__":
    mcp.run()
```

---

## ✅ Acceptance Criteria

1. **Directory Structure:**
   - [ ] `servers/gitlab/` directory created
   - [ ] All 6 files created

2. **File Validity:**
   - [ ] `pyproject.toml` has correct dependencies
   - [ ] `server_config.json` is valid JSON
   - [ ] `server.py` imports successfully
   - [ ] `README.md` has setup instructions

3. **Testing:**
   - [ ] Run: `python -c "import servers.gitlab"` (no errors)
   - [ ] Run: `python servers/gitlab/server.py` (starts without errors)

---

## 🔍 Review Checklist (for Zo)

- [ ] All files created in correct location
- [ ] Dependencies match reference servers
- [ ] JSON is valid (no syntax errors)
- [ ] Python imports work
- [ ] README has all required sections

---

## 📝 Output Format

**Submit via:**
1. Create files in `lbx_mcp_universe_mcp_servers_mothership/servers/gitlab/`
2. Copy this file to `.cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/TASK_001_COMPLETE.md`
3. Update status to `COMPLETE`
4. List any blockers or issues encountered

**Example Completion:**
```markdown
# TASK 001: COMPLETE

**Agent:** Backend Specialist  
**Time Taken:** 3 hours  
**Status:** ✅ COMPLETE

## Deliverables
- ✅ Created `servers/gitlab/pyproject.toml`
- ✅ Created `servers/gitlab/__init__.py`
- ✅ Created `servers/gitlab/__main__.py`
- ✅ Created `servers/gitlab/server_config.json`
- ✅ Created `servers/gitlab/README.md`
- ✅ Created `servers/gitlab/server.py` (stub)

## Testing
- ✅ Import test passed
- ✅ Server starts without errors

## Blockers
None

## Next Task
Ready for TASK 002 (create_project tool)
```

