#!/usr/bin/env python3
"""
Frontend Sync - Syncs API registry to frontend

Purpose: Automatically sync test results and API status to frontend
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

REGISTRY_PATH = project_root / "central" / "api-registry.yaml"
FRONTEND_DATA_DIR = project_root / "frontend" / "src" / "data"
FRONTEND_DATA_FILE = FRONTEND_DATA_DIR / "api-status.json"


def load_registry() -> Dict[str, Any]:
    """Load API registry from YAML"""
    with open(REGISTRY_PATH, 'r') as f:
        return yaml.safe_load(f)


def generate_frontend_data(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Generate frontend data from registry"""
    timestamp = datetime.now().isoformat()
    
    apis = []
    for api_name, api_data in registry.get("apis", {}).items():
        api_info = {
            "id": api_name,
            "name": api_data.get("name", api_name),
            "category": api_data.get("category", "unknown"),
            "status": api_data.get("status", "pending"),
            "mcp_server": api_data.get("mcp_server", ""),
            "endpoints": [
                {
                    "name": endpoint["name"],
                    "tested": endpoint.get("tested", False),
                    "test_result": endpoint.get("test_result", "pending"),
                    "last_test": endpoint.get("last_test"),
                    "showcase": endpoint.get("frontend_showcase", False)
                }
                for endpoint in api_data.get("endpoints", [])
            ],
            "tests": {
                "total": api_data.get("tests", {}).get("total", 0),
                "passed": api_data.get("tests", {}).get("passed", 0),
                "failed": api_data.get("tests", {}).get("failed", 0),
                "pending": api_data.get("tests", {}).get("pending", 0),
                "coverage": api_data.get("tests", {}).get("coverage", 0)
            },
            "frontend": {
                "integrated": api_data.get("frontend", {}).get("integrated", False),
                "showcase_page": api_data.get("frontend", {}).get("showcase_page", ""),
                "last_synced": timestamp
            }
        }
        apis.append(api_info)
    
    return {
        "timestamp": timestamp,
        "summary": registry.get("test_summary", {}),
        "apis": apis,
        "frontend_integration": registry.get("frontend_integration", {})
    }


def save_frontend_data(data: Dict[str, Any]):
    """Save frontend data to JSON"""
    # Ensure directory exists
    FRONTEND_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    with open(FRONTEND_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Frontend data saved: {FRONTEND_DATA_FILE}")


def update_registry_sync_timestamp(registry: Dict[str, Any]):
    """Update last_synced timestamp in registry"""
    timestamp = datetime.now().isoformat()
    
    # Update each API's frontend sync timestamp
    for api_data in registry.get("apis", {}).values():
        if "frontend" not in api_data:
            api_data["frontend"] = {}
        api_data["frontend"]["last_synced"] = timestamp
    
    # Update frontend integration timestamp
    if "frontend_integration" not in registry:
        registry["frontend_integration"] = {}
    registry["frontend_integration"]["last_synced"] = timestamp
    
    return registry


def main():
    """Main sync function"""
    print("=" * 60)
    print("Frontend Sync")
    print("=" * 60)
    
    # Load registry
    registry = load_registry()
    print(f"Loaded registry with {len(registry.get('apis', {}))} APIs")
    
    # Generate frontend data
    frontend_data = generate_frontend_data(registry)
    print(f"Generated frontend data for {len(frontend_data['apis'])} APIs")
    
    # Save frontend data
    save_frontend_data(frontend_data)
    
    # Update registry sync timestamp
    registry = update_registry_sync_timestamp(registry)
    
    # Save registry
    import yaml
    with open(REGISTRY_PATH, 'w') as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)
    
    print("\n" + "=" * 60)
    print("Sync Summary")
    print("=" * 60)
    print(f"APIs synced: {len(frontend_data['apis'])}")
    print(f"Frontend data: {FRONTEND_DATA_FILE}")
    print(f"Last synced: {frontend_data['timestamp']}")
    print("\n✅ Frontend sync complete!")


if __name__ == "__main__":
    main()

