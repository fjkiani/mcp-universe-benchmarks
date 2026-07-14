"""
Identity-as-a-Service Domain Evaluators
ZERO external dependencies - pure JSON logic validation

KEY LEARNINGS FROM INVESTMENTS DOMAIN:
1. Evaluator signature MUST match framework expectations
2. Use *args, **kwargs to catch all parameters
3. Parse JSON with EXTREME leniency (agents love markdown)
4. Return clear, actionable failure messages
5. UNWRAP Pydantic FunctionResult objects before parsing
"""
import json
from typing import Tuple, Any
try:
    from lbx_cli.mcpuniverse.evaluator.functions import compare_func
except ImportError:
    from scripts.eval_compat import compare_func


def unwrap_pydantic_and_parse_json(agent_response: Any) -> Tuple[bool, Any, str]:
    """
    Unwraps Pydantic FunctionResult and parses JSON with extreme leniency.
    
    Returns: (success: bool, data: dict, error_message: str)
    """
    try:
        # Step 1: Unwrap Pydantic FunctionResult if needed
        if hasattr(agent_response, 'model_dump'):
            agent_response = agent_response.model_dump()
        elif hasattr(agent_response, 'dict'):
            agent_response = agent_response.dict()
        elif hasattr(agent_response, '__dict__'):
            agent_response = dict(agent_response.__dict__)
        
        # Step 2: Extract nested 'result' key if present (can be nested multiple times)
        while isinstance(agent_response, dict) and 'result' in agent_response and len(agent_response) == 1:
            agent_response = agent_response['result']
        
        # Step 3: Parse JSON string if needed
        if isinstance(agent_response, str):
            cleaned = agent_response.strip()
            
            # Strip markdown code fences
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1]) if len(lines) > 2 else cleaned
            
            cleaned = cleaned.strip()
            data = json.loads(cleaned)
        elif isinstance(agent_response, dict):
            # Already a dict, use directly
            data = agent_response
        else:
            # Last resort: try to convert to dict
            return False, None, f"Could not convert to dict. Type: {type(agent_response).__name__}, Value: {str(agent_response)[:200]}"
        
        # Final sanity check
        if not isinstance(data, dict):
            return False, None, f"Final data is not a dict! Type: {type(data).__name__}, Value: {str(data)[:200]}"
        
        return True, data, ""
        
    except json.JSONDecodeError as e:
        return False, None, f"JSON parse failed: {str(e)}. Response: {str(agent_response)[:200]}"
    except Exception as e:
        return False, None, f"Unexpected error unwrapping response: {str(e)}. Type: {type(agent_response).__name__}"


@compare_func(name="identity.validate_auth_response")
async def validate_auth_response(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validates authentication flow responses (tasks 0001-0005).
    
    Tests: JSON validity, required fields, type checking, logical consistency.
    
    Framework calls with: (r.result, value, op_args, context=context)
    We accept: (agent_response, *args, **kwargs) to handle all cases.
    """
    # 1. UNWRAP AND PARSE (handles Pydantic FunctionResult + JSON parsing)
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    # 2. REQUIRED FIELDS CHECK
    required = ["user_id", "auth_status", "mfa_required", "session_token", "session_expiry", "error_reason"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}. Found: {list(data.keys())}"
    
    # 3. TYPE VALIDATION
    if not isinstance(data["user_id"], str):
        return False, f"user_id must be string, got: {type(data['user_id']).__name__}"
    
    if data["auth_status"] not in ["success", "failed"]:
        return False, f"auth_status must be 'success' or 'failed', got: '{data['auth_status']}'"
    
    if not isinstance(data["mfa_required"], bool):
        return False, f"mfa_required must be boolean, got: {type(data['mfa_required']).__name__}"
    
    # 4. LOGICAL CONSISTENCY (domain-specific business rules)
    if data["auth_status"] == "success":
        if data["session_token"] is None or data["session_token"] == "":
            return False, "Successful auth MUST provide non-empty session_token"
        if data["session_expiry"] is None or data["session_expiry"] == "":
            return False, "Successful auth MUST provide session_expiry timestamp"
        if data["error_reason"] is not None and data["error_reason"] != "":
            return False, "Successful auth should NOT have error_reason"
    
    if data["auth_status"] == "failed":
        if data["error_reason"] is None or data["error_reason"] == "":
            return False, "Failed auth MUST provide error_reason"
        if data["session_token"] is not None and data["session_token"] != "":
            return False, "Failed auth should NOT have session_token"
    
    return True, f"✓ Valid auth response: user={data['user_id']}, status={data['auth_status']}"


@compare_func(name="identity.validate_rbac_response")
async def validate_rbac_response(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validates RBAC policy evaluation responses (tasks 0006-0010).
    
    Tests: access_granted (bool), applied_roles (list), permission_breakdown (dict).
    """
    # 1. UNWRAP AND PARSE
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    # 2. Required fields
    required = ["access_granted", "applied_roles", "permission_breakdown"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}. Found: {list(data.keys())}"
    
    # 3. Type checks
    if not isinstance(data["access_granted"], bool):
        return False, f"access_granted must be boolean, got: {type(data['access_granted']).__name__}"
    
    if not isinstance(data["applied_roles"], list):
        return False, f"applied_roles must be array, got: {type(data['applied_roles']).__name__}"
    
    if len(data["applied_roles"]) == 0:
        return False, "applied_roles array cannot be empty (must have at least one role)"
    
    if not isinstance(data["permission_breakdown"], dict):
        return False, f"permission_breakdown must be object, got: {type(data['permission_breakdown']).__name__}"
    
    # 4. Validate permission_breakdown structure
    breakdown = data["permission_breakdown"]
    required_breakdown = ["requested_permission", "role_permissions", "access_decision", "reason"]
    missing_breakdown = [f for f in required_breakdown if f not in breakdown]
    if missing_breakdown:
        return False, f"permission_breakdown missing fields: {', '.join(missing_breakdown)}"
    
    # 5. Logical consistency
    if breakdown["access_decision"] not in ["granted", "denied", "granted_with_warning"]:
        return False, f"access_decision must be 'granted', 'denied', or 'granted_with_warning', got: '{breakdown['access_decision']}'"
    
    # access_granted should align with access_decision
    if data["access_granted"] and breakdown["access_decision"] == "denied":
        return False, "Inconsistent: access_granted=true but access_decision='denied'"
    
    if not data["access_granted"] and breakdown["access_decision"] in ["granted", "granted_with_warning"]:
        return False, f"Inconsistent: access_granted=false but access_decision='{breakdown['access_decision']}'"
    
    return True, f"✓ Valid RBAC response: access={data['access_granted']}, roles={len(data['applied_roles'])}, decision={breakdown['access_decision']}"


@compare_func(name="identity.validate_audit_response")
async def validate_audit_response(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validates audit trail and compliance reports (tasks 0011-0015).
    
    Tests: event_log (array), compliance_status (string), anomaly_detected (bool).
    """
    # 1. UNWRAP AND PARSE
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    # 2. Required fields
    required = ["event_log", "compliance_status", "anomaly_detected"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}. Found: {list(data.keys())}"
    
    # 3. Type checks
    if not isinstance(data["event_log"], list):
        return False, f"event_log must be array, got: {type(data['event_log']).__name__}"
    
    if len(data["event_log"]) == 0:
        return False, "event_log array cannot be empty (must have at least one event)"
    
    if data["compliance_status"] not in ["compliant", "non-compliant", "partial"]:
        return False, f"compliance_status must be 'compliant', 'non-compliant', or 'partial', got: '{data['compliance_status']}'"
    
    if not isinstance(data["anomaly_detected"], bool):
        return False, f"anomaly_detected must be boolean, got: {type(data['anomaly_detected']).__name__}"
    
    # 4. Validate event_log structure (each event should have key fields)
    for idx, event in enumerate(data["event_log"]):
        if not isinstance(event, dict):
            return False, f"event_log[{idx}] must be object, got: {type(event).__name__}"
        
        required_event_fields = ["timestamp", "user_id", "action", "resource", "result"]
        missing_event_fields = [f for f in required_event_fields if f not in event]
        if missing_event_fields:
            return False, f"event_log[{idx}] missing fields: {', '.join(missing_event_fields)}"
    
    # 5. Logical consistency
    # If anomaly detected, should have anomaly_details field
    if data["anomaly_detected"]:
        if "anomaly_details" not in data:
            return False, "anomaly_detected=true requires 'anomaly_details' field explaining the anomaly"
        if not data["anomaly_details"] or data["anomaly_details"].strip() == "":
            return False, "anomaly_details cannot be empty when anomaly_detected=true"
    
    # If non-compliant, should have explanation
    if data["compliance_status"] == "non-compliant":
        # Check if there's some explanation field (anomaly_details or other)
        has_explanation = "anomaly_details" in data or "gdpr_summary" in data or "lifecycle_summary" in data
        if not has_explanation:
            return False, "non-compliant status should include explanation field (anomaly_details, gdpr_summary, etc.)"
    
    return True, f"✓ Valid audit response: {len(data['event_log'])} events, status={data['compliance_status']}, anomaly={data['anomaly_detected']}"


# ============================================================================
# HARD TASK EVALUATORS (Tasks 0016-0025)
# Added to harden domain from 93% → 50-60% pass rate
# ============================================================================

@compare_func(name="identity.validate_concurrent_mfa_race")
async def validate_concurrent_mfa_race(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0016: Concurrent MFA race condition detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["user_id", "winning_device", "rejected_device", "race_condition_detected",
                       "auth_status", "session_token", "session_expiry", "race_logged"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("race_condition_detected"):
        return False, "Must detect race condition (two concurrent MFA requests)"
    
    if data.get("auth_status") != "success":
        return False, f"auth_status must be 'success' for winning device, got: '{data.get('auth_status')}'"
    
    if not data.get("session_token"):
        return False, "Winning device must receive non-null session_token"
    
    return True, f"✓ Race condition detected: {data.get('winning_device')} won, {data.get('rejected_device')} rejected"


@compare_func(name="identity.validate_circular_role_inheritance")
async def validate_circular_role_inheritance(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0017: Circular role inheritance cycle detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["circular_dependency_detected", "circular_path", "access_granted", "error_reason"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("circular_dependency_detected"):
        return False, "Must detect circular dependency in role hierarchy"
    
    if data.get("access_granted"):
        return False, "Must DENY access when circular dependency detected"
    
    circular_path = data.get("circular_path", [])
    if not isinstance(circular_path, list) or len(circular_path) < 3:
        return False, f"circular_path must show the loop (at least 3 roles), got: {circular_path}"
    
    return True, f"✓ Circular dependency detected: {' → '.join(circular_path)}"


@compare_func(name="identity.validate_audit_log_tampering")
async def validate_audit_log_tampering(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0018: Audit log tampering and anomaly detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["tampering_detected", "anomalies", "investigation_recommended", "alert_logged"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("tampering_detected"):
        return False, "Must detect tampering (missing events, retroactive entries, IP changes)"
    
    anomalies = data.get("anomalies", [])
    if not isinstance(anomalies, list) or len(anomalies) < 2:
        return False, f"Must detect at least 2 anomalies (gap + retroactive), got: {len(anomalies)}"
    
    if not data.get("investigation_recommended"):
        return False, "Must recommend investigation when tampering detected"
    
    return True, f"✓ Tampering detected: {len(anomalies)} anomalies found"


@compare_func(name="identity.validate_multi_tenant_leakage")
async def validate_multi_tenant_leakage(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0019: Multi-tenant permission leakage detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["cross_tenant_access_detected", "access_granted", "security_violation_logged"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("cross_tenant_access_detected"):
        return False, "Must detect cross-tenant access attempt"
    
    if data.get("access_granted"):
        return False, "Must DENY cross-tenant access (strict tenant isolation)"
    
    return True, "✓ Cross-tenant access blocked"


@compare_func(name="identity.validate_session_replay_attack")
async def validate_session_replay_attack(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0020: Session replay attack detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["replay_attack_detected", "token_used_after_logout", "auth_status", "attack_logged"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("replay_attack_detected"):
        return False, "Must detect replay attack (token used after logout)"
    
    if not data.get("token_used_after_logout"):
        return False, "Must detect token was used AFTER logout time"
    
    if data.get("auth_status") != "failed":
        return False, f"auth_status must be 'failed' for replay attack, got: '{data.get('auth_status')}'"
    
    return True, "✓ Replay attack detected and blocked"


@compare_func(name="identity.validate_distributed_auth_conflict")
async def validate_distributed_auth_conflict(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0021: Distributed authentication source conflict resolution"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["auth_sources_found", "conflicts_detected", "resolved_roles", "winning_source"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if data.get("auth_sources_found") < 2:
        return False, f"Must detect multiple auth sources, got: {data.get('auth_sources_found')}"
    
    if not data.get("conflicts_detected"):
        return False, "Must detect conflicts between auth sources"
    
    if not data.get("resolved_roles"):
        return False, "Must provide resolved role set after conflict resolution"
    
    return True, f"✓ Conflict resolved: {data.get('winning_source')} chosen"


@compare_func(name="identity.validate_compliance_conflict")
async def validate_compliance_conflict(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0022: GDPR/SOC2/HIPAA compliance conflict resolution"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["applicable_frameworks", "conflicts_detected", "gdpr_satisfied",
                       "soc2_satisfied", "hipaa_satisfied", "anonymization_applied"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    frameworks = data.get("applicable_frameworks", [])
    if len(frameworks) < 2:
        return False, f"Must detect multiple frameworks, got: {frameworks}"
    
    if not data.get("conflicts_detected"):
        return False, "Must detect conflicts between GDPR deletion vs SOC2/HIPAA retention"
    
    # Check if resolution satisfies all frameworks
    all_satisfied = (data.get("gdpr_satisfied") and 
                     data.get("soc2_satisfied") and 
                     data.get("hipaa_satisfied"))
    if not all_satisfied:
        return False, "Resolution must satisfy all three frameworks (via anonymization/pseudonymization)"
    
    return True, "✓ Compliance conflict resolved via anonymization"


@compare_func(name="identity.validate_permission_escalation_chain")
async def validate_permission_escalation_chain(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0023: Permission escalation chain detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["escalation_detected", "escalation_chain", "risk_level", "escalation_logged"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("escalation_detected"):
        return False, "Must detect rapid escalation from intern → admin"
    
    escalation_chain = data.get("escalation_chain", [])
    if not isinstance(escalation_chain, list) or len(escalation_chain) < 4:
        return False, f"Must show full escalation chain (at least 4 steps), got: {len(escalation_chain)}"
    
    risk_level = data.get("risk_level", "").lower()
    if risk_level not in ["high", "critical"]:
        return False, f"Risk level must be 'high' or 'critical' for intern→admin, got: '{risk_level}'"
    
    return True, f"✓ Escalation chain detected: {len(escalation_chain)} steps, risk={risk_level}"


@compare_func(name="identity.validate_brute_force_recovery")
async def validate_brute_force_recovery(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0024: Brute force lockout recovery workflow"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["cooldown_satisfied", "verification_methods_required", "temporary_unlock_token",
                       "password_reset_required", "recovery_approved"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("cooldown_satisfied"):
        return False, "Cooldown period must be satisfied before recovery"
    
    verification_methods = data.get("verification_methods_required", [])
    if not isinstance(verification_methods, list) or len(verification_methods) < 2:
        return False, f"Must require multi-factor verification (at least 2 methods), got: {verification_methods}"
    
    if not data.get("password_reset_required"):
        return False, "Must require password reset after brute force lockout recovery"
    
    return True, "✓ Secure recovery workflow implemented"


@compare_func(name="identity.validate_zero_day_auth_bypass")
async def validate_zero_day_auth_bypass(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0025: Zero-day authentication bypass detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["zero_day_detected", "attack_type", "jwt_signature_valid", "user_exists",
                       "privilege_injection_detected", "auth_status", "ip_blocked"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("zero_day_detected"):
        return False, "Must detect zero-day exploit (JWT alg='none' bypass)"
    
    if data.get("jwt_signature_valid"):
        return False, "JWT with alg='none' is INVALID (no signature validation)"
    
    if data.get("user_exists"):
        return False, "Attacker user must NOT exist in system"
    
    if not data.get("privilege_injection_detected"):
        return False, "Must detect privilege injection attempt (is_admin=true in JWT)"
    
    if data.get("auth_status") != "failed":
        return False, f"auth_status must be 'failed' for zero-day, got: '{data.get('auth_status')}'"
    
    if not data.get("ip_blocked"):
        return False, "Must block malicious IP address"
    
    return True, "✓ Zero-day attack detected and blocked"


@compare_func(name="identity.validate_time_travel_detection")
async def validate_time_travel_detection(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0013: Time travel detection (already exists, keeping for reference)"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"JSON parse error: {error}"
    
    required_fields = ["time_travel_detected", "auth_status", "anomaly_logged"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("time_travel_detected"):
        return False, "Must detect impossible future timestamp"
    
    if data.get("auth_status") != "failed":
        return False, "auth_status must be 'failed' for time travel anomaly"
    
    return True, "✓ Time travel anomaly detected"


# ============================================================================
# ORIGINAL TASK EVALUATORS (Tasks 0004-0015)
# These were missing from initial hardening
# ============================================================================

@compare_func(name="identity.validate_auth_with_storage")
async def validate_auth_with_storage(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0004: Authentication with MCP server storage"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["user_id", "auth_status", "session_token", "session_expiry", 
                "stored_in_task_manager", "logged_to_calendar"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}. Found: {list(data.keys())}"
    
    if data["auth_status"] != "success":
        return False, f"auth_status must be 'success', got: '{data['auth_status']}'"
    
    if not data.get("stored_in_task_manager"):
        return False, "Session must be stored in task-management server"
    
    if not data.get("logged_to_calendar"):
        return False, "Login event must be logged to calendar server"
    
    return True, f"✓ Auth with storage: user={data['user_id']}, stored and logged"


@compare_func(name="identity.validate_rbac_with_logging")
async def validate_rbac_with_logging(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0005: RBAC with audit logging"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["access_granted", "applied_roles", "permission_breakdown", "access_logged"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not isinstance(data["applied_roles"], list) or len(data["applied_roles"]) == 0:
        return False, "applied_roles must be non-empty array"
    
    if not data.get("access_logged"):
        return False, "Access decision must be logged to audit trail"
    
    return True, f"✓ RBAC with logging: access={data['access_granted']}, logged"


@compare_func(name="identity.validate_failed_login_detection")
async def validate_failed_login_detection(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0006: Failed login attempt detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["auth_status", "failed_attempts", "error_reason", "account_at_risk"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if data["auth_status"] != "failed":
        return False, "auth_status must be 'failed'"
    
    if data.get("failed_attempts", 0) < 1:
        return False, "Must track failed_attempts count"
    
    return True, f"✓ Failed login detected: {data.get('failed_attempts')} attempts"


@compare_func(name="identity.validate_mfa_timeout")
async def validate_mfa_timeout(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0007: MFA code timeout"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["mfa_expired", "auth_status", "error_reason"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("mfa_expired"):
        return False, "Must detect MFA timeout"
    
    if data["auth_status"] != "failed":
        return False, "auth_status must be 'failed' when MFA expired"
    
    return True, "✓ MFA timeout detected"


@compare_func(name="identity.validate_role_inheritance")
async def validate_role_inheritance(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0008: Role inheritance resolution"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["access_granted", "inherited_roles", "effective_permissions"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    inherited = data.get("inherited_roles", [])
    if not isinstance(inherited, list) or len(inherited) < 2:
        return False, f"Must show role inheritance chain (at least 2), got: {inherited}"
    
    return True, f"✓ Role inheritance: {len(inherited)} roles in chain"


@compare_func(name="identity.validate_session_expiry")
async def validate_session_expiry(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0009: Session expiry check"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["session_expired", "auth_status", "session_terminated"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("session_expired"):
        return False, "Must detect expired session"
    
    if data["auth_status"] != "failed":
        return False, "auth_status must be 'failed' for expired session"
    
    if not data.get("session_terminated"):
        return False, "Must terminate expired session"
    
    return True, "✓ Session expiry detected and terminated"


@compare_func(name="identity.validate_account_lockout")
async def validate_account_lockout(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0010: Account lockout after failed attempts"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["account_locked", "failed_attempts", "lockout_duration", "auth_status"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("account_locked"):
        return False, "Must lock account after threshold exceeded"
    
    if data.get("failed_attempts", 0) < 3:
        return False, f"Must track failed attempts (at least 3), got: {data.get('failed_attempts')}"
    
    if data["auth_status"] != "failed":
        return False, "auth_status must be 'failed' for locked account"
    
    return True, f"✓ Account locked: {data.get('failed_attempts')} attempts, duration={data.get('lockout_duration')}"


@compare_func(name="identity.validate_time_based_access")
async def validate_time_based_access(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0011: Time-based access control"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["access_granted", "within_time_window", "current_time_checked"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("current_time_checked"):
        return False, "Must check current time using date server"
    
    # Validate time window logic
    within_window = data.get("within_time_window")
    access = data.get("access_granted")
    if within_window and not access:
        return False, "If within time window, access should be granted"
    if not within_window and access:
        return False, "If outside time window, access should be denied"
    
    return True, f"✓ Time-based access: within_window={within_window}, access={access}"


@compare_func(name="identity.validate_concurrent_session")
async def validate_concurrent_session(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0012: Concurrent session limit enforcement"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["concurrent_sessions_detected", "session_limit_exceeded", "oldest_session_terminated"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if data.get("session_limit_exceeded") and not data.get("oldest_session_terminated"):
        return False, "Must terminate oldest session when limit exceeded"
    
    return True, f"✓ Concurrent session handled: limit_exceeded={data.get('session_limit_exceeded')}"


@compare_func(name="identity.validate_conflicting_permissions")
async def validate_conflicting_permissions(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0014: Conflicting permission resolution"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["conflicts_detected", "resolution_strategy", "final_decision"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("conflicts_detected"):
        return False, "Must detect permission conflicts"
    
    if not data.get("resolution_strategy"):
        return False, "Must specify conflict resolution strategy (e.g., 'deny-wins', 'most-restrictive')"
    
    return True, f"✓ Conflict resolved: strategy={data.get('resolution_strategy')}, decision={data.get('final_decision')}"


@compare_func(name="identity.validate_audit_trail_gap")
async def validate_audit_trail_gap(agent_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Task 0015: Audit trail gap detection"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, error
    
    required = ["gap_detected", "gap_duration_minutes", "investigation_triggered"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    
    if not data.get("gap_detected"):
        return False, "Must detect audit trail gap"
    
    gap_duration = data.get("gap_duration_minutes", 0)
    if gap_duration < 30:
        return False, f"Must detect significant gap (at least 30 min), got: {gap_duration}"
    
    if not data.get("investigation_triggered"):
        return False, "Must trigger investigation for audit gap"
    
    return True, f"✓ Audit gap detected: {gap_duration} minutes, investigation triggered"
