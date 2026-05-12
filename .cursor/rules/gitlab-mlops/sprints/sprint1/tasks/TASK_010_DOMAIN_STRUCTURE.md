# TASK 010: Domain Structure & Config

**Agent:** Domain Architect  
**Status:** TODO (Can run in parallel with TASK 001)  
**Priority:** P1  
**Estimated Time:** 3 hours

---

## 📋 Task Definition

Create the GitLab MLOps domain directory structure and configuration file.

---

## 🎯 Inputs

**Reference Domains:**
1. `domains/healthcare_receptionist/` - Pattern to follow
2. `domains/grant_application/` - Config.yaml reference
3. `.cursor/rules/gitlab-mlops/MASTER.md` - Requirements

---

## 📤 Outputs (Deliverables)

### 1. Create directory structure:
```
domains/gitlab_mlops/
├── config.yaml
├── README.md
├── tasks/           # Empty folder (tasks added in TASK 012-013)
└── evaluators/
    └── __init__.py
```

### 2. `config.yaml`
```yaml
domain: gitlab_mlops
description: "GitLab MLOps automation - tests AI agents on software project management workflows"
version: "1.0.0"

llms:
  - model: "anthropic/claude-3-5-sonnet-20241022"
    name: "claude-sonnet"
  - model: "openai/gpt-4o-2024-11-20"
    name: "gpt-4o"

mcp_servers:
  - name: "gitlab"
    description: "GitLab MCP server for project management, MRs, issues, pipelines, releases"

agent_config:
  max_iterations: 30
  system_prompt: |
    You are a GitLab automation agent helping teams manage software projects.
    
    **Available MCP Server:**
    - `gitlab` - GitLab operations (projects, MRs, issues, pipelines, releases, milestones)
    
    **Module 1: GitLab Orchestrator**
    You have access to these tools:
    - create_project() - Create new GitLab project
    - create_merge_request() - Create MR from source to target branch
    - assign_reviewers() - Assign reviewers to MR
    - create_issue() - Create issue with labels and assignee
    - link_issues() - Link issues together (blocks, relates_to)
    - get_pipeline_status() - Check CI/CD pipeline status
    - create_release() - Create release with tag
    - create_milestone() - Create milestone with due date
    
    **Guidelines:**
    - Use the `gitlab` server for all operations
    - Follow GitLab best practices (branch naming, descriptions)
    - Link issues to MRs when appropriate
    - Check pipeline status before actions
    - Return structured JSON responses

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

### 3. `README.md`
```markdown
# GitLab MLOps Automation Domain

AI agent benchmark for GitLab-based software project management workflows.

## Overview

- **Category:** Software Project Management / DevOps Automation
- **Total Tasks:** 6 (MVP Sprint 1)
- **MCP Servers:** `gitlab` (custom)
- **Difficulty:** Moderate to High
- **Expected Pass@1:** 50% (discriminative benchmark)
- **Target:** Teams building end-to-end applications

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

1. `create_project_basic_001.json` - Create new GitLab project (moderate)
2. `create_mr_basic_002.json` - Create merge request (moderate)
3. `assign_reviewers_003.json` - Assign reviewers to MR (moderate)
4. `create_issue_link_004.json` - Create issue and link to MR (complex)
5. `pipeline_status_check_005.json` - Check pipeline status (complex)
6. `create_release_milestone_006.json` - Create release with milestone (complex)

## Expected Pass Rate

- **Moderate tasks (1-3):** 100% (3/3 should pass)
- **Complex tasks (4-6):** 0% (0/3 should pass)
- **Overall:** 50% (3/6 pass)

This discriminative pass rate ensures the benchmark separates strong from weak agents.

## Setup

1. Set GitLab API token:
```bash
export GITLAB_TOKEN="glpat-xxxxx"
```

2. Run validation:
```bash
uv run alignerr_mcp validate --domain gitlab_mlops
```

## Error Classification

All evaluators use two error types:
- `[parse_error]` - JSON parsing, data structure issues (infrastructure)
- `[validation_error]` - Business logic, LLM performance issues

This separation helps debugging: parse errors = fix server, validation errors = improve prompt/agent.
```

### 4. `evaluators/__init__.py`
```python
"""Evaluators for GitLab MLOps domain"""
from .functions import *
```

---

## ✅ Acceptance Criteria

1. **Directory Structure:**
   - [ ] `domains/gitlab_mlops/` created
   - [ ] `tasks/` folder created (empty)
   - [ ] `evaluators/` folder created
   - [ ] All 3 files created

2. **Config Validation:**
   - [ ] `config.yaml` is valid YAML
   - [ ] References all 6 tasks
   - [ ] References all 6 evaluators
   - [ ] Has 2 LLMs configured
   - [ ] System prompt mentions all 8 tools

3. **README Completeness:**
   - [ ] Has overview section
   - [ ] Lists all 6 tasks
   - [ ] Shows expected pass rate
   - [ ] Has setup instructions
   - [ ] Explains error classification

---

## 🧪 Testing

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('domains/gitlab_mlops/config.yaml'))"

# Check directory structure
ls -la domains/gitlab_mlops/
ls -la domains/gitlab_mlops/tasks/
ls -la domains/gitlab_mlops/evaluators/
```

---

## 🔍 Review Checklist (for Zo)

- [ ] All directories created
- [ ] `config.yaml` has all required fields
- [ ] Task list matches SPRINT1_TASK_INDEX.md (6 tasks)
- [ ] Evaluator list matches (6 evaluators)
- [ ] System prompt is clear and actionable
- [ ] README explains the domain purpose
- [ ] Error classification explained

---

## 📝 Output Format

**Submit via:**
1. Create `domains/gitlab_mlops/` with all files
2. Copy this file to `.cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/TASK_010_COMPLETE.md`
3. Update status to `COMPLETE`

**Example Completion:**
```markdown
# TASK 010: COMPLETE

**Agent:** Domain Architect  
**Time Taken:** 2.5 hours  
**Status:** ✅ COMPLETE

## Deliverables
- ✅ Created `domains/gitlab_mlops/` directory
- ✅ Created `config.yaml` with 6 tasks
- ✅ Created `README.md`
- ✅ Created `evaluators/` folder
- ✅ Created `tasks/` folder (empty)

## Testing
- ✅ YAML syntax valid
- ✅ All directories exist
- ✅ README renders correctly

## Blockers
None

## Next Tasks
- TASK_011 (Evaluator Infrastructure) - Ready
- TASK_012 (Tasks 1-3) - Ready
```

