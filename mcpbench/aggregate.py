"""Aggregate all workers' JSONL into a stress report + figures.

Reads:
    /mnt/results/stress/<worker>/runs.jsonl   (from every worker)
Writes:
    /mnt/results/stress/runs.jsonl            (merged)
    /mnt/results/stress/report_stress.md      (readable report)
    /mnt/results/stress/figures/*.png         (leaderboard, latency violin,
                                               failure heatmap, robustness delta,
                                               throughput curve, rate-limit curve)
    /mnt/results/stress/stress_summary.json   (machine-readable summary)

Independent of the runner — usable by any worker at the end.
"""
from __future__ import annotations
import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Optional

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = ["Liberation Sans", "Arimo", "DejaVu Sans"]
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt
import numpy as np


def iter_worker_jsonls(root: Path) -> Iterable[Path]:
    """Yield all runs*.jsonl under every worker directory, EXCLUDING
    archived _v1_ files (deprecated runs from before the anyio-cancel
    fix)."""
    for p in root.glob("*/runs*.jsonl"):
        if "_v1_" in p.name:
            continue
        yield p


def load_all_runs(root: Path) -> list[dict]:
    runs: list[dict] = []
    for p in iter_worker_jsonls(root):
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    runs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return runs


def percentile(xs: list[float], p: float) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    if f == c:
        return xs[f]
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def pass_at_k(n_correct: int, n: int, k: int) -> float:
    """Standard Kulal et al. estimator."""
    if n - n_correct < k:
        return 1.0
    if k > n:
        return float(n_correct > 0)
    # 1 - C(n - c, k) / C(n, k)
    return 1.0 - math.comb(n - n_correct, k) / math.comb(n, k)


def compute_pass_at_k_curve(runs_for_task_model: list[dict]) -> dict:
    n = len(runs_for_task_model)
    c = sum(1 for r in runs_for_task_model if r.get("passed"))
    return {
        "n": n,
        "correct": c,
        "pass@1": pass_at_k(c, n, 1) if n >= 1 else 0.0,
        "pass@3": pass_at_k(c, n, 3) if n >= 3 else pass_at_k(c, n, min(3, n)),
        "pass@5": pass_at_k(c, n, 5) if n >= 5 else pass_at_k(c, n, min(5, n)),
    }


def leaderboard(runs: list[dict]) -> dict[str, dict]:
    by_model: dict[str, list[dict]] = defaultdict(list)
    for r in runs:
        by_model[r["model"]].append(r)

    board = {}
    for model, rs in by_model.items():
        # only baseline for the leaderboard
        base = [r for r in rs if r.get("perturbation_id", "baseline") == "baseline"
                and r.get("category") in ("baseline", "concurrency")]
        # group by task to compute pass@k
        by_task = defaultdict(list)
        for r in base:
            by_task[r["task"]].append(r)
        p1 = [pass_at_k(sum(1 for x in v if x["passed"]), len(v), 1) for v in by_task.values() if v]
        p3 = [pass_at_k(sum(1 for x in v if x["passed"]), len(v), 3) for v in by_task.values() if len(v) >= 1]
        p5 = [pass_at_k(sum(1 for x in v if x["passed"]), len(v), 5) for v in by_task.values() if len(v) >= 1]
        lats = [r["latency_ms"] for r in base if isinstance(r.get("latency_ms"), (int, float))]
        board[model] = {
            "n_runs": len(base),
            "pass_rate": sum(1 for r in base if r["passed"]) / len(base) if base else 0.0,
            "pass@1_mean": sum(p1) / len(p1) if p1 else 0.0,
            "pass@3_mean": sum(p3) / len(p3) if p3 else 0.0,
            "pass@5_mean": sum(p5) / len(p5) if p5 else 0.0,
            "p50_ms": percentile(lats, 0.5),
            "p95_ms": percentile(lats, 0.95),
            "p99_ms": percentile(lats, 0.99),
        }
    return board


def failure_taxonomy(runs: list[dict]) -> dict[str, dict[str, int]]:
    """Return {model: {failure_class: count}}."""
    out: dict[str, Counter] = defaultdict(Counter)
    for r in runs:
        if r.get("category") == "baseline":
            out[r["model"]][r.get("failure_class", "unknown_error")] += 1
    return {m: dict(c) for m, c in out.items()}


def robustness_delta(runs: list[dict]) -> dict:
    """For each model x perturbation, pass rate delta vs baseline."""
    by_model_pert: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in runs:
        pid = r.get("perturbation_id", "baseline")
        if r.get("category") not in ("baseline", "adversarial"):
            continue
        by_model_pert[(r["model"], pid)].append(r)

    baseline_rate: dict[str, float] = {}
    for (m, pid), rs in by_model_pert.items():
        if pid == "baseline":
            baseline_rate[m] = sum(1 for r in rs if r["passed"]) / len(rs) if rs else 0.0

    out = {}
    for (m, pid), rs in by_model_pert.items():
        if pid == "baseline" or not rs:
            continue
        pert_rate = sum(1 for r in rs if r["passed"]) / len(rs)
        out.setdefault(m, {})[pid] = {
            "baseline_rate": baseline_rate.get(m, 0.0),
            "perturbed_rate": pert_rate,
            "delta": pert_rate - baseline_rate.get(m, 0.0),
            "n": len(rs),
        }
    return out


def concurrency_curve(runs: list[dict]) -> dict:
    """{concurrency_level: [latency_ms,...]}"""
    out: dict[int, list[float]] = defaultdict(list)
    for r in runs:
        if r.get("category") != "concurrency":
            continue
        cl = int(r.get("concurrency", 1))
        out[cl].append(r["latency_ms"])
    summary = {}
    for cl, lats in sorted(out.items()):
        summary[cl] = {
            "n": len(lats),
            "p50_ms": percentile(lats, 0.5),
            "p95_ms": percentile(lats, 0.95),
            "throughput_rps": len(lats) / (max(lats) / 1000.0) if lats and max(lats) > 0 else 0.0,
        }
    return summary


def rate_limit_summary(runs: list[dict]) -> dict:
    """Per model: fraction of runs that hit rate_limit."""
    by_model: dict[str, list[dict]] = defaultdict(list)
    for r in runs:
        if r.get("category") == "ratelimit":
            by_model[r["model"]].append(r)
    out = {}
    for m, rs in by_model.items():
        rl = sum(1 for r in rs if r.get("failure_class") == "rate_limit")
        first_429_idx = next(
            (i for i, r in enumerate(rs) if r.get("failure_class") == "rate_limit"),
            None,
        )
        out[m] = {
            "n": len(rs),
            "rate_limit_hits": rl,
            "rate_limit_frac": rl / len(rs) if rs else 0.0,
            "first_429_request_index": first_429_idx,
        }
    return out


def fault_summary(runs: list[dict]) -> dict:
    """Aggregate fault-injection runs: pass rate, tool-call injected-fault
    counts, recovery patterns per model."""
    by_model: dict[str, dict] = defaultdict(lambda: {
        "n": 0,
        "passed": 0,
        "n_tool_calls": 0,
        "n_injected_faults": 0,
        "recovered_from_fault": 0,
    })
    fault_class_counts: Counter = Counter()
    for r in runs:
        if r.get("category") != "faults":
            continue
        m = r["model"]
        d = by_model[m]
        d["n"] += 1
        d["passed"] += int(r.get("passed", False))
        tool_calls = r.get("per_tool_calls") or []
        d["n_tool_calls"] += len(tool_calls)
        injected = [
            t for t in tool_calls
            if t.get("error") and "Fault-injected" in (t.get("error") or "")
        ]
        d["n_injected_faults"] += len(injected)
        for t in injected:
            err = t.get("error", "")
            if "empty" in err.lower():
                fault_class_counts["empty_string"] += 1
            elif "delay" in err.lower():
                fault_class_counts["delay_3s"] += 1
            elif "500" in err:
                fault_class_counts["simulated_500"] += 1
            elif "json" in err.lower() or "malformed" in err.lower():
                fault_class_counts["malformed_json"] += 1
            else:
                fault_class_counts["other"] += 1
        # a run "recovered" if it passed despite ≥1 injected fault
        if injected and r.get("passed"):
            d["recovered_from_fault"] += 1
    return {
        "by_model": dict(by_model),
        "fault_class_hits": dict(fault_class_counts),
    }


# ------------------- figures -------------------
def _save_fig(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def fig_leaderboard(board: dict, out: Path):
    if not board:
        return
    models = sorted(board.keys(), key=lambda m: -board[m]["pass_rate"])
    rates = [board[m]["pass_rate"] for m in models]
    fig, ax = plt.subplots(figsize=(9, 0.35 * len(models) + 1.5))
    ax.barh(range(len(models)), rates, color="#0279EE")
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([m.replace("openrouter/", "") for m in models])
    ax.invert_yaxis()
    ax.set_xlabel("pass rate (baseline)")
    ax.set_xlim(0, 1)
    ax.set_title("Model leaderboard — baseline pass rate")
    for i, v in enumerate(rates):
        ax.text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=9)
    _save_fig(fig, out)


def fig_latency(runs: list[dict], out: Path):
    by_model: dict[str, list[float]] = defaultdict(list)
    for r in runs:
        if r.get("category") == "baseline":
            by_model[r["model"]].append(r["latency_ms"])
    if not by_model:
        return
    models = sorted(by_model.keys())
    data = [by_model[m] for m in models]
    fig, ax = plt.subplots(figsize=(9, 0.35 * len(models) + 1.5))
    parts = ax.violinplot(data, vert=False, showmeans=True, showextrema=True)
    for pc in parts["bodies"]:
        pc.set_facecolor("#FF9400")
        pc.set_alpha(0.7)
    ax.set_yticks(range(1, len(models) + 1))
    ax.set_yticklabels([m.replace("openrouter/", "") for m in models])
    ax.set_xlabel("latency (ms)")
    ax.set_title("Latency distribution per model (baseline)")
    _save_fig(fig, out)


def fig_failure_heatmap(failures: dict, out: Path):
    if not failures:
        return
    all_classes = sorted({c for cls in failures.values() for c in cls})
    models = sorted(failures.keys())
    mat = np.array([[failures[m].get(c, 0) for c in all_classes] for m in models])
    if mat.size == 0:
        return
    fig, ax = plt.subplots(figsize=(1 + len(all_classes) * 1.1, 0.4 * len(models) + 1.5))
    im = ax.imshow(mat, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(all_classes)))
    ax.set_xticklabels(all_classes, rotation=45, ha="right")
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([m.replace("openrouter/", "") for m in models])
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = int(mat[i, j])
            if v > 0:
                ax.text(j, i, str(v), ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, label="# runs")
    ax.set_title("Failure taxonomy heatmap (baseline)")
    _save_fig(fig, out)


def fig_robustness(delta: dict, out: Path):
    if not delta:
        return
    perts = sorted({p for m in delta.values() for p in m})
    models = sorted(delta.keys())
    mat = np.array([[delta[m].get(p, {}).get("delta", 0.0) for p in perts] for m in models])
    if mat.size == 0:
        return
    fig, ax = plt.subplots(figsize=(1 + len(perts) * 1.5, 0.4 * len(models) + 1.5))
    lim = float(max(abs(mat.min()), abs(mat.max()), 0.05))
    im = ax.imshow(mat, cmap="RdBu", vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(len(perts)))
    ax.set_xticklabels(perts, rotation=25, ha="right")
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([m.replace("openrouter/", "") for m in models])
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i,j]:+.2f}", ha="center", va="center",
                    fontsize=8, color="black")
    fig.colorbar(im, ax=ax, label="Δ pass rate")
    ax.set_title("Robustness delta (perturbed − baseline)")
    _save_fig(fig, out)


def fig_concurrency(curve: dict, out: Path):
    if not curve:
        return
    xs = sorted(curve.keys())
    p50 = [curve[x]["p50_ms"] for x in xs]
    p95 = [curve[x]["p95_ms"] for x in xs]
    thr = [curve[x]["throughput_rps"] for x in xs]
    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.plot(xs, p50, "-o", color="#0279EE", label="p50 latency (left)")
    ax1.plot(xs, p95, "-^", color="#FF9400", label="p95 latency (left)")
    ax1.set_xlabel("concurrency level (log₂ scale)")
    ax1.set_ylabel("latency (ms)")
    ax1.set_xscale("log", base=2)
    ax1.set_xticks(xs)
    ax1.set_xticklabels([str(x) for x in xs])
    ax1.grid(alpha=0.3)
    ax2 = ax1.twinx()
    ax2.plot(xs, thr, "-s", color="#000000", label="throughput (right)")
    ax2.set_ylabel("throughput (rps)")
    ax1.set_title("Latency & throughput vs concurrency")
    # Combined legend
    l1, lab1 = ax1.get_legend_handles_labels()
    l2, lab2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, lab1 + lab2, loc="upper left")
    _save_fig(fig, out)


def fig_ratelimit(summary: dict, out: Path):
    if not summary:
        return
    models = sorted(summary.keys())
    frac = [summary[m]["rate_limit_frac"] for m in models]
    fig, ax = plt.subplots(figsize=(9, 0.4 * len(models) + 1.5))
    ax.barh(range(len(models)), frac, color="#75A025")
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([m.replace("openrouter/", "") for m in models])
    ax.set_xlabel("fraction of runs 429'd")
    ax.set_xlim(0, 1)
    ax.set_title("Rate-limit incidence per model")
    for i, v in enumerate(frac):
        ax.text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=9)
    _save_fig(fig, out)


def fig_faults(summary: dict, out: Path):
    """Bar chart: pass rate under fault injection per model + fault class counts."""
    if not summary or not summary.get("by_model"):
        return
    by_model = summary["by_model"]
    fault_classes = summary.get("fault_class_hits", {})

    models = sorted(by_model.keys())
    pass_rates = [by_model[m]["passed"] / by_model[m]["n"] if by_model[m]["n"] else 0
                  for m in models]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, max(3, 0.4 * len(models) + 1.5)))

    # Left: per-model pass rate under faults
    ax1.barh(range(len(models)), pass_rates, color="#FD9BED")
    ax1.set_yticks(range(len(models)))
    ax1.set_yticklabels([m.split("/", 1)[-1] for m in models])
    ax1.invert_yaxis()
    ax1.set_xlim(0, 1)
    ax1.set_xlabel("pass rate under fault injection")
    ax1.set_title("Model robustness to injected tool faults")
    for i, v in enumerate(pass_rates):
        n = by_model[models[i]]["n"]
        ax1.text(v + 0.01, i, f"{v:.2f} (n={n})", va="center", fontsize=9)

    # Right: fault class distribution
    classes = sorted(fault_classes.keys())
    counts = [fault_classes[c] for c in classes]
    if classes:
        ax2.bar(range(len(classes)), counts, color="#E9ED4C")
        ax2.set_xticks(range(len(classes)))
        ax2.set_xticklabels(classes, rotation=30, ha="right")
        ax2.set_ylabel("hits")
        ax2.set_title("Injected fault class distribution")
        for i, v in enumerate(counts):
            ax2.text(i, v + 0.1, str(v), ha="center", fontsize=9)
    else:
        ax2.text(0.5, 0.5, "no fault injection\ntool calls recorded",
                 ha="center", va="center", transform=ax2.transAxes)
        ax2.set_xticks([])
        ax2.set_yticks([])
    _save_fig(fig, out)


# ------------------- report -------------------
def write_report(
    root: Path,
    runs: list[dict],
    board: dict,
    failures: dict,
    delta: dict,
    conc: dict,
    rl: dict,
    faults: Optional[dict] = None,
):
    md = ["# Stress Report — mcp-universe-benchmarks\n"]
    md.append(f"Total runs: **{len(runs)}**  ")
    cats = Counter(r.get("category", "?") for r in runs)
    md.append(f"Category mix: {dict(cats)}\n")

    md.append("## Model leaderboard (baseline)\n")
    md.append("| Model | n | pass rate | pass@1 | pass@3 | pass@5 | p50 ms | p95 ms | p99 ms |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for m in sorted(board.keys(), key=lambda x: -board[x]["pass_rate"]):
        b = board[m]
        md.append(
            f"| {m.replace('openrouter/', '')} | {b['n_runs']} | {b['pass_rate']:.2f} "
            f"| {b['pass@1_mean']:.2f} | {b['pass@3_mean']:.2f} | {b['pass@5_mean']:.2f} "
            f"| {b['p50_ms']:.0f} | {b['p95_ms']:.0f} | {b['p99_ms']:.0f} |"
        )
    md.append("\n![Leaderboard](figures/leaderboard.png)\n")
    md.append("![Latency distribution](figures/latency_violin.png)\n")

    if failures:
        md.append("## Failure taxonomy (baseline)\n")
        md.append("![Failure heatmap](figures/failure_heatmap.png)\n")
        for m, cls in failures.items():
            md.append(f"- **{m.replace('openrouter/', '')}** — {dict(cls)}")
        md.append("")

    if delta:
        md.append("## Robustness delta (perturbed vs baseline)\n")
        md.append("Negative Δ = perturbation hurt the model.\n")
        md.append("![Robustness](figures/robustness_delta.png)\n")
        md.append("| Model | Perturbation | n | baseline | perturbed | Δ |")
        md.append("|---|---|---:|---:|---:|---:|")
        for m in sorted(delta.keys()):
            for pid, d in sorted(delta[m].items()):
                md.append(
                    f"| {m.replace('openrouter/', '')} | {pid} | {d['n']} "
                    f"| {d['baseline_rate']:.2f} | {d['perturbed_rate']:.2f} | {d['delta']:+.2f} |"
                )
        md.append("")

    if conc:
        md.append("## Load / concurrency\n")
        md.append("![Latency vs concurrency](figures/concurrency.png)\n")
        md.append("| concurrency | n | p50 ms | p95 ms | throughput rps |")
        md.append("|---:|---:|---:|---:|---:|")
        for cl in sorted(conc):
            c = conc[cl]
            md.append(f"| {cl} | {c['n']} | {c['p50_ms']:.0f} | {c['p95_ms']:.0f} | {c['throughput_rps']:.2f} |")
        md.append("")

    if rl:
        md.append("## Rate-limit probe\n")
        md.append("![Rate-limit](figures/ratelimit.png)\n")
        md.append("| Model | n | 429 hits | fraction | first-429 idx |")
        md.append("|---|---:|---:|---:|---:|")
        for m in sorted(rl):
            r = rl[m]
            md.append(f"| {m.replace('openrouter/', '')} | {r['n']} | {r['rate_limit_hits']} | {r['rate_limit_frac']:.2f} | {r['first_429_request_index']} |")
        md.append("")

    if faults and faults.get("by_model"):
        md.append("## Fault-injection resilience\n")
        md.append(
            "Runs in category=`faults` had the MCP tool responses randomly "
            "corrupted (empty string, +3s delay, malformed JSON, simulated 500). "
            "Below: per-model pass rate under those conditions, and the injected "
            "fault-class hit counts observed.\n"
        )
        md.append("![Fault injection](figures/faults.png)\n")
        md.append("| Model | n | passed | pass rate | tool calls | injected faults | recovered |")
        md.append("|---|---:|---:|---:|---:|---:|---:|")
        for m, d in sorted(faults["by_model"].items()):
            pr = d["passed"] / d["n"] if d["n"] else 0
            md.append(
                f"| {m.split('/', 1)[-1]} | {d['n']} | {d['passed']} | {pr:.2f} "
                f"| {d['n_tool_calls']} | {d['n_injected_faults']} | {d['recovered_from_fault']} |"
            )
        md.append("")
        if faults.get("fault_class_hits"):
            md.append("### Fault-class hits\n")
            for cls, n in sorted(faults["fault_class_hits"].items()):
                md.append(f"- **{cls}**: {n}")
            md.append("")

    md.append("## Provenance\n")
    md.append(f"Raw runs: `runs.jsonl` ({len(runs)} lines). See per-worker JSONLs under this directory.\n")

    (root / "report_stress.md").write_text("\n".join(md))


def run_aggregation(stress_root: Path):
    stress_root = Path(stress_root)
    stress_root.mkdir(parents=True, exist_ok=True)

    runs = load_all_runs(stress_root)

    # merged jsonl
    with open(stress_root / "runs.jsonl", "w") as f:
        for r in runs:
            f.write(json.dumps(r) + "\n")

    board = leaderboard(runs)
    failures = failure_taxonomy(runs)
    delta = robustness_delta(runs)
    conc = concurrency_curve(runs)
    rl = rate_limit_summary(runs)
    faults = fault_summary(runs)

    figdir = stress_root / "figures"
    fig_leaderboard(board, figdir / "leaderboard.png")
    fig_latency(runs, figdir / "latency_violin.png")
    fig_failure_heatmap(failures, figdir / "failure_heatmap.png")
    fig_robustness(delta, figdir / "robustness_delta.png")
    fig_concurrency(conc, figdir / "concurrency.png")
    fig_ratelimit(rl, figdir / "ratelimit.png")
    fig_faults(faults, figdir / "faults.png")

    with open(stress_root / "stress_summary.json", "w") as f:
        json.dump({
            "n_runs": len(runs),
            "leaderboard": board,
            "failures": failures,
            "robustness_delta": delta,
            "concurrency": conc,
            "rate_limit": rl,
            "faults": faults,
        }, f, indent=2)

    write_report(stress_root, runs, board, failures, delta, conc, rl, faults)
    return {
        "n_runs": len(runs),
        "n_models": len(board),
        "report_path": str(stress_root / "report_stress.md"),
    }
