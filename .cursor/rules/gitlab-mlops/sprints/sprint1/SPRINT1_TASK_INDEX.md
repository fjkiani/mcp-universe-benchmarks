# Sprint 1: Task Index

**Sprint Goal:** Ship GitLab MCP Server MVP with Module 1 (GitLab Orchestrator)  
**Timeline:** Week 1-2 (10-12 days)  
**Expected Outcome:** 8 tools, 6 tasks, 50% pass rate

---

## 📋 Task Structure

Each task is a standalone file with:
- **Inputs:** What the agent needs to read/understand
- **Outputs:** Exactly what files to create/modify
- **Acceptance Criteria:** Clear checklist
- **Testing:** How to validate the work
- **Review Checklist:** What Zo will verify

---

## 🎯 Task List (Total: 15 tasks)

### **Phase 1: Server Infrastructure** (TASK 001-009)

| Task ID | Task Name | Agent | Status | Time | Blocked By | Deliverable |
|---------|-----------|-------|--------|------|------------|-------------|
| TASK_001 | Server Structure | Backend Specialist | ✅ COMPLETE | 1h | - | 6 files in `servers/gitlab/` |
| TASK_002 | Tool: `create_project()` | MCP Builder | ✅ COMPLETE | 0.5h | 001 | Function in `server.py` |
| TASK_003 | Tool: `create_merge_request()` | MCP Builder | TODO | 2h | 001 | Function in `server.py` |
| TASK_004 | Tool: `assign_reviewers()` | MCP Builder | TODO | 2h | 001 | Function in `server.py` |
| TASK_005 | Tool: `create_issue()` | MCP Builder | TODO | 2h | 001 | Function in `server.py` |
| TASK_006 | Tool: `link_issues()` | MCP Builder | TODO | 2h | 001 | Function in `server.py` |
| TASK_007 | Tool: `get_pipeline_status()` | MCP Builder | TODO | 2h | 001 | Function in `server.py` |
| TASK_008 | Tool: `create_release()` | MCP Builder | TODO | 2h | 001 | Function in `server.py` |
| TASK_009 | Tool: `create_milestone()` | MCP Builder | TODO | 2h | 001 | Function in `server.py` |

**Total Phase 1 Time:** 20 hours (2.5 days if done sequentially, 1 day if parallel with 3 agents)

---

### **Phase 2: Domain Setup** (TASK 010-011)

| Task ID | Task Name | Agent | Status | Time | Blocked By | Deliverable |
|---------|-----------|-------|--------|------|------------|-------------|
| TASK_010 | Domain Structure | Domain Architect | TODO | 3h | 001 | Domain folder + `config.yaml` |
| TASK_011 | Evaluator Infrastructure | Domain Architect | TODO | 2h | 010 | `functions.py` + `error_types.py` |

**Total Phase 2 Time:** 5 hours (0.5 days)

---

### **Phase 3: Tasks & Evaluators** (TASK 012-014)

| Task ID | Task Name | Agent | Status | Time | Blocked By | Deliverable |
|---------|-----------|-------|--------|------|------------|-------------|
| TASK_012 | Tasks 1-3 (Moderate) | Task Designer | TODO | 3h | 010 | 3 JSON files |
| TASK_013 | Tasks 4-6 (Complex) | Task Designer | TODO | 3h | 010 | 3 JSON files |
| TASK_014 | Evaluators 1-6 | Evaluator Specialist | TODO | 6h | 011, 012, 013 | 6 functions in `functions.py` |

**Total Phase 3 Time:** 12 hours (1.5 days)

---

### **Phase 4: Validation** (TASK 015)

| Task ID | Task Name | Agent | Status | Time | Blocked By | Deliverable |
|---------|-----------|-------|--------|------|------------|-------------|
| TASK_015 | Local Validation | QA Specialist | TODO | 4h | ALL | `SPRINT1_RESULTS.md` |

**Total Phase 4 Time:** 4 hours (0.5 days)

---

## 📊 Parallel Execution Plan

### **Week 1 (Day 1-3):**

**Day 1:**
- Agent 1: TASK_001 (4h) → TASK_002 (2h)
- Agent 2: Standby → TASK_003 (2h) after Agent 1 finishes TASK_001
- Agent 3: TASK_010 (3h) in parallel with Agent 1

**Day 2:**
- Agent 1: TASK_004 (2h) → TASK_005 (2h) → TASK_006 (2h)
- Agent 2: TASK_007 (2h) → TASK_008 (2h) → TASK_009 (2h)
- Agent 3: TASK_011 (2h) → TASK_012 (3h)

**Day 3:**
- Agent 1: TASK_013 (3h)
- Agent 2: TASK_014 (6h) - Start after TASK_011 complete
- Agent 3: Help with TASK_014

**Day 4:**
- Agent 1: TASK_015 (4h) - Validation
- Agent 2: Documentation
- Agent 3: Testing support

**Result:** Sprint 1 complete in 4 days (vs 10-12 days sequential)

---

## 📁 File Structure After Sprint 1

```
lbx_mcp_universe_template-main/
├── lbx_mcp_universe_mcp_servers_mothership/
│   └── servers/
│       └── gitlab/
│           ├── pyproject.toml
│           ├── __init__.py
│           ├── __main__.py
│           ├── server_config.json
│           ├── README.md
│           ├── server.py                    # 8 tools
│           ├── test_create_project.py
│           └── ... (other test files)
│
├── domains/
│   └── gitlab_mlops/
│       ├── config.yaml
│       ├── README.md
│       ├── tasks/
│       │   ├── create_project_basic_001.json
│       │   ├── create_mr_basic_002.json
│       │   ├── assign_reviewers_003.json
│       │   ├── create_issue_link_004.json
│       │   ├── pipeline_status_check_005.json
│       │   └── create_release_milestone_006.json
│       └── evaluators/
│           ├── __init__.py
│           ├── error_types.py
│           └── functions.py                # 6 evaluators
│
└── .cursor/rules/gitlab-mlops/
    ├── MASTER.md
    ├── MANAGER.md
    └── sprints/
        └── sprint1/
            ├── SPRINT1_TASK_INDEX.md       # This file
            ├── tasks/                       # Task definitions
            │   ├── TASK_001_SERVER_STRUCTURE.md
            │   ├── TASK_002_TOOL_CREATE_PROJECT.md
            │   └── ... (13 more task files)
            └── deliverables/                # Completed tasks
                ├── TASK_001_COMPLETE.md
                └── ... (added as tasks complete)
```

---

## 🎯 Success Metrics

**Sprint 1 Complete When:**
- [ ] All 15 tasks marked `COMPLETE`
- [ ] All files in correct locations
- [ ] `uv run alignerr_mcp validate --domain gitlab_mlops` passes
- [ ] Test scripts run successfully
- [ ] `SPRINT1_RESULTS.md` created

**Expected Outcomes:**
- ✅ 8 MCP tools implemented
- ✅ 6 tasks created (3 moderate, 3 complex)
- ✅ 6 evaluators implemented with error classification
- ✅ 100% structure validation pass
- ✅ Ready for CI/CD testing in Sprint 2

---

## 📝 Task Completion Workflow

1. **Agent picks task** from TODO list
2. **Agent reads** task file in `tasks/` folder
3. **Agent implements** deliverables
4. **Agent tests** using provided test scripts
5. **Agent submits** by creating `TASK_XXX_COMPLETE.md` in `deliverables/`
6. **Zo reviews** using review checklist
7. **Update** this index: TODO → IN_PROGRESS → COMPLETE

---

## 🚀 Next Tasks to Create

I'll create all 15 task files now. Each will follow the pattern of TASK_001 and TASK_002:
- Clear inputs
- Exact outputs
- Acceptance criteria
- Testing instructions
- Review checklist

---

**Last Updated:** 2025-11-05  
**Status:** Task index created, individual task files in progress

