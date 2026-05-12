"""
Benchmark Runner Service
─────────────────────────
15-task identity security benchmark.
Evaluates auth, RBAC, and compliance scenarios deterministically.
Outputs pass rates by category + risk summary.
"""
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List

from services.identity.models import BenchmarkResult, BenchmarkRun, IdentityAgentResponse
from services.identity.agent import IdentityAgentService


def _now() -> datetime:
    return datetime.now(timezone.utc)


class BenchmarkRunnerService:
    """
    Runs the 15-task identity benchmark suite.
    Uses deterministic agent path (no LLM) for reproducibility.
    """

    BENCHMARK_TASKS = [
        # ── Auth Tasks ──────────────────────────────────────────────────────────
        {
            "id": "simple_auth_0001", "category": "auth", "complexity": "simple",
            "scenario": {"vertical": "mfa_auth", "user_id": "user_001",
                         "credentials_valid": True, "mfa_provided": True, "failed_attempts": 0},
            "request": "Valid user with MFA. Grant access.",
            "expected_status": "granted"
        },
        {
            "id": "simple_auth_0002", "category": "auth", "complexity": "simple",
            "scenario": {"vertical": "mfa_auth", "user_id": "user_002",
                         "credentials_valid": False, "mfa_provided": False, "failed_attempts": 0},
            "request": "Invalid credentials, no MFA.",
            "expected_status": "denied"
        },
        {
            "id": "account_lockout_0003", "category": "auth", "complexity": "moderate",
            "scenario": {"vertical": "mfa_auth", "user_id": "user_003",
                         "credentials_valid": False, "mfa_provided": False, "failed_attempts": 5},
            "request": "User has 5 failed attempts.",
            "expected_status": "locked"
        },
        {
            "id": "impossible_travel_0004", "category": "auth", "complexity": "complex",
            "scenario": {"vertical": "mfa_auth", "user_id": "user_004",
                         "credentials_valid": True, "mfa_provided": False, "failed_attempts": 0,
                         "last_login_location": "New York", "current_location": "Tokyo"},
            "request": "User logged in from NYC 10 minutes ago, now attempting from Tokyo.",
            "expected_status": "mfa_required"
        },
        {
            "id": "mfa_timeout_0005", "category": "auth", "complexity": "complex",
            "scenario": {"vertical": "mfa_auth", "user_id": "user_005",
                         "credentials_valid": True, "mfa_provided": False, "failed_attempts": 0},
            "request": "Valid credentials but MFA not provided.",
            "expected_status": "mfa_required"
        },
        # ── RBAC Tasks ──────────────────────────────────────────────────────────
        {
            "id": "simple_rbac_0006", "category": "rbac", "complexity": "simple",
            "scenario": {"vertical": "rbac_check", "user_id": "user_006",
                         "roles": ["executive"], "resource": "financial_records", "action": "read"},
            "request": "Executive accessing financial records.",
            "expected_access": True
        },
        {
            "id": "rbac_denied_0007", "category": "rbac", "complexity": "simple",
            "scenario": {"vertical": "rbac_check", "user_id": "user_007",
                         "roles": ["employee"], "resource": "financial_records", "action": "read"},
            "request": "Employee trying to access financial records.",
            "expected_access": False
        },
        {
            "id": "role_inheritance_0008", "category": "rbac", "complexity": "moderate",
            "scenario": {"vertical": "rbac_check", "user_id": "user_008",
                         "roles": ["manager"], "resource": "hr_data", "action": "read"},
            "request": "Manager accessing HR data via inherited permissions.",
            "expected_access": True
        },
        {
            "id": "over_permissioned_0009", "category": "rbac", "complexity": "complex",
            "scenario": {"vertical": "rbac_check", "user_id": "user_009",
                         "roles": ["executive", "manager", "supervisor", "employee"],
                         "resource": "financial_records", "action": "admin"},
            "request": "User with all roles — check for over-permissioned violation.",
            "expected_access": True
        },
        {
            "id": "time_based_0010", "category": "rbac", "complexity": "complex",
            "scenario": {"vertical": "rbac_check", "user_id": "user_010",
                         "roles": ["supervisor"], "resource": "audit_logs", "action": "read",
                         "time_of_request": _now().replace(hour=2).isoformat()},
            "request": "Supervisor accessing audit logs at 2AM.",
            "expected_access": False
        },
        # ── Compliance Tasks ─────────────────────────────────────────────────────
        {
            "id": "simple_audit_0011", "category": "compliance", "complexity": "simple",
            "scenario": {"vertical": "compliance_audit", "user_id": "user_011",
                         "events": [{"event_id": "e001", "event_type": "login",
                                     "timestamp": _now().isoformat(), "location": "NYC",
                                     "actor_auth_verified": True, "data_classification": "internal",
                                     "consent_verified": True}]},
            "request": "Audit standard login event for compliance.",
            "expected_compliance": "compliant"
        },
        {
            "id": "anomaly_travel_0012", "category": "compliance", "complexity": "complex",
            "scenario": {"vertical": "compliance_audit", "user_id": "user_012",
                         "events": [
                             {"event_id": "e001", "event_type": "login", "timestamp": _now().isoformat(),
                              "location": "NYC", "actor_auth_verified": True, "data_classification": "internal", "consent_verified": True},
                             {"event_id": "e002", "event_type": "data_access",
                              "timestamp": (_now() + timedelta(minutes=2)).isoformat(),
                              "location": "London", "actor_auth_verified": True, "data_classification": "pii", "consent_verified": True}
                         ]},
            "request": "Audit events: NYC then London 2 minutes apart.",
            "expected_compliance": "review_required"
        },
        {
            "id": "gdpr_violation_0013", "category": "compliance", "complexity": "complex",
            "scenario": {"vertical": "compliance_audit", "user_id": "user_013",
                         "events": [{"event_id": "e001", "event_type": "pii_access",
                                     "timestamp": _now().isoformat(), "location": "NYC",
                                     "actor_auth_verified": True, "data_classification": "pii",
                                     "consent_verified": False}]},
            "request": "PII accessed without consent verification.",
            "expected_compliance": "non_compliant"
        },
        {
            "id": "tampering_0014", "category": "compliance", "complexity": "hard",
            "scenario": {"vertical": "compliance_audit", "user_id": "user_014",
                         "check_tampering": True,
                         "events": [
                             {"event_id": "e001", "event_type": "login", "timestamp": _now().isoformat(),
                              "location": "NYC", "actor_auth_verified": True, "data_classification": "internal", "consent_verified": True},
                             {"event_id": "e001", "event_type": "data_delete", "timestamp": _now().isoformat(),
                              "location": "NYC", "actor_auth_verified": True, "data_classification": "internal", "consent_verified": True}
                         ]},
            "request": "Check for duplicate event IDs (potential tampering).",
            "expected_compliance": "review_required"
        },
        {
            "id": "off_hours_0015", "category": "compliance", "complexity": "complex",
            "scenario": {"vertical": "compliance_audit", "user_id": "user_015",
                         "events": [{"event_id": "e001", "event_type": "privileged_access",
                                     "timestamp": _now().replace(hour=3).isoformat(),
                                     "location": "NYC", "actor_auth_verified": True,
                                     "data_classification": "sensitive", "consent_verified": True}]},
            "request": "Privileged access at 3AM — detect and flag.",
            "expected_compliance": "review_required"
        },
    ]

    def __init__(self):
        self.agent = IdentityAgentService()

    async def run_benchmark(self, task_ids: Optional[List[str]] = None) -> BenchmarkRun:
        """Run all (or selected) benchmark tasks. Returns scored run report."""
        tasks = self.BENCHMARK_TASKS
        if task_ids:
            tasks = [t for t in tasks if t["id"] in task_ids]

        run_id = f"run_{uuid.uuid4().hex[:8]}"
        results: List[BenchmarkResult] = []

        for task in tasks:
            t0 = datetime.now()
            scenario = task["scenario"]
            vertical = scenario.get("vertical", "mfa_auth")
            try:
                resp = await self.agent._process_without_llm(
                    user_request=task["request"],
                    vertical=vertical,
                    scenario_context=scenario
                )
                latency = int((datetime.now() - t0).total_seconds() * 1000)
                passed, reason = self._score(task, resp)
                results.append(BenchmarkResult(
                    task_id=task["id"], category=task["category"],
                    passed=passed, score=1.0 if passed else 0.0,
                    reason=reason, latency_ms=latency, response=resp.model_dump()
                ))
            except Exception as e:
                results.append(BenchmarkResult(
                    task_id=task["id"], category=task["category"],
                    passed=False, score=0.0, reason=f"Exception: {e}",
                    latency_ms=0, response={}
                ))

        total = len(results)
        passed_count = sum(1 for r in results if r.passed)

        by_cat: dict = {}
        for r in results:
            s = by_cat.setdefault(r.category, {"total": 0, "passed": 0, "pass_rate": 0.0})
            s["total"] += 1
            if r.passed:
                s["passed"] += 1
        for cat in by_cat:
            s = by_cat[cat]
            s["pass_rate"] = round(s["passed"] / s["total"] * 100, 1)

        pass_rate = round(passed_count / total * 100, 1) if total else 0.0
        risk_summary = (
            "🔴 CRITICAL: Multiple compliance failures detected. Immediate remediation required."
            if pass_rate < 40 else
            "🟡 WARNING: Some tests failing. Review anomalies and RBAC policies."
            if pass_rate < 70 else
            "🟢 HEALTHY: Identity posture strong. Minor issues flagged for review."
        )

        return BenchmarkRun(
            run_id=run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            total_tasks=total, passed=passed_count,
            failed=total - passed_count,
            pass_rate=pass_rate, by_category=by_cat,
            results=results, risk_summary=risk_summary
        )

    def _score(self, task: dict, resp: IdentityAgentResponse) -> tuple:
        """Score a single benchmark task response against expected outcome."""
        cat = task["category"]

        if cat == "auth":
            expected, actual = task.get("expected_status"), resp.auth_status
            if actual == expected:
                return True, f"Correct auth status: {actual}"
            return False, f"Expected '{expected}', got '{actual}'"

        elif cat == "rbac":
            expected, actual = task.get("expected_access"), resp.access_granted
            if actual == expected:
                return True, f"Correct access decision: {'GRANTED' if actual else 'DENIED'}"
            return False, f"Expected access={expected}, got {actual}"

        else:  # compliance
            expected, actual = task.get("expected_compliance"), resp.compliance_status
            if actual == expected:
                return True, f"Correct compliance status: {actual}"
            if expected == "non_compliant" and actual == "review_required":
                return False, "Partially correct: review_required but expected non_compliant"
            return False, f"Expected '{expected}', got '{actual}'"
