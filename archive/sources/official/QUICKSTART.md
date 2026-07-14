# Quick Start Guide

**TL;DR for experienced developers.** New to this? Read the [full README](README.md) instead.

## 5-Minute Setup

```bash
# 1. Clone with submodules
git clone --recurse-submodules git@github.com:YOUR_USERNAME/lbx_mcp_universe_template.git
cd lbx_mcp_universe_template

# 2. Install dependencies
uv sync

# 3. Verify installation
uv run alignerr_mcp list
```

## Create Domain (Fast Track)

```bash
# 1. Create domain structure
uv run alignerr_mcp create-domain --name your_domain

# 2. Create 50+ task files in domains/your_domain/tasks/
# Follow the pattern in domains/web_search/tasks/

# 3. Update config.yaml
# - Set LLM and agent configuration
# - List all task files

# 4. Implement evaluators/functions.py
# Use @compare_func decorator

# 5. Write README.md
# Document domain, tasks, and requirements
```

## Discover MCP Servers

```bash
# List all available MCP servers and capabilities
uv run alignerr_mcp servers capabilities

# Get info on specific server
uv run alignerr_mcp servers info google_search --capabilities

# Install required servers
uv run alignerr_mcp servers install google_search

# Configure API keys
uv run alignerr_mcp env setup
```

## Validate & Submit

```bash
# Validate locally
uv run alignerr_mcp validate --domain your_domain

# Create PR
git checkout -b domains/your_domain/v1
git add domains/your_domain/
git commit -m "feat: Add your_domain with 50 tasks"
git push origin domains/your_domain/v1
gh pr create --title "Add your_domain"
```

## CI Results

After submitting PR:
1. Wait for CI validation (2-5 min)
2. Full evaluation runs (30-60 min)
3. Bot posts results with HTML report link
4. Review metrics: Pass@1 (30-70% ideal), Pass@3 (50-85% ideal)

## Key Files

```
domains/your_domain/
├── config.yaml              # Benchmark config
├── tasks/*.json             # 50+ task files
├── evaluators/functions.py  # Evaluation logic
└── README.md                # Documentation
```

## Task Template

```json
{
    "category": "general",
    "question": "Your clear, specific question here",
    "output_format": {"answer": "[Your answer]"},
    "use_specified_server": true,
    "mcp_servers": [{"name": "server-name"}],
    "evaluators": [{
        "func": "raw",
        "op": "domain_name.evaluator_function",
        "op_args": {
            "question": "Same question",
            "correct_answer": "Expected answer"
        }
    }]
}
```

## Evaluator Template

```python
from mcpuniverse.evaluation.decorators import compare_func
from typing import Tuple

@compare_func(name="your_domain.evaluator_name")
async def evaluator_name(llm_response, *args, **kwargs) -> Tuple[bool, str]:
    _, values = args
    question = values['question']
    correct_answer = values['correct_answer']
    
    # Your evaluation logic here
    # Return (passed: bool, reason: str)
    
    return True, "Reason for pass/fail"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Command not found | Use `uv run alignerr_mcp ...` |
| Empty submodules | `git submodule update --init --recursive` |
| Import errors | Check function names match in `@compare_func` and task `op` |
| CI secrets fail | Never commit API keys; use env vars |
| Pass rate wrong | Target: Pass@1 30-70%, Pass@3 50-85% |

## Need Help?

- 📖 [Full Tutorial](README.md) - Complete step-by-step guide
- 🏆 [Reference Example](REFERENCE_EXAMPLE.md) - Deep dive into web_search
- 🔌 [MCP Servers Guide](MCP_SERVERS_GUIDE.md) - Server capabilities and API setup
- 💬 **Discord Channel** - Ask questions and get real-time support

## Pro Tips

1. **Study web_search first** - It's your best guide
2. **Test locally before PR** - Save CI time
3. **Use LLM-as-a-judge** - More flexible than exact match
4. **Start with 10 tasks** - Expand after approval
5. **Name tasks consistently** - `{category}_task_{number}.json`
6. **Document everything** - Future you will thank you
7. **Zero-pad task numbers** - `0001` not `1`
8. **Validate JSON** - Use `jq` or online validators
9. **No secrets ever** - Use `.env` and git-ignore them
10. **Read bot comments** - They contain HTML report links

---

**Ready?** Create your domain and submit a PR! 🚀

