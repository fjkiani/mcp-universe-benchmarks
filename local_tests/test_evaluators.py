#!/usr/bin/env python3
"""
Evaluator Validation Tests

Tests evaluators with:
- Mock agent responses
- Pydantic unwrapping
- Pass/fail logic
- Error handling
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse
import importlib.util

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class EvaluatorTester:
    """Test evaluator functions."""
    
    def __init__(self, domains_path: Optional[str] = None):
        self.domains_path = Path(domains_path or os.getenv(
            "DOMAINS_PATH",
            Path(__file__).parent.parent / "domains"
        ))
    
    def load_evaluators(self, domain_name: str) -> Dict:
        """Load evaluator functions from a domain."""
        evaluators_path = self.domains_path / domain_name / "evaluators" / "functions.py"
        
        if not evaluators_path.exists():
            return {"error": f"Evaluators file not found: {evaluators_path}"}
        
        try:
            spec = importlib.util.spec_from_file_location(
                f"{domain_name}_evaluators",
                evaluators_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find all evaluator functions (decorated with @compare_func or @eval_func)
            evaluators = {}
            for name in dir(module):
                obj = getattr(module, name)
                if callable(obj) and hasattr(obj, "__name__"):
                    # Check if it's an async function (evaluators are async)
                    if asyncio.iscoroutinefunction(obj):
                        # Check if it has an evaluator name attribute (set by our decorators)
                        if hasattr(obj, "_evaluator_name"):
                            evaluators[obj._evaluator_name] = obj
                        # Also check if name suggests it's an evaluator (backward compat)
                        elif name.startswith("validate_") or name.startswith("check_") or name.startswith("evaluate_"):
                            evaluators[name] = obj
            
            return {
                "evaluators": evaluators,
                "module_path": str(evaluators_path),
                "count": len(evaluators)
            }
        except Exception as e:
            return {"error": f"Failed to load evaluators: {str(e)}"}
    
    def create_mock_response(self, response_type: str = "simple") -> Any:
        """Create mock agent responses for testing."""
        if response_type == "simple":
            return {
                "patient": {
                    "resourceType": "Patient",
                    "identifier": [{"value": "MRN-12345"}],
                    "name": [{"family": "Doe", "given": ["John"]}],
                    "birthDate": "1985-03-15",
                    "telecom": [{"system": "phone", "value": "555-1234"}]
                },
                "appointment": {
                    "provider": "Dr. Smith",
                    "date": "2025-11-10",
                    "time": "14:00"
                },
                "intake_form_sent": True
            }
        elif response_type == "pydantic_wrapped":
            # Simulate Pydantic FunctionResult
            class MockFunctionResult:
                def model_dump(self):
                    return {"result": self._data}
                def __init__(self, data):
                    self._data = data
            
            return MockFunctionResult({
                "patient": {
                    "resourceType": "Patient",
                    "identifier": [{"value": "MRN-12345"}],
                    "name": [{"family": "Doe", "given": ["John"]}],
                    "birthDate": "1985-03-15",
                    "telecom": [{"system": "phone", "value": "555-1234"}]
                },
                "appointment": {
                    "provider": "Dr. Smith",
                    "date": "2025-11-10",
                    "time": "14:00"
                },
                "intake_form_sent": True
            })
        elif response_type == "json_string":
            return json.dumps({
                "patient": {
                    "resourceType": "Patient",
                    "identifier": [{"value": "MRN-12345"}],
                    "name": [{"family": "Doe", "given": ["John"]}],
                    "birthDate": "1985-03-15",
                    "telecom": [{"system": "phone", "value": "555-1234"}]
                },
                "appointment": {
                    "provider": "Dr. Smith",
                    "date": "2025-11-10",
                    "time": "14:00"
                },
                "intake_form_sent": True
            })
        else:
            return {}
    
    async def test_evaluator(self, evaluator_func, mock_response: Any) -> Dict:
        """Test a single evaluator function."""
        result = {
            "status": "unknown",
            "passed": False,
            "message": "",
            "error": None
        }
        
        try:
            # Call evaluator
            passed, message = await evaluator_func(mock_response)
            
            result["status"] = "success"
            result["passed"] = passed
            result["message"] = message
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            result["message"] = f"Evaluator error: {str(e)}"
        
        return result
    
    async def test_domain_evaluators(self, domain_name: str) -> Dict:
        """Test all evaluators for a domain."""
        evaluators_info = self.load_evaluators(domain_name)
        
        if "error" in evaluators_info:
            return {
                "domain": domain_name,
                "status": "error",
                "error": evaluators_info["error"]
            }
        
        evaluators = evaluators_info["evaluators"]
        
        print(f"🔍 Testing {len(evaluators)} evaluators for domain: {domain_name}")
        print()
        
        results = []
        for name, func in evaluators.items():
            print(f"Testing: {name}...", end=" ", flush=True)
            
            # Test with different response types
            test_results = {}
            for response_type in ["simple", "pydantic_wrapped", "json_string"]:
                mock_response = self.create_mock_response(response_type)
                test_result = await self.test_evaluator(func, mock_response)
                test_results[response_type] = test_result
            
            results.append({
                "evaluator": name,
                "tests": test_results
            })
            
            # Print summary
            passed_count = sum(1 for tr in test_results.values() if tr["status"] == "success")
            if passed_count == len(test_results):
                print(f"✅ All tests passed ({passed_count}/{len(test_results)})")
            elif passed_count > 0:
                print(f"⚠️  Partial ({passed_count}/{len(test_results)} passed)")
            else:
                print(f"❌ Failed")
            print()
        
        return {
            "domain": domain_name,
            "total_evaluators": len(evaluators),
            "results": results,
            "summary": self._generate_summary(results)
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """Generate summary statistics."""
        total = len(results)
        total_tests = sum(len(r["tests"]) for r in results)
        passed_tests = sum(
            sum(1 for tr in r["tests"].values() if tr["status"] == "success")
            for r in results
        )
        
        return {
            "total_evaluators": total,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }


async def main():
    parser = argparse.ArgumentParser(description="Test evaluator functions")
    parser.add_argument(
        "--domain",
        type=str,
        required=True,
        help="Domain to test (e.g., healthcare_receptionist)"
    )
    parser.add_argument(
        "--evaluator",
        type=str,
        help="Test specific evaluator (requires --domain)"
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
    
    tester = EvaluatorTester(domains_path=args.domains_path)
    
    if args.evaluator:
        # Test single evaluator
        evaluators_info = tester.load_evaluators(args.domain)
        if "error" in evaluators_info:
            print(f"❌ {evaluators_info['error']}")
            sys.exit(1)
        
        if args.evaluator not in evaluators_info["evaluators"]:
            print(f"❌ Evaluator not found: {args.evaluator}")
            sys.exit(1)
        
        evaluator_func = evaluators_info["evaluators"][args.evaluator]
        mock_response = tester.create_mock_response("simple")
        result = await tester.test_evaluator(evaluator_func, mock_response)
        print(json.dumps(result, indent=2))
    else:
        # Test all evaluators for domain
        results = await tester.test_domain_evaluators(args.domain)
        
        # Check if results have error
        if "error" in results:
            print(f"❌ {results['error']}")
            sys.exit(1)
        
        # Print summary
        print("=" * 60)
        print("📊 Summary")
        print("=" * 60)
        if "summary" in results:
            summary = results["summary"]
            print(f"Total Evaluators: {summary['total_evaluators']}")
            print(f"Total Tests: {summary['total_tests']}")
            print(f"✅ Passed: {summary['passed_tests']}")
            print(f"📈 Pass Rate: {summary['pass_rate']:.1f}%")
        else:
            print("No summary available")
        print()
        
        # Save results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"💾 Results saved to: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())

