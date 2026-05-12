# Agent Instructions - Sprint 1: GitLab MCP Server MVP

**Copy and paste this entire file to agents in new tabs/conversations**

---

## 🎯 Your Mission

You are working on **Sprint 1** of the GitLab MLOps Automation domain. Your goal is to implement **one specific task** from the task list.

---

## 📋 Step-by-Step Instructions

### **Step 1: Check Available Tasks**

Open this file to see what tasks are available:
```
.cursor/rules/gitlab-mlops/sprints/sprint1/SPRINT1_TASK_INDEX.md
```

Look for tasks with status **TODO** that are **not blocked**.

---

### **Step 2: Pick Your Task**

Choose one task from the available list. For example:
- `TASK_001` - Server Structure (4 hours)
- `TASK_002` - Tool: create_project() (2 hours)
- `TASK_010` - Domain Structure (3 hours) - Can run in parallel with TASK_001

**Tell me:** "I'm working on TASK_XXX"

---

### **Step 3: Read Your Task File**

Your task file is located at:
```
.cursor/rules/gitlab-mlops/sprints/sprint1/tasks/TASK_XXX_*.md
```

This file contains:
- 🎯 **Inputs:** What files to review
- 📤 **Outputs:** Exact code to write (complete implementation provided)
- ✅ **Acceptance Criteria:** Checklist of requirements
- 🧪 **Testing:** How to validate your work
- 🔍 **Review Checklist:** What Zo will verify

**Read the entire task file carefully.**

---

### **Step 4: Implement the Deliverables**

Follow the **Outputs** section in your task file **exactly**. The task file provides:
- Complete file paths where to create files
- Full code to implement (not just descriptions)
- All configuration needed

**Do NOT deviate from the specification.**

Example:
- If task says create `servers/gitlab/server.py`, create it at that exact path
- If task provides a code block, use that exact code
- If task specifies dependencies, use those exact versions

---

### **Step 5: Test Your Work**

Run the test scripts provided in your task file.

Example for TASK_002:
```bash
cd servers/gitlab
python test_create_project.py
```

**All tests must pass before submitting.**

---

### **Step 6: Submit Your Completion**

Create a completion file in the deliverables folder:
```
.cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/TASK_XXX_COMPLETE.md
```

Use this format:
```markdown
# TASK XXX: COMPLETE

**Agent:** [Your Role]
**Time Taken:** [Hours]
**Status:** ✅ COMPLETE

## Deliverables
- ✅ [List each file you created]
- ✅ [And what you implemented]

## Testing
- ✅ [Test results]

## Blockers
[None or list any issues]

## Next Task
[What task is now unblocked]
```

---

### **Step 7: Notify Zo**

After creating your completion file, say:
**"TASK_XXX is complete. Please review using the checklist in the task file."**

Zo will review and update the task index.

---

## ⚠️ Important Rules

1. **Follow the task file exactly** - The code is provided, implement it as-is
2. **Don't skip testing** - All tests must pass
3. **Check dependencies** - Make sure your task isn't blocked
4. **One task at a time** - Complete one task fully before starting another
5. **Ask if unclear** - If something in the task file is confusing, ask Zo

---

## 🚫 Common Mistakes to Avoid

❌ **Don't** create files in wrong locations
❌ **Don't** modify the code provided in task files
❌ **Don't** skip the testing step
❌ **Don't** work on blocked tasks
❌ **Don't** work on tasks already IN_PROGRESS by another agent

✅ **Do** follow task file specifications exactly
✅ **Do** run all tests before submitting
✅ **Do** check task dependencies
✅ **Do** ask questions if something is unclear

---

## 📚 Context Files (If You Need Background)

**Only read these if you need context. Focus on your task file first.**

- **Project Overview:** `.cursor/rules/gitlab-mlops/MASTER.md`
- **Manager Document:** `.cursor/rules/gitlab-mlops/MANAGER.md`
- **Sprint Overview:** `.cursor/rules/gitlab-mlops/sprints/sprint1/README.md`

---

## 🎓 Example: Working on TASK_002

**Step 1:** Open `SPRINT1_TASK_INDEX.md`
- See TASK_002 is TODO
- See it's blocked by TASK_001
- Wait for TASK_001 to complete, or pick a different task

**Step 2:** Say: "I'm working on TASK_002"

**Step 3:** Read `tasks/TASK_002_TOOL_CREATE_PROJECT.md`

**Step 4:** Implement:
- Add `create_project()` function to `servers/gitlab/server.py`
- Use the exact code provided in the task file
- Create the test script

**Step 5:** Test:
```bash
cd servers/gitlab
python test_create_project.py
# Must see: ✅ All tests passed!
```

**Step 6:** Submit `deliverables/TASK_002_COMPLETE.md`

**Step 7:** Say: "TASK_002 complete. Please review."

---

## 🚀 Ready to Start?

1. Read `SPRINT1_TASK_INDEX.md`
2. Pick an available task
3. Tell me: "I'm working on TASK_XXX"
4. Follow your task file exactly
5. Test everything
6. Submit completion file

**Let's ship this MVP!** 🎯

