#!/usr/bin/env python3
"""
Add output_format field to remaining investment tasks to reduce JSON parsing errors
"""
import json
import sys

# Task-specific output formats
TASK_FORMATS = {
    "stock_research_task_0006.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "sma_50": 245.30,
            "sma_200": 238.15,
            "rsi_14": 58.2,
            "macd": 3.45,
            "macd_signal": 2.8,
            "bollinger_upper": 255.0,
            "bollinger_lower": 235.0,
            "volume_avg": 125000000,
            "trend": "Bullish",
            "recommendation": "Buy signal from technical indicators"
        },
        "expected": {
            "sma_50": "numeric",
            "sma_200": "numeric",
            "rsi_14": "numeric",
            "macd": "numeric",
            "macd_signal": "numeric",
            "bollinger_upper": "numeric",
            "bollinger_lower": "numeric",
            "volume_avg": "numeric",
            "trend": "string",
            "recommendation": "string"
        }
    },
    "stock_research_task_0007.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "peer_1_ticker": "GM",
            "peer_1_pe_ratio": 6.2,
            "peer_2_ticker": "F",
            "peer_2_pe_ratio": 7.1,
            "target_ticker": "TSLA",
            "target_pe_ratio": 45.2,
            "industry_avg_pe": 12.5,
            "relative_valuation": "Premium valuation vs peers",
            "competitive_position": "Leader in EV segment"
        },
        "expected": {
            "peer_1_ticker": "string",
            "peer_1_pe_ratio": "numeric",
            "peer_2_ticker": "string",
            "peer_2_pe_ratio": "numeric",
            "target_ticker": "string",
            "target_pe_ratio": "numeric",
            "industry_avg_pe": "numeric",
            "relative_valuation": "string",
            "competitive_position": "string"
        }
    },
    "stock_research_task_0008.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "ticker": "AAPL",
            "quarter": "Q1 2025",
            "eps_actual": 2.15,
            "eps_estimate": 2.10,
            "eps_surprise": 2.4,
            "revenue_actual": 95000000000,
            "revenue_estimate": 93000000000,
            "revenue_surprise": 2.2,
            "guidance_raised": True,
            "analyst_reaction": "Positive - strong iPhone sales",
            "recommendation": "Buy on earnings beat"
        },
        "expected": {
            "ticker": "string",
            "quarter": "string",
            "eps_actual": "numeric",
            "eps_estimate": "numeric",
            "eps_surprise": "numeric",
            "revenue_actual": "numeric",
            "revenue_estimate": "numeric",
            "revenue_surprise": "numeric",
            "guidance_raised": "boolean",
            "analyst_reaction": "string",
            "recommendation": "string"
        }
    },
    "risk_assessment_task_0009.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "sharpe_ratio": 1.45,
            "beta": 1.05,
            "alpha": 2.3,
            "volatility": 18.5,
            "max_drawdown": -12.3,
            "var_95": -2.5,
            "downside_deviation": 14.2,
            "risk_assessment": "Moderate risk profile"
        },
        "expected": {
            "sharpe_ratio": "numeric",
            "beta": "numeric",
            "alpha": "numeric",
            "volatility": "numeric",
            "max_drawdown": "numeric",
            "var_95": "numeric",
            "downside_deviation": "numeric",
            "risk_assessment": "string"
        }
    },
    "risk_assessment_task_0010.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "aapl_googl_correlation": 0.75,
            "aapl_msft_correlation": 0.82,
            "aapl_tsla_correlation": 0.45,
            "googl_msft_correlation": 0.78,
            "googl_tsla_correlation": 0.38,
            "msft_tsla_correlation": 0.42,
            "avg_correlation": 0.60,
            "diversification_score": 65,
            "recommendation": "Good diversification across tech holdings"
        },
        "expected": {
            "aapl_googl_correlation": "numeric",
            "aapl_msft_correlation": "numeric",
            "aapl_tsla_correlation": "numeric",
            "googl_msft_correlation": "numeric",
            "googl_tsla_correlation": "numeric",
            "msft_tsla_correlation": "numeric",
            "avg_correlation": "numeric",
            "diversification_score": "numeric",
            "recommendation": "string"
        }
    },
    "risk_assessment_task_0011.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "current_portfolio_value": 150000,
            "recession_scenario_value": 120000,
            "recession_loss_percent": -20.0,
            "tech_crash_scenario_value": 105000,
            "tech_crash_loss_percent": -30.0,
            "rate_hike_scenario_value": 135000,
            "rate_hike_loss_percent": -10.0,
            "worst_case_scenario": "Tech sector crash",
            "recommendation": "Reduce tech concentration"
        },
        "expected": {
            "current_portfolio_value": "numeric",
            "recession_scenario_value": "numeric",
            "recession_loss_percent": "numeric",
            "tech_crash_scenario_value": "numeric",
            "tech_crash_loss_percent": "numeric",
            "rate_hike_scenario_value": "numeric",
            "rate_hike_loss_percent": "numeric",
            "worst_case_scenario": "string",
            "recommendation": "string"
        }
    },
    "rebalancing_task_0012.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "trade_1_action": "SELL",
            "trade_1_ticker": "AAPL",
            "trade_1_shares": 25,
            "trade_2_action": "BUY",
            "trade_2_ticker": "JPM",
            "trade_2_shares": 40,
            "total_trades": 2,
            "rebalance_complete": True,
            "new_allocation_summary": "Reduced tech from 60% to 50%, increased financials to 20%"
        },
        "expected": {
            "trade_1_action": "string",
            "trade_1_ticker": "string",
            "trade_1_shares": "numeric",
            "trade_2_action": "string",
            "trade_2_ticker": "string",
            "trade_2_shares": "numeric",
            "total_trades": "numeric",
            "rebalance_complete": "boolean",
            "new_allocation_summary": "string"
        }
    },
    "rebalancing_task_0013.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "harvest_1_ticker": "TSLA",
            "harvest_1_shares": 15,
            "harvest_1_loss": -2250,
            "harvest_2_ticker": "NVDA",
            "harvest_2_shares": 10,
            "harvest_2_loss": -1500,
            "total_loss_harvested": -3750,
            "tax_savings_estimate": 1125,
            "replacement_strategy": "Buy similar sector ETFs"
        },
        "expected": {
            "harvest_1_ticker": "string",
            "harvest_1_shares": "numeric",
            "harvest_1_loss": "numeric",
            "harvest_2_ticker": "string",
            "harvest_2_shares": "numeric",
            "harvest_2_loss": "numeric",
            "total_loss_harvested": "numeric",
            "tax_savings_estimate": "numeric",
            "replacement_strategy": "string"
        }
    },
    "rebalancing_task_0014.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "current_tech_allocation": 55.0,
            "target_tech_allocation": 45.0,
            "current_healthcare_allocation": 15.0,
            "target_healthcare_allocation": 25.0,
            "rotation_rationale": "Economic cycle favoring defensive sectors",
            "trade_1_action": "SELL",
            "trade_1_sector": "Technology",
            "trade_1_amount": 15000,
            "trade_2_action": "BUY",
            "trade_2_sector": "Healthcare",
            "trade_2_amount": 15000
        },
        "expected": {
            "current_tech_allocation": "numeric",
            "target_tech_allocation": "numeric",
            "current_healthcare_allocation": "numeric",
            "target_healthcare_allocation": "numeric",
            "rotation_rationale": "string",
            "trade_1_action": "string",
            "trade_1_sector": "string",
            "trade_1_amount": "numeric",
            "trade_2_action": "string",
            "trade_2_sector": "string",
            "trade_2_amount": "numeric"
        }
    },
    "rebalancing_task_0015.json": {
        "description": "Return valid JSON with flat structure",
        "example": {
            "analysis_complete": True,
            "rebalance_needed": True,
            "total_trades": 5,
            "tax_loss_harvested": -4500,
            "tax_savings": 1350,
            "risk_reduced": True,
            "new_sharpe_ratio": 1.65,
            "execution_summary": "Rebalanced portfolio to target allocation with tax optimization"
        },
        "expected": {
            "analysis_complete": "boolean",
            "rebalance_needed": "boolean",
            "total_trades": "numeric",
            "tax_loss_harvested": "numeric",
            "tax_savings": "numeric",
            "risk_reduced": "boolean",
            "new_sharpe_ratio": "numeric",
            "execution_summary": "string"
        }
    }
}

def add_output_format_to_task(task_file):
    """Add output_format to a task file"""
    task_name = task_file.split('/')[-1]
    
    if task_name not in TASK_FORMATS:
        print(f"⚠️  No format defined for {task_name}, skipping")
        return False
    
    # Read task
    with open(task_file, 'r') as f:
        task = json.load(f)
    
    # Check if output_format already exists
    if 'output_format' in task:
        print(f"✅ {task_name} already has output_format")
        return True
    
    # Insert output_format before expected_output
    format_data = TASK_FORMATS[task_name]
    task['output_format'] = {
        "description": format_data["description"],
        "example": format_data["example"]
    }
    
    # Update expected_output
    task['expected_output'] = format_data["expected"]
    
    # Write back
    with open(task_file, 'w') as f:
        json.dump(task, f, indent=2)
    
    print(f"✅ Added output_format to {task_name}")
    return True

if __name__ == "__main__":
    tasks_dir = "domains/investments/tasks"
    
    # Process remaining tasks (0006-0015)
    for task_id in list(range(6, 9)) + list(range(9, 16)):
        if task_id <= 8:
            task_file = f"{tasks_dir}/stock_research_task_000{task_id}.json"
        elif task_id <= 11:
            task_file = f"{tasks_dir}/risk_assessment_task_00{task_id}.json"
        else:
            task_file = f"{tasks_dir}/rebalancing_task_00{task_id}.json"
        
        try:
            add_output_format_to_task(task_file)
        except Exception as e:
            print(f"❌ Error processing {task_file}: {e}")
    
    print("\n✅ Batch update complete!")

