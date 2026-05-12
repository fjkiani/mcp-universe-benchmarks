#!/usr/bin/env python3
"""
Central Test Runner - Runs all tests and updates API registry

Purpose: Automatically discover, run, and update test results in api-registry.yaml
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

REGISTRY_PATH = project_root / "central" / "api-registry.yaml"
TESTS_DIR = project_root / "tests"


def load_registry() -> Dict[str, Any]:
    """Load API registry from YAML"""
    with open(REGISTRY_PATH, 'r') as f:
        return yaml.safe_load(f)


def save_registry(registry: Dict[str, Any]):
    """Save API registry to YAML"""
    with open(REGISTRY_PATH, 'w') as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)


def discover_tests() -> List[Path]:
    """Discover all test files"""
    test_files = []
    
    if TESTS_DIR.exists():
        for test_file in TESTS_DIR.rglob("test_*.py"):
            test_files.append(test_file)
    
    return test_files


def run_test_file(test_file: Path) -> Dict[str, Any]:
    """Run a single test file and return results"""
    print(f"Running {test_file.name}...")
    
    try:
        # Run pytest on the test file
        result = subprocess.run(
            ["pytest", str(test_file), "-v", "--json-report", "--json-report-file=/tmp/test-report.json"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Parse results
        if Path("/tmp/test-report.json").exists():
            with open("/tmp/test-report.json", 'r') as f:
                report = json.load(f)
                return {
                    "passed": report.get("summary", {}).get("passed", 0),
                    "failed": report.get("summary", {}).get("failed", 0),
                    "total": report.get("summary", {}).get("total", 0),
                    "status": "passed" if result.returncode == 0 else "failed"
                }
        
        return {
            "passed": 1 if result.returncode == 0 else 0,
            "failed": 0 if result.returncode == 0 else 1,
            "total": 1,
            "status": "passed" if result.returncode == 0 else "failed"
        }
    
    except subprocess.TimeoutExpired:
        return {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "status": "failed",
            "error": "Test timeout"
        }
    except Exception as e:
        return {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "status": "failed",
            "error": str(e)
        }


def update_registry_with_results(registry: Dict[str, Any], test_results: Dict[str, Dict[str, Any]]):
    """Update registry with test results"""
    timestamp = datetime.now().isoformat()
    
    # Update each API's test results
    for api_name, api_data in registry.get("apis", {}).items():
        if api_name in test_results:
            results = test_results[api_name]
            
            # Update endpoint test results
            for endpoint in api_data.get("endpoints", []):
                endpoint_name = endpoint["name"]
                if endpoint_name in results.get("endpoints", {}):
                    endpoint["tested"] = True
                    endpoint["last_test"] = timestamp
                    endpoint["test_result"] = results["endpoints"][endpoint_name]["status"]
            
            # Update overall test stats
            api_data["tests"]["total"] = results.get("total", 0)
            api_data["tests"]["passed"] = results.get("passed", 0)
            api_data["tests"]["failed"] = results.get("failed", 0)
            api_data["tests"]["pending"] = results.get("total", 0) - results.get("passed", 0) - results.get("failed", 0)
            api_data["tests"]["coverage"] = int((results.get("passed", 0) / results.get("total", 1)) * 100)
    
    # Update summary
    total_tests = sum(api["tests"]["total"] for api in registry.get("apis", {}).values())
    total_passed = sum(api["tests"]["passed"] for api in registry.get("apis", {}).values())
    total_failed = sum(api["tests"]["failed"] for api in registry.get("apis", {}).values())
    total_pending = sum(api["tests"]["pending"] for api in registry.get("apis", {}).values())
    
    registry["test_summary"] = {
        "total_apis": len(registry.get("apis", {})),
        "total_endpoints": sum(len(api.get("endpoints", [])) for api in registry.get("apis", {}).values()),
        "total_tests": total_tests,
        "tests_passed": total_passed,
        "tests_failed": total_failed,
        "tests_pending": total_pending,
        "overall_coverage": int((total_passed / total_tests * 100) if total_tests > 0 else 0),
        "last_updated": timestamp
    }


def main():
    """Main test runner"""
    print("=" * 60)
    print("Central Test Runner")
    print("=" * 60)
    
    # Load registry
    registry = load_registry()
    print(f"Loaded registry with {len(registry.get('apis', {}))} APIs")
    
    # Discover tests
    test_files = discover_tests()
    print(f"Discovered {len(test_files)} test files")
    
    if not test_files:
        print("No tests found. Create tests in tests/api/ directory")
        return
    
    # Run tests
    test_results = {}
    for test_file in test_files:
        # Extract API name from test file (e.g., test_twilio.py -> twilio)
        api_name = test_file.stem.replace("test_", "")
        
        # Run test
        result = run_test_file(test_file)
        
        # Store results
        test_results[api_name] = result
        print(f"  {api_name}: {result['status']} ({result['passed']}/{result['total']})")
    
    # Update registry
    update_registry_with_results(registry, test_results)
    save_registry(registry)
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    summary = registry["test_summary"]
    print(f"Total APIs: {summary['total_apis']}")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['tests_passed']}")
    print(f"Failed: {summary['tests_failed']}")
    print(f"Pending: {summary['tests_pending']}")
    print(f"Coverage: {summary['overall_coverage']}%")
    print(f"\nRegistry updated: {REGISTRY_PATH}")
    
    # Trigger frontend sync
    print("\nTriggering frontend sync...")
    frontend_sync_path = project_root / "central" / "frontend-sync.py"
    if frontend_sync_path.exists():
        subprocess.run([sys.executable, str(frontend_sync_path)])
        print("Frontend synced!")
    else:
        print("Frontend sync script not found. Run: python central/frontend-sync.py")


if __name__ == "__main__":
    main()







