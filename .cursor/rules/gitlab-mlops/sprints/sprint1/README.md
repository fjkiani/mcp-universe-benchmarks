# Sprint 1: Task-Based Execution System

**Goal:** Ship GitLab MCP Server MVP with Module 1 (GitLab Orchestrator)  
**Timeline:** Week 1-2 (10-12 days, or 4 days with parallel execution)  
**Expected Outcome:** 8 tools, 6 tasks, 50% pass rate

---

## 📁 File Structure

```
.cursor/rules/gitlab-mlops/sprints/sprint1/
├── README.md                    # This file - Overview
├── SPRINT1_TASK_INDEX.md        # Task list with status tracking
├── tasks/                       # Task definitions (inputs/outputs)
│   ├── TASK_001_SERVER_STRUCTURE.md
│   ├── TASK_002_TOOL_CREATE_PROJECT.md
│   ├── TASK_003_TOOL_CREATE_MR.md
│   ├── TASK_004_TOOL_ASSIGN_REVIEWERS.md
│   ├── TASK_005_TOOL_CREATE_ISSUE.md
│   ├── TASK_006_TOOL_LINK_ISSUES.md
│   ├── TASK_007_TOOL_PIPELINE_STATUS.md
│   ├── TASK_008_TOOL_CREATE_RELEASE.md
│   ├── TASK_009_TOOL_CREATE_MILESTONE.md
│   ├── TASK_010_DOMAIN_STRUCTURE.md
│   ├── TASK_011_EVALUATOR_INFRASTRUCTURE.md
│   ├── TASK_012_TASKS_MODERATE.md
│   ├── TASK_013_TASKS_COMPLEX.md
│   ├── TASK_014_EVALUATORS.md
│   └── TASK_015_VALIDATION.md
└── deliverables/                # Completed tasks submitted here
    ├── TASK_001_COMPLETE.md
    └── ... (added as tasks complete)
```

---

## 🎯 How This System Works

### **1. Task Files = Actionable Work Items**
Each task file is a complete specification:
- **Inputs:** What files/docs to read
- **Outputs:** Exact code to write
- **Acceptance Criteria:** Checklist of requirements
- **Testing:** How to validate the work
- **Review Checklist:** What Zo will check

### **2. No Ambiguity**
- ✅ Exact file paths specified
- ✅ Complete code provided (not "implement this")
- ✅ Test scripts included
- ✅ Clear success criteria

### **3. Agent Workflow**
```
1. Pick task from SPRINT1_TASK_INDEX.md
2. Read task file (e.g., TASK_002_TOOL_CREATE_PROJECT.md)
3. Implement deliverables (create files, write code)
4. Run tests (validate work)
5. Submit TASK_XXX_COMPLETE.md to deliverables/
6. Zo reviews using checklist
7. Update task index: TODO → IN_PROGRESS → COMPLETE
```

### **4. Zo's Review Process**
For each completed task:
- [ ] All deliverables created in correct locations
- [ ] Code matches specification
- [ ] Tests run successfully
- [ ] No blockers or issues
- [ ] Ready for next dependent tasks

---

## 📊 Task Dependencies

```
TASK_001 (Server Structure)
    ├─→ TASK_002 (create_project)
    ├─→ TASK_003 (create_merge_request)
    ├─→ TASK_004 (assign_reviewers)
    ├─→ TASK_005 (create_issue)
    ├─→ TASK_006 (link_issues)
    ├─→ TASK_007 (get_pipeline_status)
    ├─→ TASK_008 (create_release)
    └─→ TASK_009 (create_milestone)

TASK_010 (Domain Structure) [Can run in parallel with TASK_001]
    └─→ TASK_011 (Evaluator Infrastructure)
        └─→ TASK_014 (Evaluators)

TASK_010 (Domain Structure)
    ├─→ TASK_012 (Tasks 1-3)
    └─→ TASK_013 (Tasks 4-6)

ALL TASKS COMPLETE → TASK_015 (Validation)
```

---

## 🚀 Parallel Execution Plan

**Day 1:**
- **Agent 1:** TASK_001 (4h) → TASK_002 (2h)
- **Agent 2:** Standby → TASK_003 (2h) after TASK_001 complete
- **Agent 3:** TASK_010 (3h) in parallel

**Day 2:**
- **Agent 1:** TASK_004 → TASK_005 → TASK_006
- **Agent 2:** TASK_007 → TASK_008 → TASK_009
- **Agent 3:** TASK_011 → TASK_012

**Day 3:**
- **Agent 1:** TASK_013
- **Agent 2:** TASK_014 (6h)
- **Agent 3:** Help with TASK_014

**Day 4:**
- **Agent 1:** TASK_015 (Validation)
- **Agents 2-3:** Documentation & testing support

**Result:** Sprint 1 complete in 4 days (vs 10-12 sequential)

---

## ✅ Success Criteria

**Sprint 1 Complete When:**
- [ ] All 15 tasks marked `COMPLETE` in index
- [ ] All deliverables in correct file locations
- [ ] All tests passing
- [ ] `uv run alignerr_mcp validate --domain gitlab_mlops` passes
- [ ] `SPRINT1_RESULTS.md` created

**Expected Outcomes:**
- ✅ 8 MCP tools implemented in `servers/gitlab/server.py`
- ✅ 6 task JSONs in `domains/gitlab_mlops/tasks/`
- ✅ 6 evaluators in `domains/gitlab_mlops/evaluators/functions.py`
- ✅ Error classification system working (`[parse_error]` / `[validation_error]`)
- ✅ 100% structure validation pass
- ✅ Ready for CI/CD testing in Sprint 2

---

## 📋 Current Status

**Total Tasks:** 15  
**Completed:** 0  
**In Progress:** 0  
**Blocked:** 0  
**TODO:** 15

**See:** `SPRINT1_TASK_INDEX.md` for detailed status

---

## 🎓 For New Agents

**First time working on this sprint?**

1. Read `SPRINT1_TASK_INDEX.md` - See all tasks and their status
2. Pick a task that's TODO and not blocked
3. Open that task file (e.g., `tasks/TASK_002_TOOL_CREATE_PROJECT.md`)
4. Follow the task specification exactly
5. Run the tests
6. Submit your completion file to `deliverables/`

**Questions?**
- See `../../MANAGER.md` for overall context
- See `../../MASTER.md` for product requirements
- Ask Zo for clarification

---

**Last Updated:** 2025-11-05  
**Status:** Task system ready, awaiting agent execution

