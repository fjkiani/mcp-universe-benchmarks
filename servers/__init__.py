"""Mock MCP servers for mcp-universe-benchmarks.

Each server is a FastMCP-based stdio server that returns deterministic mock data.
Servers are launched as subprocesses by mcpbench.mcp_client.MCPServerManager.
"""
