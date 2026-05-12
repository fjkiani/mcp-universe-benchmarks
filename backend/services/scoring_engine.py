"""
Hierarchical Scoring Engine — L1 through L4 with certification grades.

Level mapping:
  L1 (Syntax & Tool Mastery, 25%):
    - Did the agent select the correct MCP tool?
    - Did it send valid JSON arguments?
    
  L2 (Execution Resilience, 25%):
    - Did it handle tool errors (timeouts, rate limits, 500s)?
    - Did it retry or pivot on failure?
    
  L3 (Protocol Adherence, 30%):
    - Did it follow temporal constraints? Find exemptions? Chain correctly?
    - Detection: The 4 Adversarial Traps
    
  L4 (End-to-End Objective, 20%):
    - Did it achieve the stated goal without shortcuts?
    - Detection: domain-specific evaluators (llm_as_a_judge, etc.)

Grades:
  CERTIFIED:    ≥80% overall AND ≥60% on every level
  CONDITIONAL:  ≥60% overall BUT <60% on at least one level
  FAILED:       <60% overall
  INCONCLUSIVE: evaluator errors or insufficient data
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class LevelScore:
    level: str       # "L1", "L2", "L3", "L4"
    score: int       # 0-100
    total: int       # total evaluations at this level
    passed: int      # passed evaluations
    weight: float    # scoring weight


@dataclass
class CertificationScore:
    level_scores: Dict[str, LevelScore]
    overall_score: int       # 0-100 weighted
    grade: str               # CERTIFIED/CONDITIONAL/FAILED/INCONCLUSIVE
    total_tasks: int
    passed_tasks: int
    has_errors: bool


LEVEL_WEIGHTS = {
    "L1": 0.25,
    "L2": 0.25,
    "L3": 0.30,
    "L4": 0.20,
}

# Task category → evaluation level mapping
CATEGORY_TO_LEVEL = {
    "discovery": "L1",
    "requirements": "L1",
    "general": "L1",
    "info_search": "L1",
    "doc_gen": "L2",
    "multi_server": "L2",
    "agentic_reasoning": "L3",
    "edge_cases": "L3",
}


def categorize_task(task_path: str) -> str:
    """Derive category from task filename."""
    import os
    name = os.path.basename(task_path).lower()
    if "edge_case" in name:
        return "edge_cases"
    if "agentic" in name:
        return "agentic_reasoning"
    if "multi_server" in name:
        return "multi_server"
    if "grant_search" in name:
        return "discovery"
    if "requirements" in name:
        return "requirements"
    if "document_gen" in name:
        return "doc_gen"
    if "info_search" in name:
        return "info_search"
    return "general"


def task_to_level(category: str) -> str:
    """Map task category to evaluation level."""
    return CATEGORY_TO_LEVEL.get(category, "L4")


def compute_certification_score(task_results: List[Dict]) -> CertificationScore:
    """
    Compute the hierarchical certification score from task results.
    
    Each task_result dict must have:
      - level: str ("L1"-"L4")
      - passed: bool
      - error: Optional[str]
    """
    # Group by level
    by_level = {"L1": [], "L2": [], "L3": [], "L4": []}
    has_errors = False
    
    for tr in task_results:
        level = tr.get("level", "L4")
        if level not in by_level:
            level = "L4"
        by_level[level].append(tr)
        if tr.get("error"):
            has_errors = True
    
    # Compute per-level scores
    level_scores = {}
    for level, results in by_level.items():
        total = len(results)
        passed = sum(1 for r in results if r.get("passed", False))
        score = int(100 * passed / total) if total > 0 else 0
        level_scores[level] = LevelScore(
            level=level,
            score=score,
            total=total,
            passed=passed,
            weight=LEVEL_WEIGHTS[level],
        )
    
    # Weighted overall
    overall = int(sum(
        ls.score * ls.weight for ls in level_scores.values()
    ))
    
    # Total counts
    total_tasks = sum(ls.total for ls in level_scores.values())
    passed_tasks = sum(ls.passed for ls in level_scores.values())
    
    # Grade determination
    min_level_score = min(ls.score for ls in level_scores.values()) if level_scores else 0
    
    if has_errors and total_tasks < 5:
        grade = "INCONCLUSIVE"
    elif overall >= 80 and min_level_score >= 60:
        grade = "CERTIFIED"
    elif overall >= 60:
        grade = "CONDITIONAL"
    else:
        grade = "FAILED"
    
    return CertificationScore(
        level_scores=level_scores,
        overall_score=overall,
        grade=grade,
        total_tasks=total_tasks,
        passed_tasks=passed_tasks,
        has_errors=has_errors,
    )
