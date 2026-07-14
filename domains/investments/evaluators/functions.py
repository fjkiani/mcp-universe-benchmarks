"""
Evaluators for AI Investment Advisor & Portfolio Management Domain

Standardized to use @compare_func decorator and return Tuple[bool, str]
matching all other domains.
"""

import json
import re
from typing import Any, Dict, Tuple

try:
    from lbx_cli.mcpuniverse.evaluator.functions import compare_func
except ImportError:
    from scripts.eval_compat import compare_func


def _unwrap_response(llm_response: Any) -> Tuple[bool, Any, str]:
    """Unwrap Pydantic FunctionResult and parse JSON from agent response.

    Returns: (success: bool, data: dict, error_message: str)
    """
    try:
        if hasattr(llm_response, 'result'):
            response = llm_response.result
        elif hasattr(llm_response, 'model_dump'):
            d = llm_response.model_dump()
            response = d.get('result', d)
        else:
            response = llm_response

        if isinstance(response, str):
            cleaned = response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1]) if len(lines) > 2 else cleaned
            cleaned = cleaned.strip()
            data = json.loads(cleaned)
        elif isinstance(response, dict):
            data = response
        else:
            return False, None, f"Unexpected response type: {type(response).__name__}"

        if not isinstance(data, dict):
            return False, None, f"Response is not a JSON object: {type(data).__name__}"

        return True, data, ""

    except json.JSONDecodeError as e:
        return False, None, f"JSON parse failed: {str(e)}"
    except Exception as e:
        return False, None, f"Unexpected error: {str(e)}"


def _score_response(data: dict, required_fields: list, optional_fields: list = None) -> float:
    """Score a response based on field presence and data quality."""
    score = 0.0
    total = len(required_fields)

    for field in required_fields:
        if field in data and data[field] is not None:
            val = data[field]
            if isinstance(val, (int, float)) and val != 0:
                score += 1.0
            elif isinstance(val, str) and len(val) > 2:
                score += 1.0
            elif isinstance(val, list) and len(val) > 0:
                score += 1.0
            elif isinstance(val, bool):
                score += 1.0
            else:
                score += 0.5

    if optional_fields:
        for field in optional_fields:
            if field in data and data[field] is not None:
                score += 0.5
                total += 0.5

    return score / total if total > 0 else 0.0


@compare_func(name="investments.validate_portfolio_analysis")
async def validate_portfolio_analysis(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate portfolio valuation and performance tracking tasks."""
    success, data, error = _unwrap_response(llm_response)
    if not success:
        return False, f"Failed to parse response: {error}"

    required = ["total_value", "holdings"]
    optional = ["daily_return", "daily_change", "performance"]
    score = _score_response(data, required, optional)

    if score >= 0.7:
        return True, f"Portfolio analysis validated (score: {score:.2f})"
    return False, f"Portfolio analysis incomplete (score: {score:.2f}). Missing fields: {[f for f in required if f not in data]}"


@compare_func(name="investments.validate_stock_research")
async def validate_stock_research(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate stock research and technical analysis tasks."""
    success, data, error = _unwrap_response(llm_response)
    if not success:
        return False, f"Failed to parse response: {error}"

    required = ["recommendation", "trend"]
    optional = ["sma_50", "sma_200", "rsi_14", "macd", "pe_ratio", "sector",
                "peer_1_ticker", "peer_1_pe_ratio", "target_ticker", "target_pe_ratio",
                "eps_actual", "revenue_actual", "analyst_reaction", "quarter"]
    score = _score_response(data, required, optional)

    if score >= 0.7:
        return True, f"Stock research validated (score: {score:.2f})"
    return False, f"Stock research incomplete (score: {score:.2f}). Missing key fields."


@compare_func(name="investments.validate_risk_assessment")
async def validate_risk_assessment(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate risk assessment tasks."""
    success, data, error = _unwrap_response(llm_response)
    if not success:
        return False, f"Failed to parse response: {error}"

    required = ["risk_rating", "portfolio_beta"]
    optional = ["portfolio_volatility", "sharpe_ratio", "var_95", "recommendations"]
    score = _score_response(data, required, optional)

    if score >= 0.7:
        return True, f"Risk assessment validated (score: {score:.2f})"
    return False, f"Risk assessment incomplete (score: {score:.2f}). Missing key fields."


@compare_func(name="investments.validate_rebalancing")
async def validate_rebalancing(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """Validate portfolio rebalancing tasks."""
    success, data, error = _unwrap_response(llm_response)
    if not success:
        return False, f"Failed to parse response: {error}"

    required = ["recommendation"]
    optional = ["new_allocations", "trades", "target_weights", "current_weights",
                "tax_implications", "rebalanced_portfolio"]
    score = _score_response(data, required, optional)

    if score >= 0.7:
        return True, f"Rebalancing validated (score: {score:.2f})"
    return False, f"Rebalancing incomplete (score: {score:.2f}). Missing key fields."
