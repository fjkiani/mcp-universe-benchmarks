#!/usr/bin/env python3
"""
Domain validator — replaces the private `alignerr_mcp lint-domain` command.

Validates every domain under domains/ against the benchmark contract:
  - config.yaml parses as multi-doc YAML
  - >= 2 kind: llm specs
  - >= 1 kind: agent, agent llm references a defined llm name
  - >= 1 kind: benchmark; every spec.tasks path exists on disk (no ghosts)
  - Every task JSON on disk is referenced by some benchmark (no orphans)
  - Each task JSON: has question, evaluators (non-empty)
  - If task has mcp_servers (non-empty) -> use_specified_server must be true
  - For func: "raw" evaluators -> op present; op exists in evaluators/functions.py
  - No stub functions (functions with only `pass` or `...` body)
  - No unreachable imports (lbx_cli.* without try/except fallback)

Usage:
  python scripts/validate.py --domain web_search
  python scripts/validate.py --all
  python scripts/validate.py --check-slop
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = REPO_ROOT / "domains"

SLOP_DIRS = {"frontend", "backend", "central", "datasets"}
SLOP_FILES = {
    "Dockerfile", "render.yaml", "render-governance.yaml",
    "setup_all.sh", "setup_backend.sh", "setup_frontend.sh",
    "start_backend.sh", "start_frontend.sh",
}
SLOP_NAME_PATTERNS = [
    r".*STATUS.*",
    r".*SUMMARY.*",
    r".*COMPLETE.*",
    r".*AUDIT.*",
    r".*BREAKDOWN.*",
    r".*_PLAN\.md$",
]


class Violation:
    def __init__(self, domain: str, severity: str, rule: str, message: str, file: str = ""):
        self.domain = domain
        self.severity = severity
        self.rule = rule
        self.message = message
        self.file = file

    def __str__(self):
        loc = f" [{self.file}]" if self.file else ""
        return f"  [{self.severity.upper()}] {self.rule}: {self.message}{loc}"


def load_config(domain_dir: Path) -> list[dict[str, Any]]:
    config_path = domain_dir / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"config.yaml not found in {domain_dir}")
    with open(config_path) as f:
        docs = list(yaml.safe_load_all(f))
    return [d for d in docs if d is not None]


def extract_op_names_from_functions(functions_path: Path) -> set[str]:
    if not functions_path.exists():
        return set()
    with open(functions_path) as f:
        source = f.read()
    ops = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ops
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    func = decorator.func
                    func_name = ""
                    if isinstance(func, ast.Name):
                        func_name = func.id
                    elif isinstance(func, ast.Attribute):
                        func_name = func.attr
                    if func_name in ("compare_func", "eval_func"):
                        if decorator.args:
                            arg = decorator.args[0]
                            if isinstance(arg, ast.Constant):
                                ops.add(arg.value.value)
                        for kw in decorator.keywords:
                            if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                                ops.add(kw.value.value)
    return ops


def check_for_stub_functions(functions_path: Path) -> list[str]:
    if not functions_path.exists():
        return []
    with open(functions_path) as f:
        source = f.read()
    stubs = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return stubs
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if len(body) == 1:
                stmt = body[0]
                if isinstance(stmt, ast.Pass):
                    stubs.append(node.name)
                elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is ...:
                    stubs.append(node.name)
    return stubs


def _has_import_error_fallback(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                if handler.type is not None:
                    exc_names = []
                    if isinstance(handler.type, ast.Name):
                        exc_names.append(handler.type.id)
                    elif isinstance(handler.type, ast.Tuple):
                        for elt in handler.type.elts:
                            if isinstance(elt, ast.Name):
                                exc_names.append(elt.id)
                    if "ImportError" in exc_names or "ModuleNotFoundError" in exc_names:
                        return True
    return False


def check_for_unreachable_imports(functions_path: Path) -> list[str]:
    if not functions_path.exists():
        return []
    with open(functions_path) as f:
        source = f.read()
    unreachable = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return unreachable
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("lbx_cli"):
                has_fallback = _has_import_error_fallback(tree)
                if not has_fallback:
                    unreachable.append(f"from {node.module} import ...")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("lbx_cli"):
                    has_fallback = _has_import_error_fallback(tree)
                    if not has_fallback:
                        unreachable.append(f"import {alias.name}")
    return unreachable


def validate_domain(domain_name: str) -> list[Violation]:
    domain_dir = DOMAINS_DIR / domain_name
    violations: list[Violation] = []

    if not domain_dir.exists():
        violations.append(Violation(domain_name, "error", "domain_exists", f"Domain directory not found: {domain_dir}"))
        return violations

    try:
        config_docs = load_config(domain_dir)
    except FileNotFoundError as e:
        violations.append(Violation(domain_name, "error", "config_exists", str(e)))
        return violations
    except yaml.YAMLError as e:
        violations.append(Violation(domain_name, "error", "config_parse", f"Invalid YAML: {e}", "config.yaml"))
        return violations

    llms = {}
    agents = {}
    benchmarks = []

    for doc in config_docs:
        kind = doc.get("kind", "")
        spec = doc.get("spec", doc)
        if kind == "llm":
            llm_name = spec.get("name") if isinstance(spec, dict) else doc.get("name")
            if llm_name:
                llms[llm_name] = doc
            else:
                violations.append(Violation(domain_name, "error", "llm_name", "LLM spec missing 'name'", "config.yaml"))
        elif kind == "agent":
            agent_name = spec.get("name") if isinstance(spec, dict) else doc.get("name")
            if agent_name:
                agents[agent_name] = doc
            else:
                violations.append(Violation(domain_name, "error", "agent_name", "Agent spec missing 'name'", "config.yaml"))
        elif kind == "benchmark":
            benchmarks.append(doc)

    if len(llms) < 2:
        violations.append(Violation(domain_name, "error", "min_llms",
            f"config.yaml must define at least 2 LLMs, found {len(llms)}", "config.yaml"))

    if len(agents) == 0:
        violations.append(Violation(domain_name, "error", "min_agents", "config.yaml must define at least 1 agent", "config.yaml"))
    else:
        for agent_name, agent_doc in agents.items():
            spec = agent_doc.get("spec", agent_doc)
            if isinstance(spec, dict):
                agent_llm = spec.get("config", {}).get("llm") if isinstance(spec.get("config"), dict) else spec.get("llm")
                if agent_llm and agent_llm not in llms:
                    violations.append(Violation(domain_name, "error", "agent_llm_ref",
                        f"Agent '{agent_name}' references llm '{agent_llm}' which is not defined", "config.yaml"))

    if len(benchmarks) == 0:
        violations.append(Violation(domain_name, "error", "min_benchmarks", "config.yaml must define at least 1 benchmark", "config.yaml"))
    else:
        referenced_tasks = set()
        for bm in benchmarks:
            spec = bm.get("spec", bm)
            if isinstance(spec, dict):
                tasks = spec.get("tasks", [])
                for task_entry in tasks:
                    if isinstance(task_entry, str):
                        task_path = domain_dir / task_entry
                        if not task_path.exists():
                            violations.append(Violation(domain_name, "error", "task_ghost",
                                f"Benchmark references non-existent task: {task_entry}", "config.yaml"))
                        else:
                            referenced_tasks.add(task_entry)
                    elif isinstance(task_entry, dict):
                        task_path_str = task_entry.get("path", task_entry.get("file", ""))
                        if task_path_str:
                            task_path = domain_dir / task_path_str
                            if not task_path.exists():
                                violations.append(Violation(domain_name, "error", "task_ghost",
                                    f"Benchmark references non-existent task: {task_path_str}", "config.yaml"))
                            else:
                                referenced_tasks.add(task_path_str)

    tasks_dir = domain_dir / "tasks"
    if tasks_dir.exists():
        all_task_files = set()
        for task_file in tasks_dir.glob("*.json"):
            rel_path = f"tasks/{task_file.name}"
            all_task_files.add(rel_path)
        orphans = all_task_files - referenced_tasks
        if orphans:
            for orphan in sorted(orphans):
                violations.append(Violation(domain_name, "warning", "task_orphan",
                    f"Task file not referenced by any benchmark: {orphan}", orphan))

    functions_path = domain_dir / "evaluators" / "functions.py"
    if tasks_dir.exists():
        registered_ops = extract_op_names_from_functions(functions_path)
        for task_file in sorted(tasks_dir.glob("*.json")):
            task_violations = validate_task_json(domain_name, task_file, registered_ops)
            violations.extend(task_violations)

    if functions_path.exists():
        stubs = check_for_stub_functions(functions_path)
        for stub in stubs:
            violations.append(Violation(domain_name, "error", "stub_function",
                f"Stub function (pass/... only): {stub}()", "evaluators/functions.py"))
        unreachable = check_for_unreachable_imports(functions_path)
        for imp in unreachable:
            violations.append(Violation(domain_name, "error", "unreachable_import",
                f"Import without try/except ImportError fallback: {imp}", "evaluators/functions.py"))
    else:
        violations.append(Violation(domain_name, "error", "evaluators_missing",
            "evaluators/functions.py not found", "evaluators/functions.py"))

    return violations


def validate_task_json(domain_name: str, task_path: Path, registered_ops: set[str]) -> list[Violation]:
    violations = []
    rel_path = f"tasks/{task_path.name}"
    try:
        with open(task_path) as f:
            task = json.load(f)
    except json.JSONDecodeError as e:
        violations.append(Violation(domain_name, "error", "task_json_parse", f"Invalid JSON: {e}", rel_path))
        return violations

    if "question" not in task or not task["question"]:
        violations.append(Violation(domain_name, "error", "task_question", "Missing or empty 'question'", rel_path))

    if "evaluators" not in task:
        violations.append(Violation(domain_name, "error", "task_evaluators", "Missing 'evaluators' field", rel_path))
    elif not isinstance(task["evaluators"], list):
        violations.append(Violation(domain_name, "error", "task_evaluators_type", "'evaluators' must be a list", rel_path))
    elif len(task["evaluators"]) == 0:
        violations.append(Violation(domain_name, "error", "task_evaluators_empty", "'evaluators' is empty", rel_path))
    else:
        for i, ev in enumerate(task["evaluators"]):
            if not isinstance(ev, dict):
                violations.append(Violation(domain_name, "error", "evaluator_type", f"evaluators[{i}] must be a dict", rel_path))
                continue
            func_type = ev.get("func", "")
            if not func_type:
                violations.append(Violation(domain_name, "error", "evaluator_func", f"evaluators[{i}] missing 'func'", rel_path))
            op = ev.get("op", "")
            if func_type == "raw" and not op:
                violations.append(Violation(domain_name, "error", "evaluator_op", f"evaluators[{i}] func='raw' but missing 'op'", rel_path))
            if op and op != "=" and op not in registered_ops:
                violations.append(Violation(domain_name, "warning", "evaluator_op_exists",
                    f"evaluators[{i}] op='{op}' not found in evaluators/functions.py (may be external)", rel_path))

    has_mcp_servers = bool(task.get("mcp_servers"))
    use_specified = task.get("use_specified_server")
    if has_mcp_servers and not use_specified:
        violations.append(Violation(domain_name, "error", "use_specified_server",
            "Task has mcp_servers but use_specified_server is not true", rel_path))
    if use_specified is False and has_mcp_servers:
        violations.append(Violation(domain_name, "error", "use_specified_server_conflict",
            "use_specified_server=false but task has mcp_servers", rel_path))

    return violations


def check_slop() -> list[Violation]:
    violations = []
    for slop_dir in SLOP_DIRS:
        if (REPO_ROOT / slop_dir).exists():
            violations.append(Violation("_global", "error", "slop_dir", f"Slop directory exists: {slop_dir}/", slop_dir))
    for slop_file in SLOP_FILES:
        if (REPO_ROOT / slop_file).exists():
            violations.append(Violation("_global", "error", "slop_file", f"Slop file exists: {slop_file}", slop_file))
    for item in REPO_ROOT.iterdir():
        if item.name.startswith("."):
            continue
        for pattern in SLOP_NAME_PATTERNS:
            if re.match(pattern, item.name):
                violations.append(Violation("_global", "error", "slop_name", f"Slop-named file: {item.name}", item.name))
    return violations


def discover_domains() -> list[str]:
    domains = []
    for item in DOMAINS_DIR.iterdir():
        if item.is_dir() and (item / "config.yaml").exists():
            domains.append(item.name)
    return sorted(domains)


def main():
    parser = argparse.ArgumentParser(description="Validate MCP benchmark domains")
    parser.add_argument("--domain", type=str, help="Specific domain to validate")
    parser.add_argument("--all", action="store_true", help="Validate all domains")
    parser.add_argument("--check-slop", action="store_true", help="Check for slop files/dirs")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    if not args.domain and not args.all and not args.check_slop:
        parser.print_help()
        sys.exit(1)

    all_violations: list[Violation] = []
    domains_to_check: list[str] = []

    if args.check_slop:
        slop_violations = check_slop()
        all_violations.extend(slop_violations)

    if args.all:
        domains_to_check = discover_domains()
    elif args.domain:
        domains_to_check = [args.domain]

    domain_results = {}
    for domain in domains_to_check:
        violations = validate_domain(domain)
        domain_results[domain] = violations
        all_violations.extend(violations)

    errors = [v for v in all_violations if v.severity == "error"]
    warnings = [v for v in all_violations if v.severity == "warning"]

    if args.json:
        output = {
            "domains_checked": domains_to_check,
            "total_errors": len(errors),
            "total_warnings": len(warnings),
            "results": {},
        }
        for domain in domains_to_check:
            domain_v = domain_results.get(domain, [])
            output["results"][domain] = {
                "errors": [v for v in domain_v if v.severity == "error"],
                "warnings": [v for v in domain_v if v.severity == "warning"],
            }
        if args.check_slop:
            slop_v = [v for v in all_violations if v.domain == "_global"]
            output["slop_check"] = {
                "errors": [v for v in slop_v if v.severity == "error"],
                "warnings": [v for v in slop_v if v.severity == "warning"],
            }
        print(json.dumps(output, indent=2, default=lambda o: o.__dict__))
    else:
        if args.check_slop:
            slop_v = [v for v in all_violations if v.domain == "_global"]
            if slop_v:
                print("\n=== SLOP CHECK ===")
                for v in slop_v:
                    print(v)
            else:
                print("\n=== SLOP CHECK ===")
                print("  No slop files/dirs found.")

        for domain in domains_to_check:
            domain_v = domain_results.get(domain, [])
            domain_errors = [v for v in domain_v if v.severity == "error"]
            domain_warnings = [v for v in domain_v if v.severity == "warning"]
            status = "PASS" if len(domain_errors) == 0 else "FAIL"
            print(f"\n{'='*60}")
            print(f"  {domain}: {status} ({len(domain_errors)} errors, {len(domain_warnings)} warnings)")
            print(f"{'='*60}")
            for v in domain_v:
                print(v)

        print(f"\n{'='*60}")
        print(f"  SUMMARY: {len(errors)} errors, {len(warnings)} warnings across {len(domains_to_check)} domains")
        print(f"{'='*60}")
        if len(errors) == 0:
            print("  ALL DOMAINS PASS")
        else:
            print("  VALIDATION FAILED")
            for v in errors:
                print(f"    {v.domain}: {v.rule} - {v.message}")

    sys.exit(1 if len(errors) > 0 else 0)


if __name__ == "__main__":
    main()
