#!/usr/bin/env python3
"""
Full Test Suite Runner

Runs all local tests:
1. MCP Server tests
2. Task validation tests
3. Evaluator tests
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict

# Import test modules
sys.path.insert(0, str(Path(__file__).parent))

from test_mcp_servers import MCPServerTester
from test_tasks import TaskTester
from test_evaluators import EvaluatorTester


async def run_all_tests(
    domain: str = "investments",
    servers_path: str = None,
    domains_path: str = None,
    output_dir: str = None
) -> Dict:
    """Run all tests and generate comprehensive report."""
    
    output_dir = Path(output_dir or Path(__file__).parent / "results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    print("=" * 60)
    print("🧪 Local Testing Framework - Full Test Suite")
    print("=" * 60)
    print()
    
    all_results = {
        "timestamp": timestamp,
        "domain": domain,
        "tests": {}
    }
    
    # 1. MCP Server Tests
    print("=" * 60)
    print("1️⃣  MCP Server Tests")
    print("=" * 60)
    print()
    
    server_tester = MCPServerTester(servers_path=servers_path)
    
    # Test healthcare-specific servers
    healthcare_servers = None  # Auto-discover from domain mcp_servers dir
    server_results = await server_tester.run_tests(server_names=healthcare_servers)
    all_results["tests"]["mcp_servers"] = server_results
    
    print()
    
    # 2. Task Validation Tests
    print("=" * 60)
    print("2️⃣  Task Validation Tests")
    print("=" * 60)
    print()
    
    task_tester = TaskTester(domains_path=domains_path)
    task_results = task_tester.test_domain_tasks(domain)
    all_results["tests"]["tasks"] = task_results
    
    print()
    
    # 3. Evaluator Tests
    print("=" * 60)
    print("3️⃣  Evaluator Tests")
    print("=" * 60)
    print()
    
    evaluator_tester = EvaluatorTester(domains_path=domains_path)
    evaluator_results = await evaluator_tester.test_domain_evaluators(domain)
    all_results["tests"]["evaluators"] = evaluator_results
    
    print()
    
    # Generate Overall Summary
    print("=" * 60)
    print("📊 Overall Summary")
    print("=" * 60)
    print()
    
    server_summary = server_results["summary"]
    task_summary = task_results["summary"]
    evaluator_summary = evaluator_results["summary"]
    
    print("MCP Servers:")
    print(f"  ✅ Valid: {server_summary['valid']}/{server_summary['total_servers']}")
    print(f"  🔧 Tools: {server_summary['total_tools']}")
    print()
    
    print("Tasks:")
    print(f"  ✅ Valid: {task_summary['valid']}/{task_summary['total_tasks']}")
    print(f"  📈 Pass Rate: {task_summary['pass_rate']:.1f}%")
    print()
    
    print("Evaluators:")
    print(f"  Total: {evaluator_summary['total_evaluators']}")
    print(f"  ✅ Passed: {evaluator_summary['passed_tests']}/{evaluator_summary['total_tests']}")
    print(f"  📈 Pass Rate: {evaluator_summary['pass_rate']:.1f}%")
    print()
    
    # Calculate overall health
    overall_health = "🟢 Healthy"
    if (server_summary["errors"] > 0 or 
        task_summary["errors"] > 0 or 
        evaluator_summary["pass_rate"] < 50):
        overall_health = "🟡 Warning"
    if (server_summary["errors"] > server_summary["total_servers"] * 0.5 or
        task_summary["errors"] > task_summary["total_tasks"] * 0.5):
        overall_health = "🔴 Critical"
    
    print(f"Overall Health: {overall_health}")
    print()
    
    # Save results
    results_file = output_dir / f"test_results_{timestamp}.json"
    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"💾 Full results saved to: {results_file}")
    print()
    
    return all_results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run full local test suite")
    parser.add_argument(
        "--domain",
        type=str,
        default="investments",
        help="Domain to test"
    )
    parser.add_argument(
        "--servers-path",
        type=str,
        help="Path to MCP servers directory"
    )
    parser.add_argument(
        "--domains-path",
        type=str,
        help="Path to domains directory"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    
    results = asyncio.run(run_all_tests(
        domain=args.domain,
        servers_path=args.servers_path,
        domains_path=args.domains_path,
        output_dir=args.output_dir
    ))
    
    # Exit code based on health
    exit_code = 0
    if results["tests"]["mcp_servers"]["summary"]["errors"] > 0:
        exit_code = 1
    if results["tests"]["tasks"]["summary"]["errors"] > 0:
        exit_code = 1
    
    sys.exit(exit_code)






