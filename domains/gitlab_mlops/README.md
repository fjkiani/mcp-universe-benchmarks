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






