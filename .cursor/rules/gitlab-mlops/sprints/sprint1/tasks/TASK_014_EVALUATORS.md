# TASK 014: Implement Evaluator Functions

**Agent:** Evaluator Specialist  
**Status:** TODO (Blocked by TASK_011, TASK_012, TASK_013)  
**Priority:** P2  
**Estimated Time:** 6 hours

---

## 📋 Task Definition

Implement 6 evaluator functions for the GitLab MLOps tasks.

---

## 🎯 Inputs

**Reference:**
1. `domains/healthcare_receptionist/evaluators/functions.py` - Pattern to follow
2. `domains/gitlab_mlops/evaluators/error_types.py` - Already created in TASK_011
3. `domains/gitlab_mlops/evaluators/functions.py` - Add evaluators here

**Requirements:**
- Use `@compare_func` decorator
- Use `unwrap_pydantic_and_parse_json` helper
- Implement error classification (`[parse_error]` vs `[validation_error]`)

---

## 📤 Output (Deliverable)

Add these 6 functions to `domains/gitlab_mlops/evaluators/functions.py`:

```python
@compare_func(name="gitlab_mlops.validate_project_creation")
async def validate_project_creation(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate GitLab project creation (TASK_001)"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error  # Already tagged with [parse_error]
    
    # VALIDATION ERRORS: Business logic
    required_fields = ['project_id', 'project_url', 'project_name', 'visibility', 'initialized_with_readme']
    for field in required_fields:
        if field not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] Missing required field: {field}"
    
    # Check project_id is numeric
    if not isinstance(data.get('project_id'), (int, str)):
        return False, f"[{ErrorType.VALIDATION_ERROR}] project_id must be numeric"
    
    # Check visibility
    if data.get('visibility') not in ['private', 'internal', 'public']:
        return False, f"[{ErrorType.VALIDATION_ERROR}] visibility must be 'private', 'internal', or 'public'"
    
    # Check initialized_with_readme is boolean
    if not isinstance(data.get('initialized_with_readme'), bool):
        return False, f"[{ErrorType.VALIDATION_ERROR}] initialized_with_readme must be boolean"
    
    return True, "Project creation validated"


@compare_func(name="gitlab_mlops.validate_mr_creation")
async def validate_mr_creation(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate merge request creation (TASK_002)"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    required_fields = ['mr_id', 'mr_url', 'source_branch', 'target_branch', 'title', 'status']
    for field in required_fields:
        if field not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] Missing required field: {field}"
    
    # Check branches are different
    if data.get('source_branch') == data.get('target_branch'):
        return False, f"[{ErrorType.VALIDATION_ERROR}] source_branch and target_branch must be different"
    
    # Check status
    valid_statuses = ['opened', 'merged', 'closed', 'locked']
    if data.get('status') not in valid_statuses:
        return False, f"[{ErrorType.VALIDATION_ERROR}] status must be one of: {valid_statuses}"
    
    return True, "MR creation validated"


@compare_func(name="gitlab_mlops.validate_reviewer_assignment")
async def validate_reviewer_assignment(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate reviewer assignment (TASK_003)"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    required_fields = ['mr_id', 'reviewers_assigned', 'reviewer_ids']
    for field in required_fields:
        if field not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] Missing required field: {field}"
    
    # Check reviewers_assigned is boolean
    if not isinstance(data.get('reviewers_assigned'), bool):
        return False, f"[{ErrorType.VALIDATION_ERROR}] reviewers_assigned must be boolean"
    
    # Check reviewer_ids is list
    if not isinstance(data.get('reviewer_ids'), list):
        return False, f"[{ErrorType.VALIDATION_ERROR}] reviewer_ids must be a list"
    
    # Check at least 1 reviewer
    if len(data.get('reviewer_ids', [])) < 1:
        return False, f"[{ErrorType.VALIDATION_ERROR}] Must assign at least 1 reviewer"
    
    return True, "Reviewer assignment validated"


@compare_func(name="gitlab_mlops.validate_issue_creation_and_link")
async def validate_issue_creation_and_link(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate issue creation and linking (TASK_004) - Complex"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    required_fields = ['issue_id', 'issue_url', 'title', 'labels', 'linked_to_mr', 'link_type', 'mr_id']
    for field in required_fields:
        if field not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] Missing required field: {field}"
    
    # Check labels is list with at least 1 label
    if not isinstance(data.get('labels'), list) or len(data.get('labels', [])) < 1:
        return False, f"[{ErrorType.VALIDATION_ERROR}] labels must be a list with at least 1 label"
    
    # Check linked_to_mr
    if not isinstance(data.get('linked_to_mr'), bool):
        return False, f"[{ErrorType.VALIDATION_ERROR}] linked_to_mr must be boolean"
    
    # If linked, check link_type
    if data.get('linked_to_mr'):
        valid_link_types = ['relates_to', 'blocks', 'is_blocked_by']
        if data.get('link_type') not in valid_link_types:
            return False, f"[{ErrorType.VALIDATION_ERROR}] link_type must be one of: {valid_link_types}"
    
    return True, "Issue creation and linking validated"


@compare_func(name="gitlab_mlops.validate_pipeline_status_check")
async def validate_pipeline_status_check(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate pipeline status check (TASK_005) - Complex"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    required_fields = ['pipeline_id', 'status']
    for field in required_fields:
        if field not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] Missing required field: {field}"
    
    # Check status
    valid_statuses = ['running', 'pending', 'success', 'failed', 'canceled', 'skipped']
    if data.get('status') not in valid_statuses:
        return False, f"[{ErrorType.VALIDATION_ERROR}] status must be one of: {valid_statuses}"
    
    # If failed, check for failure analysis
    if data.get('status') == 'failed':
        if 'failed_jobs' not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] For failed pipelines, must include failed_jobs"
        if 'failure_reasons' not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] For failed pipelines, must include failure_reasons"
    
    return True, "Pipeline status check validated"


@compare_func(name="gitlab_mlops.validate_release_and_milestone")
async def validate_release_and_milestone(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate release and milestone creation (TASK_006) - Complex"""
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, error
    
    required_fields = ['milestone_id', 'milestone_title', 'release_tag', 'release_name', 'milestone_linked']
    for field in required_fields:
        if field not in data:
            return False, f"[{ErrorType.VALIDATION_ERROR}] Missing required field: {field}"
    
    # Check dates if provided
    if 'start_date' in data and 'due_date' in data:
        # Basic date format check (YYYY-MM-DD)
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, data.get('start_date', '')):
            return False, f"[{ErrorType.VALIDATION_ERROR}] start_date must be in YYYY-MM-DD format"
        if not re.match(date_pattern, data.get('due_date', '')):
            return False, f"[{ErrorType.VALIDATION_ERROR}] due_date must be in YYYY-MM-DD format"
    
    # Check milestone_linked is boolean
    if not isinstance(data.get('milestone_linked'), bool):
        return False, f"[{ErrorType.VALIDATION_ERROR}] milestone_linked must be boolean"
    
    return True, "Release and milestone validated"
```

---

## ✅ Acceptance Criteria

1. **Implementation:**
   - [ ] All 6 evaluators added
   - [ ] All use `@compare_func`
   - [ ] All use error classification
   - [ ] All return `(bool, str)` tuple

2. **Testing:**
   - [ ] Can import all functions
   - [ ] Functions have correct signatures

---

## 🧪 Testing

```bash
# Test imports
python3 -c "from domains.gitlab_mlops.evaluators.functions import validate_project_creation"
python3 -c "from domains.gitlab_mlops.evaluators.functions import validate_mr_creation"
```

---

## 📝 Output Format

**Submit via:**
1. Update `domains/gitlab_mlops/evaluators/functions.py`
2. Submit `deliverables/TASK_014_COMPLETE.md`

