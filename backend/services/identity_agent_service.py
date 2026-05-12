"""
Identity Agent Service — The Core Engine 🔐

Processes identity management workflows using GPT-4o function calling.
Three verticals:
  - mfa_auth:       MFA verification, session management, lockout detection
  - rbac_check:     Role-based access evaluation, permission inheritance
  - compliance_audit: SOC2/GDPR audit trail, anomaly detection, remediation

Each vertical maps to real-world scenarios from the 25-task benchmark.
The benchmark_runner sub-system scores agent performance and surfaces failures.
"""
import os
import json
import uuid
import random
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Literal, Any, Optional, List, Dict
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ─── Response Models ──────────────────────────────────────────────────────────

class ActionTrace(BaseModel):
    tool: str
    args: dict
    result: dict
    success: bool
    latency_ms: Optional[int] = None


class IdentityAgentResponse(BaseModel):
    message: str
    vertical: str
    actions: List[ActionTrace] = []
    # Auth specific
    auth_status: Optional[str] = None          # granted | denied | mfa_required | locked
    session_token: Optional[str] = None
    session_expiry: Optional[str] = None
    mfa_required: bool = False
    # RBAC specific
    access_granted: Optional[bool] = None
    applied_roles: List[str] = []
    permission_breakdown: Optional[dict] = None
    # Audit specific
    anomaly_detected: Optional[bool] = None
    compliance_status: Optional[str] = None    # compliant | non_compliant | review_required
    event_log: List[dict] = []
    # Remediation
    remediation_suggested: Optional[str] = None
    remediation_applied: bool = False
    # Risk scoring
    risk_score: Optional[int] = None           # 0-100
    risk_level: Optional[str] = None           # LOW | MEDIUM | HIGH | CRITICAL
    error: Optional[str] = None


class BenchmarkResult(BaseModel):
    task_id: str
    category: str
    passed: bool
    score: float                 # 0.0 - 1.0
    reason: str
    latency_ms: int
    response: dict


class BenchmarkRun(BaseModel):
    run_id: str
    timestamp: str
    total_tasks: int
    passed: int
    failed: int
    pass_rate: float
    by_category: Dict[str, dict]
    results: List[BenchmarkResult]
    risk_summary: str


# ─── Identity Logic Engine (Zero-API, Deterministic) ─────────────────────────

def evaluate_auth_request(
    user_id: str,
    credentials_valid: bool,
    mfa_provided: bool,
    failed_attempts: int,
    last_login_location: str = "",
    current_location: str = ""
) -> dict:
    """Deterministic auth evaluation — core identity logic."""
    ts = datetime.now(timezone.utc)

    # Lockout rule: 3+ failed attempts within 5 mins → locked
    if failed_attempts >= 3:
        return {
            "user_id": user_id,
            "auth_status": "locked",
            "mfa_required": False,
            "session_token": None,
            "session_expiry": None,
            "error_reason": f"Account locked after {failed_attempts} failed attempts. Reset required.",
            "risk_score": 85,
            "risk_level": "HIGH",
            "lockout_until": (ts + timedelta(minutes=30)).isoformat()
        }

    if not credentials_valid:
        return {
            "user_id": user_id,
            "auth_status": "denied",
            "mfa_required": False,
            "session_token": None,
            "session_expiry": None,
            "error_reason": "Invalid credentials",
            "risk_score": 60,
            "risk_level": "MEDIUM"
        }

    # Impossible travel detection
    if last_login_location and current_location and last_login_location != current_location:
        mfa_required = True
        risk_score = 75
    elif mfa_provided:
        mfa_required = False
        risk_score = 5
    else:
        mfa_required = True
        risk_score = 30

    if mfa_provided or not mfa_required:
        token = f"tok_{uuid.uuid4().hex[:32]}"
        expiry = (ts + timedelta(hours=1)).isoformat()
        status = "granted"
    else:
        token = None
        expiry = None
        status = "mfa_required"

    return {
        "user_id": user_id,
        "auth_status": status,
        "mfa_required": mfa_required,
        "session_token": token,
        "session_expiry": expiry,
        "error_reason": None if status == "granted" else "MFA required",
        "risk_score": risk_score,
        "risk_level": "LOW" if risk_score < 30 else ("MEDIUM" if risk_score < 60 else "HIGH"),
        "anomaly": bool(last_login_location and current_location and last_login_location != current_location)
    }


def evaluate_rbac_request(
    user_id: str,
    roles: List[str],
    resource: str,
    action: str,
    time_of_request: Optional[str] = None
) -> dict:
    """RBAC policy engine with role inheritance and time-based controls."""

    # Inheritance hierarchy: executive > manager > supervisor > employee
    ROLE_HIERARCHY = {
        "executive": {"manager", "supervisor", "employee"},
        "manager": {"supervisor", "employee"},
        "supervisor": {"employee"},
        "employee": set()
    }

    # Resource permission matrix
    PERMISSIONS = {
        "financial_records": {"executive", "manager"},
        "hr_data": {"executive", "manager", "hr_specialist"},
        "audit_logs": {"executive", "manager", "compliance_officer"},
        "user_management": {"executive", "manager"},
        "read_only_reports": {"executive", "manager", "supervisor", "employee"},
        "api_keys": {"executive", "developer"},
        "pii_data": {"executive", "data_engineer", "compliance_officer"},
    }

    # Expand roles via inheritance
    effective_roles = set(roles)
    for role in roles:
        effective_roles |= ROLE_HIERARCHY.get(role, set())

    allowed_roles = PERMISSIONS.get(resource, {"executive"})
    access_granted = bool(effective_roles & allowed_roles)

    # Time-based enforcement (business hours: Mon-Fri 9am-6pm UTC)
    if time_of_request:
        try:
            req_time = datetime.fromisoformat(time_of_request.replace("Z", "+00:00"))
            is_weekend = req_time.weekday() >= 5
            off_hours = req_time.hour < 9 or req_time.hour >= 18
            if (is_weekend or off_hours) and "executive" not in effective_roles:
                access_granted = False
        except Exception:
            pass

    # Least-privilege flag: over-permissioned roles
    over_permissioned = len(effective_roles & allowed_roles) > 1 and len(roles) > 2

    return {
        "user_id": user_id,
        "access_granted": access_granted,
        "applied_roles": list(effective_roles),
        "permission_breakdown": {
            "requested_resource": resource,
            "requested_action": action,
            "allowed_roles_for_resource": list(allowed_roles),
            "user_effective_roles": list(effective_roles),
            "matched_roles": list(effective_roles & allowed_roles),
            "decision_reason": (
                "Access granted via role inheritance." if access_granted
                else "No matching role for this resource/action combination."
            ),
            "over_permissioned_flag": over_permissioned
        },
        "risk_score": 20 if access_granted else 40,
        "risk_level": "LOW" if access_granted else "MEDIUM"
    }


def generate_audit_trail(
    user_id: str,
    events: List[dict],
    check_tampering: bool = False
) -> dict:
    """Generate compliance audit trail with anomaly detection."""
    ts = datetime.now(timezone.utc)

    # Detect anomalies: rapid successive events, unusual hours, impossible geo
    anomalies = []
    for i, event in enumerate(events):
        if i > 0:
            prev = events[i - 1]
            # Same user, different country within 1 minute
            if (event.get("location", "") != prev.get("location", "")
                    and event.get("location") and prev.get("location")):
                anomalies.append({
                    "type": "impossible_travel",
                    "event_index": i,
                    "detail": f"Location change: {prev['location']} → {event['location']}"
                })

        # Off-hours access to sensitive resources
        event_time = event.get("timestamp", "")
        if event_time:
            try:
                dt = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
                if dt.hour < 6 or dt.hour > 22:
                    anomalies.append({
                        "type": "off_hours_access",
                        "event_index": i,
                        "detail": f"Access at {dt.strftime('%H:%M UTC')} on {dt.strftime('%A')}"
                    })
            except Exception:
                pass

    # Tamper detection: check sequential event IDs (simplified)
    if check_tampering and events:
        ids = [e.get("event_id", "") for e in events]
        tamper_gaps = [ids[i] for i in range(1, len(ids)) if ids[i] <= ids[i-1]]
        if tamper_gaps:
            anomalies.append({
                "type": "audit_tampering",
                "detail": f"Non-sequential event IDs detected: {tamper_gaps}",
                "severity": "CRITICAL"
            })

    # Compliance status
    gdpr_ok = all(e.get("data_classification") != "pii" or e.get("consent_verified") for e in events)
    soc2_ok = all(e.get("actor_auth_verified", True) for e in events)

    compliance_status = "compliant"
    if not gdpr_ok or not soc2_ok:
        compliance_status = "non_compliant"
    elif anomalies:
        compliance_status = "review_required"

    risk_score = min(100, len(anomalies) * 25)

    return {
        "user_id": user_id,
        "event_log": events,
        "anomaly_detected": bool(anomalies),
        "anomalies": anomalies,
        "compliance_status": compliance_status,
        "gdpr_compliant": gdpr_ok,
        "soc2_compliant": soc2_ok,
        "audit_generated_at": ts.isoformat(),
        "risk_score": risk_score,
        "risk_level": "LOW" if risk_score < 30 else ("MEDIUM" if risk_score < 60 else ("HIGH" if risk_score < 80 else "CRITICAL"))
    }


def suggest_remediation(
    issue_type: str,
    context: dict
) -> dict:
    """Autonomous remediation suggestion engine."""
    REMEDIATIONS = {
        "account_locked": {
            "action": "unlock_account_with_forced_mfa",
            "description": "Unlock account and force MFA re-enrollment on next login.",
            "commands": ["okta.resetFactor(userId)", "okta.unlockUser(userId)"],
            "estimated_fix_time": "< 30 seconds",
            "risk": "LOW",
            "auto_apply": True
        },
        "over_permissioned_role": {
            "action": "prune_excess_roles",
            "description": "Remove roles above least-privilege baseline.",
            "commands": ["okta.removeGroupMembership(userId, excessRole)"],
            "estimated_fix_time": "< 1 minute",
            "risk": "MEDIUM",
            "auto_apply": False
        },
        "impossible_travel": {
            "action": "force_session_termination_and_mfa",
            "description": "Kill all active sessions and require step-up MFA.",
            "commands": ["okta.revokeUserSessions(userId)", "okta.requireMFA(userId, 'step-up')"],
            "estimated_fix_time": "< 10 seconds",
            "risk": "LOW",
            "auto_apply": True
        },
        "audit_tampering": {
            "action": "isolate_and_alert",
            "description": "Isolate affected account, alert SOC team, preserve evidence.",
            "commands": ["okta.suspendUser(userId)", "siem.alert(severity='CRITICAL')"],
            "estimated_fix_time": "Immediate — requires SOC review",
            "risk": "HIGH",
            "auto_apply": False
        },
        "off_hours_access": {
            "action": "enforce_time_based_policy",
            "description": "Apply time-based access restriction policy to user's roles.",
            "commands": ["okta.updateAccessPolicy(userId, timeRestriction=BusinessHours)"],
            "estimated_fix_time": "< 2 minutes",
            "risk": "LOW",
            "auto_apply": True
        },
        "failed_login_pattern": {
            "action": "enable_adaptive_mfa",
            "description": "Enable risk-based adaptive MFA for this user's IP range.",
            "commands": ["okta.enableAdaptiveMFA(userId)", "okta.setIPZonePolicy(ipRange)"],
            "estimated_fix_time": "< 1 minute",
            "risk": "LOW",
            "auto_apply": True
        }
    }

    remedy = REMEDIATIONS.get(issue_type, {
        "action": "manual_review_required",
        "description": "This scenario requires manual security team review.",
        "commands": [],
        "estimated_fix_time": "Unknown",
        "risk": "HIGH",
        "auto_apply": False
    })

    return {
        "issue_type": issue_type,
        "context": context,
        "remediation": remedy,
        "suggested_at": datetime.now(timezone.utc).isoformat()
    }


# ─── OpenAI Tool Definitions ──────────────────────────────────────────────────

IDENTITY_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "evaluate_authentication",
            "description": "Evaluate an authentication request. Handles MFA, lockout, session token generation, and risk scoring. Always call this first for auth scenarios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "credentials_valid": {"type": "boolean", "description": "Whether provided credentials are valid"},
                    "mfa_provided": {"type": "boolean", "description": "Whether MFA code was provided"},
                    "failed_attempts": {"type": "integer", "description": "Number of failed login attempts in last 5 minutes"},
                    "last_login_location": {"type": "string", "description": "Location of last successful login (city/country)"},
                    "current_location": {"type": "string", "description": "Location of current login attempt"}
                },
                "required": ["user_id", "credentials_valid", "mfa_provided", "failed_attempts"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_rbac",
            "description": "Evaluate RBAC access request. Checks role inheritance, time-based restrictions, and least-privilege compliance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "roles": {"type": "array", "items": {"type": "string"}, "description": "User's assigned roles"},
                    "resource": {"type": "string", "description": "Resource being accessed (e.g. financial_records, pii_data)"},
                    "action": {"type": "string", "description": "Action being performed (read, write, delete, admin)"},
                    "time_of_request": {"type": "string", "description": "ISO8601 timestamp of access request"}
                },
                "required": ["user_id", "roles", "resource", "action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_audit_log",
            "description": "Generate a compliance audit trail and detect anomalies. Use for SOC2/GDPR compliance scenarios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User whose events to audit"},
                    "events": {
                        "type": "array",
                        "description": "List of identity events to audit",
                        "items": {
                            "type": "object",
                            "properties": {
                                "event_id": {"type": "string"},
                                "event_type": {"type": "string"},
                                "timestamp": {"type": "string"},
                                "location": {"type": "string"},
                                "resource": {"type": "string"},
                                "actor_auth_verified": {"type": "boolean"},
                                "data_classification": {"type": "string"},
                                "consent_verified": {"type": "boolean"}
                            }
                        }
                    },
                    "check_tampering": {"type": "boolean", "description": "Whether to check for audit log tampering"}
                },
                "required": ["user_id", "events"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_remediation",
            "description": "Get autonomous remediation suggestion for an identity security issue. Returns actionable fix commands.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_type": {
                        "type": "string",
                        "enum": ["account_locked", "over_permissioned_role", "impossible_travel", "audit_tampering", "off_hours_access", "failed_login_pattern"],
                        "description": "Type of security issue to remediate"
                    },
                    "context": {"type": "object", "description": "Context from previous tool calls (user_id, roles, anomalies, etc.)"}
                },
                "required": ["issue_type", "context"]
            }
        }
    }
]


# ─── System Prompts per Vertical ──────────────────────────────────────────────

IDENTITY_SYSTEM_PROMPTS = {
    "mfa_auth": """You are an AI identity security agent specializing in authentication workflows.

Your job: Evaluate authentication requests against enterprise security policies.

WORKFLOW:
1. ALWAYS call evaluate_authentication first with the scenario details
2. If auth_status is "locked" → call apply_remediation with issue_type "account_locked"
3. If anomaly detected (impossible_travel) → call apply_remediation with issue_type "impossible_travel"  
4. If mfa_required → explain exactly what MFA step is needed
5. If failed_login_pattern detected → call apply_remediation

OUTPUT:
- Explain the auth decision in plain English
- If access denied: say exactly why and how to fix
- If remediation suggested: state whether it can be auto-applied
- Always include risk score context

Be precise. Identity mistakes have consequences.""",

    "rbac_check": """You are an AI identity security agent specializing in access control evaluation.

Your job: Evaluate RBAC requests and surface over-permissioned roles.

WORKFLOW:
1. ALWAYS call evaluate_rbac first
2. If access_denied AND over-permissioned flag is True → call apply_remediation with "over_permissioned_role"
3. Check time-based restrictions (off-hours access) → call apply_remediation with "off_hours_access" if triggered
4. Explain the full permission inheritance chain
5. Flag least-privilege violations

OUTPUT:
- State clearly: ACCESS GRANTED or ACCESS DENIED
- Show the role inheritance path that led to the decision
- Flag any over-permissioned roles
- Suggest remediation for policy violations

Be precise. No ambiguity in security decisions.""",

    "compliance_audit": """You are an AI compliance officer specializing in SOC2/GDPR audit trail analysis.

Your job: Analyze identity events for anomalies and compliance violations.

WORKFLOW:
1. ALWAYS call generate_audit_log with the event data
2. If anomaly_detected:
   - For impossible_travel: call apply_remediation
   - For audit_tampering: call apply_remediation immediately (CRITICAL)
   - For off_hours_access: call apply_remediation
3. State compliance_status clearly
4. Generate a risk assessment

OUTPUT:
- Lead with compliance_status (COMPLIANT / NON-COMPLIANT / REVIEW REQUIRED)  
- List all anomalies found
- For each anomaly: severity, root cause, and remediation
- Provide estimated hours to resolve if non-compliant

Every audit trail gap is a liability."""
}


# ─── Main Identity Agent ──────────────────────────────────────────────────────

class IdentityAgentService:
    """
    Core identity security agent.
    GPT-4o function calling → deterministic identity logic → structured response.
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    async def process(
        self,
        user_request: str,
        vertical: Literal["mfa_auth", "rbac_check", "compliance_audit"],
        scenario_context: Optional[dict] = None
    ) -> IdentityAgentResponse:
        """Main entry: natural language request → agent actions → structured response."""

        if not self.client:
            return await self._process_without_llm(user_request, vertical, scenario_context)

        system_prompt = IDENTITY_SYSTEM_PROMPTS.get(vertical, IDENTITY_SYSTEM_PROMPTS["mfa_auth"])
        context_str = json.dumps(scenario_context, indent=2) if scenario_context else "No additional context provided."

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Identity Security Request:\n{user_request}\n\n"
                    f"Context:\n{context_str}"
                )
            }
        ]

        actions = []
        auth_result = None
        rbac_result = None
        audit_result = None
        remediation_result = None

        # Agentic loop
        for _iteration in range(6):
            t0 = datetime.now()
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=IDENTITY_TOOLS,
                tool_choice="auto",
                temperature=0.1
            )
            llm_latency = int((datetime.now() - t0).total_seconds() * 1000)

            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                break

            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                t1 = datetime.now()
                result, success = self._dispatch_tool(name, args)
                tool_latency = int((datetime.now() - t1).total_seconds() * 1000)

                # Track key results
                if name == "evaluate_authentication":
                    auth_result = result
                elif name == "evaluate_rbac":
                    rbac_result = result
                elif name == "generate_audit_log":
                    audit_result = result
                elif name == "apply_remediation":
                    remediation_result = result

                actions.append(ActionTrace(
                    tool=name, args=args, result=result,
                    success=success, latency_ms=tool_latency
                ))
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result)
                })

        final_message = msg.content or "Identity evaluation complete."

        return self._build_response(
            final_message, vertical, actions,
            auth_result, rbac_result, audit_result, remediation_result
        )

    def _dispatch_tool(self, name: str, args: dict) -> tuple:
        """Route tool name → identity logic function."""
        try:
            if name == "evaluate_authentication":
                result = evaluate_auth_request(
                    user_id=args.get("user_id", "user_001"),
                    credentials_valid=args.get("credentials_valid", False),
                    mfa_provided=args.get("mfa_provided", False),
                    failed_attempts=args.get("failed_attempts", 0),
                    last_login_location=args.get("last_login_location", ""),
                    current_location=args.get("current_location", "")
                )
            elif name == "evaluate_rbac":
                result = evaluate_rbac_request(
                    user_id=args.get("user_id", "user_001"),
                    roles=args.get("roles", ["employee"]),
                    resource=args.get("resource", "read_only_reports"),
                    action=args.get("action", "read"),
                    time_of_request=args.get("time_of_request")
                )
            elif name == "generate_audit_log":
                result = generate_audit_trail(
                    user_id=args.get("user_id", "user_001"),
                    events=args.get("events", []),
                    check_tampering=args.get("check_tampering", False)
                )
            elif name == "apply_remediation":
                result = suggest_remediation(
                    issue_type=args.get("issue_type", "manual_review_required"),
                    context=args.get("context", {})
                )
            else:
                result = {"error": f"Unknown identity tool: {name}"}
            return result, True
        except Exception as e:
            return {"error": str(e), "tool": name}, False

    def _build_response(
        self,
        message: str,
        vertical: str,
        actions: List[ActionTrace],
        auth_result, rbac_result, audit_result, remediation_result
    ) -> IdentityAgentResponse:
        """Assemble the final structured response from all tool results."""
        resp = IdentityAgentResponse(
            message=message,
            vertical=vertical,
            actions=actions
        )

        if auth_result:
            resp.auth_status = auth_result.get("auth_status")
            resp.session_token = auth_result.get("session_token")
            resp.session_expiry = auth_result.get("session_expiry")
            resp.mfa_required = auth_result.get("mfa_required", False)
            resp.risk_score = auth_result.get("risk_score")
            resp.risk_level = auth_result.get("risk_level")

        if rbac_result:
            resp.access_granted = rbac_result.get("access_granted")
            resp.applied_roles = rbac_result.get("applied_roles", [])
            resp.permission_breakdown = rbac_result.get("permission_breakdown")
            resp.risk_score = rbac_result.get("risk_score")
            resp.risk_level = rbac_result.get("risk_level")

        if audit_result:
            resp.anomaly_detected = audit_result.get("anomaly_detected")
            resp.compliance_status = audit_result.get("compliance_status")
            resp.event_log = audit_result.get("event_log", [])
            resp.risk_score = audit_result.get("risk_score")
            resp.risk_level = audit_result.get("risk_level")

        if remediation_result:
            remedy = remediation_result.get("remediation", {})
            resp.remediation_suggested = remedy.get("action")
            resp.remediation_applied = remedy.get("auto_apply", False)

        return resp

    async def _process_without_llm(
        self,
        user_request: str,
        vertical: str,
        scenario_context: Optional[dict] = None
    ) -> IdentityAgentResponse:
        """Fallback: direct logic without LLM. Still produces realistic outputs."""
        ctx = scenario_context or {}
        actions = []

        if vertical == "mfa_auth":
            auth = evaluate_auth_request(
                user_id=ctx.get("user_id", "user_demo"),
                credentials_valid=ctx.get("credentials_valid", True),
                mfa_provided=ctx.get("mfa_provided", False),
                failed_attempts=ctx.get("failed_attempts", 0),
                last_login_location=ctx.get("last_login_location", ""),
                current_location=ctx.get("current_location", "")
            )
            actions.append(ActionTrace(tool="evaluate_authentication", args=ctx, result=auth, success=True))

            if auth.get("auth_status") == "locked":
                remedy = suggest_remediation("account_locked", auth)
                actions.append(ActionTrace(tool="apply_remediation", args={"issue_type": "account_locked", "context": auth}, result=remedy, success=True))

            return self._build_response(
                f"Authentication evaluated: {auth.get('auth_status', 'unknown').upper()}. Risk: {auth.get('risk_level', 'UNKNOWN')}.",
                vertical, actions, auth, None, None,
                remedy if auth.get("auth_status") == "locked" else None
            )

        elif vertical == "rbac_check":
            rbac = evaluate_rbac_request(
                user_id=ctx.get("user_id", "user_demo"),
                roles=ctx.get("roles", ["employee"]),
                resource=ctx.get("resource", "read_only_reports"),
                action=ctx.get("action", "read")
            )
            actions.append(ActionTrace(tool="evaluate_rbac", args=ctx, result=rbac, success=True))
            return self._build_response(
                f"Access {'GRANTED' if rbac['access_granted'] else 'DENIED'} for {ctx.get('resource', 'resource')}.",
                vertical, actions, None, rbac, None, None
            )

        else:  # compliance_audit
            events = ctx.get("events", [
                {"event_id": "evt_001", "event_type": "login", "timestamp": datetime.now(timezone.utc).isoformat(),
                 "location": "NYC", "actor_auth_verified": True, "data_classification": "internal"}
            ])
            audit = generate_audit_trail(ctx.get("user_id", "user_demo"), events, ctx.get("check_tampering", False))
            actions.append(ActionTrace(tool="generate_audit_log", args=ctx, result=audit, success=True))
            return self._build_response(
                f"Audit complete. Status: {audit['compliance_status'].upper()}. Anomalies: {len(audit.get('anomalies', []))}.",
                vertical, actions, None, None, audit, None
            )


# ─── Benchmark Runner ─────────────────────────────────────────────────────────

class BenchmarkRunnerService:
    """
    Runs the 25-task identity benchmark autonomously.
    Computes pass rates by category and surfaces failures for remediation.
    """

    BENCHMARK_TASKS = [
        # Simple auth
        {"id": "simple_auth_0001", "category": "auth", "complexity": "simple",
         "scenario": {"vertical": "mfa_auth", "user_id": "user_001", "credentials_valid": True, "mfa_provided": True, "failed_attempts": 0},
         "request": "Valid user with MFA. Grant access.",
         "expected_status": "granted"},
        {"id": "simple_auth_0002", "category": "auth", "complexity": "simple",
         "scenario": {"vertical": "mfa_auth", "user_id": "user_002", "credentials_valid": False, "mfa_provided": False, "failed_attempts": 0},
         "request": "Invalid credentials, no MFA.",
         "expected_status": "denied"},
        {"id": "account_lockout_0003", "category": "auth", "complexity": "moderate",
         "scenario": {"vertical": "mfa_auth", "user_id": "user_003", "credentials_valid": False, "mfa_provided": False, "failed_attempts": 5},
         "request": "User has 5 failed attempts.",
         "expected_status": "locked"},
        {"id": "impossible_travel_0004", "category": "auth", "complexity": "complex",
         "scenario": {"vertical": "mfa_auth", "user_id": "user_004", "credentials_valid": True, "mfa_provided": False, "failed_attempts": 0,
                      "last_login_location": "New York", "current_location": "Tokyo"},
         "request": "User logged in from NYC 10 minutes ago, now attempting from Tokyo.",
         "expected_status": "mfa_required"},
        {"id": "mfa_timeout_0005", "category": "auth", "complexity": "complex",
         "scenario": {"vertical": "mfa_auth", "user_id": "user_005", "credentials_valid": True, "mfa_provided": False, "failed_attempts": 0},
         "request": "Valid credentials but MFA not provided.",
         "expected_status": "mfa_required"},
        # RBAC tasks
        {"id": "simple_rbac_0006", "category": "rbac", "complexity": "simple",
         "scenario": {"vertical": "rbac_check", "user_id": "user_006", "roles": ["executive"], "resource": "financial_records", "action": "read"},
         "request": "Executive accessing financial records.",
         "expected_access": True},
        {"id": "rbac_denied_0007", "category": "rbac", "complexity": "simple",
         "scenario": {"vertical": "rbac_check", "user_id": "user_007", "roles": ["employee"], "resource": "financial_records", "action": "read"},
         "request": "Employee trying to access financial records.",
         "expected_access": False},
        {"id": "role_inheritance_0008", "category": "rbac", "complexity": "moderate",
         "scenario": {"vertical": "rbac_check", "user_id": "user_008", "roles": ["manager"], "resource": "hr_data", "action": "read"},
         "request": "Manager accessing HR data via inherited permissions.",
         "expected_access": True},
        {"id": "over_permissioned_0009", "category": "rbac", "complexity": "complex",
         "scenario": {"vertical": "rbac_check", "user_id": "user_009", "roles": ["executive", "manager", "supervisor", "employee"], "resource": "financial_records", "action": "admin"},
         "request": "User with all roles — check for over-permissioned violation.",
         "expected_access": True},
        {"id": "time_based_0010", "category": "rbac", "complexity": "complex",
         "scenario": {"vertical": "rbac_check", "user_id": "user_010", "roles": ["supervisor"], "resource": "audit_logs",
                      "action": "read",
                      "time_of_request": (datetime.now(timezone.utc).replace(hour=2)).isoformat()},
         "request": "Supervisor accessing audit logs at 2AM.",
         "expected_access": False},
        # Compliance tasks
        {"id": "simple_audit_0011", "category": "compliance", "complexity": "simple",
         "scenario": {"vertical": "compliance_audit", "user_id": "user_011",
                      "events": [{"event_id": "e001", "event_type": "login", "timestamp": datetime.now(timezone.utc).isoformat(),
                                  "location": "NYC", "actor_auth_verified": True, "data_classification": "internal", "consent_verified": True}]},
         "request": "Audit standard login event for compliance.",
         "expected_compliance": "compliant"},
        {"id": "anomaly_travel_0012", "category": "compliance", "complexity": "complex",
         "scenario": {"vertical": "compliance_audit", "user_id": "user_012",
                      "events": [
                          {"event_id": "e001", "event_type": "login", "timestamp": datetime.now(timezone.utc).isoformat(), "location": "NYC", "actor_auth_verified": True, "data_classification": "internal", "consent_verified": True},
                          {"event_id": "e002", "event_type": "data_access", "timestamp": (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat(), "location": "London", "actor_auth_verified": True, "data_classification": "pii", "consent_verified": True}
                      ]},
         "request": "Audit events showing NYC then London 2 minutes apart.",
         "expected_compliance": "review_required"},
        {"id": "gdpr_violation_0013", "category": "compliance", "complexity": "complex",
         "scenario": {"vertical": "compliance_audit", "user_id": "user_013",
                      "events": [{"event_id": "e001", "event_type": "pii_access", "timestamp": datetime.now(timezone.utc).isoformat(),
                                  "location": "NYC", "actor_auth_verified": True, "data_classification": "pii", "consent_verified": False}]},
         "request": "PII accessed without consent verification.",
         "expected_compliance": "non_compliant"},
        {"id": "tampering_0014", "category": "compliance", "complexity": "hard",
         "scenario": {"vertical": "compliance_audit", "user_id": "user_014",
                      "check_tampering": True,
                      "events": [
                          {"event_id": "e001", "event_type": "login", "timestamp": datetime.now(timezone.utc).isoformat(), "location": "NYC", "actor_auth_verified": True, "data_classification": "internal", "consent_verified": True},
                          {"event_id": "e001", "event_type": "data_delete", "timestamp": datetime.now(timezone.utc).isoformat(), "location": "NYC", "actor_auth_verified": True, "data_classification": "internal", "consent_verified": True}
                      ]},
         "request": "Check for duplicate event IDs (potential tampering).",
         "expected_compliance": "review_required"},
        {"id": "off_hours_0015", "category": "compliance", "complexity": "complex",
         "scenario": {"vertical": "compliance_audit", "user_id": "user_015",
                      "events": [{"event_id": "e001", "event_type": "privileged_access",
                                  "timestamp": datetime.now(timezone.utc).replace(hour=3).isoformat(),
                                  "location": "NYC", "actor_auth_verified": True, "data_classification": "sensitive", "consent_verified": True}]},
         "request": "Privileged access at 3AM detect and flag.",
         "expected_compliance": "review_required"},
    ]

    def __init__(self):
        self.agent = IdentityAgentService()

    async def run_benchmark(self, task_ids: Optional[List[str]] = None) -> BenchmarkRun:
        """Run all (or selected) benchmark tasks and return scored results."""
        tasks = self.BENCHMARK_TASKS
        if task_ids:
            tasks = [t for t in tasks if t["id"] in task_ids]

        run_id = f"run_{uuid.uuid4().hex[:8]}"
        results = []

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

                # Score the response
                passed, reason = self._score(task, resp)
                results.append(BenchmarkResult(
                    task_id=task["id"],
                    category=task["category"],
                    passed=passed,
                    score=1.0 if passed else 0.0,
                    reason=reason,
                    latency_ms=latency,
                    response=resp.model_dump()
                ))
            except Exception as e:
                results.append(BenchmarkResult(
                    task_id=task["id"],
                    category=task["category"],
                    passed=False,
                    score=0.0,
                    reason=f"Exception: {str(e)}",
                    latency_ms=0,
                    response={}
                ))

        # Compute summary
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        by_cat = {}
        for r in results:
            cat = r.category
            if cat not in by_cat:
                by_cat[cat] = {"total": 0, "passed": 0, "pass_rate": 0.0}
            by_cat[cat]["total"] += 1
            if r.passed:
                by_cat[cat]["passed"] += 1
        for cat in by_cat:
            by_cat[cat]["pass_rate"] = round(by_cat[cat]["passed"] / by_cat[cat]["total"] * 100, 1)

        pass_rate = round(passed / total * 100, 1) if total > 0 else 0.0
        risk_summary = (
            "🔴 CRITICAL: Multiple compliance failures detected. Immediate remediation required."
            if pass_rate < 40
            else "🟡 WARNING: Some tests failing. Review anomalies and RBAC policies."
            if pass_rate < 70
            else "🟢 HEALTHY: Identity posture strong. Minor issues flagged for review."
        )

        return BenchmarkRun(
            run_id=run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            total_tasks=total,
            passed=passed,
            failed=total - passed,
            pass_rate=pass_rate,
            by_category=by_cat,
            results=results,
            risk_summary=risk_summary
        )

    def _score(self, task: dict, resp: IdentityAgentResponse) -> tuple:
        """Score a benchmark response against expected outcomes."""
        cat = task["category"]

        if cat == "auth":
            expected = task.get("expected_status")
            actual = resp.auth_status
            if actual == expected:
                return True, f"Correct auth status: {actual}"
            return False, f"Expected '{expected}', got '{actual}'"

        elif cat == "rbac":
            expected = task.get("expected_access")
            actual = resp.access_granted
            if actual == expected:
                return True, f"Correct access decision: {'GRANTED' if actual else 'DENIED'}"
            return False, f"Expected access={'{'}{expected}{'}'}, got {'{'}{actual}{'}'}"

        else:  # compliance
            expected = task.get("expected_compliance")
            actual = resp.compliance_status
            if actual == expected:
                return True, f"Correct compliance status: {actual}"
            # Partial credit: review_required instead of non_compliant is still a flag
            if expected == "non_compliant" and actual == "review_required":
                return False, f"Partially correct: flagged as review_required but expected non_compliant"
            return False, f"Expected '{expected}', got '{actual}'"


# Global singletons
identity_agent = IdentityAgentService()
benchmark_runner = BenchmarkRunnerService()
