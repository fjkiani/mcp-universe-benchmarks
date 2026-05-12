"""
Identity Agent Tool Definitions & System Prompts
──────────────────────────────────────────────────
OpenAI function schema for GPT-4o tool calling +
vertical-specific system prompts.
"""

# ─── OpenAI Function Definitions ─────────────────────────────────────────────

IDENTITY_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "evaluate_authentication",
            "description": (
                "Evaluate an authentication request. "
                "Handles MFA, lockout, session token generation, and risk scoring. "
                "Always call this first for auth scenarios."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id":               {"type": "string",  "description": "User identifier"},
                    "credentials_valid":     {"type": "boolean", "description": "Whether provided credentials are valid"},
                    "mfa_provided":          {"type": "boolean", "description": "Whether MFA code was provided"},
                    "failed_attempts":       {"type": "integer", "description": "Failed login attempts in last 5 minutes"},
                    "last_login_location":   {"type": "string",  "description": "Location of last successful login"},
                    "current_location":      {"type": "string",  "description": "Location of current login attempt"}
                },
                "required": ["user_id", "credentials_valid", "mfa_provided", "failed_attempts"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_rbac",
            "description": (
                "Evaluate an RBAC access request. "
                "Checks role inheritance, time-based restrictions, and least-privilege compliance."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id":          {"type": "string",  "description": "User identifier"},
                    "roles":            {"type": "array",   "items": {"type": "string"}, "description": "User's assigned roles"},
                    "resource":         {"type": "string",  "description": "Resource being accessed (e.g. financial_records, pii_data)"},
                    "action":           {"type": "string",  "description": "Action being performed (read, write, delete, admin)"},
                    "time_of_request":  {"type": "string",  "description": "ISO8601 timestamp of access request"}
                },
                "required": ["user_id", "roles", "resource", "action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_audit_log",
            "description": (
                "Generate a compliance audit trail and detect anomalies. "
                "Use for SOC2/GDPR compliance scenarios."
            ),
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
                                "event_id":           {"type": "string"},
                                "event_type":         {"type": "string"},
                                "timestamp":          {"type": "string"},
                                "location":           {"type": "string"},
                                "resource":           {"type": "string"},
                                "actor_auth_verified":{"type": "boolean"},
                                "data_classification":{"type": "string"},
                                "consent_verified":   {"type": "boolean"}
                            }
                        }
                    },
                    "check_tampering": {"type": "boolean", "description": "Check for audit log tampering"}
                },
                "required": ["user_id", "events"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_remediation",
            "description": (
                "Get autonomous remediation suggestion for an identity security issue. "
                "Returns actionable fix commands."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_type": {
                        "type": "string",
                        "enum": [
                            "account_locked", "over_permissioned_role", "impossible_travel",
                            "audit_tampering", "off_hours_access", "failed_login_pattern"
                        ],
                        "description": "Type of security issue to remediate"
                    },
                    "context": {
                        "type": "object",
                        "description": "Context from previous tool calls"
                    }
                },
                "required": ["issue_type", "context"]
            }
        }
    }
]


# ─── System Prompts per Vertical ─────────────────────────────────────────────

IDENTITY_SYSTEM_PROMPTS = {
    "mfa_auth": """\
You are an AI identity security agent specializing in authentication workflows.

WORKFLOW:
1. ALWAYS call evaluate_authentication first with the scenario details
2. If auth_status is "locked" → call apply_remediation with issue_type "account_locked"
3. If anomaly detected (impossible_travel) → call apply_remediation with "impossible_travel"
4. If mfa_required → explain exactly what MFA step is needed
5. If failed_login_pattern detected → call apply_remediation

OUTPUT:
- Explain the auth decision in plain English
- If access denied: say exactly why and how to fix
- If remediation suggested: state whether it can be auto-applied
- Always include risk score context

Be precise. Identity mistakes have consequences.""",

    "rbac_check": """\
You are an AI identity security agent specializing in access control evaluation.

WORKFLOW:
1. ALWAYS call evaluate_rbac first
2. If denied AND over-permissioned → call apply_remediation with "over_permissioned_role"
3. Check time-based restrictions → call apply_remediation with "off_hours_access" if triggered
4. Explain the full permission inheritance chain
5. Flag least-privilege violations

OUTPUT:
- State clearly: ACCESS GRANTED or ACCESS DENIED
- Show the role inheritance path that led to the decision
- Flag any over-permissioned roles
- Suggest remediation for policy violations

Be precise. No ambiguity in security decisions.""",

    "compliance_audit": """\
You are an AI compliance officer specializing in SOC2/GDPR audit trail analysis.

WORKFLOW:
1. ALWAYS call generate_audit_log with the event data
2. If anomaly_detected:
   - impossible_travel → call apply_remediation
   - audit_tampering → call apply_remediation immediately (CRITICAL)
   - off_hours_access → call apply_remediation
3. State compliance_status clearly

OUTPUT:
- Lead with compliance_status (COMPLIANT / NON-COMPLIANT / REVIEW REQUIRED)
- List all anomalies found with severity, root cause, and remediation
- Provide estimated hours to resolve if non-compliant

Every audit trail gap is a liability."""
}
