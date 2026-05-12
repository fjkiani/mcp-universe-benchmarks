"""Service for reading from central API registry"""
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class RegistryService:
    """Service to read from central/api-registry.yaml"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.registry_path = self.project_root / "central" / "api-registry.yaml"
        self.frontend_data_path = self.project_root / "frontend" / "src" / "data" / "api-status.json"
    
    def read_registry(self) -> Dict[str, Any]:
        """Read api-registry.yaml"""
        try:
            with open(self.registry_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
    
    def read_frontend_data(self) -> Dict[str, Any]:
        """Read frontend-synced data (api-status.json)"""
        try:
            with open(self.frontend_data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return empty structure if file doesn't exist
            return {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_apis": 0,
                    "total_endpoints": 0,
                    "total_tests": 0,
                    "tests_passed": 0,
                    "tests_failed": 0,
                    "tests_pending": 0,
                    "overall_coverage": 0,
                },
                "apis": [],
                "frontend_integration": {
                    "total_showcases": 0,
                    "integrated_apis": 0,
                    "showcase_pages": [],
                    "last_synced": None,
                }
            }
    
    def get_apis(self) -> List[Dict[str, Any]]:
        """Get all APIs from registry"""
        registry = self.read_registry()
        apis = registry.get("apis", {})
        
        result = []
        for api_id, api_data in apis.items():
            api_info = {
                "id": api_id,
                "name": api_data.get("name", api_id),
                "category": api_data.get("category", "unknown"),
                "status": api_data.get("status", "pending"),
                "mcp_server": api_data.get("mcp_server", ""),
                "endpoints": api_data.get("endpoints", []),
                "tests": api_data.get("tests", {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "pending": 0,
                    "coverage": 0,
                }),
                "frontend": api_data.get("frontend", {
                    "integrated": False,
                    "showcase_page": "",
                    "last_synced": None,
                })
            }
            result.append(api_info)
        
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary from registry"""
        registry = self.read_registry()
        apis = registry.get("apis", {})
        
        total_apis = len(apis)
        total_endpoints = 0
        total_tests = 0
        tests_passed = 0
        tests_failed = 0
        tests_pending = 0
        
        for api_data in apis.values():
            endpoints = api_data.get("endpoints", [])
            total_endpoints += len(endpoints)
            
            tests = api_data.get("tests", {})
            total_tests += tests.get("total", 0)
            tests_passed += tests.get("passed", 0)
            tests_failed += tests.get("failed", 0)
            tests_pending += tests.get("pending", 0)
        
        overall_coverage = (tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_apis": total_apis,
            "total_endpoints": total_endpoints,
            "total_tests": total_tests,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "tests_pending": tests_pending,
            "overall_coverage": round(overall_coverage, 2),
        }

