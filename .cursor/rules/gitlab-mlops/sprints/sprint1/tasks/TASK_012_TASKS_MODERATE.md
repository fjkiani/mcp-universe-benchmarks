# TASK 012: Create Moderate Complexity Tasks (1-3)

**Agent:** Task Designer  
**Status:** TODO (Blocked by TASK_010)  
**Priority:** P2  
**Estimated Time:** 3 hours

---

## 📋 Task Definition

Create 3 moderate complexity task JSON files for the GitLab MLOps domain.

---

## 🎯 Inputs

**Reference Domains:**
1. `domains/healthcare_receptionist/tasks/patient_intake_basic_001.json` - Task structure
2. `domains/grant_application/tasks/` - Complexity examples
3. `.cursor/rules/gitlab-mlops/MASTER.md` - Requirements

**Task Requirements:**
- Complexity: Moderate
- Target Pass Rate: 100% (these should pass)
- MCP Server: `gitlab`
- Clear, achievable goals

---

## 📤 Outputs (Deliverables)

### 1. `domains/gitlab_mlops/tasks/create_project_basic_001.json`

```json
{
  "category": "project_management",
  "question": "Create a new GitLab project called 'ml-model-training' with description 'Machine learning model training pipeline'. Set visibility to private and initialize with README. Return JSON with project_id, project_url, and confirmation that README was initialized.",
  "output_format": {
    "project_id": 12345,
    "project_url": "https://gitlab.com/username/ml-model-training",
    "project_name": "ml-model-training",
    "visibility": "private",
    "initialized_with_readme": true
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "gitlab_mlops.validate_project_creation",
      "op_args": {}
    }
  ]
}
```

### 2. `domains/gitlab_mlops/tasks/create_mr_basic_002.json`

```json
{
  "category": "merge_requests",
  "question": "Create a merge request in project 'ml-model-training' (project_id: 12345) from branch 'feature/add-training-script' to branch 'main'. Title: 'Add initial training script'. Description: 'This MR adds the initial model training script for the ML pipeline.' Return JSON with mr_id, mr_url, source_branch, target_branch, and status.",
  "output_format": {
    "mr_id": 1,
    "mr_url": "https://gitlab.com/username/ml-model-training/-/merge_requests/1",
    "source_branch": "feature/add-training-script",
    "target_branch": "main",
    "title": "Add initial training script",
    "status": "opened"
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "gitlab_mlops.validate_mr_creation",
      "op_args": {}
    }
  ]
}
```

### 3. `domains/gitlab_mlops/tasks/assign_reviewers_003.json`

```json
{
  "category": "merge_requests",
  "question": "Assign reviewers to merge request #1 in project 'ml-model-training' (project_id: 12345). Assign user IDs: 100 (senior ML engineer) and 101 (DevOps engineer). Use intelligent assignment based on: 1) Code changes involve training scripts (ML expertise needed), 2) Pipeline configuration changes (DevOps expertise needed). Return JSON confirming reviewer assignment with reviewer_ids and their roles.",
  "output_format": {
    "mr_id": 1,
    "reviewers_assigned": true,
    "reviewer_ids": [100, 101],
    "assignments": [
      {"user_id": 100, "role": "ML Engineer", "reason": "Training script changes"},
      {"user_id": 101, "role": "DevOps Engineer", "reason": "Pipeline configuration"}
    ]
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "gitlab_mlops.validate_reviewer_assignment",
      "op_args": {}
    }
  ]
}
```

---

## ✅ Acceptance Criteria

1. **Files Created:**
   - [ ] All 3 JSON files created in `domains/gitlab_mlops/tasks/`
   - [ ] Valid JSON syntax
   - [ ] All required fields present

2. **Task Quality:**
   - [ ] Questions are clear and actionable
   - [ ] Output formats show expected structure
   - [ ] MCP servers specified correctly
   - [ ] Evaluators referenced correctly

3. **Complexity:**
   - [ ] Tasks are moderate (achievable, clear goals)
   - [ ] Expected pass rate: 100%

---

## 🧪 Testing

```bash
# Validate JSON syntax
python3 -m json.tool domains/gitlab_mlops/tasks/create_project_basic_001.json
python3 -m json.tool domains/gitlab_mlops/tasks/create_mr_basic_002.json
python3 -m json.tool domains/gitlab_mlops/tasks/assign_reviewers_003.json

# Validate structure
python3 local_tests/test_tasks.py --domain gitlab_mlops
```

---

## 📝 Output Format

**Submit via:**
1. Create all 3 JSON files
2. Submit `deliverables/TASK_012_COMPLETE.md`

**Example Completion:**
```markdown
# TASK 012: COMPLETE

**Agent:** Task Designer  
**Status:** ✅ COMPLETE

## Deliverables
- ✅ Created `create_project_basic_001.json`
- ✅ Created `create_mr_basic_002.json`
- ✅ Created `assign_reviewers_003.json`

## Testing
- ✅ All JSON valid
- ✅ Structure validated

## Next Task
Ready for TASK_013 (Complex tasks)
```




