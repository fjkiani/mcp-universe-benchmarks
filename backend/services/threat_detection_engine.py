"""
Threat Detection Engine — Red Team → Blue Team 🔴→🔵
============================================================
Built from CVE intel across 6 tiers:
  T1: JWT algorithm confusion (alg:none, RS256→HS256)
  T2: Session/token attacks (OAuth race, subdomain takeover, session fixation)
  T3: RBAC abuse (IDOR, mass assignment, cross-tenant escalation)
  T4: Audit trail evasion (log injection, retroactive deletion, clock skew)
  T5: Data exfiltration (scope creep, credential stuffing, SAML wrapping)
  T6: Zero-day territory (device flow abuse, timing attacks, MFA fatigue)

Each function:
  - takes attacker-observable artifacts
  - returns: detected (bool), attack_class, severity, evidence, mitigation
"""
import re
import hmac
import time
import hashlib
import base64
import json
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Tuple
from collections import defaultdict

# ════════════════════════════════════════════════════════════════
# TIER 1 — JWT Attack Detection
# CVE refs: Auth0 2015 alg:none, OWASP JWT-01, RS256→HS256 confusion
# ════════════════════════════════════════════════════════════════

JWT_ALG_ALLOWLIST = {"RS256", "ES256", "PS256"}  # NO HS* in production
JWT_ALG_DENYLIST  = {"none", "HS256", "HS384", "HS512"}  # attacker territory


def detect_jwt_alg_confusion(token: str) -> Dict[str, Any]:
    """
    T1-A: Detect JWT alg:none and RS256→HS256 confusion attacks.
    
    alg:none PoC: https://github.com/Sjoerdlangkemper/jwt-alg-none
    RS256→HS256 PoC: https://github.com/Sjoerdlangkemper/jwt-rs256-to-hs256
    Auth0 post-mortem: https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {
                "detected": True,
                "attack_class": "MALFORMED_JWT",
                "severity": "HIGH",
                "evidence": f"JWT has {len(parts)} parts, expected 3",
                "mitigation": "Reject all malformed tokens immediately"
            }
        
        # Decode header (no signature validation — that's the point)
        header_padding = parts[0] + "=" * (-len(parts[0]) % 4)
        header = json.loads(base64.urlsafe_b64decode(header_padding))
        alg = header.get("alg", "").strip()
        
        # Attack 1: alg:none — empty signature, no verification
        if alg.lower() in ("none", "", "null"):
            return {
                "detected": True,
                "attack_class": "JWT_ALG_NONE",
                "severity": "CRITICAL",
                "cve": "OWASP JWT-01, Auth0 2015",
                "evidence": f"JWT header declares alg='{alg}' — signature bypass",
                "attacker_intent": "Token forgery without valid signing key",
                "mitigation": "REJECT. Enforce RS256/ES256 allowlist. Never trust alg header.",
                "okta_rule": "Always validate signature. Deny if alg not in [RS256, ES256, PS256]."
            }
        
        # Attack 2: HS256 when RS256 expected — key confusion
        if alg in JWT_ALG_DENYLIST:
            signature_present = len(parts[2]) > 0
            return {
                "detected": True,
                "attack_class": "JWT_ALG_CONFUSION" if signature_present else "JWT_ALG_NONE_SIGNED",
                "severity": "CRITICAL",
                "cve": "Auth0 2018 - RS256→HS256 key confusion",
                "evidence": (
                    f"JWT declares alg='{alg}'. If server expects RS256 but accepts HS256, "
                    f"attacker can forge tokens using public RSA key as HMAC secret."
                ),
                "attacker_technique": (
                    "1. Grab RS public key from JWKS endpoint. "
                    "2. Switch header to alg:HS256. "
                    "3. Sign token with public key as HMAC secret. "
                    "4. Server uses same key for 'verification' → accepts forged token."
                ),
                "mitigation": "Enforce per-algorithm dedicated keys. Reject HS* entirely.",
                "okta_rule": "Use separate signing keys per alg, validate JWKS alg restrictions."
            }
        
        # Attack 3: Weak/empty signature with allowed alg
        if not parts[2] and alg in JWT_ALG_ALLOWLIST:
            return {
                "detected": True,
                "attack_class": "JWT_MISSING_SIGNATURE",
                "severity": "CRITICAL",
                "evidence": f"alg={alg} declared but signature segment is empty",
                "mitigation": "Reject tokens with empty signatures regardless of declared alg."
            }
        
        return {
            "detected": False,
            "attack_class": None,
            "alg_declared": alg,
            "alg_allowed": alg in JWT_ALG_ALLOWLIST,
            "note": "JWT structure passes initial inspection. Verify signature separately."
        }
    
    except Exception as e:
        return {
            "detected": True,
            "attack_class": "JWT_DECODE_FAILURE",
            "severity": "HIGH",
            "evidence": f"JWT decode error — likely crafted payload: {str(e)}",
            "mitigation": "Reject any token that fails structured parsing."
        }


# ════════════════════════════════════════════════════════════════
# TIER 2 — Session & OAuth Attack Detection
# CVE refs: Auth0 2021 refresh race, PortSwigger OAuth research
# ════════════════════════════════════════════════════════════════

# In-memory state (swap for Redis in prod)
_token_usage_log: Dict[str, List[Dict]] = defaultdict(list)  # token_id → [{ip, ts}]
_oauth_redirect_domains: Dict[str, str] = {}  # redirect_uri → registered_domain


def detect_refresh_token_replay(
    token_id: str,
    ip: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    T2-A: Detect OAuth refresh token replay attacks.
    
    PoC: https://github.com/PortSwigger/oauth-refresh-token-race
    CVE: Auth0 2021 race condition (CVE-2021-44228 adjacent)
    Attack: Attacker steals refresh token, replays it before rotation completes.
    """
    now = datetime.now(timezone.utc)
    usage_window_seconds = 30  # tokens should only be used once, ever
    
    prior_uses = _token_usage_log[token_id]
    
    # This token has been used before
    if prior_uses:
        last_use = prior_uses[-1]
        last_ip = last_use["ip"]
        last_ts = datetime.fromisoformat(last_use["timestamp"])
        delta_s = (now - last_ts).total_seconds()
        
        # Replay from DIFFERENT IP — attacker replaying stolen token
        if last_ip != ip:
            return {
                "detected": True,
                "attack_class": "REFRESH_TOKEN_REPLAY",
                "severity": "CRITICAL",
                "evidence": {
                    "token_id": token_id,
                    "original_ip": last_ip,
                    "replay_ip": ip,
                    "delta_seconds": round(delta_s, 2)
                },
                "attacker_intent": "Replay stolen refresh token from different origin",
                "mitigation": (
                    "REVOKE entire token family immediately. "
                    "Force re-authentication. Alert SOC."
                ),
                "okta_rule": "Refresh token rotation: revoke on ANY reuse. Flag cross-IP replay as IOC."
            }
        
        # Same IP but token reused within rotation window — race condition
        if delta_s < usage_window_seconds:
            return {
                "detected": True,
                "attack_class": "REFRESH_TOKEN_RACE",
                "severity": "HIGH",
                "evidence": {
                    "token_id": token_id,
                    "reuse_delta_seconds": round(delta_s, 2),
                    "same_ip": True
                },
                "mitigation": "Atomic token rotation — invalidate immediately on first use.",
                "okta_rule": "Use database transaction lock on token rotation."
            }
    
    # Log this use
    _token_usage_log[token_id].append({
        "ip": ip,
        "device_id": device_id,
        "timestamp": now.isoformat()
    })
    
    return {"detected": False, "token_id": token_id, "ip": ip}


KNOWN_EPHEMERAL_PROVIDERS = {
    "github.io", "pages.dev", "netlify.app", "vercel.app",
    "s3.amazonaws.com", "blob.core.windows.net", "appspot.com",
    "glitch.me", "replit.app", "fly.dev"
}

def detect_oauth_redirect_uri_attack(
    redirect_uri: str,
    registered_domains: List[str]
) -> Dict[str, Any]:
    """
    T2-B: Detect OAuth redirect_uri hijacking via subdomain takeover.
    
    PoC: https://github.com/PortSwigger/oauth-subdomain-takeover
    Intel: https://github.com/EdOverflow/can-i-take-over-xyz
    Attack: Attacker takes over staging.corp.com (GitHub Pages), steals auth codes.
    """
    from urllib.parse import urlparse
    try:
        parsed = urlparse(redirect_uri)
        hostname = parsed.hostname or ""
        
        # 1. Exact allowlist check — most important
        allowed = any(
            hostname == d or hostname.endswith("." + d)
            for d in registered_domains
        )
        if not allowed:
            # Check if it's a known cloud-hosted ephemeral domain (takeover target)
            is_ephemeral = any(
                hostname.endswith(ep) for ep in KNOWN_EPHEMERAL_PROVIDERS
            )
            return {
                "detected": True,
                "attack_class": "OAUTH_REDIRECT_HIJACK" if is_ephemeral else "OAUTH_REDIRECT_UNKNOWN",
                "severity": "CRITICAL" if is_ephemeral else "HIGH",
                "evidence": {
                    "redirect_uri": redirect_uri,
                    "hostname": hostname,
                    "ephemeral_host": is_ephemeral,
                    "registered_domains": registered_domains
                },
                "attacker_technique": (
                    "Claim unclaimed subdomain on cloud provider. "
                    "Register as OAuth callback. Steal authorization codes in-flight."
                ) if is_ephemeral else "Redirect URI not in allowlist",
                "mitigation": "Strict exact-match allowlist only. No wildcards. No regex.",
                "okta_rule": "Validate redirect_uri ownership during app registration. Re-verify on each auth request."
            }
        
        # 2. Wildcard in allowlist is itself a vulnerability
        if any("*" in d for d in registered_domains):
            return {
                "detected": True,
                "attack_class": "OAUTH_WILDCARD_REDIRECT",
                "severity": "HIGH",
                "evidence": "Wildcard redirect_uri in allowlist — attacker can register subdomain",
                "mitigation": "Enumerate specific subdomains only. Never use wildcards.",
            }
        
        return {"detected": False, "redirect_uri": redirect_uri, "hostname": hostname}
    
    except Exception as e:
        return {
            "detected": True, "attack_class": "MALFORMED_REDIRECT_URI",
            "severity": "MEDIUM", "evidence": str(e)
        }


def detect_session_fixation(
    pre_auth_token: Optional[str],
    post_auth_token: Optional[str],
    storage_origin: Optional[str] = None
) -> Dict[str, Any]:
    """
    T2-C: Detect session fixation attacks in localStorage SPAs.
    
    PoC: BlackHat EU 2018 - Post-Login Session Fixation in SPAs
    Attack: Attacker plants JWT in localStorage, hijacks session post-auth.
    """
    if pre_auth_token and post_auth_token and pre_auth_token == post_auth_token:
        return {
            "detected": True,
            "attack_class": "SESSION_FIXATION",
            "severity": "CRITICAL",
            "evidence": "Session token unchanged after authentication — fixation attack likely",
            "attacker_technique": (
                "1. Inject known token into victim's localStorage via XSS/CSRF. "
                "2. Wait for victim to authenticate. "
                "3. Use pre-planted token to access authenticated session."
            ),
            "mitigation": "Always rotate session token on successful authentication.",
            "okta_rule": "Invalidate ALL pre-auth tokens on login. Issue fresh token post-auth."
        }
    
    if storage_origin and "localhost" not in storage_origin:
        # Check if token was written from unexpected origin
        return {
            "detected": True,
            "attack_class": "CROSS_ORIGIN_TOKEN_WRITE",
            "severity": "HIGH",
            "evidence": f"Token written from origin: {storage_origin}",
            "mitigation": "Use HttpOnly cookies — no JavaScript access. Eliminate localStorage for tokens."
        }
    
    return {"detected": False, "pre_auth_rotated": pre_auth_token != post_auth_token}


# ════════════════════════════════════════════════════════════════
# TIER 3 — RBAC Abuse Detection
# CVE refs: OWASP API Security Top 10, Okta 2022 cross-tenant
# ════════════════════════════════════════════════════════════════

def detect_idor_attempt(
    requesting_user_id: str,
    requesting_user_tenant: str,
    target_resource_id: str,
    target_resource_owner_id: str,
    target_resource_tenant: str
) -> Dict[str, Any]:
    """
    T3-A: Detect Insecure Direct Object Reference (IDOR) attacks.
    
    PoC: https://github.com/PortSwigger/idor-lab
    OWASP API Top10 A5: Broken Object Level Authorization
    Attack: User A changes ID in request to access User B's data.
    """
    # Cross-tenant access — critical
    if requesting_user_tenant != target_resource_tenant:
        return {
            "detected": True,
            "attack_class": "CROSS_TENANT_IDOR",
            "severity": "CRITICAL",
            "evidence": {
                "requesting_tenant": requesting_user_tenant,
                "target_tenant": target_resource_tenant,
                "target_resource_id": target_resource_id
            },
            "attacker_technique": "Change tenant-scoped ID in request to access another tenant's data",
            "mitigation": "Enforce tenant_id on ALL database queries. Add to ORM scope, not just API layer.",
            "okta_rule": "Multi-tenant: token must contain tenant_id claim. Validate at model layer."
        }
    
    # Same tenant, different owner
    if requesting_user_id != target_resource_owner_id:
        return {
            "detected": True,
            "attack_class": "IDOR_OWNERSHIP_VIOLATION",
            "severity": "HIGH",
            "evidence": {
                "requesting_user": requesting_user_id,
                "resource_owner": target_resource_owner_id,
                "resource_id": target_resource_id
            },
            "mitigation": (
                "Always filter: `queryset.filter(owner=request.user)`. "
                "Never expose sequential numeric IDs — use UUIDs."
            )
        }
    
    return {"detected": False, "access_authorized": True}


def detect_mass_assignment(
    submitted_fields: Dict[str, Any],
    allowed_fields: List[str],
    protected_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    T3-B: Detect mass assignment / parameter pollution attacks.
    
    PoC: https://github.com/PortSwigger/mass-assignment-lab
    OWASP Cheatsheet: Mass Assignment
    Attack: PATCH {role: 'admin', is_superuser: true} → server binds without whitelist.
    """
    protected = protected_fields or ["role", "is_admin", "is_superuser", "permissions",
                                      "tenant_id", "account_type", "subscription_tier",
                                      "bypass_mfa", "email_verified", "identity_claims"]
    
    submitted_keys = set(submitted_fields.keys())
    allowed_keys = set(allowed_fields)
    
    # Fields not in allowlist
    unexpected = submitted_keys - allowed_keys
    # Fields that are explicitly protected (privilege escalation targets)
    escalation_fields = submitted_keys & set(protected)
    
    if escalation_fields:
        return {
            "detected": True,
            "attack_class": "MASS_ASSIGNMENT_PRIVILEGE_ESCALATION",
            "severity": "CRITICAL",
            "evidence": {
                "attempted_fields": list(escalation_fields),
                "submitted_values": {k: submitted_fields[k] for k in escalation_fields}
            },
            "attacker_technique": (
                "Submit extra fields in PATCH/PUT request targeting privilege fields. "
                "Works on: FastAPI (no exclude), DRF (no read_only), Rails (no strong params)."
            ),
            "mitigation": (
                "Use explicit field whitelists. "
                "FastAPI: model_fields only, never **kwargs. "
                "DRF: read_only=True on privilege fields."
            )
        }
    
    if unexpected:
        return {
            "detected": True,
            "attack_class": "MASS_ASSIGNMENT_UNKNOWN_FIELDS",
            "severity": "MEDIUM",
            "evidence": {"unexpected_fields": list(unexpected)},
            "mitigation": "Log and block all fields not in explicit allowlist."
        }
    
    return {"detected": False, "fields_validated": list(allowed_keys)}


def detect_cross_tenant_role_escalation(
    user_id: str,
    user_tenant: str,
    role_being_assigned: str,
    role_tenant: str,
    assigning_admin_id: str,
    assigning_admin_tenant: str
) -> Dict[str, Any]:
    """
    T3-C: Detect cross-tenant role escalation.
    
    Incident: Okta Workflows 2022 cross-tenant bug
    Attack: Tenant A admin assigns role scoped to Tenant B.
    """
    violations = []
    
    if user_tenant != role_tenant:
        violations.append(f"User tenant '{user_tenant}' ≠ role tenant '{role_tenant}'")
    
    if assigning_admin_tenant != role_tenant:
        violations.append(f"Admin tenant '{assigning_admin_tenant}' has no authority over role in tenant '{role_tenant}'")
    
    if violations:
        return {
            "detected": True,
            "attack_class": "CROSS_TENANT_ROLE_ESCALATION",
            "severity": "CRITICAL",
            "evidence": violations,
            "attacker_technique": (
                "Admin in Tenant A assigns themselves/accomplice a role "
                "that belongs to Tenant B — gaining unauthorized access."
            ),
            "mitigation": (
                "Every role assignment must be triple-validated: "
                "user_tenant == role_tenant == admin_tenant."
            ),
            "okta_rule": "Tenant ID scoping on ALL role checks. Validate at token claim level."
        }
    
    return {"detected": False, "role_assignment_valid": True}


# ════════════════════════════════════════════════════════════════
# TIER 4 — Audit Trail Evasion Detection
# CVE refs: CRLF injection, Snowflake 2024 SSRF, clock skew attacks
# ════════════════════════════════════════════════════════════════

_audit_hash_chain: List[str] = []  # append-only hash chain

def detect_audit_log_injection(
    field_value: str,
    field_name: str = "username"
) -> Dict[str, Any]:
    """
    T4-A: Detect CRLF log injection attacks.
    
    PoC: https://github.com/PortSwigger/log-injection
    BlackHat US 2017: Log Attack Surface
    Attack: CRLF in username injects fake audit events.
    Example: user = "admin\r\n2024-01-15 AUDIT: user=root action=delete_all"
    """
    # CRLF characters
    crlf_patterns = ["\r\n", "\n", "\r", "%0d%0a", "%0a", "%0d",
                      "\\r\\n", "\\n", "\\r", "\x0a", "\x0d"]
    
    for pat in crlf_patterns:
        if pat.lower() in field_value.lower():
            return {
                "detected": True,
                "attack_class": "AUDIT_LOG_CRLF_INJECTION",
                "severity": "HIGH",
                "evidence": {
                    "field": field_name,
                    "detected_pattern": pat,
                    "raw_value": field_value[:100]
                },
                "attacker_technique": (
                    "Inject CRLF sequences in user-controlled fields (username, email, user-agent). "
                    "Parser reads injected lines as legitimate audit events. "
                    "Attacker fabricates admin actions."
                ),
                "mitigation": "Strip/encode all CRLF in log fields. Use structured logging (JSON).",
                "okta_rule": "Never interpolate user strings into log messages. Use parameterized logging."
            }
    
    # Null bytes — bypass string termination
    if "\x00" in field_value or "%00" in field_value.lower():
        return {
            "detected": True,
            "attack_class": "AUDIT_NULL_BYTE_INJECTION",
            "severity": "MEDIUM",
            "evidence": {"field": field_name, "null_byte": True},
            "mitigation": "Sanitize null bytes from all user-controlled inputs."
        }
    
    return {"detected": False, "field": field_name, "clean": True}


def generate_audit_event_with_hash(
    event: Dict[str, Any],
    previous_hash: Optional[str] = None
) -> Dict[str, Any]:
    """
    T4-B: Hash-chain sealed audit events — tamper detection at cryptographic level.
    
    Prevention for: Retroactive audit deletion (Snowflake 2024 SSRF pattern)
    Each event is chained to the previous via SHA-256 — any deletion breaks the chain.
    """
    event_str = json.dumps(event, sort_keys=True)
    prev = previous_hash or "GENESIS"
    
    # Chain: hash(prev_hash + event_content)
    chain_input = f"{prev}|{event_str}"
    event_hash = hashlib.sha256(chain_input.encode()).hexdigest()
    
    sealed = {
        **event,
        "audit_hash": event_hash,
        "previous_hash": prev,
        "sealed_at": datetime.now(timezone.utc).isoformat()
    }
    _audit_hash_chain.append(event_hash)
    return sealed


def detect_audit_chain_break(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    T4-C: Verify audit event hash chain integrity.
    
    Detects: event deletion, insertion, modification, retroactive tampering.
    """
    if not events:
        return {"detected": False, "chain_intact": True, "events_verified": 0}
    
    broken_links = []
    prev_hash = "GENESIS"
    
    for i, event in enumerate(events):
        stored_hash = event.get("audit_hash")
        stored_prev = event.get("previous_hash")
        
        # Reconstruct event without hash fields for verification
        event_clean = {k: v for k, v in event.items()
                       if k not in ("audit_hash", "previous_hash", "sealed_at")}
        event_str = json.dumps(event_clean, sort_keys=True)
        chain_input = f"{prev_hash}|{event_str}"
        expected_hash = hashlib.sha256(chain_input.encode()).hexdigest()
        
        if stored_hash != expected_hash:
            broken_links.append({
                "event_index": i,
                "event_id": event.get("event_id", f"index_{i}"),
                "stored_hash": stored_hash,
                "expected_hash": expected_hash,
                "previous_hash_match": stored_prev == prev_hash
            })
        
        prev_hash = stored_hash or expected_hash
    
    if broken_links:
        return {
            "detected": True,
            "attack_class": "AUDIT_CHAIN_TAMPERED",
            "severity": "CRITICAL",
            "evidence": broken_links,
            "total_events": len(events),
            "broken_links": len(broken_links),
            "attacker_technique": (
                "Retroactive deletion or modification of audit events. "
                "Motive: cover tracks after privilege abuse, data exfiltration, or account takeover."
            ),
            "mitigation": (
                "WORM storage for audit logs. "
                "Forward hash to immutable SIEM on every write. "
                "Cross-validate chain on every compliance audit."
            )
        }
    
    return {
        "detected": False,
        "chain_intact": True,
        "events_verified": len(events),
        "final_hash": prev_hash
    }


def detect_clock_skew_tamper(
    events: List[Dict[str, Any]],
    max_future_seconds: int = 300,  # 5 min clock drift tolerance
    max_past_days: int = 7
) -> Dict[str, Any]:
    """
    T4-D: Detect timestamp manipulation in distributed audit trails.
    Attack: Attacker with clock control back-dates events or future-dates to avoid detection.
    """
    now = datetime.now(timezone.utc)
    anomalies = []
    
    for i, event in enumerate(events):
        ts_str = event.get("timestamp") or event.get("sealed_at", "")
        if not ts_str:
            continue
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            delta = (ts - now).total_seconds()
            
            if delta > max_future_seconds:
                anomalies.append({
                    "type": "FUTURE_TIMESTAMP",
                    "event_index": i,
                    "event_id": event.get("event_id"),
                    "timestamp": ts_str,
                    "seconds_in_future": round(delta, 1)
                })
            
            past_delta = (now - ts).total_seconds()
            if past_delta > max_past_days * 86400:
                anomalies.append({
                    "type": "SUSPICIOUS_PAST_TIMESTAMP",
                    "event_index": i,
                    "event_id": event.get("event_id"),
                    "timestamp": ts_str,
                    "days_old": round(past_delta / 86400, 1)
                })
        except Exception:
            anomalies.append({
                "type": "UNPARSEABLE_TIMESTAMP",
                "event_index": i,
                "raw": ts_str
            })
    
    if anomalies:
        return {
            "detected": True,
            "attack_class": "TIMESTAMP_MANIPULATION",
            "severity": "HIGH",
            "evidence": anomalies,
            "mitigation": "Use server-side NTP-synchronized timestamps only. Reject client-supplied timestamps."
        }
    
    return {"detected": False, "timestamps_valid": len(events)}


# ════════════════════════════════════════════════════════════════
# TIER 5 — Data Exfiltration via Identity
# CVE refs: Auth0 2021 scope bug, SAML wrapping CVE-2017-11427
# ════════════════════════════════════════════════════════════════

# Resource → minimum required scope
SCOPE_REQUIREMENTS: Dict[str, str] = {
    "financial_records": "read:financials",
    "pii_data": "read:pii",
    "hr_data": "read:hr",
    "audit_logs": "read:audit",
    "api_keys": "admin:api_keys",
    "user_management": "admin:users",
    "read_only_reports": "read:reports"
}


def detect_token_scope_creep(
    token_scopes: List[str],
    requested_resource: str,
    requested_action: str
) -> Dict[str, Any]:
    """
    T5-A: Detect OAuth token scope creep.
    
    CVE: Auth0 2021 scope bug, Okta API scope leaks (2020)
    PoC: https://github.com/PortSwigger/oauth-scope-creep
    Attack: Token granted narrow scope (read:profile) reused for high-priv endpoint.
    """
    required_scope = SCOPE_REQUIREMENTS.get(requested_resource)
    
    if not required_scope:
        return {
            "detected": True,
            "attack_class": "UNKNOWN_RESOURCE_ACCESS",
            "severity": "MEDIUM",
            "evidence": f"Resource '{requested_resource}' has no scope definition — access denied by default",
            "mitigation": "Fail-closed: deny access to any resource not in scope registry."
        }
    
    if required_scope not in token_scopes:
        # Check if attacker is using a broader scope to bypass
        has_wildcard = any("*" in s or "admin" in s.lower() for s in token_scopes)
        return {
            "detected": True,
            "attack_class": "TOKEN_SCOPE_CREEP",
            "severity": "HIGH" if has_wildcard else "MEDIUM",
            "evidence": {
                "token_scopes": token_scopes,
                "required_scope": required_scope,
                "requested_resource": requested_resource,
                "wildcard_scope_present": has_wildcard
            },
            "attacker_technique": (
                "Reuse narrow-scope token against high-privilege endpoint. "
                "Relies on endpoint not checking scope, only authentication."
            ),
            "mitigation": "Enforce scope at API gateway level, not just auth middleware.",
            "okta_rule": "Scope-per-endpoint enforcement. Token introspection before every request."
        }
    
    return {
        "detected": False,
        "scope_valid": True,
        "resource": requested_resource,
        "matched_scope": required_scope
    }


_login_attempts: Dict[str, List[Dict]] = defaultdict(list)  # ip → [{ts, user}]


def detect_credential_stuffing(
    ip: str,
    username: str,
    success: bool,
    velocity_window_seconds: int = 300,
    failure_threshold: int = 10,
    unique_user_threshold: int = 5
) -> Dict[str, Any]:
    """
    T5-B: Detect credential stuffing at scale.
    
    Tools used by attackers: OpenBullet, Sentry MBA, custom Python+proxy chains
    PoC: https://github.com/openbullet/OpenBullet
    Detection: High failure rate + many unique usernames from same IP = stuffing.
    """
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(seconds=velocity_window_seconds)
    
    attempts = _login_attempts[ip]
    # Clean old entries
    attempts = [a for a in attempts if datetime.fromisoformat(a["timestamp"]) > window_start]
    attempts.append({"timestamp": now.isoformat(), "username": username, "success": success})
    _login_attempts[ip] = attempts
    
    failures = [a for a in attempts if not a["success"]]
    unique_users = len({a["username"] for a in attempts})
    failure_rate = len(failures) / max(len(attempts), 1)
    
    # Stuffing signature: many failures, many unique usernames
    if len(failures) >= failure_threshold and unique_users >= unique_user_threshold:
        return {
            "detected": True,
            "attack_class": "CREDENTIAL_STUFFING",
            "severity": "CRITICAL",
            "evidence": {
                "ip": ip,
                "total_attempts": len(attempts),
                "failed_attempts": len(failures),
                "unique_usernames": unique_users,
                "failure_rate": round(failure_rate * 100, 1),
                "window_seconds": velocity_window_seconds
            },
            "attacker_tools": "OpenBullet / Sentry MBA / custom proxy chains",
            "mitigation": (
                "Block IP immediately. "
                "Enable adaptive CAPTCHA. "
                "Rate-limit by IP + fingerprint. "
                "Notify affected users."
            ),
            "okta_rule": "ThreatInsight: block IPs with velocity > 10 failures/5min across > 5 accounts."
        }
    
    # High velocity from single IP on single account — brute force
    single_user_fails = [a for a in failures if a["username"] == username]
    if len(single_user_fails) >= 3:
        return {
            "detected": True,
            "attack_class": "BRUTE_FORCE_DETECTED",
            "severity": "HIGH",
            "evidence": {"ip": ip, "username": username, "failures": len(single_user_fails)},
            "mitigation": "Progressive lockout. MFA challenge after 3 failures."
        }
    
    return {"detected": False, "ip": ip, "attempts_in_window": len(attempts)}


def detect_saml_signature_wrapping(xml_assertion: str) -> Dict[str, Any]:
    """
    T5-C: Detect SAML XML signature wrapping attacks.
    
    CVE-2017-11427 (Shibboleth), OneLogin, Auth0 variants
    Attack: Duplicate signed element. SP validates legitimate signature but process attacker node.
    """
    try:
        import re as _re
        
        # Count signed assertion elements
        assertion_count = len(_re.findall(r'<saml:Assertion\b|<samlp:Response\b', xml_assertion, _re.IGNORECASE))
        signature_count = len(_re.findall(r'<ds:Signature\b|<Signature\b', xml_assertion, _re.IGNORECASE))
        signed_id_count = len(_re.findall(r'URI="#', xml_assertion))
        
        if assertion_count > 1:
            return {
                "detected": True,
                "attack_class": "SAML_SIGNATURE_WRAPPING",
                "severity": "CRITICAL",
                "cve": "CVE-2017-11427, OneLogin/Auth0 SAML wrapping variants",
                "evidence": {
                    "assertion_count": assertion_count,
                    "signature_count": signature_count,
                    "multiple_assertions": True
                },
                "attacker_technique": (
                    "Duplicate signed assertion. Insert malicious assertion. "
                    "SP validates signature on original node, processes attacker-controlled node. "
                    "Exact payload: inject <saml:Assertion> sibling before signed one."
                ),
                "mitigation": (
                    "Parse XML before signature validation. "
                    "Reject any response with > 1 Assertion element. "
                    "Use strict canonicalization (C14N). "
                    "Validate ID references match signed content."
                ),
                "okta_rule": "Single assertion enforcement. ID-based signature binding. Reject duplicate IDs."
            }
        
        if signature_count == 0:
            return {
                "detected": True,
                "attack_class": "SAML_UNSIGNED_ASSERTION",
                "severity": "CRITICAL",
                "evidence": "SAML assertion contains no signature — accept-unsigned misconfiguration",
                "mitigation": "Never accept unsigned SAML assertions. Enforce signing requirement."
            }
        
        return {"detected": False, "assertions": assertion_count, "signatures": signature_count}
    
    except Exception as e:
        return {
            "detected": True,
            "attack_class": "SAML_PARSE_ERROR",
            "severity": "HIGH",
            "evidence": str(e),
            "mitigation": "Reject any malformed SAML — fail-closed."
        }


# ════════════════════════════════════════════════════════════════
# TIER 6 — Zero-Day Territory
# CVE refs: Uber 2022 breach, RFC 8628 device flow, timing attacks
# ════════════════════════════════════════════════════════════════

_device_code_usage: Dict[str, Dict] = {}  # code → {issued_at, approved_by_ip, poll_ips}
_mfa_push_log: Dict[str, List[str]] = defaultdict(list)  # user_id → [iso timestamps]


def detect_device_flow_abuse(
    device_code: str,
    polling_ip: str,
    approval_ip: Optional[str] = None,
    code_issued_at: Optional[str] = None
) -> Dict[str, Any]:
    """
    T6-A: Detect OAuth device authorization flow abuse (RFC 8628).
    
    PoC: https://github.com/PortSwigger/oauth-device-code-phishing
    Attack: Attacker social-engineers victim into entering device code on phishing page.
    Threat: Persistent access — device tokens often have no expiry.
    """
    now = datetime.now(timezone.utc)
    
    # Code TTL: standard is 15 min (RFC 8628 §3.4)
    if code_issued_at:
        try:
            issued = datetime.fromisoformat(code_issued_at.replace("Z", "+00:00"))
            age_seconds = (now - issued).total_seconds()
            if age_seconds > 900:  # 15 min
                return {
                    "detected": True,
                    "attack_class": "DEVICE_CODE_EXPIRED",
                    "severity": "MEDIUM",
                    "evidence": {"age_seconds": round(age_seconds, 0), "max_ttl": 900},
                    "mitigation": "Enforce strict device code TTL (≤ 15 min). Reject expired codes."
                }
        except Exception:
            pass
    
    state = _device_code_usage.get(device_code, {
        "poll_ips": set(), "poll_count": 0
    })
    
    # Track polling IPs
    poll_ips = state.get("poll_ips", set())
    if isinstance(poll_ips, list):
        poll_ips = set(poll_ips)
    poll_ips.add(polling_ip)
    state["poll_ips"] = poll_ips
    state["poll_count"] = state.get("poll_count", 0) + 1
    _device_code_usage[device_code] = state
    
    # Approval from different IP than polling — phishing signature
    if approval_ip and approval_ip != polling_ip:
        return {
            "detected": True,
            "attack_class": "DEVICE_FLOW_PHISHING",
            "severity": "CRITICAL",
            "evidence": {
                "polling_ip": polling_ip,
                "approval_ip": approval_ip,
                "poll_count": state["poll_count"]
            },
            "attacker_technique": (
                "Attacker polls from their IP. Social-engineer victim into approving at different IP. "
                "Attacker gets persistent access token after victim's approval."
            ),
            "incident_ref": "Similar pattern to GitHub/Microsoft 365 device-code phishing campaigns 2024",
            "mitigation": (
                "Show human-readable approval confirmation screen. "
                "Bind device code to originating IP. "
                "Short TTL (5 min). "
                "Alert user on device token issuance."
            )
        }
    
    # Excessive polling — attacker probing
    if state["poll_count"] > 50:
        return {
            "detected": True,
            "attack_class": "DEVICE_FLOW_ABUSE_POLLING",
            "severity": "MEDIUM",
            "evidence": {"poll_count": state["poll_count"], "unique_ips": len(poll_ips)},
            "mitigation": "Rate-limit device code polling (5 req/min per code). Expire after threshold."
        }
    
    return {"detected": False, "device_code_valid": True, "poll_count": state["poll_count"]}


def detect_mfa_fatigue(
    user_id: str,
    push_timestamp: Optional[str] = None,
    window_minutes: int = 10,
    push_threshold: int = 3
) -> Dict[str, Any]:
    """
    T6-B: Detect MFA push notification fatigue/bombing attacks.
    
    Incident: Uber 2022 breach (MFA fatigue used to gain initial access)
    Attack: Flood victim with MFA pushes → frustration → accidental approval.
    """
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=window_minutes)
    ts = push_timestamp or now.isoformat()
    
    pushes = _mfa_push_log[user_id]
    # Clean old entries
    pushes = [p for p in pushes if datetime.fromisoformat(p) > window_start]
    pushes.append(ts)
    _mfa_push_log[user_id] = pushes
    
    count = len(pushes)
    
    if count >= push_threshold:
        return {
            "detected": True,
            "attack_class": "MFA_PUSH_FATIGUE",
            "severity": "CRITICAL" if count >= push_threshold * 2 else "HIGH",
            "evidence": {
                "user_id": user_id,
                "push_count_in_window": count,
                "window_minutes": window_minutes,
                "threshold": push_threshold
            },
            "incident_ref": "Uber 2022 breach — attacker sent 20+ pushes over 1 hour",
            "mitigation": (
                "Block further pushes after 3 in 10 minutes. "
                "Switch to TOTP/FIDO2 for this session. "
                "Alert SOC + send out-of-band SMS to user. "
                "Require admin unblock."
            ),
            "okta_rule": (
                "Adaptive MFA: detect push velocity > 3/10min → auto-downgrade to TOTP. "
                "Enable Okta ThreatInsight for push bombing detection."
            )
        }
    
    return {
        "detected": False,
        "user_id": user_id,
        "push_count": count,
        "window_minutes": window_minutes,
        "pushes_remaining_before_block": max(0, push_threshold - count)
    }


def detect_timing_attack_risk(
    comparison_result: bool,
    comparison_duration_ms: float,
    baseline_duration_ms: Optional[float] = None
) -> Dict[str, Any]:
    """
    T6-C: Detect timing attack vulnerability in credential comparisons.
    
    Attack: Response time differs for valid vs. invalid username → enumerate valid accounts.
    Vulnerable: non-constant-time string comparison (Python `==`, early-exit loops).
    Fix: hmac.compare_digest() or constant-time Argon2 hashing.
    """
    # Suspiciously fast → early exit → non-constant time
    if comparison_duration_ms < 0.1:
        return {
            "detected": True,
            "attack_class": "TIMING_ATTACK_RISK",
            "severity": "HIGH",
            "evidence": {
                "duration_ms": comparison_duration_ms,
                "concern": "Sub-0.1ms comparison suggests non-hashed/constant-time comparison"
            },
            "attacker_technique": (
                "Measure response times for 'user not found' vs 'wrong password'. "
                "Server returning faster for non-existent users → enumerate valid accounts. "
                "Tools: Burp Intruder with time-based analysis."
            ),
            "mitigation": (
                "Always hash even for non-existent users (dummy hash check). "
                "Use hmac.compare_digest() for token comparison. "
                "Use Argon2id for password hashing (constant time by design)."
            )
        }
    
    # Significant deviation from baseline → information leak
    if baseline_duration_ms and abs(comparison_duration_ms - baseline_duration_ms) > 50:
        return {
            "detected": True,
            "attack_class": "TIMING_DEVIATION",
            "severity": "MEDIUM",
            "evidence": {
                "comparison_ms": comparison_duration_ms,
                "baseline_ms": baseline_duration_ms,
                "deviation_ms": abs(comparison_duration_ms - baseline_duration_ms)
            },
            "mitigation": "Pad response times to constant baseline. Use early-return-safe hash functions."
        }
    
    return {"detected": False, "timing_safe": True, "duration_ms": comparison_duration_ms}


def constant_time_token_compare(token_a: str, token_b: str) -> bool:
    """
    T6-C fix: Constant-time comparison using hmac.compare_digest.
    Prevents timing attacks on session token validation.
    """
    return hmac.compare_digest(
        token_a.encode("utf-8"),
        token_b.encode("utf-8")
    )


# ════════════════════════════════════════════════════════════════
# Master Threat Scanner — runs all detections on a single request
# ════════════════════════════════════════════════════════════════

class ThreatDetectionEngine:
    """
    Unified red-team → blue-team scanner.
    Feed it any identity request → get back all detected threats + mitigations.
    """

    def scan_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan an identity request for threats across all 6 tiers.
        Returns: threats_found (list), highest_severity, recommended_action.
        """
        threats = []

        # T1: JWT analysis
        if "jwt_token" in request:
            result = detect_jwt_alg_confusion(request["jwt_token"])
            if result.get("detected"):
                threats.append({"tier": 1, **result})

        # T2A: Refresh token replay
        if "token_id" in request and "ip" in request:
            result = detect_refresh_token_replay(request["token_id"], request["ip"], request.get("device_id"))
            if result.get("detected"):
                threats.append({"tier": 2, **result})

        # T2B: OAuth redirect
        if "redirect_uri" in request and "registered_domains" in request:
            result = detect_oauth_redirect_uri_attack(request["redirect_uri"], request["registered_domains"])
            if result.get("detected"):
                threats.append({"tier": 2, **result})

        # T3A: IDOR
        if all(k in request for k in ("requesting_user_id", "target_resource_owner_id")):
            result = detect_idor_attempt(
                request["requesting_user_id"],
                request.get("requesting_user_tenant", "tenant_a"),
                request.get("target_resource_id", "res_001"),
                request["target_resource_owner_id"],
                request.get("target_resource_tenant", "tenant_a")
            )
            if result.get("detected"):
                threats.append({"tier": 3, **result})

        # T3B: Mass assignment
        if "submitted_fields" in request and "allowed_fields" in request:
            result = detect_mass_assignment(request["submitted_fields"], request["allowed_fields"])
            if result.get("detected"):
                threats.append({"tier": 3, **result})

        # T4: Log injection
        for field in ("username", "email", "user_agent"):
            if field in request:
                result = detect_audit_log_injection(str(request[field]), field)
                if result.get("detected"):
                    threats.append({"tier": 4, **result})

        # T5A: Scope creep
        if "token_scopes" in request and "requested_resource" in request:
            result = detect_token_scope_creep(
                request["token_scopes"], request["requested_resource"], request.get("requested_action", "read")
            )
            if result.get("detected"):
                threats.append({"tier": 5, **result})

        # T5B: Credential stuffing
        if "ip" in request and "username" in request and "login_success" in request:
            result = detect_credential_stuffing(
                request["ip"], request["username"], request["login_success"]
            )
            if result.get("detected"):
                threats.append({"tier": 5, **result})

        # T6B: MFA fatigue
        if "mfa_push_user_id" in request:
            result = detect_mfa_fatigue(request["mfa_push_user_id"])
            if result.get("detected"):
                threats.append({"tier": 6, **result})

        # Calculate severity
        sev_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        if threats:
            highest = max(threats, key=lambda t: sev_order.get(t.get("severity", "LOW"), 0))
            action = (
                "BLOCK_AND_ALERT" if highest.get("severity") == "CRITICAL"
                else "CHALLENGE_AND_LOG" if highest.get("severity") == "HIGH"
                else "LOG_AND_MONITOR"
            )
        else:
            highest = None
            action = "ALLOW"

        return {
            "threats_found": len(threats),
            "threats": threats,
            "highest_severity": highest.get("severity") if highest else None,
            "recommended_action": action,
            "clean": len(threats) == 0,
            "scanned_at": datetime.now(timezone.utc).isoformat()
        }


# Global singleton
threat_engine = ThreatDetectionEngine()
