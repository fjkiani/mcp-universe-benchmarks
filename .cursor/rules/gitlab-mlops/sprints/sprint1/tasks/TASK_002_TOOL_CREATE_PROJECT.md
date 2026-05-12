# TASK 002: Implement `create_project()` Tool

**Agent:** MCP Server Builder  
**Status:** TODO (Blocked by TASK 001)  
**Priority:** P2  
**Estimated Time:** 2 hours

---

## 📋 Task Definition

Implement the `create_project()` tool in the GitLab MCP server.

---

## 🎯 Inputs

**Required Files:**
1. `servers/gitlab/server.py` - Add tool here
2. GitLab API Docs: https://docs.gitlab.com/ee/api/projects.html#create-project

**API Specification:**
- **Endpoint:** `POST /api/v4/projects`
- **Auth:** Header `PRIVATE-TOKEN: {GITLAB_TOKEN}`
- **Required Params:** `name`
- **Optional Params:** `description`, `visibility`, `initialize_with_readme`

**API Response Example:**
```json
{
  "id": 123,
  "name": "ml-model-training",
  "web_url": "https://gitlab.com/username/ml-model-training",
  "created_at": "2025-11-05T10:00:00Z",
  "visibility": "private"
}
```

---

## 📤 Output (Deliverable)

Add this function to `servers/gitlab/server.py`:

```python
@mcp.tool()
async def create_project(
    name: str,
    description: str = "",
    visibility: str = "private",
    initialize_with_readme: bool = True
) -> str:
    """
    Create a new GitLab project.
    
    Args:
        name: Project name (required)
        description: Project description (optional)
        visibility: Project visibility - 'private', 'internal', or 'public' (default: 'private')
        initialize_with_readme: Initialize with README.md (default: True)
    
    Returns:
        JSON string with project_id, project_url, project_name, visibility, created_at
    
    Example:
        >>> result = await create_project(
        ...     name="ml-model-training",
        ...     description="Machine learning model training pipeline",
        ...     visibility="private"
        ... )
        >>> print(result)
        {"project_id": 123, "project_url": "https://...", ...}
    """
    if not GITLAB_TOKEN:
        return json.dumps({
            "error": "GITLAB_TOKEN not set",
            "success": False
        })
    
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {
        "name": name,
        "description": description,
        "visibility": visibility,
        "initialize_with_readme": initialize_with_readme
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GITLAB_URL}/api/v4/projects",
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            project = response.json()
            
            return json.dumps({
                "success": True,
                "project_id": project["id"],
                "project_url": project["web_url"],
                "project_name": project["name"],
                "visibility": project["visibility"],
                "initialized_with_readme": initialize_with_readme,
                "created_at": project["created_at"]
            })
    
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error": f"GitLab API error: {e.response.status_code} - {e.response.text}",
            "success": False
        })
    except Exception as e:
        return json.dumps({
            "error": f"Failed to create project: {str(e)}",
            "success": False
        })
```

---

## ✅ Acceptance Criteria

1. **Implementation:**
   - [ ] Function decorated with `@mcp.tool()`
   - [ ] All 4 parameters implemented
   - [ ] Docstring with examples
   - [ ] Error handling for missing token
   - [ ] HTTP error handling
   - [ ] Returns JSON string

2. **Testing:**
   - [ ] Function can be imported
   - [ ] Function signature matches specification
   - [ ] Returns valid JSON string

3. **Code Quality:**
   - [ ] Type hints for all parameters
   - [ ] Clear error messages
   - [ ] Follows reference pattern from `nexhealth` server

---

## 🧪 Testing Script

Create `servers/gitlab/test_create_project.py`:

```python
import asyncio
import json
from dotenv import load_dotenv
from server import create_project

load_dotenv()

async def test_create_project():
    """Test create_project tool"""
    result = await create_project(
        name="test-project-mvp",
        description="Test project for MVP",
        visibility="private"
    )
    
    data = json.loads(result)
    print(f"✅ Success: {data.get('success')}")
    print(f"📦 Project ID: {data.get('project_id')}")
    print(f"🔗 URL: {data.get('project_url')}")
    
    assert data.get('success') == True
    assert 'project_id' in data
    assert 'project_url' in data
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_create_project())
```

**Run test:**
```bash
cd servers/gitlab
python test_create_project.py
```

---

## 🔍 Review Checklist (for Zo)

- [ ] Function added to `server.py`
- [ ] All parameters match specification
- [ ] Docstring is complete
- [ ] Error handling covers all cases
- [ ] Returns JSON string (not dict)
- [ ] Test script runs successfully
- [ ] No hardcoded values (uses env vars)

---

## 📝 Output Format

**Submit via:**
1. Update `servers/gitlab/server.py` with new tool
2. Create `servers/gitlab/test_create_project.py`
3. Copy this file to `.cursor/rules/gitlab-mlops/sprints/sprint1/deliverables/TASK_002_COMPLETE.md`
4. Update status to `COMPLETE`
5. Include test results

**Example Completion:**
```markdown
# TASK 002: COMPLETE

**Agent:** MCP Server Builder  
**Time Taken:** 1.5 hours  
**Status:** ✅ COMPLETE

## Deliverables
- ✅ Implemented `create_project()` in `servers/gitlab/server.py`
- ✅ Added docstring with examples
- ✅ Added error handling
- ✅ Created test script

## Test Results
```
✅ Success: True
📦 Project ID: 12345
🔗 URL: https://gitlab.com/username/test-project-mvp

✅ All tests passed!
```

## Code Stats
- Lines added: 45
- Functions: 1
- Tests: 1

## Blockers
None

## Next Task
Ready for TASK 003 (create_merge_request tool)
```

