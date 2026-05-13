"""
Identity Agent Service
───────────────────────
OpenRouter-powered function-calling agent for identity security workflows.
Falls back to deterministic logic if OpenRouter is unavailable.

Replaces the previous OpenAI GPT-4o dependency with OpenRouter free-tier models.
"""
import os
import json
from datetime import datetime, timezone
from typing import Literal, Optional, List

from dotenv import load_dotenv

from services.identity.models import ActionTrace, IdentityAgentResponse
from services.identity.tools import IDENTITY_TOOLS, IDENTITY_SYSTEM_PROMPTS
from services.identity.engine import (
    evaluate_auth_request,
    evaluate_rbac_request,
    generate_audit_trail,
    suggest_remediation,
)

load_dotenv()

# ─── Try OpenRouter service ───────────────────────────────────────────────────
try:
    from services.openrouter_service import call_llm_with_messages
    OPENROUTER_AVAILABLE = True
except ImportError:
    OPENROUTER_AVAILABLE = False


class IdentityAgentService:
    """
    Core identity agent.
    OpenRouter (Hermes 405B reasoning model) drives the agentic loop;
    deterministic engine handles every tool call.
    No external APIs in the tool layer — 100% deterministic, zero latency for logic.
    """

    async def process(
        self,
        user_request: str,
        vertical: Literal["mfa_auth", "rbac_check", "compliance_audit"],
        scenario_context: Optional[dict] = None
    ) -> IdentityAgentResponse:
        """
        Entry point: natural language request -> agent loop -> structured response.
        Uses OpenRouter LLM if available, otherwise falls back to direct logic.
        """
        if OPENROUTER_AVAILABLE:
            try:
                return await self._process_with_llm(user_request, vertical, scenario_context)
            except Exception as e:
                import logging
                logging.getLogger("identity_agent").warning(
                    f"OpenRouter unavailable ({e}), falling back to deterministic logic"
                )
        return await self._process_without_llm(user_request, vertical, scenario_context)

    # ── LLM path ──────────────────────────────────────────────────────────────

    async def _process_with_llm(
        self,
        user_request: str,
        vertical: str,
        scenario_context: Optional[dict]
    ) -> IdentityAgentResponse:
        """OpenRouter agentic loop with tool calling."""
        system_prompt = IDENTITY_SYSTEM_PROMPTS.get(vertical, IDENTITY_SYSTEM_PROMPTS["mfa_auth"])
        context_str = json.dumps(scenario_context, indent=2) if scenario_context else "No additional context."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Identity Security Request:\n{user_request}\n\nContext:\n{context_str}"}
        ]

        actions: List[ActionTrace] = []
        auth_result = rbac_result = audit_result = remediation_result = None

        for _ in range(6):  # max 6 iterations
            result = await call_llm_with_messages(
                role="reasoning",  # Hermes 405B — best for function calling
                messages=messages,
                tools=IDENTITY_TOOLS,
                temperature=0.1,
            )

            content = result.get("content", "")
            tool_calls = result.get("tool_calls")

            # Append assistant message to history
            assistant_msg = {"role": "assistant", "content": content}
            if tool_calls:
                assistant_msg["tool_calls"] = tool_calls
            messages.append(assistant_msg)

            if not tool_calls:
                break

            for tc in tool_calls:
                name = tc["function"]["name"]
                try:
                    args = json.loads(tc["function"]["arguments"])
                except (json.JSONDecodeError, KeyError):
                    args = {}

                t1 = datetime.now()
                dispatch_result, success = self._dispatch(name, args)
                tool_latency = int((datetime.now() - t1).total_seconds() * 1000)

                if name == "evaluate_authentication":
                    auth_result = dispatch_result
                elif name == "evaluate_rbac":
                    rbac_result = dispatch_result
                elif name == "generate_audit_log":
                    audit_result = dispatch_result
                elif name == "apply_remediation":
                    remediation_result = dispatch_result

                actions.append(ActionTrace(
                    tool=name, args=args, result=dispatch_result,
                    success=success, latency_ms=tool_latency
                ))
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.get("id", ""),
                    "content": json.dumps(dispatch_result)
                })

        final_message = content or "Identity evaluation complete."
        return self._build_response(
            final_message, vertical, actions,
            auth_result, rbac_result, audit_result, remediation_result
        )

    # ── Fallback path (no LLM) ─────────────────────────────────────────────────

    async def _process_without_llm(
        self,
        user_request: str,
        vertical: str,
        scenario_context: Optional[dict]
    ) -> IdentityAgentResponse:
        """Direct deterministic processing — no LLM required. Still fully functional."""
        ctx = scenario_context or {}
        actions: List[ActionTrace] = []
        remedy = None

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
                actions.append(ActionTrace(
                    tool="apply_remediation",
                    args={"issue_type": "account_locked", "context": auth},
                    result=remedy, success=True
                ))
            elif auth.get("anomaly"):
                remedy = suggest_remediation("impossible_travel", auth)
                actions.append(ActionTrace(
                    tool="apply_remediation",
                    args={"issue_type": "impossible_travel", "context": auth},
                    result=remedy, success=True
                ))

            return self._build_response(
                f"Authentication evaluated: {auth.get('auth_status', 'unknown').upper()}. "
                f"Risk: {auth.get('risk_level', 'UNKNOWN')}.",
                vertical, actions, auth, None, None, remedy
            )

        elif vertical == "rbac_check":
            rbac = evaluate_rbac_request(
                user_id=ctx.get("user_id", "user_demo"),
                roles=ctx.get("roles", ["employee"]),
                resource=ctx.get("resource", "read_only_reports"),
                action=ctx.get("action", "read"),
                time_of_request=ctx.get("time_of_request")
            )
            actions.append(ActionTrace(tool="evaluate_rbac", args=ctx, result=rbac, success=True))
            return self._build_response(
                f"Access {'GRANTED' if rbac['access_granted'] else 'DENIED'} for {ctx.get('resource', 'resource')}.",
                vertical, actions, None, rbac, None, None
            )

        else:  # compliance_audit
            events = ctx.get("events", [{
                "event_id": "evt_001", "event_type": "login",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "location": "NYC", "actor_auth_verified": True, "data_classification": "internal"
            }])
            audit = generate_audit_trail(
                ctx.get("user_id", "user_demo"), events, ctx.get("check_tampering", False)
            )
            actions.append(ActionTrace(tool="generate_audit_log", args=ctx, result=audit, success=True))

            for anomaly in audit.get("anomalies", []):
                atype = anomaly.get("type")
                if atype in ("impossible_travel", "audit_tampering", "off_hours_access"):
                    remedy = suggest_remediation(atype, audit)
                    actions.append(ActionTrace(
                        tool="apply_remediation",
                        args={"issue_type": atype, "context": audit},
                        result=remedy, success=True
                    ))
                    break

            return self._build_response(
                f"Audit complete. Status: {audit['compliance_status'].upper()}. "
                f"Anomalies: {len(audit.get('anomalies', []))}.",
                vertical, actions, None, None, audit, remedy
            )

    # ── Tool dispatch ──────────────────────────────────────────────────────────

    def _dispatch(self, name: str, args: dict) -> tuple:
        """Route tool name -> engine function."""
        try:
            if name == "evaluate_authentication":
                result = evaluate_auth_request(**{
                    k: args[k] for k in
                    ["user_id", "credentials_valid", "mfa_provided", "failed_attempts",
                     "last_login_location", "current_location"]
                    if k in args
                })
            elif name == "evaluate_rbac":
                result = evaluate_rbac_request(**{
                    k: args[k] for k in
                    ["user_id", "roles", "resource", "action", "time_of_request"]
                    if k in args
                })
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
                result = {"error": f"Unknown tool: {name}"}
            return result, True
        except Exception as e:
            return {"error": str(e), "tool": name}, False

    # ── Response assembly ──────────────────────────────────────────────────────

    def _build_response(
        self,
        message: str,
        vertical: str,
        actions: List[ActionTrace],
        auth_result, rbac_result, audit_result, remediation_result
    ) -> IdentityAgentResponse:
        resp = IdentityAgentResponse(message=message, vertical=vertical, actions=actions)

        if auth_result:
            resp.auth_status    = auth_result.get("auth_status")
            resp.session_token  = auth_result.get("session_token")
            resp.session_expiry = auth_result.get("session_expiry")
            resp.mfa_required   = auth_result.get("mfa_required", False)
            resp.risk_score     = auth_result.get("risk_score")
            resp.risk_level     = auth_result.get("risk_level")

        if rbac_result:
            resp.access_granted       = rbac_result.get("access_granted")
            resp.applied_roles        = rbac_result.get("applied_roles", [])
            resp.permission_breakdown = rbac_result.get("permission_breakdown")
            resp.risk_score           = rbac_result.get("risk_score")
            resp.risk_level           = rbac_result.get("risk_level")

        if audit_result:
            resp.anomaly_detected  = audit_result.get("anomaly_detected")
            resp.compliance_status = audit_result.get("compliance_status")
            resp.event_log         = audit_result.get("event_log", [])
            resp.risk_score        = audit_result.get("risk_score")
            resp.risk_level        = audit_result.get("risk_level")

        if remediation_result:
            remedy = remediation_result.get("remediation", {})
            resp.remediation_suggested = remedy.get("action")
            resp.remediation_applied   = remedy.get("auto_apply", False)

        return resp


# Global singleton
identity_agent = IdentityAgentService()
