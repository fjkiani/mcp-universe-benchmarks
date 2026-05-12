# Web Search Domain - Task Breakdown

## Overview

This domain contains **55 tasks** across **5 categories**, demonstrating various aspects of web search capabilities.

## Task Categories

### 1. Person Identification (20 tasks)

Tasks that require identifying a person based on career statistics, achievements, or characteristics.

**Examples:**
- `info_search_task_0001.json` - Identify football player by season statistics
- `info_search_task_0002.json` - Find athlete by multiple season records
- `info_search_task_0009.json` - Identify person by career milestones

**Files:**
- info_search_task_0001, 0002, 0009, 0010, 0011, 0012, 0013, 0014, 0015, 0016
- info_search_task_0017, 0020, 0023, 0024, 0025, 0036, 0045, 0046
- multi-server_task_google_search_notion_0001, 0002

**Difficulty:** Medium  
**Skills Tested:** 
- Multi-source data aggregation
- Statistical reasoning
- Pattern matching

---

### 2. Entity Discovery (17 tasks)

Tasks requiring discovery of entities (companies, organizations, products) based on characteristics.

**Examples:**
- `info_search_task_0003.json` - Find company by product features
- `info_search_task_0004.json` - Identify organization by mission
- `info_search_task_0005.json` - Discover product by specifications

**Files:**
- info_search_task_0003, 0004, 0005, 0006, 0008, 0021, 0022, 0028, 0030
- info_search_task_0032, 0034, 0035, 0037, 0040, 0041
- multi-server_task_google_search_notion_0004, 0005

**Difficulty:** Medium  
**Skills Tested:**
- Entity recognition
- Characteristic matching
- Contextual reasoning

---

### 3. Metric Matching (4 tasks)

Tasks requiring finding entities that match specific metrics or measurements.

**Examples:**
- `info_search_task_0018.json` - Find based on numerical metrics
- `info_search_task_0026.json` - Match performance statistics
- `info_search_task_0050.json` - Identify by quantitative data

**Files:**
- info_search_task_0018, 0026, 0050
- multi-server_task_google_search_notion_0003

**Difficulty:** Medium-Hard  
**Skills Tested:**
- Numerical reasoning
- Data comparison
- Precision matching

---

### 4. Complex Reasoning (9 tasks)

Tasks requiring multi-step reasoning and synthesis of information from multiple sources.

**Examples:**
- `info_search_task_0007.json` - Multi-step logical deduction
- `info_search_task_0019.json` - Temporal reasoning
- `info_search_task_0027.json` - Causal relationship analysis

**Files:**
- info_search_task_0007, 0019, 0027, 0029, 0039
- info_search_task_0042, 0043, 0048, 0049

**Difficulty:** Hard  
**Skills Tested:**
- Multi-step reasoning
- Information synthesis
- Logical deduction
- Temporal understanding

---

### 5. Factual Lookup (5 tasks)

Direct factual information retrieval tasks.

**Examples:**
- `info_search_task_0031.json` - Historical facts
- `info_search_task_0033.json` - Current information
- `info_search_task_0038.json` - Specific data points

**Files:**
- info_search_task_0031, 0033, 0038, 0044, 0047

**Difficulty:** Easy-Medium  
**Skills Tested:**
- Factual recall
- Source verification
- Data extraction

---

## Task Structure

All tasks follow a consistent structure:

```json
{
    "category": "general",
    "question": "Detailed question with specific requirements",
    "output_format": {
        "answer": "[Your answer]"
    },
    "use_specified_server": true,
    "mcp_servers": [
        {
            "name": "google-search"
        },
        {
            "name": "fetch"
        }
    ],
    "evaluators": [
        {
            "func": "raw",
            "op": "google_search.llm_as_a_judge",
            "op_args": {
                "question": "...",
                "correct_answer": "Expected Answer"
            }
        }
    ]
}
```

## Task Design Principles

### 1. Clarity
- ✅ Questions are specific and unambiguous
- ✅ Clear success criteria
- ✅ Well-defined output format

### 2. Verifiability
- ✅ Answers can be verified through web search
- ✅ Ground truth is reliable and current
- ✅ Multiple sources available for verification

### 3. Appropriate Difficulty
- ✅ Not trivially easy (requires search)
- ✅ Not impossibly hard (has solution)
- ✅ Balanced difficulty distribution

### 4. Real-world Relevance
- ✅ Based on actual use cases
- ✅ Practical scenarios
- ✅ Common search patterns

### 5. Diversity
- ✅ Multiple categories
- ✅ Various difficulty levels
- ✅ Different reasoning types

## Difficulty Distribution

```
Easy:          5 tasks  (10%)  - Direct factual lookup
Medium:       37 tasks  (67%)  - Person/entity identification
Hard:          9 tasks  (16%)  - Complex reasoning
Very Hard:     4 tasks  (7%)   - Metric matching
```

## Expected Performance

### Pass@1 (Single Attempt)
- **Target Range:** 40-60%
- **GPT-4o:** ~55%
- **Claude-3.5-Sonnet:** ~50%
- **Gemini-2.0-Flash:** ~45%

### Pass@3 (Three Attempts)
- **Target Range:** 60-80%
- **GPT-4o:** ~75%
- **Claude-3.5-Sonnet:** ~70%

## Task Naming Convention

```
info_search_task_XXXX.json          # Standard search tasks (50)
multi-server_task_*_XXXX.json       # Multi-server tasks (5)
```

**Pattern:**
- Sequential numbering (0001-0050)
- Zero-padded (4 digits)
- Descriptive prefix

## MCP Servers Used

### Primary: google-search
- **Purpose:** Perform Google searches
- **Tools:** google-search
- **Required:** SERP_API_KEY

### Secondary: fetch
- **Purpose:** Retrieve specific URLs
- **Tools:** fetch-url
- **Required:** Built-in (no API key)

## Evaluation Method

### LLM-as-a-Judge

All tasks use the `google_search.llm_as_a_judge` evaluator:

**Process:**
1. Agent generates response
2. Evaluator constructs prompt with:
   - Original question
   - Agent's response
   - Correct answer
3. GPT-4 judges if response is correct
4. Returns pass/fail with reasoning

**Advantages:**
- ✅ Handles answer variations
- ✅ Understands context and phrasing
- ✅ More flexible than exact string match
- ✅ Can handle synonyms and reformulations

## Task Creation Guidelines

When adding new tasks to this domain:

### 1. Follow the Template

Use existing tasks as templates:

```json
{
    "category": "general",
    "question": "Clear, specific question",
    "output_format": {
        "answer": "[Your answer]"
    },
    "use_specified_server": true,
    "mcp_servers": [
        {"name": "google-search"},
        {"name": "fetch"}
    ],
    "evaluators": [
        {
            "func": "raw",
            "op": "google_search.llm_as_a_judge",
            "op_args": {
                "question": "Same as above",
                "correct_answer": "Verified answer"
            }
        }
    ]
}
```

### 2. Verify Ground Truth

Before adding a task:
- ✅ Verify the correct answer via multiple sources
- ✅ Ensure answer is current and accurate
- ✅ Check that answer can be found via Google search

### 3. Test the Task

```bash
# Test individual task
alignerr validate --domain web_search --tasks info_search_task_XXXX
```

### 4. Maintain Balance

Keep difficulty distribution balanced:
- 10% Easy (direct facts)
- 70% Medium (requires reasoning)
- 20% Hard (complex multi-step)

## Statistics

| Metric | Value |
|--------|-------|
| Total Tasks | 55 |
| Simple Search Tasks | 50 |
| Multi-Server Tasks | 5 |
| Average Task Size | 26 lines |
| Total Lines | ~1,430 lines |

## Quality Metrics

This domain meets all quality criteria:

✅ **Pass@k Range:** 10-80% (challenging but fair)  
✅ **Zero Score Rate:** <10% (tasks are solvable)  
✅ **Task Count:** 55 (good coverage)  
✅ **Diversity:** 5 categories  
✅ **Documentation:** Complete  

## Use as Reference

When creating new domains:

1. **Study task structure** - See how tasks are formatted
2. **Review config.yaml** - Understand benchmark configuration
3. **Examine evaluators** - Learn evaluation strategies
4. **Check README** - Follow documentation standards
5. **Analyze distribution** - Balance difficulty appropriately

---

**This is the gold standard for domain implementation!** 🏆

Use it as your guide for creating high-quality benchmark domains.

