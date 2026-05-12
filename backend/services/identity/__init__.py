"""
Identity Services Package
─────────────────────────
Modular breakdown of the identity engine:

  models    — Pydantic data models (ActionTrace, IdentityAgentResponse, etc.)
  engine    — Deterministic policy logic (auth, RBAC, compliance, remediation)
  tools     — OpenAI function definitions + system prompts per vertical
  agent     — IdentityAgentService (GPT-4o + tool dispatch + fallback)
  benchmark — BenchmarkRunnerService (15-task suite, scoring, risk summary)

Usage (external):
  from services.identity import identity_agent, benchmark_runner
"""
from services.identity.agent import IdentityAgentService
from services.identity.benchmark import BenchmarkRunnerService

# Global singletons — same interface as before
identity_agent = IdentityAgentService()
benchmark_runner = BenchmarkRunnerService()

__all__ = ["identity_agent", "benchmark_runner", "IdentityAgentService", "BenchmarkRunnerService"]
