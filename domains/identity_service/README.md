# Identity-as-a-Service (IDaaS) Domain

**Status:** Phase 1 - Scaffolding Complete  
**Next:** Phase 2 - Task Authoring

## Overview
Tests AI agents on identity management workflows: authentication, RBAC, and audit compliance.

**Focus:** Evaluator testing + MCP server integration with zero external dependencies.

## Key Features
- ✅ **Zero external APIs** - No API keys required
- ✅ **3 MCP servers** - `task-management`, `calendar`, `date` (all built-in)
- ✅ **Real tool integration** - Agent learns to call MCP servers
- ✅ **Deterministic evaluation** - No external dependencies
- ✅ **15 tasks** across 3 categories
- ✅ **3 battle-tested evaluator functions**

## Why These MCP Servers?
This domain uses zero-API servers to:
1. **Test real MCP integration** - Agent makes actual tool calls
2. **Zero setup required** - No API keys, no external accounts
3. **Instant local testing** - Servers work out-of-the-box
4. **Deterministic results** - No external API failures
5. **Complete template** - Shows evaluator + tooling patterns

## Task Categories

### 1. Identity Verification (tasks 0001-0005)
- Multi-factor authentication flows
- Password reset validation
- Account lockout detection
- Session token generation
- Credential verification

**MCP Servers:** `task-management` (store auth attempts), `calendar` (log events), `date` (calculate expiry)  
**Evaluator:** `identity.validate_auth_response`  
**Tests:** JSON structure, required fields (user_id, auth_status, mfa_required, session_token, session_expiry, error_reason), logical consistency

### 2. Access Control (tasks 0006-0010)
- RBAC policy evaluation
- Permission inheritance checks
- Resource access validation
- Role assignment logic
- Least-privilege principle

**MCP Servers:** `task-management` (store policies), `calendar` (track permission changes)  
**Evaluator:** `identity.validate_rbac_response`  
**Tests:** access_granted (bool), applied_roles (array), permission_breakdown (object)

### 3. Audit & Compliance (tasks 0011-0015)
- Access audit trail generation
- Suspicious login pattern detection
- GDPR/SOC2 compliance reports
- Session anomaly detection
- Identity lifecycle events

**MCP Servers:** `calendar` (audit log), `date` (timestamp validation), `task-management` (event tracking)  
**Evaluator:** `identity.validate_audit_response`  
**Tests:** event_log (array), compliance_status (enum), anomaly_detected (bool)

## Running Locally

### Step 1: Structure validation (30 seconds)
```bash
alignerr validate --domain identity_service --no-callbacks
```
**Expected:** "Validation Status: Passed"

### Step 2: Evaluator discovery (1 minute)
```bash
export OPENAI_API_KEY=sk-...
alignerr validate --domain identity_service --model openai/gpt-4o-mini --no-callbacks
```
**Expected:** "Total Evaluators: 3" (or 15 if counted per-task)

### Step 3: Full test (3 minutes)
```bash
alignerr validate --domain identity_service --model openai/gpt-4o-mini
```
**Expected:** 40-60% pass rate, detailed pass/fail reasons

## Success Metrics

### **Benchmark Quality Standards (CI/CD Evaluation)**
- **Pass@1 Rate:** 30-70% (NOT 80%! Benchmarks must discriminate)
- **Zero Perfect Tasks:** No task at 100% pass (too easy = delete)
- **<10% Broken Tasks:** <2 tasks at 0% pass (broken = fix or delete)
- **Complexity Distribution:** Mix of Moderate/Complex (no all-Simple domain)
- **Avg Complexity Score:** 35-50/100 (Moderate difficulty)

### **Evaluator Quality Metrics**
- **Evaluator Coverage:** 100% (all tasks have evaluators)
- **False Negative Rate:** <5% (evaluator incorrectly fails good response)
- **False Positive Rate:** <3% (evaluator incorrectly passes bad response)
- **Evaluator Accuracy:** >90% (overall correct judgments)

### **Infrastructure Metrics**
- **MCP Server Usage:** 3 servers (task-management, calendar, date)
- **Unique MCP Servers:** 3 (verified in CI/CD report)
- **External Dependencies:** 0 API keys required
- **Agent Response Rate:** >90% (not "None")

## Troubleshooting

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| "Total Evaluators: 0" | Decorator/signature issue | Check `@compare_func(name=...)` and `async def` |
| "Agent Response: None" | Task prompt unclear | Simplify question, add output format examples |
| JSON parse errors | Agent wraps in markdown | Evaluator should strip code fences (already included) |
| Low pass rate | Agent confusion or evaluator too strict | Iterate on ONE task at a time |

## Lessons from Investments Domain
This domain incorporates learnings from 10+ failed CI/CD runs on the Investments domain:
1. **Correct evaluator signature:** `async def func(agent_response: Any, *args, **kwargs)`
2. **Extreme JSON leniency:** Strip markdown fences, handle whitespace
3. **Clear error messages:** Show what was expected vs. received
4. **No external APIs:** Avoid dependency hell (Alpha Vantage nightmare)

## Development Status
- [x] Phase 0: Proposal
- [x] Phase 1: Scaffolding
- [ ] Phase 2: Task Authoring
- [ ] Phase 3: Evaluator Implementation
- [ ] Phase 4: Local Testing
- [ ] Phase 5: Documentation
- [ ] Phase 6: CI/CD Submission

