# Zo's Sprint Management Guide

**How to manage multiple agents working on Sprint 1**

---

## 🎯 Your Role

You are the **Sprint Manager** coordinating multiple agents to complete Sprint 1 tasks in parallel.

---

## 📋 Daily Workflow

### **Morning: Assign Tasks**

1. **Review Current Status**
   ```bash
   # Check what's complete
   ls -la .cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/
   
   # Review task index
   cat .cursor/rules/gitlab-mlops/sprints/sprint1/SPRINT1_TASK_INDEX.md
   ```

2. **Identify Available Tasks**
   - Tasks that are TODO
   - Tasks that are NOT blocked by incomplete dependencies
   - Tasks not already assigned to another agent

3. **Assign to Agents**
   - Open new tab/conversation with agent
   - Paste prompt from `PROMPT_FOR_AGENTS.txt`
   - Or directly assign: "Agent X, you are assigned TASK_005. Read the task file and begin."

---

### **During Day: Monitor Progress**

**When agent says "I'm working on TASK_XXX":**
1. ✅ Verify task is not blocked
2. ✅ Update `SPRINT1_TASK_INDEX.md`: TODO → IN_PROGRESS
3. ✅ Note which agent is working on it
4. ✅ Confirm agent has read the task file

**If agent asks questions:**
- First: "Did you read the task file completely?"
- Then: Answer based on task specification
- Avoid: Changing the spec (stick to what's in the task file)

---

### **When Agent Submits Completion:**

Agent should say: **"TASK_XXX is complete. Please review."**

**Your Review Process:**

1. **Check Deliverable File Exists**
   ```bash
   cat .cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/TASK_XXX_COMPLETE.md
   ```

2. **Review Using Task Checklist**
   - Open the original task file: `tasks/TASK_XXX_*.md`
   - Go to "🔍 Review Checklist" section
   - Verify each item

3. **Verify Files Created**
   ```bash
   # Example for TASK_001
   ls -la lbx_mcp_universe_mcp_servers_mothership/servers/gitlab/
   
   # Example for TASK_002
   cat lbx_mcp_universe_mcp_servers_mothership/servers/gitlab/server.py
   ```

4. **Run Tests**
   ```bash
   # Run the test scripts mentioned in task file
   cd servers/gitlab
   python test_create_project.py
   ```

5. **Update Task Index**
   - Change status: IN_PROGRESS → COMPLETE
   - Note completion time
   - Update any newly unblocked tasks

---

## 📊 Parallel Execution Strategy

### **Day 1 Plan:**

**Agent 1 (Backend Specialist):**
```
Morning: TASK_001 (4 hours)
Afternoon: TASK_002 (2 hours)
```

**Agent 2 (MCP Builder):**
```
Morning: Wait for TASK_001
Afternoon: TASK_003 (2 hours)
```

**Agent 3 (Domain Architect):**
```
Morning: TASK_010 (3 hours) - Parallel with TASK_001
Afternoon: TASK_011 (2 hours)
```

### **Assign Tasks Like This:**

**To Agent 1:**
> "Agent 1, you are Backend Specialist. Start with TASK_001 (Server Structure).
> 
> Read: .cursor/rules/gitlab-mlops/sprints/sprint1/tasks/TASK_001_SERVER_STRUCTURE.md
> 
> Implement exactly as specified, then submit completion file."

**To Agent 3 (Parallel):**
> "Agent 3, you are Domain Architect. Start with TASK_010 (Domain Structure).
> 
> This can run in parallel with TASK_001.
> 
> Read: .cursor/rules/gitlab-mlops/sprints/sprint1/tasks/TASK_010_DOMAIN_STRUCTURE.md"

---

## ⚠️ Common Issues & Solutions

### **Issue: Agent says "Task file is too long"**
**Solution:** "Focus on the Outputs section. That's what you need to implement. Everything else is context."

### **Issue: Agent wants to modify the spec**
**Solution:** "Follow the task file exactly as written. If you see an issue, note it in your completion file under 'Blockers' but implement as specified."

### **Issue: Tests fail**
**Solution:** "Review the Acceptance Criteria in the task file. What's missing? Fix it before submitting."

### **Issue: Agent is blocked**
**Solution:** "This task is blocked by TASK_XXX. Pick a different task from the TODO list, or wait for TASK_XXX to complete."

### **Issue: Two agents pick same task**
**Solution:** "Agent 2, TASK_005 is already IN_PROGRESS by Agent 1. Pick a different TODO task. See SPRINT1_TASK_INDEX.md for available tasks."

---

## 📈 Progress Tracking

### **Quick Status Check:**

```bash
# Count completed tasks
ls .cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/ | wc -l

# Count total tasks (should be 15)
ls .cursor/rules/gitlab-mlops/sprints/sprint1/tasks/ | wc -l

# View index status
grep -E "TODO|IN_PROGRESS|COMPLETE" .cursor/rules/gitlab-mlops/sprints/sprint1/SPRINT1_TASK_INDEX.md
```

### **Update Manager on Progress:**

Daily update format:
```markdown
## Sprint 1 Progress - Day X

**Completed:** X/15 tasks
**In Progress:** X tasks
**Blocked:** X tasks

**Completed Today:**
- TASK_001: Server Structure ✅
- TASK_010: Domain Structure ✅

**In Progress:**
- TASK_002: create_project() (Agent 1)
- TASK_011: Evaluator Infrastructure (Agent 3)

**Blockers:**
None

**Tomorrow's Plan:**
- Complete TASK_002-009 (all tools)
- Start TASK_012-013 (tasks)
```

---

## ✅ Sprint 1 Complete When:

- [ ] All 15 tasks COMPLETE in index
- [ ] 15 completion files in `deliverables/`
- [ ] All files created in correct locations:
  - [ ] `servers/gitlab/` with 8 tools
  - [ ] `domains/gitlab_mlops/` with config
  - [ ] `domains/gitlab_mlops/tasks/` with 6 JSONs
  - [ ] `domains/gitlab_mlops/evaluators/` with functions
- [ ] All tests passing
- [ ] `TASK_015` validation complete
- [ ] `SPRINT1_RESULTS.md` created

**Then:** Ready for Sprint 2 (CI/CD testing)

---

## 🎯 Success Metrics

**Efficiency:**
- Sequential: 10-12 days
- Parallel (3 agents): 4 days
- **Goal:** Complete in 4 days

**Quality:**
- 100% structure validation pass
- All tests passing
- Error classification working
- Ready for CI/CD

---

**Remember:** Your job is to coordinate, not implement. Agents implement. You review and unblock.

