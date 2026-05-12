# TASK 003: Implement `create_merge_request()` Tool

**Agent:** MCP Server Builder  
**Status:** TODO (Blocked by TASK_001)  
**Priority:** P2  
**Estimated Time:** 2 hours

---

## 📋 Task Definition

Implement the `create_merge_request()` tool in the GitLab MCP server.

---

## 🎯 Inputs

**Required Files:**
1. `servers/gitlab/server.py` - Add tool here (after TASK_002)
2. GitLab API Docs: https://docs.gitlab.com/ee/api/merge_requests.html#create-mr

**API Specification:**
- **Endpoint:** `POST /api/v4/projects/:id/merge_requests`
- **Auth:** Header `PRIVATE-TOKEN: {GITLAB_TOKEN}`
- **Required Params:** `source_branch`, `target_branch`, `title`
- **Optional Params:** `description`, `assignee_id`, `reviewer_ids`

---

## 📤 Output (Deliverable)

Add this function to `servers/gitlab/server.py`:

```python
@mcp.tool()
async def create_merge_request(
    project_id: str,
    source_branch: str,
    target_branch: str,
    title: str,
    description: str = "",
    assignee_id: int = None,
    reviewer_ids: list = None
) -> str:
    """
    Create a merge request in GitLab.
    
    Args:
        project_id: Project ID or path (required)
        source_branch: Source branch name (required)
        target_branch: Target branch name (required)
        title: MR title (required)
        description: MR description (optional)
        assignee_id: User ID to assign (optional)
        reviewer_ids: List of reviewer user IDs (optional)
    
    Returns:
        JSON string with mr_id, mr_url, source_branch, target_branch, title, status
    """
    if not GITLAB_TOKEN:
        return json.dumps({"error": "GITLAB_TOKEN not set", "success": False})
    
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": title,
        "description": description
    }
    
    if assignee_id:
        data["assignee_id"] = assignee_id
    if reviewer_ids:
        data["reviewer_ids"] = reviewer_ids
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests",
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            mr = response.json()
            
            return json.dumps({
                "success": True,
                "mr_id": mr["iid"],
                "mr_url": mr["web_url"],
                "source_branch": mr["source_branch"],
                "target_branch": mr["target_branch"],
                "title": mr["title"],
                "status": mr["state"],
                "created_at": mr["created_at"]
            })
    
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error": f"GitLab API error: {e.response.status_code} - {e.response.text}",
            "success": False
        })
    except Exception as e:
        return json.dumps({
            "error": f"Failed to create merge request: {str(e)}",
            "success": False
        })
```

---

## ✅ Acceptance Criteria

1. **Implementation:**
   - [ ] Function decorated with `@mcp.tool()`
   - [ ] All 7 parameters implemented
   - [ ] Docstring with examples
   - [ ] Error handling
   - [ ] Returns JSON string

2. **Testing:**
   - [ ] Test script created
   - [ ] Test passes

---

## 🧪 Testing Script

Create `servers/gitlab/test_create_mr.py`:

```python
import asyncio
import json
from dotenv import load_dotenv
from server import create_merge_request

load_dotenv()

async def test_create_mr():
    """Test create_merge_request tool"""
    result = await create_merge_request(
        project_id="your-project-id",
        source_branch="feature-test",
        target_branch="main",
        title="Test MR from MVP",
        description="Testing MR creation"
    )
    
    data = json.loads(result)
    print(f"✅ Success: {data.get('success')}")
    print(f"📋 MR ID: {data.get('mr_id')}")
    print(f"🔗 URL: {data.get('mr_url')}")
    
    assert data.get('success') == True
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_create_mr())
```

---

## 📝 Output Format

**Submit via:**
1. Update `servers/gitlab/server.py`
2. Create test script
3. Submit `deliverables/TASK_003_COMPLETE.md`

