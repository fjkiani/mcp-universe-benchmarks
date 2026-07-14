"""Mock gitlab MCP server — GitLab project/issue/MR operations."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("gitlab")

_PROJECTS = {
    "12345": {"id": 12345, "name": "ml-model-training", "path": "ml/model-training", "default_branch": "main", "web_url": "https://gitlab.example.com/ml/model-training"},
}

_ISSUES = []
_MRS = []


@mcp.tool()
async def create_issue(project_id: int, title: str, description: str = "", labels: str = "") -> str:
    """Create an issue in a GitLab project.

    Args:
        project_id: The project ID
        title: Issue title
        description: Issue description
        labels: Comma-separated labels

    Returns:
        JSON with the created issue
    """
    issue_id = len(_ISSUES) + 1
    issue = {"id": issue_id, "iid": issue_id, "project_id": project_id, "title": title, "description": description, "labels": labels.split(",") if labels else [], "state": "opened", "web_url": f"https://gitlab.example.com/ml/model-training/-/issues/{issue_id}"}
    _ISSUES.append(issue)
    return json.dumps({"issue": issue, "status": "created"}, indent=2)


@mcp.tool()
async def create_merge_request(project_id: int, source_branch: str, target_branch: str, title: str, description: str = "") -> str:
    """Create a merge request in a GitLab project.

    Args:
        project_id: The project ID
        source_branch: Source branch name
        target_branch: Target branch name
        title: MR title
        description: MR description

    Returns:
        JSON with the created merge request
    """
    mr_id = len(_MRS) + 1
    mr = {"id": mr_id, "iid": mr_id, "project_id": project_id, "source_branch": source_branch, "target_branch": target_branch, "title": title, "description": description, "state": "opened", "web_url": f"https://gitlab.example.com/ml/model-training/-/merge_requests/{mr_id}"}
    _MRS.append(mr)
    return json.dumps({"mr": mr, "status": "created"}, indent=2)


@mcp.tool()
async def assign_reviewers(project_id: int, merge_request_iid: int, reviewer_ids: str) -> str:
    """Assign reviewers to a merge request.

    Args:
        project_id: The project ID
        merge_request_iid: The merge request IID
        reviewer_ids: Comma-separated user IDs

    Returns:
        JSON with the assignment result
    """
    ids = [int(x.strip()) for x in reviewer_ids.split(",") if x.strip()]
    return json.dumps({"project_id": project_id, "merge_request_iid": merge_request_iid, "reviewer_ids": ids, "status": "assigned"}, indent=2)


@mcp.tool()
async def get_project(project_id: int) -> str:
    """Get project information.

    Args:
        project_id: The project ID

    Returns:
        JSON with project details
    """
    pid = str(project_id)
    if pid in _PROJECTS:
        return json.dumps({"project": _PROJECTS[pid]}, indent=2)
    return json.dumps({"error": f"Project {project_id} not found"}, indent=2)


@mcp.tool()
async def list_issues(project_id: int, state: str = "opened") -> str:
    """List issues in a project.

    Args:
        project_id: The project ID
        state: Filter by state ('opened', 'closed', 'all')

    Returns:
        JSON array of issues
    """
    issues = [i for i in _ISSUES if i["project_id"] == project_id]
    if state != "all":
        issues = [i for i in issues if i["state"] == state]
    return json.dumps({"issues": issues, "count": len(issues)}, indent=2)


@mcp.tool()
async def add_issue_link(project_id: int, issue_iid: int, target_issue_iid: int, link_type: str = "relates_to") -> str:
    """Link two issues together.

    Args:
        project_id: The project ID
        issue_iid: Source issue IID
        target_issue_iid: Target issue IID
        link_type: Link type ('relates_to', 'blocks', 'is_blocked_by')

    Returns:
        JSON with the link result
    """
    return json.dumps({"project_id": project_id, "source_issue_iid": issue_iid, "target_issue_iid": target_issue_iid, "link_type": link_type, "status": "linked"}, indent=2)


@mcp.tool()
async def add_labels(project_id: int, issue_iid: int, labels: str) -> str:
    """Add labels to an issue.

    Args:
        project_id: The project ID
        issue_iid: Issue IID
        labels: Comma-separated labels to add

    Returns:
        JSON with the update result
    """
    return json.dumps({"project_id": project_id, "issue_iid": issue_iid, "labels_added": labels.split(","), "status": "updated"}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
