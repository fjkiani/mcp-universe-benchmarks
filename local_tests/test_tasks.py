#!/usr/bin/env python3
"""
Task Execution Tests

Tests task execution with:
- Task JSON parsing
- MCP server integration
- Mock LLM responses
- Response validation
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TaskTester:
    """Test task execution and validation."""
    
    def __init__(self, domains_path: Optional[str] = None):
        self.domains_path = Path(domains_path or os.getenv(
            "DOMAINS_PATH",
            Path(__file__).parent.parent / "domains"
        ))
        self.results = []
    
    def discover_domains(self) -> List[str]:
        """Discover all domains."""
        domains = []
        for domain_dir in self.domains_path.iterdir():
            if domain_dir.is_dir() and (domain_dir / "config.yaml").exists():
                domains.append(domain_dir.name)
        return sorted(domains)
    
    def discover_tasks(self, domain_name: str) -> List[str]:
        """Discover all tasks for a domain."""
        domain_dir = self.domains_path / domain_name
        tasks_dir = domain_dir / "tasks"
        
        if not tasks_dir.exists():
            return []
        
        tasks = []
        for task_file in tasks_dir.glob("*.json"):
            tasks.append(task_file.stem)
        
        return sorted(tasks)
    
    def validate_task_json(self, task_path: Path) -> Dict:
        """Validate a task JSON file structure."""
        result = {
            "task": task_path.stem,
            "status": "unknown",
            "errors": [],
            "warnings": []
        }
        
        try:
            with open(task_path, "r") as f:
                task_data = json.load(f)
            
            # Required fields
            required_fields = ["question", "evaluators"]
            for field in required_fields:
                if field not in task_data:
                    result["errors"].append(f"Missing required field: {field}")
            
            # Check evaluators format
            if "evaluators" in task_data:
                evaluators = task_data["evaluators"]
                if not isinstance(evaluators, list):
                    result["errors"].append("evaluators must be a list")
                else:
                    for i, evaluator in enumerate(evaluators):
                        if not isinstance(evaluator, dict):
                            result["errors"].append(f"evaluators[{i}] must be a dict")
                        else:
                            if "func" not in evaluator:
                                result["errors"].append(f"evaluators[{i}] missing 'func' field")
                            if "op" not in evaluator:
                                result["errors"].append(f"evaluators[{i}] missing 'op' field")
            
            # Check mcp_servers format
            if "mcp_servers" in task_data:
                mcp_servers = task_data["mcp_servers"]
                if not isinstance(mcp_servers, list):
                    result["errors"].append("mcp_servers must be a list")
                else:
                    for i, server in enumerate(mcp_servers):
                        if isinstance(server, str):
                            result["warnings"].append(f"mcp_servers[{i}] is string, should be object with 'name' field")
                        elif isinstance(server, dict):
                            if "name" not in server:
                                result["errors"].append(f"mcp_servers[{i}] missing 'name' field")
            
            # Optional fields
            optional_fields = ["category", "output_format", "use_specified_server"]
            for field in optional_fields:
                if field not in task_data:
                    result["warnings"].append(f"Missing optional field: {field}")
            
            if result["errors"]:
                result["status"] = "error"
            elif result["warnings"]:
                result["status"] = "warning"
            else:
                result["status"] = "valid"
            
            result["fields"] = list(task_data.keys())
            
        except json.JSONDecodeError as e:
            result["status"] = "error"
            result["errors"].append(f"Invalid JSON: {str(e)}")
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(f"Unexpected error: {str(e)}")
        
        return result
    
    def test_domain_tasks(self, domain_name: str) -> Dict:
        """Test all tasks for a domain."""
        domain_dir = self.domains_path / domain_name
        tasks_dir = domain_dir / "tasks"
        
        if not tasks_dir.exists():
            return {
                "domain": domain_name,
                "status": "error",
                "error": f"Tasks directory not found: {tasks_dir}"
            }
        
        tasks = self.discover_tasks(domain_name)
        
        print(f"🔍 Testing {len(tasks)} tasks for domain: {domain_name}")
        print()
        
        results = []
        for task_name in tasks:
            task_path = tasks_dir / f"{task_name}.json"
            print(f"Testing: {task_name}...", end=" ", flush=True)
            
            result = self.validate_task_json(task_path)
            result["domain"] = domain_name
            results.append(result)
            
            if result["status"] == "valid":
                print("✅ Valid")
            elif result["status"] == "warning":
                print("⚠️  Warning")
                if result["warnings"]:
                    print(f"   {result['warnings'][0]}")
            else:
                print("❌ Error")
                if result["errors"]:
                    print(f"   {result['errors'][0]}")
            print()
        
        return {
            "domain": domain_name,
            "total_tasks": len(tasks),
            "results": results,
            "summary": self._generate_summary(results)
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """Generate summary statistics."""
        total = len(results)
        valid = sum(1 for r in results if r["status"] == "valid")
        warnings = sum(1 for r in results if r["status"] == "warning")
        errors = sum(1 for r in results if r["status"] == "error")
        
        return {
            "total_tasks": total,
            "valid": valid,
            "warnings": warnings,
            "errors": errors,
            "pass_rate": (valid / total * 100) if total > 0 else 0
        }


async def main():
    parser = argparse.ArgumentParser(description="Test task execution")
    parser.add_argument(
        "--domain",
        type=str,
        help="Test specific domain (e.g., healthcare_receptionist)"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Test specific task (requires --domain)"
    )
    parser.add_argument(
        "--domains-path",
        type=str,
        help="Path to domains directory"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output JSON file for results"
    )
    
    args = parser.parse_args()
    
    tester = TaskTester(domains_path=args.domains_path)
    
    if args.task and args.domain:
        # Test single task
        task_path = tester.domains_path / args.domain / "tasks" / f"{args.task}.json"
        if not task_path.exists():
            print(f"❌ Task not found: {task_path}")
            sys.exit(1)
        
        result = tester.validate_task_json(task_path)
        result["domain"] = args.domain
        results = {"results": [result], "summary": tester._generate_summary([result])}
        print(json.dumps(result, indent=2))
    elif args.domain:
        # Test all tasks for domain
        results = tester.test_domain_tasks(args.domain)
    else:
        # Test all domains
        domains = tester.discover_domains()
        print(f"🔍 Testing {len(domains)} domains...")
        print()
        
        all_results = []
        for domain in domains:
            domain_results = tester.test_domain_tasks(domain)
            all_results.extend(domain_results["results"])
        
        results = {
            "total_domains": len(domains),
            "results": all_results,
            "summary": tester._generate_summary(all_results)
        }
    
    # Print summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    summary = results["summary"]
    print(f"Total Tasks: {summary['total_tasks']}")
    print(f"✅ Valid: {summary['valid']}")
    print(f"⚠️  Warnings: {summary['warnings']}")
    print(f"❌ Errors: {summary['errors']}")
    print(f"📈 Pass Rate: {summary['pass_rate']:.1f}%")
    print()
    
    # Automatically save results to backend-readable format
    if args.domain:
        # Save in format that backend expects (same as run_all_tests.py)
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_file = results_dir / f"test_results_{timestamp}.json"
        
        # Format results to match run_all_tests.py structure
        formatted_results = {
            "timestamp": timestamp,
            "domain": args.domain,
            "tests": {
                "tasks": {
                    "domain": args.domain,
                    "total_tasks": summary["total_tasks"],
                    "results": results.get("results", []),
                    "summary": {
                        "total_tasks": summary["total_tasks"],
                        "valid": summary["valid"],
                        "warnings": summary["warnings"],
                        "errors": summary["errors"],
                        "pass_rate": summary["pass_rate"]
                    }
                }
            }
        }
        
        with open(results_file, "w") as f:
            json.dump(formatted_results, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")
        print(f"   (Backend will automatically pick this up)")
        print()
    
    # Also save to custom output if specified
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"💾 Custom results saved to: {output_path}")
    
    # Exit code
    exit_code = 0 if summary["errors"] == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())

