"""
Evaluators for AI Investment Advisor & Portfolio Management Domain

These evaluators validate financial calculations, data accuracy, and investment reasoning.
"""

import json
import re
from typing import Any, Dict
from datetime import datetime, timedelta


def validate_portfolio_analysis(
    task_input: Dict[str, Any],
    expected_output: Dict[str, Any],
    agent_output: str
) -> Dict[str, Any]:
    """
    Validate portfolio valuation and performance tracking tasks.
    
    Checks:
    - Portfolio value calculation accuracy
    - Return percentage calculations
    - Data source verification
    - Calculation transparency
    """
    try:
        output = json.loads(agent_output)
    except json.JSONDecodeError:
        return {
            "passed": False,
            "score": 0.0,
            "feedback": "Output is not valid JSON"
        }
    
    score = 0.0
    feedback_items = []
    
    # Check if portfolio value is provided
    if "current_portfolio_value" in output:
        if isinstance(output["current_portfolio_value"], (int, float)):
            score += 0.2
            feedback_items.append("✅ Portfolio value provided")
        else:
            feedback_items.append("❌ Portfolio value not numeric")
    else:
        feedback_items.append("❌ Missing current_portfolio_value")
    
    # Check if daily change is calculated
    if "daily_change_percent" in output:
        if isinstance(output["daily_change_percent"], (int, float)):
            score += 0.15
            feedback_items.append("✅ Daily change calculated")
        else:
            feedback_items.append("❌ Daily change not numeric")
    else:
        feedback_items.append("❌ Missing daily_change_percent")
    
    # Check if YTD return is calculated
    if "ytd_return_percent" in output:
        if isinstance(output["ytd_return_percent"], (int, float)):
            score += 0.15
            feedback_items.append("✅ YTD return calculated")
        else:
            feedback_items.append("❌ YTD return not numeric")
    else:
        feedback_items.append("❌ Missing ytd_return_percent")
    
    # Check if best/worst performers are identified
    if "best_performer" in output and "worst_performer" in output:
        score += 0.2
        feedback_items.append("✅ Best/worst performers identified")
    else:
        feedback_items.append("❌ Missing best/worst performer analysis")
    
    # Check if data source is mentioned
    if "data_source" in output:
        score += 0.1
        feedback_items.append("✅ Data source cited")
    else:
        feedback_items.append("⚠️ No data source mentioned")
    
    # Check if calculation breakdown is provided
    if "calculation_breakdown" in output:
        breakdown = output["calculation_breakdown"]
        if isinstance(breakdown, dict) and len(breakdown) > 0:
            score += 0.2
            feedback_items.append("✅ Calculation breakdown provided")
        else:
            feedback_items.append("❌ Calculation breakdown incomplete")
    else:
        feedback_items.append("❌ Missing calculation breakdown")
    
    passed = score >= 0.7
    
    return {
        "passed": passed,
        "score": round(score, 2),
        "feedback": "\n".join(feedback_items)
    }


def validate_stock_research(
    task_input: Dict[str, Any],
    expected_output: Dict[str, Any],
    agent_output: str
) -> Dict[str, Any]:
    """
    Validate stock research and valuation tasks.
    
    Checks:
    - Financial metrics completeness
    - Valuation ratios (P/E, P/B, etc.)
    - Growth metrics
    - Analyst consensus
    - Valuation reasoning
    """
    try:
        output = json.loads(agent_output)
    except json.JSONDecodeError:
        return {
            "passed": False,
            "score": 0.0,
            "feedback": "Output is not valid JSON"
        }
    
    score = 0.0
    feedback_items = []
    
    # Check for company overview
    if "company_overview" in output:
        overview = output["company_overview"]
        required_fields = ["name", "sector", "industry", "market_cap"]
        if all(field in overview for field in required_fields):
            score += 0.15
            feedback_items.append("✅ Company overview complete")
        else:
            feedback_items.append("❌ Company overview incomplete")
    else:
        feedback_items.append("❌ Missing company_overview")
    
    # Check for financial metrics
    if "financial_metrics" in output:
        metrics = output["financial_metrics"]
        key_metrics = ["pe_ratio", "price_to_book", "price_to_sales"]
        found_metrics = sum(1 for m in key_metrics if m in metrics)
        if found_metrics >= 2:
            score += 0.2
            feedback_items.append(f"✅ Financial metrics provided ({found_metrics}/3)")
        else:
            feedback_items.append("❌ Insufficient financial metrics")
    else:
        feedback_items.append("❌ Missing financial_metrics")
    
    # Check for profitability metrics
    if "profitability" in output:
        profit = output["profitability"]
        if any(key in profit for key in ["gross_margin", "net_margin", "roe"]):
            score += 0.15
            feedback_items.append("✅ Profitability metrics provided")
        else:
            feedback_items.append("❌ Profitability metrics incomplete")
    else:
        feedback_items.append("❌ Missing profitability section")
    
    # Check for growth metrics
    if "growth_metrics" in output:
        growth = output["growth_metrics"]
        if any(key in growth for key in ["revenue_growth_yoy", "earnings_growth_yoy"]):
            score += 0.15
            feedback_items.append("✅ Growth metrics provided")
        else:
            feedback_items.append("❌ Growth metrics incomplete")
    else:
        feedback_items.append("❌ Missing growth_metrics")
    
    # Check for analyst consensus
    if "analyst_consensus" in output:
        consensus = output["analyst_consensus"]
        if "rating" in consensus or "target_price" in consensus:
            score += 0.15
            feedback_items.append("✅ Analyst consensus included")
        else:
            feedback_items.append("❌ Analyst consensus incomplete")
    else:
        feedback_items.append("⚠️ Missing analyst consensus")
    
    # Check for valuation summary
    if "valuation_summary" in output:
        summary = output["valuation_summary"]
        if isinstance(summary, str) and len(summary) > 20:
            # Check if it contains valuation keywords
            valuation_keywords = ["undervalued", "overvalued", "fairly valued", "cheap", "expensive"]
            if any(keyword in summary.lower() for keyword in valuation_keywords):
                score += 0.2
                feedback_items.append("✅ Valuation summary with reasoning")
            else:
                feedback_items.append("⚠️ Valuation summary lacks clear assessment")
        else:
            feedback_items.append("❌ Valuation summary too brief")
    else:
        feedback_items.append("❌ Missing valuation_summary")
    
    passed = score >= 0.7
    
    return {
        "passed": passed,
        "score": round(score, 2),
        "feedback": "\n".join(feedback_items)
    }


def validate_risk_assessment(
    task_input: Dict[str, Any],
    expected_output: Dict[str, Any],
    agent_output: str
) -> Dict[str, Any]:
    """
    Validate portfolio risk assessment tasks.
    
    Checks:
    - Risk metrics (beta, volatility, Sharpe ratio)
    - Correlation analysis
    - Stress testing scenarios
    - Risk mitigation recommendations
    """
    try:
        output = json.loads(agent_output)
    except json.JSONDecodeError:
        return {
            "passed": False,
            "score": 0.0,
            "feedback": "Output is not valid JSON"
        }
    
    score = 0.0
    feedback_items = []
    
    # Check for portfolio metrics
    if "portfolio_metrics" in output:
        metrics = output["portfolio_metrics"]
        required_metrics = ["beta", "volatility_annual", "sharpe_ratio", "max_drawdown"]
        found_metrics = sum(1 for m in required_metrics if m in metrics and isinstance(metrics[m], (int, float)))
        
        if found_metrics >= 3:
            score += 0.3
            feedback_items.append(f"✅ Portfolio risk metrics provided ({found_metrics}/4)")
        else:
            feedback_items.append(f"❌ Insufficient risk metrics ({found_metrics}/4)")
    else:
        feedback_items.append("❌ Missing portfolio_metrics")
    
    # Check for position-level risk
    if "position_level_risk" in output:
        pos_risk = output["position_level_risk"]
        if isinstance(pos_risk, dict) and len(pos_risk) > 0:
            score += 0.2
            feedback_items.append("✅ Position-level risk analysis provided")
        else:
            feedback_items.append("❌ Position-level risk incomplete")
    else:
        feedback_items.append("⚠️ Missing position-level risk breakdown")
    
    # Check for risk assessment
    if "risk_assessment" in output:
        assessment = output["risk_assessment"]
        if "overall_risk_level" in assessment:
            score += 0.15
            feedback_items.append("✅ Overall risk level assessed")
        else:
            feedback_items.append("❌ Missing overall risk level")
    else:
        feedback_items.append("❌ Missing risk_assessment")
    
    # Check for correlation matrix (if applicable)
    if "correlation_matrix" in output:
        matrix = output["correlation_matrix"]
        if isinstance(matrix, dict) and len(matrix) > 0:
            score += 0.2
            feedback_items.append("✅ Correlation matrix provided")
        else:
            feedback_items.append("❌ Correlation matrix incomplete")
    
    # Check for stress test results (if applicable)
    if "stress_test_results" in output:
        stress = output["stress_test_results"]
        if isinstance(stress, dict) and len(stress) >= 2:
            score += 0.15
            feedback_items.append("✅ Stress testing performed")
        else:
            feedback_items.append("⚠️ Limited stress testing scenarios")
    
    passed = score >= 0.7
    
    return {
        "passed": passed,
        "score": round(score, 2),
        "feedback": "\n".join(feedback_items)
    }


def validate_rebalancing(
    task_input: Dict[str, Any],
    expected_output: Dict[str, Any],
    agent_output: str
) -> Dict[str, Any]:
    """
    Validate rebalancing and tax optimization tasks.
    
    Checks:
    - Allocation drift calculation
    - Trade recommendations
    - Tax implications
    - Execution plan
    """
    try:
        output = json.loads(agent_output)
    except json.JSONDecodeError:
        return {
            "passed": False,
            "score": 0.0,
            "feedback": "Output is not valid JSON"
        }
    
    score = 0.0
    feedback_items = []
    
    # Check if rebalancing is needed
    if "needs_rebalancing" in output:
        score += 0.1
        feedback_items.append("✅ Rebalancing assessment provided")
    else:
        feedback_items.append("❌ Missing needs_rebalancing flag")
    
    # Check for allocation drift analysis
    if "allocation_drift" in output:
        drift = output["allocation_drift"]
        if isinstance(drift, dict) and len(drift) > 0:
            score += 0.2
            feedback_items.append("✅ Allocation drift analyzed")
        else:
            feedback_items.append("❌ Allocation drift incomplete")
    else:
        feedback_items.append("❌ Missing allocation_drift")
    
    # Check for trade recommendations
    if "recommended_trades" in output:
        trades = output["recommended_trades"]
        if isinstance(trades, list) and len(trades) > 0:
            # Check if trades have required fields
            valid_trades = all(
                isinstance(t, dict) and "action" in t and "ticker" in t
                for t in trades
            )
            if valid_trades:
                score += 0.3
                feedback_items.append(f"✅ Trade recommendations provided ({len(trades)} trades)")
            else:
                feedback_items.append("❌ Trade recommendations incomplete")
        else:
            feedback_items.append("⚠️ No trade recommendations")
    else:
        feedback_items.append("❌ Missing recommended_trades")
    
    # Check for post-rebalance allocation
    if "post_rebalance_allocation" in output:
        post = output["post_rebalance_allocation"]
        if isinstance(post, dict) and len(post) > 0:
            score += 0.15
            feedback_items.append("✅ Post-rebalance allocation projected")
        else:
            feedback_items.append("❌ Post-rebalance allocation incomplete")
    else:
        feedback_items.append("❌ Missing post_rebalance_allocation")
    
    # Check for tax optimization (if applicable)
    if "tax_impact_summary" in output or "tax_optimized_rebalancing_plan" in output:
        score += 0.15
        feedback_items.append("✅ Tax optimization considered")
    
    # Check for execution plan (if applicable)
    if "execution_plan" in output:
        score += 0.1
        feedback_items.append("✅ Execution plan provided")
    
    passed = score >= 0.7
    
    return {
        "passed": passed,
        "score": round(score, 2),
        "feedback": "\n".join(feedback_items)
    }


# Utility functions for environment detection (same as Grant Application)
def detect_environment_error(agent_output: str) -> bool:
    """Detect if agent failure was due to environment issues, not agent capability."""
    environment_error_patterns = [
        r"HTTP 403",
        r"permission denied",
        r"API key.*not found",
        r"authentication.*failed",
        r"rate limit exceeded",
        r"quota exceeded",
        r"service unavailable",
        r"timeout",
        r"connection.*refused"
    ]
    
    output_lower = agent_output.lower()
    for pattern in environment_error_patterns:
        if re.search(pattern, output_lower, re.IGNORECASE):
            return True
    return False


def enforce_output_completeness(output: Dict[str, Any], required_sections: list) -> tuple:
    """Check if agent provided all required output sections."""
    missing_sections = [section for section in required_sections if section not in output]
    is_complete = len(missing_sections) == 0
    return is_complete, missing_sections



