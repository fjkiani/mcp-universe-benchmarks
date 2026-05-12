# TASK 013: Create Complex Tasks (4-6)

**Agent:** Task Designer  
**Status:** TODO (Blocked by TASK_010)  
**Priority:** P2  
**Estimated Time:** 3 hours

---

## 📋 Task Definition

Create 3 complex task JSON files for the GitLab MLOps domain.

---

## 🎯 Inputs

**Reference:**
1. `domains/healthcare_receptionist/tasks/triage_stroke_symptoms_029.json` - Complex task pattern
2. `.cursor/rules/gitlab-mlops/MASTER.md` - Requirements

**Task Requirements:**
- Complexity: Complex
- Target Pass Rate: 0% (these should fail - discriminative)
- MCP Server: `gitlab`
- Multi-step workflows, edge cases

---

## 📤 Outputs (Deliverables)

### 1. `domains/gitlab_mlops/tasks/create_issue_link_004.json`

```json
{
  "category": "issues",
  "question": "Create an issue in project 'ml-model-training' (project_id: 12345) with title 'Implement data preprocessing pipeline' and description 'Need to add data preprocessing before training. This includes: data validation, normalization, and feature engineering.' Add labels: 'enhancement', 'ml-pipeline', 'high-priority'. Assign to user_id: 100. Then link this issue to merge request #1 with link_type 'relates_to' to show the MR is related to this issue. Return JSON with issue_id, issue_url, labels, assignee, and link confirmation.",
  "output_format": {
    "issue_id": 5,
    "issue_url": "https://gitlab.com/username/ml-model-training/-/issues/5",
    "title": "Implement data preprocessing pipeline",
    "labels": ["enhancement", "ml-pipeline", "high-priority"],
    "assignee_id": 100,
    "linked_to_mr": true,
    "link_type": "relates_to",
    "mr_id": 1
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "gitlab_mlops.validate_issue_creation_and_link",
      "op_args": {}
    }
  ]
}
```

### 2. `domains/gitlab_mlops/tasks/pipeline_status_check_005.json`

```json
{
  "category": "ci_cd",
  "question": "Check the status of pipeline #789 in project 'ml-model-training' (project_id: 12345). If the pipeline is 'failed', analyze which jobs failed and return detailed information: failed_jobs (list of job names), failure_reasons, and recommendations for fixes. If pipeline is 'running', return estimated completion time. If 'success', return job durations. Return comprehensive JSON with pipeline_id, status, and relevant details based on status.",
  "output_format": {
    "pipeline_id": 789,
    "status": "failed",
    "failed_jobs": ["test:unit", "build:docker"],
    "failure_reasons": {
      "test:unit": "Test case test_preprocessing failed: AssertionError",
      "build:docker": "Docker build failed: base image not found"
    },
    "recommendations": [
      "Fix failing unit test in test_preprocessing.py",
      "Update Dockerfile base image to python:3.9-slim"
    ],
    "total_duration": "5m 32s"
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "gitlab_mlops.validate_pipeline_status_check",
      "op_args": {}
    }
  ]
}
```

### 3. `domains/gitlab_mlops/tasks/create_release_milestone_006.json`

```json
{
  "category": "project_management",
  "question": "Create a milestone in project 'ml-model-training' (project_id: 12345) with title 'v1.0 - Initial Release', description 'First production release of the ML training pipeline', start_date '2025-11-01', and due_date '2025-11-30'. Then create a release with tag 'v1.0.0', name 'Version 1.0 - Production Ready', and description 'Release notes: - Initial training pipeline, - Data preprocessing, - Model evaluation metrics, - Docker deployment'. Link the release to the milestone. Return JSON with milestone_id, milestone_url, release_tag, release_url, and confirmation that they are linked.",
  "output_format": {
    "milestone_id": 10,
    "milestone_title": "v1.0 - Initial Release",
    "milestone_url": "https://gitlab.com/username/ml-model-training/-/milestones/10",
    "start_date": "2025-11-01",
    "due_date": "2025-11-30",
    "release_tag": "v1.0.0",
    "release_name": "Version 1.0 - Production Ready",
    "release_url": "https://gitlab.com/username/ml-model-training/-/releases/v1.0.0",
    "milestone_linked": true
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "gitlab"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "gitlab_mlops.validate_release_and_milestone",
      "op_args": {}
    }
  ]
}
```

---

## ✅ Acceptance Criteria

1. **Files Created:**
   - [ ] All 3 JSON files created
   - [ ] Valid JSON syntax

2. **Complexity:**
   - [ ] Multi-step workflows
   - [ ] Edge case handling
   - [ ] Expected pass rate: 0% (discriminative)

---

## 🧪 Testing

```bash
# Validate JSON
python3 -m json.tool domains/gitlab_mlops/tasks/create_issue_link_004.json
python3 -m json.tool domains/gitlab_mlops/tasks/pipeline_status_check_005.json
python3 -m json.tool domains/gitlab_mlops/tasks/create_release_milestone_006.json
```

---

## 📝 Output Format

**Submit via:**
1. Create all 3 JSON files
2. Submit `deliverables/TASK_013_COMPLETE.md`




