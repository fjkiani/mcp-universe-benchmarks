"""CLI entrypoint for mcpbench — replaces alignerr_mcp."""
import sys
import json
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(
    name="mcpbench",
    help="MCP Universe Benchmarks — validate, run, and list models.",
    no_args_is_help=True,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


@app.command()
def validate(
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Specific domain to validate"),
    all_domains: bool = typer.Option(False, "--all", "-a", help="Validate all domains"),
    check_slop: bool = typer.Option(False, "--check-slop", help="Check for slop files/dirs"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Validate domain structure against the benchmark contract."""
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.validate import validate_domain, check_slop, discover_domains, Violation

    all_violations = []
    domains_to_check = []

    if check_slop:
        all_violations.extend(check_slop())

    if all_domains:
        domains_to_check = discover_domains()
    elif domain:
        domains_to_check = [domain]
    else:
        typer.echo("Error: must specify --domain or --all")
        raise typer.Exit(1)

    domain_results = {}
    for d in domains_to_check:
        v = validate_domain(d)
        domain_results[d] = v
        all_violations.extend(v)

    errors = [v for v in all_violations if v.severity == "error"]
    warnings = [v for v in all_violations if v.severity == "warning"]

    if json_output:
        output = {
            "domains_checked": domains_to_check,
            "total_errors": len(errors),
            "total_warnings": len(warnings),
            "results": {},
        }
        for d in domains_to_check:
            dv = domain_results.get(d, [])
            output["results"][d] = {
                "errors": [v.__dict__ for v in dv if v.severity == "error"],
                "warnings": [v.__dict__ for v in dv if v.severity == "warning"],
            }
        typer.echo(json.dumps(output, indent=2))
    else:
        for d in domains_to_check:
            dv = domain_results.get(d, [])
            de = [v for v in dv if v.severity == "error"]
            dw = [v for v in dv if v.severity == "warning"]
            status = "PASS" if len(de) == 0 else "FAIL"
            typer.echo(f"\n{'='*60}")
            typer.echo(f"  {d}: {status} ({len(de)} errors, {len(dw)} warnings)")
            typer.echo(f"{'='*60}")
            for v in dv:
                typer.echo(str(v))

        typer.echo(f"\n{'='*60}")
        typer.echo(f"  SUMMARY: {len(errors)} errors, {len(warnings)} warnings across {len(domains_to_check)} domains")
        typer.echo(f"{'='*60}")
        if len(errors) == 0:
            typer.echo("  ALL DOMAINS PASS")
        else:
            typer.echo("  VALIDATION FAILED")

    raise typer.Exit(1 if len(errors) > 0 else 0)


@app.command()
def run(
    domain: str = typer.Option(..., "--domain", "-d", help="Domain to run"),
    models: str = typer.Option("openrouter/meta-llama/llama-3.3-70b-instruct:free", "--models", "-m", help="Comma-separated model slugs"),
    runs: int = typer.Option(1, "--runs", "-r", help="Runs per model (Pass@K)"),
    concurrent: int = typer.Option(1, "--concurrent", "-c", help="Max concurrent runs"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate without LLM calls"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
):
    """Run benchmark evaluation against one or more models."""
    sys.path.insert(0, str(REPO_ROOT))
    from mcpbench.runner import BenchmarkRunner

    runner = BenchmarkRunner(
        repo_root=REPO_ROOT,
        domain=domain,
        models=[m.strip() for m in models.split(",")],
        runs_per_model=runs,
        concurrent_runs=concurrent,
        dry_run=dry_run,
    )
    results = runner.run()

    results_json = json.dumps(results, indent=2, default=str)
    if output:
        Path(output).write_text(results_json)
        typer.echo(f"Results written to {output}")
    else:
        typer.echo(results_json)


@app.command()
def stress(
    category: str = typer.Option(..., "--category", "-c",
        help="baseline | adversarial | faults | concurrency | ratelimit"),
    domain: str = typer.Option(..., "--domain", "-d", help="Domain to run"),
    models: str = typer.Option(..., "--models", "-m",
        help="Comma-separated model slugs"),
    runs: int = typer.Option(3, "--runs", "-r",
        help="Runs per (task, model) — controls pass@k"),
    perturbation: str = typer.Option("baseline", "--perturbation",
        help="baseline | prompt_injection | contradictory | noisy_prefix | gold_swap | all"),
    concurrency: int = typer.Option(1, "--concurrency",
        help="For --category concurrency: parallel-run level"),
    max_tasks: int = typer.Option(0, "--max-tasks",
        help="If >0, only run first N tasks of the domain (for smoke tests)"),
    worker_id: str = typer.Option("worker-0", "--worker-id",
        help="Worker tag written into every run record"),
    out_dir: str = typer.Option("/mnt/results/stress", "--out-dir",
        help="Root output directory"),
    fault_seed: int = typer.Option(0, "--fault-seed",
        help="RNG seed for fault injection (category=faults)"),
    dry_run: bool = typer.Option(False, "--dry-run",
        help="Skip real LLM calls; just exercise the pipeline"),
):
    """Run a stress-test category and append JSONL to <out-dir>/<worker-id>/runs.jsonl."""
    import asyncio
    sys.path.insert(0, str(REPO_ROOT))
    from mcpbench.stress import StressRunner
    from mcpbench.perturbations import apply_perturbation, PERTURBATIONS
    from mcpbench.fault_injection import FaultInjector

    model_list = [m.strip() for m in models.split(",")]
    out_path = Path(out_dir) / worker_id / "runs.jsonl"

    # perturbation set
    if category == "adversarial":
        perts = list(PERTURBATIONS.keys()) if perturbation == "all" else [perturbation]
        if "baseline" in perts:
            perts.remove("baseline")
    else:
        perts = ["baseline"]

    # fault injection hook
    tool_hook = None
    if category == "faults":
        injector = FaultInjector(seed=fault_seed)
        tool_hook = injector.hook

    # NOTE: max_tasks caps the tasks per benchmark spec (per model), not the
    # total across all models. Applied inside StressRunner via slice.
    task_filter = None

    all_results = []
    for pid in perts:
        # For adversarial category we need to mutate loaded tasks. We do that
        # by monkeypatching StressRunner._load_tasks.
        runner = StressRunner(
            repo_root=REPO_ROOT,
            domain=domain,
            models=model_list,
            runs_per_model=runs,
            concurrent_runs=1,
            dry_run=dry_run,
            out_path=out_path,
            worker_id=worker_id,
            category=category,
            perturbation_id=pid,
            tool_call_hook=tool_hook,
            task_filter=task_filter,
        )

        # max_tasks: slice each benchmark's task list — applied per-load,
        # so every (model × benchmark) pass respects the cap independently.
        if max_tasks > 0:
            original_load = runner._load_tasks
            def _sliced(bm, _orig=original_load, _n=max_tasks):
                return _orig(bm)[:_n]
            runner._load_tasks = _sliced

        if pid != "baseline":
            base_load = runner._load_tasks
            def _wrapped(bm, _base=base_load):
                tasks = _base(bm)
                return [apply_perturbation(pid, t) for t in tasks]
            runner._load_tasks = _wrapped

        result = runner.run()
        # tag concurrency runs
        if category == "concurrency":
            for r in result["results"]:
                r["concurrency"] = concurrency
        all_results.append(result)

    typer.echo(json.dumps({
        "category": category,
        "worker_id": worker_id,
        "domain": domain,
        "n_runs": sum(len(r["results"]) for r in all_results),
        "runs_jsonl": str(out_path),
    }, indent=2))


@app.command()
def aggregate(
    root: str = typer.Option("/mnt/results/stress", "--root",
        help="Stress root — one subdirectory per worker with runs.jsonl"),
):
    """Merge all workers' JSONL, compute stats, write report_stress.md + figures."""
    sys.path.insert(0, str(REPO_ROOT))
    from mcpbench.aggregate import run_aggregation
    summary = run_aggregation(Path(root))
    typer.echo(json.dumps(summary, indent=2))


@app.command(name="list-models")
def list_models(
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="Filter by provider"),
    tier: Optional[str] = typer.Option(None, "--tier", "-t", help="Filter by tier (free/paid)"),
):
    """List available models from the model registry."""
    sys.path.insert(0, str(REPO_ROOT))
    from mcpbench.models import ModelRegistry

    registry = ModelRegistry(REPO_ROOT / "mcpbench" / "models.yaml")
    models = registry.list_models(provider=provider, tier=tier)

    if not models:
        typer.echo("No models found matching criteria.")
        return

    typer.echo(f"\n{'Slug':55s} {'Provider':12s} {'Tier':6s} {'Context':>10s}  Tools")
    typer.echo("-" * 95)
    for m in models:
        tools = "yes" if m.get("supports_tools") else "no"
        typer.echo(f"{m['slug']:55s} {m['provider']:12s} {m['tier']:6s} {m.get('context',0):>10}  {tools}")


if __name__ == "__main__":
    app()
