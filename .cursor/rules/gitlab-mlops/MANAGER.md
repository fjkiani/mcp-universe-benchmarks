# GitLab MLOps Automation - Manager Document

**Production-Ready MVP Delivery Plan**

**Last Updated:** 2025-11-05  
**Status:** Active Sprint Planning  
**Target:** Ship production-ready GitLab server for teams to build end-to-end applications

---

## ⚡ Quick Start for Agents

**All tasks are defined in:** `.cursor/rules/gitlab-mlops/sprints/sprint1/tasks/`

**Task Index:** `.cursor/rules/gitlab-mlops/sprints/sprint1/SPRINT1_TASK_INDEX.md`

**Each task file contains:**
- 🎯 **Inputs:** What to read/understand
- 📤 **Outputs:** Exact files to create/modify
- ✅ **Acceptance Criteria:** Clear checklist
- 🧪 **Testing:** How to validate
- 🔍 **Review Checklist:** What Zo will verify

**Pick a task from the index, implement it, submit to `deliverables/` folder.**

---

## 🎯 Mission Statement

**Manager's Request:** "Proposal to build a Gitlab server which can be used across team members to build end to end applications"

**Our Goal:** Ship a production-ready GitLab MCP server MVP that teams can pull and use to build end-to-end applications, validated with discriminative benchmarking (35-40% pass rate).

**Why We'll Succeed:**
- ✅ **Proven track record:** Shipped `investments` (26.7%), `grant_application` (50%), `identity_service` (44%)
- ✅ **Error classification mastery:** Learned `[parse_error]` vs `[validation_error]` separation
- ✅ **CI/CD understanding:** Know how mothership works, tests trigger, pass/fail patterns
- ✅ **Client-ready:** Manager will showcase to client - we nail the demo

---

## 📊 Lessons Learned from Previous Domains

### **From Investments Domain:**
- ✅ **26.7% pass rate is production-ready** (all moderate tasks pass, complex tasks fail)
- ✅ **Ship as-is mentality** - don't over-engineer, discriminative is the goal
- ✅ **MCP server simplicity** - `stock-portfolio` server worked well with minimal tools

### **From Grant Application Domain:**
- ✅ **50% pass rate is ideal** - discriminative and production-ready
- ✅ **Multi-server orchestration** - Used 6 servers together successfully
- ✅ **Complex workflows** - Multi-step tasks with conditional branching work

### **From Identity Service Domain:**
- ✅ **44% pass rate after hardening** - Started at 93%, brought down to 44% by adding complex tasks
- ✅ **Error classification works** - `[parse_error]` vs `[validation_error]` helps debugging
- ✅ **Safety-critical testing** - 100% accuracy on emergent cases (triage)

### **From Healthcare Receptionist (in progress):**
- ✅ **Custom MCP servers** - Built `twilio_hipaa`, `assemblyai`, `videosdk`, `nexhealth`
- ✅ **Real API integrations** - All servers use real APIs, not mocks
- ✅ **40 tasks, 23 tools** - Validated across all workflows

### **Key Insights for GitLab:**
1. **Start small** - 3 tasks to validate, then expand to 12, then 40
2. **Separate server testing from LLM testing** - Manager's feedback: "good idea, would be good to separate the two error classes"
3. **Error classification** - Tag all errors with `[parse_error]` or `[validation_error]`
4. **Target 35-40% pass rate** - Discriminative benchmark, not too easy or hard
5. **Ship MVP fast** - Get basic GitLab Orchestrator module working first

---

## 🏗️ MVP Architecture Decision

**Single Server: `gitlab`** (Like `nexhealth` with 6 tools)

### **MVP Scope: Module 1 Only (GitLab Orchestrator)**
For fast MVP delivery, we'll start with **Module 1 (GitLab Orchestrator)** only - 8 tools, 6 tasks.

**Why Module 1 First:**
- ✅ **Core functionality** - Project management, MR, issues, pipelines
- ✅ **Proven API** - GitLab REST/GraphQL API is well-documented
- ✅ **Team can use it** - Basic GitLab operations teams need daily
- ✅ **Fast to build** - 8 tools, 6 tasks = 1-2 weeks
- ✅ **Validates pattern** - Proves 1 server with modules works

### **Module 1: GitLab Orchestrator** (8 tools)

**Tools to Build:**
1. `create_project()` - Create GitLab project with structure
2. `create_merge_request()` - Create MR with description, reviewers
3. `assign_reviewers()` - Assign reviewers to MR
4. `create_issue()` - Create issue with labels, assignee
5. `link_issues()` - Link related issues (blocks, relates to)
6. `get_pipeline_status()` - Check CI/CD pipeline status
7. `create_release()` - Create release with changelog
8. `create_milestone()` - Create milestone, assign issues

**API Integration:**
- GitLab REST API (primary) - https://docs.gitlab.com/ee/api/
- GitLab GraphQL API (for complex queries)
- Authentication: Personal Access Token (PAT)

**6 Tasks to Create:**
1. `create_project_basic_001.json` - Create new GitLab project (moderate)
2. `create_mr_basic_002.json` - Create merge request (moderate)
3. `assign_reviewers_003.json` - Assign reviewers to MR (moderate)
4. `create_issue_link_004.json` - Create issue and link to MR (complex)
5. `pipeline_status_check_005.json` - Check pipeline status and report (complex)
6. `create_release_milestone_006.json` - Create release with milestone (complex)

**Expected Pass Rate:** 50% (3/6 tasks pass) - Moderate tasks pass, complex fail

---

## 📋 Sprint 1: MVP Foundation (Week 1-2)

### **Goal:** Ship basic GitLab server with Module 1, validate with 6 tasks

### **Priority 1: GitLab Server Structure** (Agent: Backend Specialist)

**Deliverables:**
1. Create `lbx_mcp_universe_mcp_servers_mothership/servers/gitlab/` directory
2. Create `server.py` with FastMCP setup
3. Create `pyproject.toml` with dependencies
4. Create `__init__.py` and `__main__.py`
5. Create `server_config.json` with metadata
6. Create `README.md` with setup instructions

**Files to Create:**
```
servers/gitlab/
├── server.py           # Main server file
├── pyproject.toml      # Dependencies
├── __init__.py         # Package init
├── __main__.py         # Entry point
├── server_config.json  # Server metadata
└── README.md           # Documentation
```

**Dependencies (pyproject.toml):**
```toml
[project]
name = "gitlab-mcp-server"
version = "1.0.0"
dependencies = [
    "httpx>=0.24.0",
    "python-dotenv>=1.0.0",
    "fastmcp>=0.2.0"
]
```

**Environment Variables (.env):**
```
GITLAB_URL=https://gitlab.com
GITLAB_TOKEN=glpat-xxxxx
```

**Success Criteria:**
- ✅ Server structure created
- ✅ `pyproject.toml` with correct dependencies
- ✅ `server_config.json` with server metadata
- ✅ `README.md` with setup instructions

**Timeline:** 1 day

---

### **Priority 2: Module 1 Tools (8 tools)** (Agent: MCP Server Builder)

**Deliverables:**
Build 8 tools in `servers/gitlab/server.py`:

1. **`create_project()`**
   - Input: `name`, `description`, `visibility` (private/public), `initialize_with_readme`
   - Output: `project_id`, `project_url`, `created_at`
   - API: `POST /api/v4/projects`

2. **`create_merge_request()`**
   - Input: `project_id`, `source_branch`, `target_branch`, `title`, `description`
   - Output: `mr_id`, `mr_url`, `created_at`
   - API: `POST /api/v4/projects/:id/merge_requests`

3. **`assign_reviewers()`**
   - Input: `project_id`, `mr_id`, `reviewer_ids` (list of user IDs)
   - Output: `assigned_reviewers` (list), `mr_url`
   - API: `PUT /api/v4/projects/:id/merge_requests/:mr_iid`

4. **`create_issue()`**
   - Input: `project_id`, `title`, `description`, `labels`, `assignee_id`
   - Output: `issue_id`, `issue_url`, `created_at`
   - API: `POST /api/v4/projects/:id/issues`

5. **`link_issues()`**
   - Input: `project_id`, `issue_id`, `target_issue_id`, `link_type` (blocks/relates_to)
   - Output: `link_created`, `link_type`, `link_url`
   - API: `POST /api/v4/projects/:id/issues/:issue_iid/links`

6. **`get_pipeline_status()`**
   - Input: `project_id`, `pipeline_id`
   - Output: `status`, `stages`, `failed_jobs`, `duration`, `pipeline_url`
   - API: `GET /api/v4/projects/:id/pipelines/:pipeline_id`

7. **`create_release()`**
   - Input: `project_id`, `tag_name`, `name`, `description`, `ref` (commit SHA or branch)
   - Output: `release_id`, `release_url`, `created_at`
   - API: `POST /api/v4/projects/:id/releases`

8. **`create_milestone()`**
   - Input: `project_id`, `title`, `description`, `due_date`, `start_date`
   - Output: `milestone_id`, `milestone_url`, `created_at`
   - API: `POST /api/v4/projects/:id/milestones`

**Implementation Pattern (Example):**
```python
from mcp.server.fastmcp import FastMCP
import httpx
import os

mcp = FastMCP("gitlab")

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

@mcp.tool()
async def create_project(
    name: str,
    description: str = "",
    visibility: str = "private",
    initialize_with_readme: bool = True
) -> str:
    """Create a new GitLab project."""
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {
        "name": name,
        "description": description,
        "visibility": visibility,
        "initialize_with_readme": initialize_with_readme
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITLAB_URL}/api/v4/projects",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        project = response.json()
        
        return json.dumps({
            "project_id": project["id"],
            "project_url": project["web_url"],
            "created_at": project["created_at"]
        })
```

**Success Criteria:**
- ✅ All 8 tools implemented
- ✅ All tools use GitLab REST API
- ✅ All tools return JSON strings
- ✅ All tools have proper error handling
- ✅ All tools have docstrings

**Timeline:** 3-4 days

---

### **Priority 3: Server Validation Testing** (Agent: Testing Specialist)

**Deliverables:**
1. Create `servers/gitlab/test_server_structure.py` - Structure validation
2. Create `servers/gitlab/test_api_calls.py` - API call validation
3. Run validation tests locally

**Test 1: Structure Validation**
```python
# test_server_structure.py
import sys
import importlib.util

def test_server_structure():
    """Validate server file structure"""
    # Check imports
    spec = importlib.util.spec_from_file_location("gitlab_server", "server.py")
    module = importlib.util.module_from_spec(spec)
    
    # Check FastMCP instance
    assert hasattr(module, 'mcp'), "Server must define 'mcp' FastMCP instance"
    
    # Check 8 tools exist
    tools = ['create_project', 'create_merge_request', 'assign_reviewers', 
             'create_issue', 'link_issues', 'get_pipeline_status',
             'create_release', 'create_milestone']
    
    for tool in tools:
        assert tool in dir(module), f"Tool '{tool}' not found"
    
    print("✅ Server structure validated")

if __name__ == "__main__":
    test_server_structure()
```

**Test 2: API Call Validation**
```python
# test_api_calls.py
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_gitlab_connection():
    """Test GitLab API connectivity"""
    import httpx
    
    GITLAB_URL = os.getenv("GITLAB_URL")
    GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
    
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    
    async with httpx.AsyncClient() as client:
        # Test connection
        response = await client.get(f"{GITLAB_URL}/api/v4/user", headers=headers)
        response.raise_for_status()
        user = response.json()
        print(f"✅ Connected to GitLab as: {user['username']}")

if __name__ == "__main__":
    asyncio.run(test_gitlab_connection())
```

**Success Criteria:**
- ✅ Structure validation passes
- ✅ API connectivity test passes
- ✅ All 8 tools can be imported
- ✅ GitLab API token works

**Timeline:** 1 day

---

### **Priority 4: Domain Creation** (Agent: Domain Architect)

**Deliverables:**
1. Create `domains/gitlab_mlops/` directory
2. Create `config.yaml` with agent configuration
3. Create `evaluators/functions.py` with error classification
4. Create `README.md` with domain overview

**Directory Structure:**
```
domains/gitlab_mlops/
├── config.yaml              # Agent configuration
├── tasks/                   # Task JSON files (6 tasks)
├── evaluators/
│   ├── __init__.py
│   ├── functions.py         # Evaluator functions
│   └── error_types.py       # Error classification
└── README.md                # Domain documentation
```

**config.yaml:**
```yaml
domain: gitlab_mlops
description: "GitLab MLOps automation domain - tests AI agents on software project management workflows"
version: "1.0.0"

llms:
  - model: "anthropic/claude-3-5-sonnet-20241022"
    name: "claude-sonnet"
  - model: "openai/gpt-4o-2024-11-20"
    name: "gpt-4o"

mcp_servers:
  - name: "gitlab"
    description: "GitLab MCP server for project management, MRs, issues, pipelines"

agent_config:
  max_iterations: 30
  system_prompt: |
    You are a GitLab automation agent. You help teams manage software projects using GitLab.
    
    **Available MCP Server:**
    - `gitlab` - GitLab operations (create project, MR, issue, pipeline status, release, milestone)
    
    **Your Capabilities:**
    - Create and configure GitLab projects
    - Create merge requests with reviewers
    - Create and link issues
    - Check pipeline status and report failures
    - Create releases and milestones
    
    **Guidelines:**
    - Use the `gitlab` server for all GitLab operations
    - Follow GitLab best practices (branch naming, MR descriptions, issue labels)
    - Link issues to MRs when appropriate
    - Check pipeline status before merging
    - Create meaningful release notes

tasks:
  - file: "tasks/create_project_basic_001.json"
    evaluator: "gitlab_mlops.validate_project_creation"
  - file: "tasks/create_mr_basic_002.json"
    evaluator: "gitlab_mlops.validate_mr_creation"
  - file: "tasks/assign_reviewers_003.json"
    evaluator: "gitlab_mlops.validate_reviewer_assignment"
  - file: "tasks/create_issue_link_004.json"
    evaluator: "gitlab_mlops.validate_issue_creation_and_link"
  - file: "tasks/pipeline_status_check_005.json"
    evaluator: "gitlab_mlops.validate_pipeline_status_check"
  - file: "tasks/create_release_milestone_006.json"
    evaluator: "gitlab_mlops.validate_release_and_milestone"
```

**evaluators/error_types.py:**
```python
"""
Error Type Classification for Evaluators

Separates two error classes:
1. Parse/Infrastructure Errors (JSON parsing, data structure issues)
2. Validation/Business Logic Errors (LLM performance, task completion)
"""

from enum import Enum

class ErrorType(Enum):
    """Error classification types"""
    PARSE_ERROR = "parse_error"  # JSON parsing, data structure issues
    VALIDATION_ERROR = "validation_error"  # Business logic, LLM performance
```

**evaluators/functions.py (starter):**
```python
from lbx_cli.mcpuniverse.evaluator.functions import compare_func
from typing import Tuple, Any
import json
from .error_types import ErrorType

def unwrap_pydantic_and_parse_json(agent_response: Any) -> Tuple[bool, Any, str]:
    """Unwrap Pydantic objects and parse JSON from agent response"""
    try:
        # Handle Pydantic FunctionResult objects
        if hasattr(agent_response, 'content'):
            content = agent_response.content
            if isinstance(content, list) and len(content) > 0:
                first_item = content[0]
                if hasattr(first_item, 'text'):
                    text = first_item.text
                else:
                    text = str(first_item)
            else:
                text = str(content)
        else:
            text = str(agent_response)
        
        # Clean markdown code blocks
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        # Parse JSON
        data = json.loads(text)
        return True, data, ""
    
    except json.JSONDecodeError as e:
        return False, None, f"[{ErrorType.PARSE_ERROR.value}] JSON parsing failed: {str(e)}"
    except Exception as e:
        return False, None, f"[{ErrorType.PARSE_ERROR.value}] Failed to extract response: {str(e)}"

# Evaluator functions will be added in Priority 6
```

**README.md:**
```markdown
# GitLab MLOps Automation Domain

AI agent benchmark for GitLab-based software project management workflows.

## Overview

- **Category:** Software Project Management / DevOps Automation
- **Total Tasks:** 6 (MVP) → 40 (Full Implementation)
- **MCP Servers:** `gitlab` (custom)
- **Difficulty:** Moderate to High
- **Expected Pass@1:** 35-40% (discriminative benchmark)

## Domain Purpose

Tests AI agents' ability to:
- Create and configure GitLab projects
- Manage merge requests and reviewers
- Create and link issues
- Monitor CI/CD pipelines
- Create releases and milestones

## MVP Scope (Sprint 1)

**Module 1: GitLab Orchestrator** (8 tools, 6 tasks)
- Basic project management operations
- MR creation and reviewer assignment
- Issue creation and linking
- Pipeline status monitoring
- Release and milestone creation

## Tasks

1. `create_project_basic_001.json` - Create new GitLab project
2. `create_mr_basic_002.json` - Create merge request
3. `assign_reviewers_003.json` - Assign reviewers to MR
4. `create_issue_link_004.json` - Create issue and link to MR
5. `pipeline_status_check_005.json` - Check pipeline status
6. `create_release_milestone_006.json` - Create release with milestone

## Setup

1. Set GitLab API token: `GITLAB_TOKEN=glpat-xxxxx`
2. Run validation: `uv run alignerr_mcp validate --domain gitlab_mlops`
```

**Success Criteria:**
- ✅ Domain directory created
- ✅ `config.yaml` with agent configuration
- ✅ `evaluators/functions.py` with error classification
- ✅ `README.md` with domain overview

**Timeline:** 1 day

---

### **Priority 5: Task Creation (6 tasks)** (Agent: Task Designer)

**Deliverables:**
Create 6 task JSON files in `domains/gitlab_mlops/tasks/`:

**Task 1: `create_project_basic_001.json`** (Moderate - Should Pass)
```json
{
  "task_id": "create_project_basic_001",
  "name": "Create Basic GitLab Project",
  "description": "Create a new GitLab project with basic configuration",
  "difficulty": "moderate",
  "question": "Create a new GitLab project named 'ml-model-training' with description 'Machine learning model training pipeline' and private visibility. Initialize it with a README file.",
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "output_format": {
    "project_id": "number or string",
    "project_url": "string",
    "project_name": "string",
    "visibility": "string",
    "initialized_with_readme": "boolean"
  },
  "evaluators": [
    {
      "name": "gitlab_mlops.validate_project_creation",
      "weight": 1.0
    }
  ]
}
```

**Task 2: `create_mr_basic_002.json`** (Moderate - Should Pass)
```json
{
  "task_id": "create_mr_basic_002",
  "name": "Create Merge Request",
  "description": "Create a merge request from feature branch to main",
  "difficulty": "moderate",
  "question": "In project ID 12345, create a merge request from branch 'feature/add-model-training' to 'main' with title 'Add model training pipeline' and description 'Implements new training pipeline with hyperparameter tuning'.",
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "output_format": {
    "mr_id": "number or string",
    "mr_url": "string",
    "source_branch": "string",
    "target_branch": "string",
    "title": "string"
  },
  "evaluators": [
    {
      "name": "gitlab_mlops.validate_mr_creation",
      "weight": 1.0
    }
  ]
}
```

**Task 3: `assign_reviewers_003.json`** (Moderate - Should Pass)
```json
{
  "task_id": "assign_reviewers_003",
  "name": "Assign Reviewers to MR",
  "description": "Assign reviewers to a merge request",
  "difficulty": "moderate",
  "question": "For project ID 12345, assign users with IDs [101, 102] as reviewers to merge request #42.",
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "output_format": {
    "mr_id": "number or string",
    "assigned_reviewers": "list of user IDs",
    "mr_url": "string"
  },
  "evaluators": [
    {
      "name": "gitlab_mlops.validate_reviewer_assignment",
      "weight": 1.0
    }
  ]
}
```

**Task 4: `create_issue_link_004.json`** (Complex - Should Fail)
```json
{
  "task_id": "create_issue_link_004",
  "name": "Create Issue and Link to MR",
  "description": "Create an issue and link it to an existing merge request",
  "difficulty": "complex",
  "question": "In project ID 12345, create an issue titled 'Bug: Model accuracy degradation' with description 'Model accuracy dropped from 95% to 87% after recent changes' and label 'bug'. Then link this issue to merge request #42 using 'relates_to' link type.",
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "output_format": {
    "issue_id": "number or string",
    "issue_url": "string",
    "mr_id": "number or string",
    "link_type": "string",
    "link_created": "boolean"
  },
  "evaluators": [
    {
      "name": "gitlab_mlops.validate_issue_creation_and_link",
      "weight": 1.0
    }
  ]
}
```

**Task 5: `pipeline_status_check_005.json`** (Complex - Should Fail)
```json
{
  "task_id": "pipeline_status_check_005",
  "name": "Check Pipeline Status and Report Failures",
  "description": "Check pipeline status and provide detailed failure report",
  "difficulty": "complex",
  "question": "For project ID 12345, check the status of pipeline #987. If the pipeline failed, identify which stages and jobs failed, extract error messages, and provide a summary report.",
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "output_format": {
    "pipeline_id": "number or string",
    "status": "string",
    "failed_stages": "list of stage names",
    "failed_jobs": "list of job names",
    "error_summary": "string",
    "pipeline_url": "string"
  },
  "evaluators": [
    {
      "name": "gitlab_mlops.validate_pipeline_status_check",
      "weight": 1.0
    }
  ]
}
```

**Task 6: `create_release_milestone_006.json`** (Complex - Should Fail)
```json
{
  "task_id": "create_release_milestone_006",
  "name": "Create Release with Milestone",
  "description": "Create a release and associate it with a milestone",
  "difficulty": "complex",
  "question": "In project ID 12345, create a milestone titled 'v1.0.0' with description 'Initial production release' and due date '2025-12-31'. Then create a release tagged 'v1.0.0' with name 'Version 1.0.0' and description 'First production release with core features: model training, evaluation, and deployment'.",
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "output_format": {
    "milestone_id": "number or string",
    "milestone_url": "string",
    "release_id": "number or string",
    "release_url": "string",
    "tag_name": "string"
  },
  "evaluators": [
    {
      "name": "gitlab_mlops.validate_release_and_milestone",
      "weight": 1.0
    }
  ]
}
```

**Success Criteria:**
- ✅ All 6 tasks created
- ✅ 3 moderate tasks (should pass)
- ✅ 3 complex tasks (should fail)
- ✅ All tasks have proper `output_format`
- ✅ All tasks reference correct evaluators

**Timeline:** 2 days

---

### **Priority 6: Evaluator Functions (6 evaluators)** (Agent: Evaluator Specialist)

**Deliverables:**
Add 6 evaluator functions to `domains/gitlab_mlops/evaluators/functions.py`:

**Evaluator 1: `validate_project_creation`**
```python
@compare_func(name="gitlab_mlops.validate_project_creation")
async def validate_project_creation(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate GitLab project creation"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error  # Already tagged with [parse_error]
    
    # VALIDATION ERRORS: Business logic checks
    
    # Check project_id
    if 'project_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'project_id' field"
    
    # Check project_url
    if 'project_url' not in data or not isinstance(data['project_url'], str):
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing or invalid 'project_url' field"
    
    # Check project_name
    project_name = data.get('project_name', '')
    if 'ml-model-training' not in project_name.lower():
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Project name incorrect (expected 'ml-model-training', got '{project_name}')"
    
    # Check visibility
    visibility = data.get('visibility', '')
    if visibility != 'private':
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Visibility incorrect (expected 'private', got '{visibility}')"
    
    # Check initialized_with_readme
    if not data.get('initialized_with_readme', False):
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Project not initialized with README"
    
    return True, "Project creation validated successfully"
```

**Evaluator 2: `validate_mr_creation`**
```python
@compare_func(name="gitlab_mlops.validate_mr_creation")
async def validate_mr_creation(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate merge request creation"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    # VALIDATION ERRORS
    
    # Check mr_id
    if 'mr_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'mr_id' field"
    
    # Check mr_url
    if 'mr_url' not in data or not isinstance(data['mr_url'], str):
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing or invalid 'mr_url' field"
    
    # Check source_branch
    source_branch = data.get('source_branch', '')
    if 'feature/add-model-training' not in source_branch:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Source branch incorrect (expected 'feature/add-model-training', got '{source_branch}')"
    
    # Check target_branch
    target_branch = data.get('target_branch', '')
    if target_branch != 'main':
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Target branch incorrect (expected 'main', got '{target_branch}')"
    
    # Check title
    title = data.get('title', '')
    if 'Add model training pipeline' not in title:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] MR title incorrect"
    
    return True, "MR creation validated successfully"
```

**Evaluator 3: `validate_reviewer_assignment`**
```python
@compare_func(name="gitlab_mlops.validate_reviewer_assignment")
async def validate_reviewer_assignment(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate reviewer assignment to MR"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    # VALIDATION ERRORS
    
    # Check mr_id
    if 'mr_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'mr_id' field"
    
    # Check assigned_reviewers
    assigned_reviewers = data.get('assigned_reviewers', [])
    if not isinstance(assigned_reviewers, list):
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] 'assigned_reviewers' must be a list"
    
    if len(assigned_reviewers) != 2:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Expected 2 reviewers, got {len(assigned_reviewers)}"
    
    # Check reviewer IDs (should be 101 and 102)
    expected_reviewers = {101, 102}
    actual_reviewers = set(assigned_reviewers)
    if actual_reviewers != expected_reviewers:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Reviewer IDs incorrect (expected {expected_reviewers}, got {actual_reviewers})"
    
    return True, "Reviewer assignment validated successfully"
```

**Evaluator 4: `validate_issue_creation_and_link`**
```python
@compare_func(name="gitlab_mlops.validate_issue_creation_and_link")
async def validate_issue_creation_and_link(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate issue creation and link to MR"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    # VALIDATION ERRORS
    
    # Check issue_id
    if 'issue_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'issue_id' field"
    
    # Check issue_url
    if 'issue_url' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'issue_url' field"
    
    # Check mr_id
    if 'mr_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'mr_id' field"
    
    # Check link_type
    link_type = data.get('link_type', '')
    if link_type != 'relates_to':
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Link type incorrect (expected 'relates_to', got '{link_type}')"
    
    # Check link_created
    if not data.get('link_created', False):
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Link not created"
    
    return True, "Issue creation and link validated successfully"
```

**Evaluator 5: `validate_pipeline_status_check`**
```python
@compare_func(name="gitlab_mlops.validate_pipeline_status_check")
async def validate_pipeline_status_check(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate pipeline status check and failure report"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    # VALIDATION ERRORS
    
    # Check pipeline_id
    if 'pipeline_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'pipeline_id' field"
    
    # Check status
    status = data.get('status', '')
    if not status:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'status' field"
    
    # Check failed_stages (if pipeline failed)
    if status == 'failed':
        if 'failed_stages' not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'failed_stages' for failed pipeline"
        
        if 'failed_jobs' not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'failed_jobs' for failed pipeline"
        
        if 'error_summary' not in data or not data['error_summary']:
            return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing or empty 'error_summary' for failed pipeline"
    
    # Check pipeline_url
    if 'pipeline_url' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'pipeline_url' field"
    
    return True, "Pipeline status check validated successfully"
```

**Evaluator 6: `validate_release_and_milestone`**
```python
@compare_func(name="gitlab_mlops.validate_release_and_milestone")
async def validate_release_and_milestone(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate release and milestone creation"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    # VALIDATION ERRORS
    
    # Check milestone_id
    if 'milestone_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'milestone_id' field"
    
    # Check milestone_url
    if 'milestone_url' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'milestone_url' field"
    
    # Check release_id
    if 'release_id' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'release_id' field"
    
    # Check release_url
    if 'release_url' not in data:
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing 'release_url' field"
    
    # Check tag_name
    tag_name = data.get('tag_name', '')
    if tag_name != 'v1.0.0':
        return False, f"[{ErrorType.VALIDATION_ERROR.value}] Tag name incorrect (expected 'v1.0.0', got '{tag_name}')"
    
    return True, "Release and milestone creation validated successfully"
```

**Success Criteria:**
- ✅ All 6 evaluators implemented
- ✅ All evaluators use error classification (`[parse_error]` / `[validation_error]`)
- ✅ All evaluators validate required fields
- ✅ All evaluators have clear failure messages

**Timeline:** 2-3 days

---

### **Priority 7: Local Validation** (Agent: QA Specialist)

**Deliverables:**
1. Update submodules: `git submodule update --init --recursive`
2. Sync dependencies: `uv sync`
3. Run structure validation: `uv run alignerr_mcp validate --domain gitlab_mlops`
4. Document results in `SPRINT1_RESULTS.md`

**Validation Steps:**
```bash
# 1. Update submodules
cd /Users/fahadkiani/Desktop/development/lbx_mcp_universe_template-main
git submodule update --init --recursive

# 2. Sync dependencies
uv sync

# 3. Validate domain structure
uv run alignerr_mcp validate --domain gitlab_mlops

# 4. Check for errors
# - Task JSON structure
# - Evaluator function signatures
# - config.yaml validity
```

**Expected Results:**
- ✅ All 6 tasks pass structure validation
- ✅ All 6 evaluators pass signature validation
- ✅ `config.yaml` is valid

**Create `SPRINT1_RESULTS.md`:**
```markdown
# Sprint 1 Results - GitLab MVP

**Date:** 2025-11-XX  
**Status:** Structure Validation Complete

## Validation Results

### Task Validation
- ✅ `create_project_basic_001.json` - Valid
- ✅ `create_mr_basic_002.json` - Valid
- ✅ `assign_reviewers_003.json` - Valid
- ✅ `create_issue_link_004.json` - Valid
- ✅ `pipeline_status_check_005.json` - Valid
- ✅ `create_release_milestone_006.json` - Valid

**Total:** 6/6 tasks valid (100%)

### Evaluator Validation
- ✅ `validate_project_creation` - Valid
- ✅ `validate_mr_creation` - Valid
- ✅ `validate_reviewer_assignment` - Valid
- ✅ `validate_issue_creation_and_link` - Valid
- ✅ `validate_pipeline_status_check` - Valid
- ✅ `validate_release_and_milestone` - Valid

**Total:** 6/6 evaluators valid (100%)

### MCP Server Validation
- ✅ `gitlab` server structure valid
- ✅ 8 tools implemented
- ⏳ API testing pending (requires GitLab token)

## Next Steps
1. Obtain GitLab API token for testing
2. Run API connectivity tests
3. Push to GitHub for CI/CD testing
```

**Success Criteria:**
- ✅ Structure validation passes
- ✅ No linter errors
- ✅ Results documented

**Timeline:** 1 day

---

### **Sprint 1 Summary**

**Total Timeline:** 10-12 days

**Deliverables:**
- ✅ GitLab MCP server with Module 1 (8 tools)
- ✅ Domain structure with 6 tasks
- ✅ 6 evaluators with error classification
- ✅ Local validation complete
- ✅ Documentation (README, SPRINT1_RESULTS)

**Expected Pass Rate:** 50% (3/6 tasks pass)
- Moderate tasks (3): ✅ Pass
- Complex tasks (3): ❌ Fail

**Ready for:** Sprint 2 (CI/CD testing and expansion)

---

## 📋 Sprint 2: CI/CD Testing & Module 2 (Week 3-4)

### **Goal:** Test in CI/CD, expand to 12 tasks, add Code Intelligence module

### **Priority 1: CI/CD Testing** (Agent: DevOps Specialist)

**Deliverables:**
1. Obtain GitLab API token for testing
2. Add `GITLAB_TOKEN` to `.env` (local) and GitHub Secrets (CI/CD)
3. Push to GitHub on feature branch
4. Trigger CI/CD and review results
5. Document pass rate in `SPRINT2_RESULTS.md`

**Steps:**
```bash
# 1. Create feature branch
git checkout -b feature/gitlab-mlops-mvp

# 2. Add all files
git add domains/gitlab_mlops/
git add lbx_mcp_universe_mcp_servers_mothership/servers/gitlab/

# 3. Commit with clear message
git commit -m "Add GitLab MLOps MVP - Module 1 (8 tools, 6 tasks)"

# 4. Push to GitHub
git push origin feature/gitlab-mlops-mvp

# 5. Create Pull Request
# - Title: "GitLab MLOps MVP - Module 1 (GitLab Orchestrator)"
# - Description: Include SPRINT1_RESULTS.md content
```

**CI/CD Will:**
- Run `alignerr_mcp validate --domain gitlab_mlops`
- Run LLM tests (Pass@1)
- Generate test report

**Expected Results:**
- **Pass@1:** 50% (3/6 tasks pass)
- **Moderate tasks:** 100% (3/3 pass)
- **Complex tasks:** 0% (0/3 pass)

**Success Criteria:**
- ✅ CI/CD passes (no infrastructure errors)
- ✅ Pass rate between 40-60% (discriminative)
- ✅ All `[parse_error]` vs `[validation_error]` tagged correctly

**Timeline:** 2 days

---

### **Priority 2: Module 2 (Code Intelligence) - 6 tools** (Agent: MCP Server Builder)

**Deliverables:**
Add 6 new tools to `servers/gitlab/server.py`:

1. `get_mr_diff()` - Get MR diff for code review
2. `comment_on_mr()` - Add comment to MR
3. `get_project_languages()` - Get programming languages used in project
4. `list_project_files()` - List files in project
5. `get_file_content()` - Get content of a specific file
6. `update_mr_description()` - Update MR description

**Success Criteria:**
- ✅ All 6 tools implemented
- ✅ All tools use GitLab REST API
- ✅ Server structure validation passes

**Timeline:** 3 days

---

### **Priority 3: Expand to 12 Tasks** (Agent: Task Designer)

**Deliverables:**
Add 6 new tasks (3 moderate, 3 complex) using Module 2 tools:

7. `get_mr_diff_review_007.json` - Get MR diff (moderate)
8. `comment_on_mr_008.json` - Add comment to MR (moderate)
9. `list_project_files_009.json` - List project files (moderate)
10. `code_review_analysis_010.json` - Analyze code for issues (complex)
11. `security_scan_011.json` - Scan for security issues (complex)
12. `architecture_review_012.json` - Review architecture patterns (complex)

**Success Criteria:**
- ✅ 6 new tasks created
- ✅ 3 moderate + 3 complex
- ✅ All tasks reference Module 2 tools

**Timeline:** 2 days

---

### **Priority 4: Add 6 Evaluators** (Agent: Evaluator Specialist)

**Deliverables:**
Add 6 new evaluators for tasks 7-12

**Success Criteria:**
- ✅ All evaluators use error classification
- ✅ All evaluators validate Module 2 outputs

**Timeline:** 2 days

---

### **Sprint 2 Summary**

**Total Timeline:** 9-10 days

**Deliverables:**
- ✅ CI/CD tested (50% pass rate)
- ✅ Module 2 (Code Intelligence) added (6 tools)
- ✅ 12 total tasks (6 new)
- ✅ 12 total evaluators (6 new)

**Expected Pass Rate:** 50% (6/12 tasks pass)

**Ready for:** Sprint 3 (Modules 3-4, expand to 28 tasks)

---

## 📋 Sprint 3: Modules 3-4 & Expansion (Week 5-6)

### **Goal:** Add CI/CD Intelligence + MLOps Automation modules, expand to 28 tasks

**Modules:**
- Module 3: CI/CD Intelligence (8 tools)
- Module 4: MLOps Automation (8 tools)

**Tasks:** 16 new tasks (8 + 8)

**Expected Pass Rate:** 40% (11/28 tasks pass)

---

## 📋 Sprint 4: Modules 5-7 & Final Hardening (Week 7-8)

### **Goal:** Add Data Pipeline, Resource Optimization, Collaboration modules, expand to 40 tasks, achieve 35-40% pass rate

**Modules:**
- Module 5: Data Pipeline (6 tools)
- Module 6: Resource Optimization (5 tools)
- Module 7: Collaboration Intelligence (5 tools)

**Tasks:** 12 new tasks (6 + 4 + 2)

**Expected Pass Rate:** 35-40% (14-16/40 tasks pass)

**Ready for:** Production deployment, client demo

---

## 🎯 Success Metrics

**MVP (Sprint 1-2):**
- ✅ GitLab server with Modules 1-2 (14 tools)
- ✅ 12 tasks, 50% pass rate
- ✅ Teams can use for basic GitLab operations
- ✅ **Timeline:** 3-4 weeks

**Full Product (Sprint 1-4):**
- ✅ GitLab server with all 7 modules (46 tools)
- ✅ 40 tasks, 35-40% pass rate
- ✅ Production-ready, client demo-ready
- ✅ **Timeline:** 8-10 weeks

---

## 🚀 Parallel Execution Strategy

**Multiple agents can work simultaneously:**

**Week 1:**
- Agent 1: Server structure + Module 1 tools (1-4)
- Agent 2: Module 1 tools (5-8)
- Agent 3: Domain creation + config.yaml
- Agent 4: Task 1-3 creation

**Week 2:**
- Agent 1: Task 4-6 creation
- Agent 2: Evaluator 1-3
- Agent 3: Evaluator 4-6
- Agent 4: Testing + validation

**Result:** Sprint 1 complete in 2 weeks (vs 3-4 weeks sequential)

---

## 📚 Documentation Requirements

### **For Each Sprint:**
1. `SPRINT_X_RESULTS.md` - Test results, pass rate, issues
2. Update `README.md` - Current status, tasks completed
3. Update `MASTER.md` - Overall progress

### **For Client Demo:**
1. `DEMO.md` - Demo script, talking points
2. `PRODUCTION_READY.md` - Deployment guide for teams
3. Video walkthrough (5-10 min)

---

## 🎓 How Teams Will Use This

**Scenario 1: Create Project and MR**
```python
# Team pulls gitlab domain
git clone <repo>
cd lbx_mcp_universe_template

# Install dependencies
uv sync

# Use GitLab server
from servers.gitlab import create_project, create_merge_request

# Create project
project = await create_project(
    name="my-new-app",
    description="My awesome application",
    visibility="private"
)

# Create MR
mr = await create_merge_request(
    project_id=project.id,
    source_branch="feature/new-feature",
    target_branch="main",
    title="Add new feature"
)
```

**Scenario 2: CI/CD Pipeline Monitoring**
```python
# Check pipeline status
status = await get_pipeline_status(
    project_id=12345,
    pipeline_id=987
)

if status.failed:
    print(f"Failed jobs: {status.failed_jobs}")
    print(f"Error summary: {status.error_summary}")
```

---

## 🔗 Key Links

- **GitLab API Docs:** https://docs.gitlab.com/ee/api/
- **GitLab Personal Access Tokens:** https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
- **MCP Protocol:** https://modelcontextprotocol.io/
- **FastMCP:** https://github.com/jlowin/fastmcp

---

**Last Updated:** 2025-11-05  
**Status:** Sprint 1 Ready to Execute  
**Next Review:** End of Sprint 1 (Week 2)

