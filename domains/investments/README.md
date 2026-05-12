# AI Investment Advisor & Portfolio Management Domain

**⚠️ RESEARCH USE ONLY - NOT FINANCIAL ADVICE**

## Overview

This domain tests AI agents on real-world investment decision workflows including portfolio analysis, stock research, risk assessment, and automated rebalancing with complex financial reasoning and market data synthesis.

## Task Categories

### 1. Portfolio Analysis (4 tasks)
- **0001**: Calculate portfolio value and daily performance metrics
- **0002**: Calculate diversification metrics and sector allocation
- **0003**: Track performance over multiple timeframes with benchmarking
- **0004**: Generate comprehensive portfolio report (multi-server orchestration)

### 2. Stock Research & Valuation (4 tasks)
- **0005**: Research company fundamentals and extract key financial metrics
- **0006**: Perform technical analysis with indicators and chart patterns
- **0007**: Perform peer comparison analysis for competitive positioning
- **0008**: Research earnings report and generate investment memo

### 3. Risk Assessment (3 tasks)
- **0009**: Calculate portfolio risk metrics (beta, volatility, Sharpe ratio, max drawdown)
- **0010**: Build correlation matrix and identify diversification opportunities
- **0011**: Perform stress testing and scenario analysis for market crash events

### 4. Rebalancing Recommendations (4 tasks)
- **0012**: Recommend rebalancing trades to restore target asset allocation
- **0013**: Optimize rebalancing with tax-loss harvesting to minimize capital gains
- **0014**: Sector rotation strategy based on economic cycle and market momentum
- **0015**: Comprehensive portfolio rebalancing (ultimate complexity - 5+ MCP servers)

## Difficulty Distribution

- **Medium (20%)**: Tasks 0001, 0005 - Basic calculations and data retrieval
- **Hard (40%)**: Tasks 0002, 0003, 0006, 0009, 0012 - Financial analysis and metrics
- **Very Hard (30%)**: Tasks 0004, 0007, 0008, 0010, 0013, 0014 - Multi-server orchestration and optimization
- **Expert (10%)**: Tasks 0011, 0015 - Complex modeling and full workflow integration

## MCP Servers Required

1. **stock-portfolio**: Real-time stock quotes, historical data, company fundamentals (Alpha Vantage API)
2. **google-search**: Market news, analyst reports, economic indicators
3. **google-sheets**: Portfolio tracking, correlation matrices, performance charts
4. **pdf-generator**: Professional investment reports and research memos
5. **calendar**: Earnings dates, rebalancing schedules, review reminders

## API Keys Needed

- **Alpha Vantage API** (free tier: 25 requests/day, premium available)
- **SERP API** (market news and analyst coverage)
- **Google OAuth** (for Sheets integration)
- **OpenAI API** (financial reasoning and analysis)

## Expected Pass@1 Rate

**Target: 35%** (appropriately challenging for financial AI)

### Breakdown by Category:
- **Portfolio Analysis**: 60% (straightforward calculations)
- **Stock Research**: 40% (requires data synthesis)
- **Risk Assessment**: 25% (complex statistical analysis)
- **Rebalancing**: 20% (multi-constraint optimization)

## Key Challenges

1. **Real-time Market Data**: Tasks use live market data, not static datasets
2. **Financial Calculations**: Accurate P/E ratios, beta, Sharpe ratio, tax implications
3. **Tax Optimization**: Understanding holding periods, wash sale rules, capital gains
4. **Risk Modeling**: Correlation matrices, stress testing, VaR calculations
5. **Multi-Server Orchestration**: Chaining stock data + sheets + PDF + calendar

## Ground Truth Sources

- **Alpha Vantage**: Real-time and historical market data
- **SEC Filings**: 10-K, 10-Q reports for fundamental analysis
- **Yahoo Finance/Google Finance**: Market data validation
- **Academic Papers**: Portfolio theory, risk management research
- **Regulatory Guidance**: SEC, FINRA rules for investment advice

## Financial Disclaimer

**⚠️ IMPORTANT LEGAL NOTICE**

This is a research benchmark for AI evaluation purposes only. All content is for educational and testing purposes.

**This is NOT:**
- Financial advice or investment recommendations
- A substitute for professional financial planning
- Regulatory-approved investment guidance

**Key Disclaimers:**
- All portfolio examples are hypothetical
- Past performance does not guarantee future results
- Investing involves risk of loss
- Consult a licensed financial advisor for actual investment decisions
- We make no warranties about accuracy or completeness of data
- Not intended for actual trading or investment decisions

**Regulatory Compliance:**
- Not registered as an investment advisor (SEC)
- Not a broker-dealer (FINRA)
- Educational research tool only

## Sample Task

**Task 0001: Calculate Portfolio Performance**

```json
{
  "input": {
    "holdings": [
      {"ticker": "AAPL", "shares": 100},
      {"ticker": "GOOGL", "shares": 50},
      {"ticker": "MSFT", "shares": 75}
    ]
  },
  "expected_output": {
    "current_portfolio_value": 52350.00,
    "daily_change_percent": 1.25,
    "ytd_return_percent": 18.5,
    "best_performer": {"ticker": "NVDA", "return_percent": 35.2},
    "calculation_breakdown": {...}
  }
}
```

## Evaluation Criteria

### Portfolio Analysis
- Value calculation accuracy (within 1% of actual)
- Return percentage calculations
- Data freshness (real-time or latest available)
- Calculation transparency

### Stock Research
- Financial metrics completeness
- Valuation reasoning quality
- Data accuracy vs SEC filings
- Analyst data currency

### Risk Assessment
- Risk metric calculation accuracy (beta, Sharpe, VaR)
- Correlation matrix correctness
- Stress test scenario realism
- Actionable risk mitigation recommendations

### Rebalancing
- Allocation drift calculations
- Trade sizing accuracy
- Tax optimization logic
- Constraint compliance (max allocation, wash sales)

## Scaling Plan

**Phase 1 (Initial Release)**: 15 tasks
**Phase 2 (Week 2-3)**: Scale to 35 tasks
- Add options strategies (covered calls, protective puts)
- International diversification (currency risk, ADRs)
- Alternative assets (REITs, commodities, crypto)

**Phase 3 (Week 4)**: Scale to 50+ tasks
- ESG investing and screening
- Retirement planning workflows
- Asset allocation by age/risk tolerance
- Portfolio insurance strategies

## Commercial Applications

While this is a research benchmark, similar AI capabilities power:
- Robo-advisors ($50B+ market)
- Portfolio management tools
- Investment research platforms
- Financial planning software

---

**Built for the LBX MCP Universe**
**Domain Type**: Real-world financial workflows
**Complexity**: Medium to Expert
**MCP Servers**: 5 (stock-portfolio, google-search, google-sheets, pdf-generator, calendar)

