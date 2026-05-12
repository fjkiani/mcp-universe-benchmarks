"""
Identity Policy Engine (Zero-API, Deterministic)
──────────────────────────────────────────────────
Pure Python implementations of:
  - evaluate_auth_request()  — MFA, lockout, impossible travel
  - evaluate_rbac_request()  — Role inheritance, time-based controls
  - generate_audit_trail()   — SOC2/GDPR anomaly detection, tamper check
  - suggest_remediation()    — 6 issue types → Okta commands
"""
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List


# ─── Auth Engine ──────────────────────────────────────────────────────────────

def evaluate_auth_request(
    user_id: str,
    credentials_valid: bool,
    mfa_provided: bool,
    failed_attempts: int,
    last_login_location: str = "",
    current_location: str = ""
) -> dict:
    """
    Deterministic auth evaluation.
    Rules:
      - 3+ failed attempts → locked (30-min cooldown)
      - Invalid credentials → denied
      - Location change without MFA → mfa_required (impossible travel)
      - Valid creds + no MFA → mfa_required
      - Valid creds + MFA → granted
    """
    ts = datetime.now(timezone.utc)

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

    # Impossible travel: different locations → require MFA
    impossible_travel = (
        bool(last_login_location and current_location and last_login_location != current_location)
    )
    if impossible_travel:
        mfa_required, risk_score = True, 75
    elif mfa_provided:
        mfa_required, risk_score = False, 5
    else:
        mfa_required, risk_score = True, 30

    if mfa_provided or not mfa_required:
        token = f"tok_{uuid.uuid4().hex[:32]}"
        expiry = (ts + timedelta(hours=1)).isoformat()
        status = "granted"
    else:
        token = expiry = None
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
        "anomaly": impossible_travel
    }


# ─── RBAC Engine ──────────────────────────────────────────────────────────────

# Role inheritance: parent role automatically inherits child permissions
ROLE_HIERARCHY: dict = {
    "executive":  {"manager", "supervisor", "employee"},
    "manager":    {"supervisor", "employee"},
    "supervisor": {"employee"},
    "employee":   set()
}

# Resource → roles that may access it
RESOURCE_PERMISSIONS: dict = {
    "financial_records":  {"executive", "manager"},
    "hr_data":            {"executive", "manager", "hr_specialist"},
    "audit_logs":         {"executive", "manager", "compliance_officer"},
    "user_management":    {"executive", "manager"},
    "read_only_reports":  {"executive", "manager", "supervisor", "employee"},
    "api_keys":           {"executive", "developer"},
    "pii_data":           {"executive", "data_engineer", "compliance_officer"},
}


def evaluate_rbac_request(
    user_id: str,
    roles: List[str],
    resource: str,
    action: str,
    time_of_request: Optional[str] = None
) -> dict:
    """
    RBAC policy engine.
    Rules:
      - Expands roles through ROLE_HIERARCHY (manager inherits supervisor + employee)
      - Denies off-hours access for non-executives (Mon-Fri 09:00-18:00 UTC)
      - Flags over-permissioned users (multiple redundant permissions)
    """
    effective_roles = set(roles)
    for role in roles:
        effective_roles |= ROLE_HIERARCHY.get(role, set())

    allowed_roles = RESOURCE_PERMISSIONS.get(resource, {"executive"})
    access_granted = bool(effective_roles & allowed_roles)

    # Time-based enforcement
    if time_of_request:
        try:
            req_time = datetime.fromisoformat(time_of_request.replace("Z", "+00:00"))
            is_weekend = req_time.weekday() >= 5
            off_hours = req_time.hour < 9 or req_time.hour >= 18
            if (is_weekend or off_hours) and "executive" not in effective_roles:
                access_granted = False
        except Exception:
            pass

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


# ─── Compliance / Audit Engine ────────────────────────────────────────────────

def generate_audit_trail(
    user_id: str,
    events: List[dict],
    check_tampering: bool = False
) -> dict:
    """
    Compliance audit trail with anomaly detection.
    Detects: impossible travel, off-hours access, duplicate event IDs (tampering),
             GDPR consent violations, unverified authentication.
    """
    ts = datetime.now(timezone.utc)
    anomalies = []

    for i, event in enumerate(events):
        if i > 0:
            prev = events[i - 1]
            if (event.get("location") and prev.get("location")
                    and event["location"] != prev["location"]):
                anomalies.append({
                    "type": "impossible_travel",
                    "event_index": i,
                    "detail": f"Location change: {prev['location']} → {event['location']}"
                })

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

    # Tamper detection: non-sequential or duplicate event IDs
    if check_tampering and events:
        ids = [e.get("event_id", "") for e in events]
        tamper_gaps = [ids[i] for i in range(1, len(ids)) if ids[i] <= ids[i - 1]]
        if tamper_gaps:
            anomalies.append({
                "type": "audit_tampering",
                "detail": f"Non-sequential event IDs detected: {tamper_gaps}",
                "severity": "CRITICAL"
            })

    gdpr_ok = all(
        e.get("data_classification") != "pii" or e.get("consent_verified")
        for e in events
    )
    soc2_ok = all(e.get("actor_auth_verified", True) for e in events)

    if not gdpr_ok or not soc2_ok:
        compliance_status = "non_compliant"
    elif anomalies:
        compliance_status = "review_required"
    else:
        compliance_status = "compliant"

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
        "risk_level": (
            "LOW" if risk_score < 30 else
            "MEDIUM" if risk_score < 60 else
            "HIGH" if risk_score < 80 else "CRITICAL"
        )
    }


# ─── Remediation Engine ───────────────────────────────────────────────────────

REMEDIATION_CATALOG: dict = {
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
        "commands": [
            "okta.revokeUserSessions(userId)",
            "okta.requireMFA(userId, 'step-up')"
        ],
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
        "commands": [
            "okta.updateAccessPolicy(userId, timeRestriction=BusinessHours)"
        ],
        "estimated_fix_time": "< 2 minutes",
        "risk": "LOW",
        "auto_apply": True
    },
    "failed_login_pattern": {
        "action": "enable_adaptive_mfa",
        "description": "Enable risk-based adaptive MFA for this user's IP range.",
        "commands": [
            "okta.enableAdaptiveMFA(userId)",
            "okta.setIPZonePolicy(ipRange)"
        ],
        "estimated_fix_time": "< 1 minute",
        "risk": "LOW",
        "auto_apply": True
    }
}


def suggest_remediation(issue_type: str, context: dict) -> dict:
    """
    Autonomous remediation lookup.
    Returns: action, commands, whether auto-apply is safe, estimated fix time.
    """
    remedy = REMEDIATION_CATALOG.get(issue_type, {
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
