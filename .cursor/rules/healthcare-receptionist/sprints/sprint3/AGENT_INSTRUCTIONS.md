# Agent Instructions - Sprint 3: Task Expansion

**Copy and paste this entire file to agents in new tabs/conversations**

---

## 🎯 Your Mission

You are working on **Sprint 3** of the Healthcare Receptionist domain. Your goal is to create **one specific task** from the task list.

---

## 📋 Step-by-Step Instructions

### **Step 1: Check Available Tasks**

Open this file to see what tasks are available:
```
.cursor/rules/healthcare-receptionist/sprints/sprint3/SPRINT3_TASK_INDEX.md
```

Look for tasks with status **TODO** that are **not blocked**.

---

### **Step 2: Pick Your Task**

Choose one task from the available list. For example:
- `TASK_016` - Insurance Prior Auth (2 hours)
- `TASK_017` - Insurance Benefits Inquiry (2 hours)
- `TASK_024` - Orchestration Multi-Channel (3 hours)

**Tell me:** "I'm working on TASK_XXX"

---

### **Step 3: Read Your Task File**

Your task file is located at:
```
.cursor/rules/healthcare-receptionist/sprints/sprint3/tasks/TASK_XXX_*.md
```

This file contains:
- 🎯 **Inputs:** What files to review (reference tasks)
- 📤 **Outputs:** Exact JSON to create (complete code provided)
- ✅ **Acceptance Criteria:** Checklist of requirements
- 🧪 **Testing:** How to validate your work
- 🔍 **Review Checklist:** What Zo will verify

**Read the entire task file carefully.**

---

### **Step 4: Review Reference Tasks**

The task file will tell you which existing tasks to review. For example:
- `patient_intake_insurance_verification_003.json` - Insurance pattern
- `appointment_specialist_referral_010.json` - Referral workflow

**Read these reference tasks to understand the pattern.**

---

### **Step 5: Implement the Deliverable**

Follow the **Outputs** section in your task file **exactly**. The task file provides:
- Complete JSON structure
- All required fields
- Example values

**Do NOT deviate from the specification.**

Example:
- If task says create `insurance_prior_auth_016.json`, create it at that exact path
- If task provides JSON, use that exact structure
- If task specifies MCP servers, use those exact servers

---

### **Step 6: Test Your Work**

Run the test scripts provided in your task file.

Example for TASK_016:
```bash
# Validate JSON syntax
python3 -m json.tool domains/healthcare_receptionist/tasks/insurance_prior_auth_016.json
```

**All tests must pass before submitting.**

---

### **Step 7: Submit Your Completion**

Create a completion file in the deliverables folder:
```
.cursor/rules/healthcare-receptionist/sprints/sprint3/deliverables/TASK_XXX_COMPLETE.md
```

Use this format:
```markdown
# TASK XXX: COMPLETE

**Agent:** [Your Role]
**Time Taken:** [Hours]
**Status:** ✅ COMPLETE

## Deliverables
- ✅ [List file you created]

## Testing
- ✅ [Test results]

## Blockers
[None or list any issues]

## Next Task
[What task is now unblocked]
```

---

### **Step 8: Notify Zo**

After creating your completion file, say:
**"TASK_XXX is complete. Please review using the checklist in the task file."**

Zo will review and update the task index.

---

## ⚠️ Important Rules

1. **Follow the task file exactly** - The JSON is provided, use it as-is
2. **Don't skip testing** - All tests must pass
3. **Check dependencies** - Make sure your task isn't blocked
4. **One task at a time** - Complete one task fully before starting another
5. **Review reference tasks** - Understand the pattern before creating

---

## 🚫 Common Mistakes to Avoid

❌ **Don't** create files in wrong locations
❌ **Don't** modify the JSON structure provided in task files
❌ **Don't** skip the testing step
❌ **Don't** work on blocked tasks
❌ **Don't** work on tasks already IN_PROGRESS by another agent

✅ **Do** follow task file specifications exactly
✅ **Do** review reference tasks first
✅ **Do** run all tests before submitting
✅ **Do** check task dependencies
✅ **Do** ask questions if something is unclear

---

## 📚 Context Files (If You Need Background)

**Only read these if you need context. Focus on your task file first.**

- **Project Overview:** `.cursor/rules/healthcare-receptionist/MASTER.md`
- **Domain Config:** `domains/healthcare_receptionist/config.yaml`
- **Existing Tasks:** `domains/healthcare_receptionist/tasks/`
- **Evaluators:** `domains/healthcare_receptionist/evaluators/functions.py`

---

## 🎓 Example: Working on TASK_016

**Step 1:** Open `SPRINT3_TASK_INDEX.md`
- See TASK_016 is TODO
- See it's not blocked

**Step 2:** Say: "I'm working on TASK_016"

**Step 3:** Read `tasks/TASK_016_INSURANCE_PRIOR_AUTH.md`

**Step 4:** Review reference tasks:
- `patient_intake_insurance_verification_003.json`
- `appointment_specialist_referral_010.json`

**Step 5:** Implement:
- Create `domains/healthcare_receptionist/tasks/insurance_prior_auth_016.json`
- Use the exact JSON provided in the task file

**Step 6:** Test:
```bash
python3 -m json.tool domains/healthcare_receptionist/tasks/insurance_prior_auth_016.json
# Must see: Valid JSON
```

**Step 7:** Submit `deliverables/TASK_016_COMPLETE.md`

**Step 8:** Say: "TASK_016 complete. Please review."

---

## 🚀 Ready to Start?

1. Read `SPRINT3_TASK_INDEX.md`
2. Pick an available task
3. Tell me: "I'm working on TASK_XXX"
4. Follow your task file exactly
5. Test everything
6. Submit completion file

**Let's expand to 40 tasks!** 🎯



