# TASK 011: Evaluator Infrastructure

**Agent:** Domain Architect  
**Status:** TODO (Blocked by TASK 010)  
**Priority:** P1  
**Estimated Time:** 2 hours

---

## 📋 Task Definition

Create the evaluator infrastructure with error classification system.

---

## 🎯 Inputs

**Reference Files:**
1. `domains/healthcare_receptionist/evaluators/error_types.py` - Pattern to follow
2. `domains/healthcare_receptionist/evaluators/functions.py` - Reference implementation
3. Manager's feedback: "good idea, would be good to separate the two error classes"

---

## 📤 Outputs (Deliverables)

### 1. `domains/gitlab_mlops/evaluators/error_types.py`
```python
"""
Error Type Classification for Evaluators

Separates two error classes (Manager's request):
1. Parse/Infrastructure Errors (JSON parsing, data structure issues)
2. Validation/Business Logic Errors (LLM performance, task completion)
"""

from enum import Enum

class ErrorType(Enum):
    """Error classification types"""
    PARSE_ERROR = "parse_error"  # JSON parsing, data structure issues
    VALIDATION_ERROR = "validation_error"  # Business logic, LLM performance
```

### 2. `domains/gitlab_mlops/evaluators/functions.py`
```python
"""Evaluator functions for GitLab MLOps domain"""
from lbx_cli.mcpuniverse.evaluator.functions import compare_func
from typing import Tuple, Any
import json
from .error_types import ErrorType

def unwrap_pydantic_and_parse_json(agent_response: Any) -> Tuple[bool, Any, str]:
    """
    Unwrap Pydantic objects and parse JSON from agent response.
    
    This handles the common case where responses come wrapped in Pydantic
    FunctionResult objects with nested content structures.
    
    Returns:
        (success: bool, data: dict, error: str)
        - If success: (True, parsed_data, "")
        - If failure: (False, None, "[parse_error] error message")
    """
    try:
        # Handle Pydantic FunctionResult objects
        if hasattr(agent_response, 'content'):
            content = agent_response.content
            if isinstance(content, list) and len(content) > 0:
                first_item = content[0]
                if hasattr(first_item, 'text'):
                    text = first_item.text
                else:
                    text = str(first_item)
            else:
                text = str(content)
        else:
            text = str(agent_response)
        
        # Clean markdown code blocks
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        # Parse JSON
        data = json.loads(text)
        return True, data, ""
    
    except json.JSONDecodeError as e:
        error_msg = f"[{ErrorType.PARSE_ERROR.value}] JSON parsing failed: {str(e)}"
        return False, None, error_msg
    except Exception as e:
        error_msg = f"[{ErrorType.PARSE_ERROR.value}] Failed to extract response: {str(e)}"
        return False, None, error_msg


# ============================================
# EVALUATOR FUNCTIONS
# ============================================
# Individual evaluators will be added by TASK 014
# This file provides the infrastructure and helper functions


# Example evaluator pattern (not used yet):
# @compare_func(name="gitlab_mlops.example_evaluator")
# async def example_evaluator(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
#     """Example evaluator pattern"""
#     success, data, error = unwrap_pydantic_and_parse_json(llm_response)
#     if not success:
#         return False, error  # Already tagged with [parse_error]
#     
#     # VALIDATION ERRORS: Business logic checks
#     if 'required_field' not in data:
#         return False, f"[{ErrorType.VALIDATION_ERROR.value}] Missing required field"
#     
#     return True, "Validation passed"
```

---

## ✅ Acceptance Criteria

1. **Files Created:**
   - [ ] `error_types.py` created
   - [ ] `functions.py` created with helper function
   - [ ] Both files in `domains/gitlab_mlops/evaluators/`

2. **Error Classification:**
   - [ ] `ErrorType` enum defined
   - [ ] `PARSE_ERROR` for infrastructure issues
   - [ ] `VALIDATION_ERROR` for LLM performance issues
   - [ ] Helper function returns errors tagged with type

3. **Code Quality:**
   - [ ] Docstrings explain error separation
   - [ ] Helper function handles Pydantic objects
   - [ ] Helper function handles markdown code blocks
   - [ ] Returns tuple: `(success, data, error)`

---

## 🧪 Testing

Create `domains/gitlab_mlops/evaluators/test_infrastructure.py`:

```python
"""Test evaluator infrastructure"""
import json
from error_types import ErrorType
from functions import unwrap_pydantic_and_parse_json

def test_parse_json():
    """Test JSON parsing"""
    # Valid JSON
    response = '{"project_id": 123, "project_url": "https://gitlab.com"}'
    success, data, error = unwrap_pydantic_and_parse_json(response)
    assert success == True
    assert data["project_id"] == 123
    print("✅ Valid JSON parsing works")
    
    # JSON with markdown
    response = '```json\n{"project_id": 123}\n```'
    success, data, error = unwrap_pydantic_and_parse_json(response)
    assert success == True
    assert data["project_id"] == 123
    print("✅ Markdown code block parsing works")
    
    # Invalid JSON
    response = '{"invalid": json}'
    success, data, error = unwrap_pydantic_and_parse_json(response)
    assert success == False
    assert "[parse_error]" in error
    print("✅ Invalid JSON returns parse_error")
    
    print("\n✅ All infrastructure tests passed!")

if __name__ == "__main__":
    test_parse_json()
```

**Run test:**
```bash
cd domains/gitlab_mlops/evaluators
python test_infrastructure.py
```

---

## 🔍 Review Checklist (for Zo)

- [ ] `error_types.py` defines both error types
- [ ] `functions.py` has `unwrap_pydantic_and_parse_json` helper
- [ ] Helper function handles all edge cases
- [ ] Errors are tagged with `[parse_error]` or `[validation_error]`
- [ ] Docstrings explain the error separation
- [ ] Test script runs successfully
- [ ] Code follows healthcare_receptionist pattern

---

## 📝 Output Format

**Submit via:**
1. Create both files in `domains/gitlab_mlops/evaluators/`
2. Create test script
3. Copy this file to `.cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/TASK_011_COMPLETE.md`
4. Update status to `COMPLETE`
5. Include test results

**Example Completion:**
```markdown
# TASK 011: COMPLETE

**Agent:** Domain Architect  
**Time Taken:** 1.5 hours  
**Status:** ✅ COMPLETE

## Deliverables
- ✅ Created `error_types.py`
- ✅ Created `functions.py` with helper
- ✅ Created test script
- ✅ All tests pass

## Test Results
```
✅ Valid JSON parsing works
✅ Markdown code block parsing works
✅ Invalid JSON returns parse_error

✅ All infrastructure tests passed!
```

## Code Stats
- Files created: 2
- Functions: 1 helper
- Error types: 2

## Blockers
None

## Next Task
Ready for TASK_014 (individual evaluators)
```




