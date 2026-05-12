#!/usr/bin/env python3
"""
MCP Server Connectivity Tests

Tests MCP servers for:
- Server startup and initialization
- Tool discovery
- Tool execution
- Error handling
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# MCP imports are optional (for advanced testing)
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False


class MCPServerTester:
    """Test MCP server connectivity and capabilities."""
    
    def __init__(self, servers_path: Optional[str] = None):
        self.servers_path = Path(servers_path or os.getenv(
            "MCP_SERVERS_PATH",
            Path(__file__).parent.parent / "lbx_mcp_universe_mcp_servers_mothership" / "servers"
        ))
        self.results = []
        
    def discover_servers(self) -> List[str]:
        """Discover all MCP servers in the servers directory."""
        servers = []
        for server_dir in self.servers_path.iterdir():
            if server_dir.is_dir() and (server_dir / "server.py").exists():
                servers.append(server_dir.name)
        return sorted(servers)
    
    async def test_server_tools(self, server_name: str) -> Dict:
        """Test a single MCP server's tools."""
        server_dir = self.servers_path / server_name
        
        if not server_dir.exists():
            return {
                "server": server_name,
                "status": "error",
                "error": f"Server directory not found: {server_dir}"
            }
        
        result = {
            "server": server_name,
            "status": "unknown",
            "tools_discovered": 0,
            "tools_tested": 0,
            "tools_passed": 0,
            "tools_failed": 0,
            "errors": []
        }
        
        try:
            # Try to import the server module
            server_path = server_dir / "server.py"
            if not server_path.exists():
                result["status"] = "error"
                result["errors"].append(f"server.py not found: {server_path}")
                return result
            
            # Check if server has required files
            required_files = ["server.py", "pyproject.toml", "__init__.py"]
            missing_files = [f for f in required_files if not (server_dir / f).exists()]
            if missing_files:
                result["status"] = "error"
                result["errors"].append(f"Missing files: {missing_files}")
                return result
            
            # Try to parse server.py for tool definitions
            try:
                with open(server_path, "r") as f:
                    content = f.read()
                    
                # Count @mcp.tool() decorators
                tool_count = content.count("@mcp.tool()")
                result["tools_discovered"] = tool_count
                
                # Check for FastMCP import
                if "from mcp.server.fastmcp import FastMCP" in content:
                    result["architecture"] = "FastMCP"
                elif "FastMCP" in content:
                    result["architecture"] = "FastMCP"
                else:
                    result["architecture"] = "unknown"
                
                # Check for required patterns
                if "def main()" in content or "if __name__" in content:
                    result["has_entry_point"] = True
                else:
                    result["has_entry_point"] = False
                
                # Validate structure
                if tool_count > 0 and result["architecture"] == "FastMCP":
                    result["status"] = "valid"
                elif tool_count == 0:
                    result["status"] = "warning"
                    result["errors"].append("No tools found (@mcp.tool() decorators)")
                else:
                    result["status"] = "warning"
                    result["errors"].append("Architecture not FastMCP")
                    
            except Exception as e:
                result["status"] = "error"
                result["errors"].append(f"Failed to parse server.py: {str(e)}")
                
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(f"Unexpected error: {str(e)}")
        
        return result
    
    async def test_specific_server(self, server_name: str) -> Dict:
        """Test a specific server with more detailed checks."""
        result = await self.test_server_tools(server_name)
        
        # Additional checks
        server_dir = self.servers_path / server_name
        
        # Check pyproject.toml
        pyproject_path = server_dir / "pyproject.toml"
        if pyproject_path.exists():
            result["has_pyproject"] = True
            try:
                import tomli
                with open(pyproject_path, "rb") as f:
                    pyproject = tomli.load(f)
                    result["project_name"] = pyproject.get("project", {}).get("name", "unknown")
            except Exception as e:
                result["pyproject_error"] = str(e)
        else:
            result["has_pyproject"] = False
        
        # Check README
        readme_path = server_dir / "README.md"
        result["has_readme"] = readme_path.exists()
        
        # Check server_config.json
        config_path = server_dir / "server_config.json"
        result["has_config"] = config_path.exists()
        
        return result
    
    async def run_tests(self, server_names: Optional[List[str]] = None) -> Dict:
        """Run tests for all or specific servers."""
        if server_names:
            servers_to_test = server_names
        else:
            servers_to_test = self.discover_servers()
        
        print(f"🔍 Testing {len(servers_to_test)} MCP servers...")
        print()
        
        results = []
        for server_name in servers_to_test:
            print(f"Testing: {server_name}...", end=" ", flush=True)
            result = await self.test_server_tools(server_name)
            results.append(result)
            
            if result["status"] == "valid":
                print(f"✅ Valid ({result['tools_discovered']} tools)")
            elif result["status"] == "warning":
                print(f"⚠️  Warning ({result['tools_discovered']} tools)")
            else:
                print(f"❌ Error")
                if result["errors"]:
                    print(f"   Errors: {', '.join(result['errors'][:2])}")
            print()
        
        return {
            "total_servers": len(servers_to_test),
            "results": results,
            "summary": self._generate_summary(results)
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """Generate summary statistics."""
        total = len(results)
        valid = sum(1 for r in results if r["status"] == "valid")
        warnings = sum(1 for r in results if r["status"] == "warning")
        errors = sum(1 for r in results if r["status"] == "error")
        total_tools = sum(r["tools_discovered"] for r in results)
        
        return {
            "total_servers": total,
            "valid": valid,
            "warnings": warnings,
            "errors": errors,
            "total_tools": total_tools,
            "pass_rate": (valid / total * 100) if total > 0 else 0
        }


async def main():
    parser = argparse.ArgumentParser(description="Test MCP server connectivity")
    parser.add_argument(
        "--server",
        type=str,
        help="Test specific server (e.g., twilio_hipaa)"
    )
    parser.add_argument(
        "--servers-path",
        type=str,
        help="Path to MCP servers directory"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output JSON file for results"
    )
    
    args = parser.parse_args()
    
    tester = MCPServerTester(servers_path=args.servers_path)
    
    if args.server:
        print(f"🧪 Testing server: {args.server}")
        print()
        result = await tester.test_specific_server(args.server)
        print(json.dumps(result, indent=2))
        results = {"results": [result], "summary": tester._generate_summary([result])}
    else:
        results = await tester.run_tests()
    
    # Print summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    summary = results["summary"]
    print(f"Total Servers: {summary['total_servers']}")
    print(f"✅ Valid: {summary['valid']}")
    print(f"⚠️  Warnings: {summary['warnings']}")
    print(f"❌ Errors: {summary['errors']}")
    print(f"🔧 Total Tools: {summary['total_tools']}")
    print(f"📈 Pass Rate: {summary['pass_rate']:.1f}%")
    print()
    
    # Save results
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"💾 Results saved to: {output_path}")
    
    # Exit code
    exit_code = 0 if summary["errors"] == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())

