"""
Report Parser — converts existing YAML benchmark reports to JSON for the API.

The YAML format (verified from reports/20251027_132402__grant_application__report.yaml):
  - Uses !!python/object: serialization (PyYAML specific)
  - Contains: BenchmarkResult → BenchmarkConfig + task_results + task_trace_ids
  - Each task_result has evaluation_results[] with passed/reason/error

Edge case: PyYAML's full_load or UnsafeLoader is needed to deserialize 
  !!python/object tags. We use safe regex parsing as a fallback that works
  without the CLI module imported.
"""
import os
import re
from pathlib import Path
from typing import List, Dict

# Reports directory — relative to project root, not backend root
REPORTS_DIR = Path(__file__).parent.parent.parent / "reports"


def parse_yaml_reports() -> List[Dict]:
    """Parse all YAML report files into JSON-serializable dicts."""
    reports = []
    
    if not REPORTS_DIR.exists():
        return reports
    
    for yaml_file in sorted(REPORTS_DIR.glob("*__report.yaml"), reverse=True):
        try:
            report = _parse_single_report(yaml_file)
            if report:
                reports.append(report)
        except Exception:
            continue  # Skip malformed reports
    
    return reports


def _parse_single_report(filepath: Path) -> Dict:
    """
    Parse a single YAML report file.
    
    Filename format: 20251027_132402__grant_application__report.yaml
    → date=2025-10-27, time=13:24:02, domain=grant_application
    """
    filename = filepath.stem
    parts = filename.split("__")
    
    timestamp_str = parts[0] if len(parts) >= 1 else ""
    domain = parts[1] if len(parts) >= 2 else "unknown"
    
    # Read file content
    with open(filepath, "r") as f:
        content = f.read()
    
    # Extract pass/fail counts using regex (safer than full deserialization)
    passed_count = content.count("passed: true")
    failed_count = content.count("passed: false")
    total = passed_count + failed_count
    
    # Extract error messages
    errors = re.findall(r"reason: (.+)", content)
    
    # Extract agent/model info if available
    model_match = re.search(r"model:\s*(.+)", content)
    model = model_match.group(1).strip() if model_match else "unknown"
    
    return {
        "source": "historical_yaml",
        "filename": filepath.name,
        "domain": domain,
        "timestamp": timestamp_str,
        "model": model,
        "total_evaluations": total,
        "passed": passed_count,
        "failed": failed_count,
        "pass_rate": round(passed_count / total * 100, 1) if total > 0 else 0,
        "error_summary": errors[:5],  # First 5 errors
    }
