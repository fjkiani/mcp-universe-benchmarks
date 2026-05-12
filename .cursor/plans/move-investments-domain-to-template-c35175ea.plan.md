---
name: Fix Investments Domain - Complete Gap Analysis & Fix Plan
overview: ""
todos:
  - id: 6fdc55d4-d4c4-4ead-a1ae-e2ca7d880949
    content: Read all 15 investment task JSON files to understand current structure and input data
    status: pending
  - id: 286cd791-f05f-419d-bd5d-158585693583
    content: Update portfolio_analysis_task_0001-0004.json to embed input data in question field
    status: pending
  - id: 8bc189dc-dc86-4315-b77b-10f27d8facaa
    content: Update stock_research_task_0005-0008.json to embed input data in question field
    status: pending
  - id: 7a72ff67-42c4-4adb-b332-64348c1418ef
    content: Update risk_assessment_task_0009-0011.json to embed input data in question field
    status: pending
  - id: 6049397b-74c2-44f9-b171-1fa47961f385
    content: Update rebalancing_task_0012-0015.json to embed input data in question field
    status: pending
  - id: 09150551-6422-4967-90bd-28dd50f20be2
    content: Verify all tasks have properly formatted questions with all input data embedded
    status: pending
isProject: false
---

# Fix Investments Domain - Complete Gap Analysis & Fix Plan

## Critical Issues Identified

### Issue 1: Input Field Not Read (PRIMARY)

- **Problem**: `input` field in task JSON is ignored by `TaskConfig` model
- **Evidence**: Test results show agents responding with "Portfolio holdings not specified"
- **Impact**: All 15 tasks failing because agents can't see input data
- **Fix**: Embed all input data into `question` field

### Issue 2: Missing Evaluators Configuration (CRITICAL)

- **Problem**: Investment tasks have NO `evaluators` field
- **Evidence**: Grep search found zero matches for "evaluators" in investment tasks
- **Impact**: Tasks cannot be evaluated properly
- **Fix**: Add `evaluators` array to each task with proper structure

### Issue 3: Wrong MCP Servers Field Name

- **Problem**: Tasks use `required_mcp_servers` instead of `mcp_servers`
- **Evidence**: `TaskConfig` expects `mcp_servers` field
- **Impact**: MCP servers not being loaded for tasks
- **Fix**: Rename `required_mcp_servers` to `mcp_servers` and format as array of objects

### Issue 4: Missing use_specified_server Field

- **Problem**: Tasks don't have `use_specified_server` field
- **Impact**: Agents may use wrong servers
- **Fix**: Add `"use_specified_server": true` to all tasks

### Issue 5: Evaluator Field Mismatches

- **Problem**: Some evaluators check for fields not in `expected_output`
- **Examples**: 
  - stock_research_task_0006/0007: Evaluator expects `company_name`, `valuation_summary` but not in expected_output
  - rebalancing_task_0013/0014/0015: Evaluator expects `rebalancing_needed`, `rationale` but not in expected_output
- **Impact**: Tasks fail validation even when agent provides correct output
- **Fix**: Align expected_output with evaluator requirements OR update evaluators

## Task Structure Comparison

### Correct Structure (from web_search/gitlab_mlops):

```json
{
  "category": "category_name",
  "question": "Question with all data embedded",
  "output_format": {...},
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "server-name"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "domain_name.evaluator_function",
      "op_args": {...}
    }
  ]
}
```

### Current Investment Tasks Structure (WRONG):

```json
{
  "id": "...",
  "question": "Question without input data",
  "category": "...",
  "difficulty": "...",
  "description": "...",
  "input": {...},  // ❌ NOT READ
  "output_format": {...},
  "expected_output": {...},
  "required_mcp_servers": [...],  // ❌ WRONG FIELD NAME
  "task_type": "...",
  "evaluation_criteria": {...},
  "test_data_note": "..."
  // ❌ MISSING: evaluators, use_specified_server
}
```

## Input Data Patterns Across Tasks

### Pattern 1: Simple Holdings (task 0001, 0002)

```json
"input": {
  "holdings": [{"ticker": "AAPL", "shares": 100}],
  "purchase_dates": {"AAPL": "2024-01-15"}  // separate object
}
```

### Pattern 2: Holdings with Embedded Data (task 0003, 0004, 0009, 0011)

```json
"input": {
  "holdings": [
    {
      "ticker": "AAPL",
      "shares": 100,
      "purchase_date": "2023-01-15",  // embedded
      "purchase_price": 130.5
    }
  ],
  "benchmark": "^GSPC"  // additional field
}
```

### Pattern 3: Single Ticker (task 0005, 0006, 0008)

```json
"input": {
  "ticker": "TSLA",
  "analysis_type": "fundamental",
  "timeframe": "3_months",
  "indicators_requested": [...]
}
```

### Pattern 4: Peer Comparison (task 0007)

```json
"input": {
  "target_company": "AMD",
  "peer_group": ["NVDA", "INTC"],
  "comparison_metrics": [...]
}
```

### Pattern 5: Current Holdings (task 0012, 0013, 0014, 0015)

```json
"input": {
  "current_holdings": [...],  // different field name
  "current_total_value": 68500,
  "target_allocation": {...},
  "current_allocation": {...}
}
```

## Fix Strategy for First 5 Tasks

### Task 1: portfolio_analysis_task_0001.json

**Input to embed:**

- Holdings: AAPL (100 shares), GOOGL (50 shares), MSFT (75 shares)
- Purchase dates: AAPL (2024-01-15), GOOGL (2024-02-10), MSFT (2024-03-05)

**Format:**

```
Calculate the current total value of this portfolio, daily performance metrics, and identify the best and worst performing holdings based on year-to-date returns.

Portfolio Holdings:
- AAPL: 100 shares (purchased 2024-01-15)
- GOOGL: 50 shares (purchased 2024-02-10)
- MSFT: 75 shares (purchased 2024-03-05)
```

**Add:**

- `evaluators` array with `investments.validate_portfolio_analysis`
- `mcp_servers` array (rename from `required_mcp_servers`)
- `use_specified_server: true`
- Remove: `id`, `difficulty`, `description`, `task_type`, `evaluation_criteria`, `test_data_note` (optional, keep for docs)

### Task 2: portfolio_analysis_task_0002.json

**Input to embed:**

- Holdings: AAPL (100), GOOGL (50), MSFT (75), TSLA (25), JPM (60), JNJ (40)

**Format:**

```
Analyze the diversification of this portfolio by calculating the Herfindahl-Hirschman Index (HHI), sector allocation breakdown, and concentration risk metrics.

Portfolio Holdings:
- AAPL: 100 shares
- GOOGL: 50 shares
- MSFT: 75 shares
- TSLA: 25 shares
- JPM: 60 shares
- JNJ: 40 shares
```

### Task 3: portfolio_analysis_task_0003.json

**Input to embed:**

- Holdings with purchase dates/prices + benchmark

**Format:**

```
Calculate and compare portfolio performance across multiple timeframes (1-day, 1-week, 1-month, 3-month, YTD, 1-year) and benchmark against S&P 500 index.

Portfolio Holdings:
- AAPL: 100 shares (purchased 2023-01-15 at $130.50)
- GOOGL: 50 shares (purchased 2023-06-10 at $120.30)
- MSFT: 75 shares (purchased 2023-09-05 at $315.20)

Benchmark: S&P 500 (^GSPC)
```

### Task 4: portfolio_analysis_task_0004.json

**Input to embed:**

- Holdings with purchase data + report_type

**Format:**

```
Generate a comprehensive portfolio performance report including valuation, performance metrics, sector allocation, top holdings, and risk indicators using multiple MCP servers.

Portfolio Holdings:
- AAPL: 100 shares (purchased 2023-01-15 at $130.50)
- GOOGL: 50 shares (purchased 2023-06-10 at $120.30)
- MSFT: 75 shares (purchased 2023-09-05 at $315.20)
- TSLA: 25 shares (purchased 2024-01-10 at $240.00)
- JPM: 60 shares (purchased 2024-02-20 at $175.50)

Report Type: quarterly_review
```

### Task 5: stock_research_task_0005.json

**Input to embed:**

- Ticker + analysis_type

**Format:**

```
Research the fundamental financial metrics for TSLA (Tesla Inc) including P/E ratio, revenue growth, profit margins, debt levels, and competitive positioning.

Company: TSLA
Analysis Type: fundamental
```

## Evaluator Configuration

Each task needs evaluators array. Based on task types:

- **portfolio_analysis_task_0001-0004**: Use `investments.validate_portfolio_analysis`
- **stock_research_task_0005-0008**: Use `investments.validate_stock_research`
- **risk_assessment_task_0009-0011**: Use `investments.validate_risk_assessment`
- **rebalancing_task_0012-0015**: Use `investments.validate_rebalancing`

**Evaluator format:**

```json
"evaluators": [
  {
    "func": "raw",
    "op": "investments.validate_portfolio_analysis",
    "op_args": {
      "task_input": {},  // Can be empty, evaluator gets from task
      "expected_output": {}  // From expected_output field
    }
  }
]
```

## MCP Servers Configuration

Convert from:

```json
"required_mcp_servers": ["stock-portfolio"]
```

To:

```json
"mcp_servers": [
  {"name": "stock-portfolio"}
]
```

## Files to Fix (First 5 for Testing)

1. `portfolio_analysis_task_0001.json`
2. `portfolio_analysis_task_0002.json`
3. `portfolio_analysis_task_0003.json`
4. `portfolio_analysis_task_0004.json`
5. `stock_research_task_0005.json`

## Validation After Fix

After fixing first 5 tasks, verify:

- ✅ Question field contains all input data
- ✅ Evaluators array present and properly formatted
- ✅ mcp_servers array present (not required_mcp_servers)
- ✅ use_specified_server field present
- ✅ JSON is valid
- ✅ Task structure matches working domains