# Web Search Domain - Reference Implementation

**Status:** ✅ Reference-Grade Example

Note that the tasks here are very simple, real tasks should have additional complexity.
It demonstrates best practices for structure, task design, evaluation, and documentation.

## Overview

The Web Search domain tests an AI agent's ability to perform web searches and retrieve accurate information using Google Search and Fetch MCP servers.

**Category:** Information & Search  
**Total Tasks:** 50  
**MCP Servers:** google-search, fetch  
**Difficulty:** Medium  

## Domain Structure

```
web_search/
├── config.yaml              # Benchmark configuration
├── tasks/                   # 50 task definition files
│   ├── info_search_task_0001.json
│   ├── info_search_task_0002.json
│   ├── ... (48 more tasks)
│   └── info_search_task_0050.json
├── evaluators/              # Evaluation functions
│   ├── __init__.py
│   └── functions.py
└── README.md                # This file
```

## Task Examples

### Simple Information Search

**Task:** Find a person based on career statistics
```json
{
    "category": "general",
    "question": "I'm looking for someone based on the clues below: 
                 - Score 16 goals in 2024-25 season
                 - Score 1 goal in UEFA Champions League 2024-25 season...",
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
                "correct_answer": "Ollie Watkins"
            }
        }
    ]
}
```

## Configuration

### LLM Configuration

Uses LiteLLM for flexible model support:

```yaml
kind: llm
spec:
  name: llm-1
  type: litellm
  config:
    model_name: openai/gpt-4.1
```

### Agent Configuration

Uses ReAct agent optimized for web search:

```yaml
kind: agent
spec:
  name: ReAct-agent
  type: react
  config:
    llm: llm-1
    instruction: You are an agent for web searching...
    max_iterations: 20
    summarize_tool_response: false
```

### Task Configuration

**Total Tasks:** 50
- 50 information search tasks (info_search_task_0001 to _0050)

Each task tests different aspects of web search:
- Factual information retrieval
- Historical data lookup
- Current events
- Statistical information
- Multi-step reasoning

## Evaluation Strategy

### LLM-as-a-Judge

Uses custom evaluator function that employs an LLM to judge response quality:

```python
def llm_as_a_judge(question, correct_answer, agent_response, **kwargs):
    """
    Evaluate agent response using LLM-based judgment.
    
    Uses an LLM to determine if the agent's response matches
    the expected answer, accounting for variations in phrasing.
    """
```

**Benefits:**
- ✅ Handles answer variations
- ✅ Understands context
- ✅ More flexible than exact match
- ✅ Better for open-ended questions

## Required Services

### API Keys

- **SERP_API_KEY** - For Google search functionality
  - Get it at: https://serpapi.com/
  - Required for: google-search MCP server

### MCP Servers

- **google-search** - Google search capabilities
- **fetch** - URL fetching and content retrieval

Install with:
```bash
alignerr servers install google_search
# fetch is typically a built-in MCP server
```

## Usage

### Validate This Domain

```bash
# Basic validation
alignerr validate --domain web_search

# With specific model
alignerr validate --domain web_search --model openai/gpt-4o

# Pass@k validation (quality assurance)
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5
```

### Expected Results

**Pass@3 Rate:** 40-60% (challenging but solvable)  
**Average Score:** 50-70%  
**Execution Time:** ~30-60 seconds per task  

## Task Design Principles

This domain demonstrates excellent task design:

### 1. Clear Questions
Each task has a specific, unambiguous question.

### 2. Verifiable Answers
All answers can be verified through web search.

### 3. Appropriate Difficulty
- Not too easy (>80% pass rate)
- Not too hard (<10% pass rate)
- Requires actual search and reasoning

### 4. Diverse Topics
Tasks cover various domains:
- Sports statistics
- Historical facts
- Current events
- Scientific information
- Entertainment data

### 5. Proper Evaluation
Uses LLM-as-a-judge for flexible answer matching.

## Best Practices Demonstrated

### ✅ Task Files
- Consistent naming convention (info_search_task_XXXX.json)
- Clear category labels
- Structured output format
- Proper MCP server specification
- Well-defined evaluators

### ✅ Configuration
- Clean YAML structure
- Sensible agent parameters
- Flexible LLM configuration
- Complete task references

### ✅ Evaluators
- Domain-specific evaluation functions
- LLM-based judgment for flexibility
- Clear pass/fail criteria
- Handles answer variations

### ✅ Documentation
- Comprehensive README
- Usage examples
- API key requirements
- Expected results

## File Statistics

```
web_search/
├── config.yaml          (80 lines)
├── tasks/               (50 files, ~1,300 lines total)
└── evaluators/          (2 files)
    ├── __init__.py
    └── functions.py
```

## Testing

### Run Single Task

```bash
# Using alignerr (when it supports individual tasks)
alignerr validate --domain web_search --tasks info_search_task_0001
```

### Run Full Domain

```bash
alignerr validate --domain web_search
```

### Quality Validation

```bash
# Ensure pass@k is in acceptable range (10-80%)
alignerr validate --domain web_search \
  --runs 3 \
  --models openai/gpt-5,anthropic/claude-sonnet-4-5
```

## Extending This Example

### Add More Tasks

1. Create new JSON file in `tasks/`
2. Follow the same structure as existing tasks
3. Update `config.yaml` to reference new task
4. Test the new task

### Modify Evaluation

Edit `evaluators/functions.py` to add custom evaluation logic.

### Change Agent Type

Modify `config.yaml` to use different agent:
- `basic` - Simple LLM agent
- `function-call` - Function calling agent
- `react` - Reasoning and acting agent (current)
- `reflection` - Self-reflective agent

## Why This Is a Reference Example

✅ **Complete** - All components present and working  
✅ **Well-documented** - Clear README and comments  
✅ **Proper Scale** - 50 tasks (good coverage)  
✅ **Best Practices** - Follows all guidelines  
✅ **Real-world** - Practical use case  
✅ **Tested** - Known to work well  
✅ **Flexible** - LLM-as-a-judge evaluation  
✅ **Maintainable** - Clean structure  

## Use This Template For

When creating new domains, use this as your template for:
- Directory structure
- Config file format
- Task file format
- Evaluator implementation
- Documentation style
- Naming conventions

## Support

For questions about this reference implementation:
- Study the task files in `tasks/`
- Review `evaluators/functions.py`
- Check `config.yaml` structure
- See main README for general guidelines

---

**This is the gold standard for domain implementation!** 🏆

Use it as a reference when creating your own domains.

---

*Last updated: 2025-10-13*

