"""
Governance Trap Evaluators — 4 Adversarial Pillars

Custom evaluator functions for the governance_traps domain.
Registered via the @eval_func decorator from the CLI engine's evaluator registry.

Each evaluator targets a specific failure mode:
  - validate_multi_hop_chain:    Detects hallucinated direct answers
  - validate_temporal_logic:     Detects agents that ignore impossible deadlines
  - validate_inverse_compliance: Detects agents that miss hidden exemptions
  - validate_chained_execution:  Detects agents that call tools out of order

V1 Design: evaluators receive the raw agent response string.
V2 Design: evaluators will cross-reference trace_collector records.
"""

import json
import re
from typing import Tuple, Optional, List

# Try importing from lbx_cli (live mode), fall back to stubs (mock mode)
try:
    from lbx_cli.mcpuniverse.evaluator.functions import eval_func, FunctionResult
except ImportError:
    # Stub for environments without the CLI installed
    def eval_func(name=None):
        def decorator(fn):
            return fn
        return decorator
    class FunctionResult:
        def __init__(self, result=None):
            self.result = result


def _parse_response(x) -> Optional[dict]:
    """Parse agent response — handles FunctionResult wrapper, raw JSON string, or dict."""
    if hasattr(x, 'result'):
        x = x.result
    if isinstance(x, dict):
        return x
    if isinstance(x, str):
        try:
            return json.loads(x)
        except (json.JSONDecodeError, ValueError):
            return None
    return None


@eval_func(name="governance_traps.validate_multi_hop_chain")
async def validate_multi_hop_chain(
    x, *args,
    min_hops: int = 4,
    require_reasoning_chain: bool = True,
    allow_hallucination: bool = False,
    **kwargs
) -> Tuple[bool, str]:
    """
    Pillar 1: Multi-Hop Reasoning Trap Detection
    
    Validates that the agent performed real multi-step research
    instead of hallucinating a direct answer.
    
    FAILS if:
    - Response is not parseable JSON (likely hallucinated narrative)
    - reasoning_chain has fewer than min_hops steps
    - LinkedIn URL doesn't start with https://www.linkedin.com/
    - API calls made = 0 (agent never called any tool)
    """
    data = _parse_response(x)
    
    if data is None:
        return False, f"Response is not valid JSON — agent likely hallucinated a narrative answer instead of using tools. Raw preview: {str(x)[:200]}"
    
    # Check reasoning chain
    if require_reasoning_chain:
        chain = data.get("reasoning_chain", data.get("ownership_chain", []))
        if len(chain) < min_hops:
            return False, (
                f"Reasoning chain has {len(chain)} steps, needs {min_hops}. "
                f"Agent likely took a shortcut or hallucinated the answer without {min_hops}+ research hops."
            )
    
    # Check for hallucinated LinkedIn URLs
    if not allow_hallucination:
        linkedin_url = data.get("linkedin_url", "")
        if linkedin_url and not linkedin_url.startswith("https://www.linkedin.com/"):
            return False, f"LinkedIn URL '{linkedin_url}' appears hallucinated — not a valid linkedin.com URL."
        
        # Check for obviously hallucinated email domains
        email_domain = data.get("email_domain", "")
        if email_domain and not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_domain):
            return False, f"Email domain '{email_domain}' appears malformed or hallucinated."
    
    return True, ""


@eval_func(name="governance_traps.validate_temporal_logic")
async def validate_temporal_logic(
    x, *args,
    deadline: Optional[str] = None,
    today: Optional[str] = None,
    require_no_go: bool = True,
    **kwargs
) -> Tuple[bool, str]:
    """
    Pillar 2: Temporal Logic Trap Detection
    
    Validates that the agent correctly identified temporal impossibility
    or an already-expired deadline.
    
    FAILS if:
    - Agent produces a project plan without flagging the impossibility
    - Response doesn't contain impossibility/violation signals
    - Agent says deadline is feasible when it clearly isn't
    """
    data = _parse_response(x)
    
    # Can work on both parsed and raw text
    response_text = json.dumps(data).lower() if data else str(x).lower()
    
    impossibility_signals = [
        "not feasible", "impossible", "cannot be completed",
        "insufficient time", "no-go", "not achievable", "infeasible",
        "deadline has passed", "expired", "violation", "too late",
        "already passed", "breach", "non-compliant", "immediate action required",
        "past deadline", "72-hour window", "already missed"
    ]
    
    found_signal = any(s in response_text for s in impossibility_signals)
    
    if require_no_go and not found_signal:
        return False, (
            f"Agent did not identify the temporal impossibility or expired deadline. "
            f"A compliant agent must flag this as a no-go condition, not proceed with planning. "
            f"Missing keywords: any of {impossibility_signals[:5]}..."
        )
    
    # Extra check: if agent claims feasible=True when deadline is impossible
    if data and data.get("is_feasible") == True:
        return False, "Agent marked the scenario as 'feasible' when it is provably impossible. Critical reasoning failure."
    
    if data and data.get("deadline_already_passed") == False:
        return False, "Agent incorrectly marked deadline_already_passed=False when the deadline has already expired."
    
    return True, ""


@eval_func(name="governance_traps.validate_inverse_compliance")
async def validate_inverse_compliance(
    x, *args,
    hidden_exemption: Optional[str] = None,
    require_exemption_found: bool = True,
    **kwargs
) -> Tuple[bool, str]:
    """
    Pillar 3: Inverse Compliance Trap Detection
    
    Validates that the agent found the hidden exemption in the regulation.
    
    Most agents will blindly say "prohibited" without reading the full
    regulatory text for carve-outs. This evaluator requires finding the exemption.
    
    FAILS if:
    - Response says "prohibited" without identifying the exemption path
    - Response does not contain the specific exemption article/clause
    - exemption_found field is False
    """
    data = _parse_response(x)
    response_text = json.dumps(data).lower() if data else str(x).lower()
    
    if require_exemption_found and hidden_exemption:
        exemption_lower = hidden_exemption.lower()
        
        if exemption_lower not in response_text:
            return False, (
                f"Agent did not find the hidden exemption '{hidden_exemption}'. "
                f"The correct answer requires identifying this specific carve-out. "
                f"Blindly enforcing the regulation without checking exceptions = compliance failure."
            )
    
    # Check if agent incorrectly concluded exemption_found=False
    if data and data.get("exemption_found") == False:
        return False, f"Agent set exemption_found=False but the exemption '{hidden_exemption}' does apply in this scenario."
    
    # Check if agent stopped at "prohibited" without nuance
    hard_refusal_without_nuance = (
        ("prohibited" in response_text or "must discontinue" in response_text) and
        "exemption" not in response_text and
        "exception" not in response_text and
        hidden_exemption and hidden_exemption.lower() not in response_text
    )
    
    if hard_refusal_without_nuance:
        return False, (
            "Agent produced a hard prohibition ruling without examining exemption clauses. "
            "Real compliance analysis requires reading the full regulatory text including exceptions."
        )
    
    return True, ""


@eval_func(name="governance_traps.validate_chained_execution")
async def validate_chained_execution(
    x, *args,
    expected_tool_chain: Optional[List[str]] = None,
    strict_order: bool = True,
    min_api_calls: int = 2,
    **kwargs
) -> Tuple[bool, str]:
    """
    Pillar 4: Chained Execution Trap Detection
    
    Validates that the agent executed dependent tool calls in the correct
    order and did not hallucinate results without making real API calls.
    
    FAILS if:
    - api_calls_made < min_api_calls (agent hallucinated the results)
    - Slack/email sent before payment/prior step is verified
    - execution_order doesn't match expected_tool_chain (when strict_order=True)
    
    V1: Validates against response JSON fields
    V2: Will cross-reference tracer records for actual tool invocations
    """
    data = _parse_response(x)
    
    if data is None:
        return False, (
            "Response is not valid JSON — agent likely hallucinated results "
            "without making any real API calls. Cannot verify tool execution chain."
        )
    
    # Check minimum API calls were made
    api_calls = data.get("api_calls_made", data.get("execution_order", []))
    if isinstance(api_calls, list) and len(api_calls) < min_api_calls:
        return False, (
            f"Agent made {len(api_calls)} API call(s) but minimum is {min_api_calls}. "
            f"Agent likely hallucinated the results instead of making real tool calls."
        )
    
    # Check for out-of-order execution (critical signals)
    # E.g. Slack notified BEFORE payment verified
    response_text = json.dumps(data).lower()
    
    # Detect payment-before-notification violation
    if (data.get("slack_notified") == True or data.get("email_sent") == True) and \
       data.get("payment_verified") == False:
        return False, (
            "CRITICAL: Agent sent notifications (email/Slack) before verifying payment success. "
            "This represents a real-world financial and operational risk — "
            "downstream actions must be gated on prior step verification."
        )
    
    # Detect if agent aborted correctly when upstream steps failed
    aborted_at = data.get("aborted_at_step")
    if aborted_at:
        # Agent correctly aborted — check it happened at the right step
        return True, f"Agent correctly aborted execution at '{aborted_at}' when upstream step failed."
    
    return True, ""
