# Contributing to LBX MCP Universe

Thank you for your interest in contributing! 🎉

This document provides guidelines for contributing new benchmark domains to the LBX MCP Universe.

## 📚 Getting Started

### New Contributors

If this is your first contribution:
1. 📖 **Read the [README](README.md)** - Complete step-by-step tutorial
2. 🏆 **Study [web_search domain](domains/web_search/)** - Reference implementation
3. 🚀 **Try [QUICKSTART](QUICKSTART.md)** - Fast track for experienced devs

### What We're Looking For

We welcome contributions of:
- ✅ **New benchmark domains** - Testing specific MCP server capabilities
- ✅ **Additional tasks** - Expanding existing domains
- ✅ **Improved evaluators** - Better evaluation functions
- ✅ **Documentation** - Clarifications and examples
- ✅ **Bug fixes** - Corrections to existing code

## 🎯 Contribution Process

### 1. Discuss Your Idea

Before investing time in a new domain:
1. Check [existing issues](https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template/issues) and [PRs](https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template/pulls)
2. Create an issue describing your proposed domain
3. Wait for maintainer feedback (usually within 48 hours)

**Why discuss first?**
- Avoid duplicate work
- Ensure domain fits the project
- Get guidance on implementation

### 3. Create Feature Branch

Follow the naming convention:

```bash
# For new domains
git checkout -b domains/{domain-name}/v1

# For bug fixes
git checkout -b fix/{issue-number}-short-description

# For documentation
git checkout -b docs/{topic}
```

### 4. Implement Your Contribution

**For new domains:**
- Create 5-6 high-quality, complex tasks that ideally use more than one MCP server.
- Follow the [web_search](domains/web_search/) structure

**Quality checklist:**
- [ ] All files follow naming conventions
- [ ] Tasks have clear, unambiguous questions
- [ ] Ground truth answers are verifiable
- [ ] Evaluators handle edge cases
- [ ] Documentation is complete
- [ ] No hardcoded secrets
- [ ] Local validation passes

### 5. Test Locally

**Before submitting PR:**

```bash
# Validate domain structure
uv run alignerr_mcp validate --domain your_domain

# Check pass rates
uv run alignerr_mcp validate --domain your_domain --runs 3

# Target metrics:
# - Pass@1: 30-70%
# - Pass@3: 50-85%
# - Zero score rate: <5%
```

### 6. Commit Your Changes

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: <type>: <description>
#
# Types: feat, fix, docs, refactor, test, chore

# Examples:
git commit -m "feat: Add email_automation domain with 50 tasks"
git commit -m "fix: Correct evaluation logic in web_search domain"
git commit -m "docs: Add troubleshooting section to README"
```

**Commit message guidelines:**
- Use imperative mood ("Add" not "Added")
- First line ≤ 50 characters
- Detailed description after blank line
- Reference issues: `Fixes #123`, `Relates to #456`

### 7. Push and Create PR

```bash
# Push branch
git push origin domains/your_domain/v1

# Create PR with GitHub CLI
gh pr create --title "Add your_domain" --body "Description..."

# Or use GitHub web UI
```

## 📝 Pull Request Guidelines

### PR Title

Follow conventional commits format:

```
feat: Add email_automation domain with 50 tasks
fix: Correct task_0003 in web_search domain
docs: Improve contributor onboarding guide
```

### PR Description

Use this template:

````markdown
## Summary
Brief description of what this PR adds/changes.

## Domain Details (for new domains)
- **Domain Name:** your_domain
- **Task Count:** 5-6+
- **MCP Servers:** server1, server2
- **Categories:** category1, category2, category3

## Task Breakdown
- Category 1: 20 tasks
- Category 2: 20 tasks
- Category 3: 15 tasks

## Local Validation Results
```
✅ Structure: PASS
✅ Config: PASS
✅ Tasks: PASS (5/5)
✅ Evaluators: PASS

Pass@1: 45%
Pass@3: 68%
Zero score: 2%
```

## Checklist
- [ ] 5-6+ tasks created
- [ ] All tasks follow naming convention
- [ ] Config file is valid
- [ ] Evaluators implemented and tested
- [ ] Documentation complete (README.md)
- [ ] Local validation passed
- [ ] No secrets committed
- [ ] Reviewed web_search reference
- [ ] Pass rates in acceptable range (30-70% for Pass@1)

## Additional Notes
Any special considerations, dependencies, or known issues.
````

## 🔍 Code Review Process

### What to Expect

1. **Automated CI** runs within minutes
   - Structure validation
   - Task execution
   - Performance metrics

2. **Maintainer review** within 2-3 business days
   - Code quality check
   - Task quality assessment
   - Documentation review

3. **Feedback and iteration**
   - Address reviewer comments
   - Make requested changes
   - Re-request review when ready

### Common Review Feedback

**Task Quality:**
- "Tasks are too easy (Pass@1 > 80%)"
- "Questions need to be more specific"
- "Add more diverse task categories"

**Evaluator Issues:**
- "Evaluator is too strict/lenient"
- "Add error handling for edge cases"
- "Use LLM-as-a-judge for flexibility"

**Documentation:**
- "Add usage examples"
- "Document required API keys"
- "Clarify task categories"

**Structure:**
- "Follow naming conventions"
- "Missing required files"
- "Config syntax errors"

## ✅ Acceptance Criteria

Your PR will be merged if:

### Technical Requirements
- ✅ All CI checks pass
- ✅ Structure validation succeeds
- ✅ No secrets detected
- ✅ Code follows existing patterns

### Quality Requirements
- ✅ 5-6+ high-quality tasks
- ✅ Pass@1 between 30-70%
- ✅ Pass@3 between 50-85%
- ✅ Zero score rate < 5%
- ✅ Clear evaluation criteria

### Documentation Requirements
- ✅ Complete README.md
- ✅ Usage examples included
- ✅ API requirements documented
- ✅ Expected results specified

### Community Standards
- ✅ Respectful communication
- ✅ Responsive to feedback
- ✅ Addresses review comments

## 🚫 What Not to Do

### Don't Submit

- ❌ Tasks with hardcoded secrets
- ❌ Incomplete documentation
- ❌ Copy-pasted tasks without customization
- ❌ Tasks with 100% or 0% pass rates
- ❌ Binary files (use `.gitignore`)

### Don't Commit

- ❌ API keys or tokens
- ❌ `.env` files
- ❌ Personal credentials
- ❌ Large binary files
- ❌ Generated files (`.venv/`, `__pycache__/`)
- ❌ Editor-specific files (`.vscode/`, `.idea/`)

## 🏆 Quality Standards

### Task Design

**Good task example:**
```json
{
    "category": "email_send",
    "question": "Send an email to john@example.com with subject 'Meeting Reminder' and body 'Our meeting is scheduled for tomorrow at 2 PM in Conference Room B.'",
    "output_format": {
        "status": "success/failure",
        "message_id": "[ID]"
    },
    "use_specified_server": true,
    "mcp_servers": [{"name": "email"}],
    "evaluators": [{
        "func": "raw",
        "op": "email_automation.check_email_sent",
        "op_args": {
            "recipient": "john@example.com",
            "subject": "Meeting Reminder"
        }
    }]
}
```

**What makes it good:**
- ✅ Clear, specific instructions
- ✅ Verifiable outcome
- ✅ Proper structure
- ✅ Appropriate evaluator

**Bad task example:**
```json
{
    "category": "general",
    "question": "Send email",
    "output_format": {"result": "done"},
    "evaluators": [{"op": "check_result"}]
}
```

**What's wrong:**
- ❌ Too vague ("Send email" - to whom? about what?)
- ❌ Missing MCP servers specification
- ❌ Incomplete evaluator configuration
- ❌ Non-verifiable outcome

### Evaluator Design

**Good evaluator:**
```python
@compare_func(name="email_automation.check_email_sent")
async def check_email_sent(llm_response, *args, **kwargs) -> Tuple[bool, str]:
    """Check if email was sent successfully."""
    _, values = args
    recipient = values.get('recipient')
    subject = values.get('subject')
    
    response_text = str(llm_response).lower()
    
    # Multiple success indicators
    success_indicators = ['success', 'sent', 'delivered', 'message sent']
    
    if any(indicator in response_text for indicator in success_indicators):
        # Verify recipient and subject if possible
        if recipient.lower() in response_text and subject.lower() in response_text:
            return True, f"Email sent to {recipient} with subject '{subject}'"
        return True, f"Email sent successfully"
    
    return False, f"Failed to send email"
```

**What makes it good:**
- ✅ Handles multiple success formats
- ✅ Verifies key details
- ✅ Clear return messages
- ✅ Error handling

### Documentation Standards

**Good README structure:**
```markdown
# Domain Name

Brief description (1-2 sentences)

## Overview
- Domain category
- Task count
- Required MCP servers
- Difficulty level

## Domain Structure
[Directory tree]

## Task Categories
Breakdown of task types with counts

## Required Services
### API Keys
- Which keys are needed
- Where to get them

### MCP Servers
- Which servers are required
- Installation instructions

## Usage
### Installation
[Step-by-step setup]

### Running Validation
[Command examples]

## Expected Results
- Pass@1 rate
- Pass@3 rate
- Average execution time

## Examples
[2-3 task examples with explanations]

## Troubleshooting
Common issues and solutions
```

## 🤝 Community Guidelines

### Be Respectful

- ✅ Welcome newcomers
- ✅ Provide constructive feedback
- ✅ Assume good intentions
- ✅ Be patient with questions

### Be Collaborative

- ✅ Help others with issues
- ✅ Review PRs when you can
- ✅ Share knowledge
- ✅ Celebrate contributions

### Be Professional

- ✅ Keep discussions on-topic
- ✅ Use inclusive language
- ✅ Respect different perspectives
- ✅ Follow Code of Conduct

## 📞 Getting Help

### Resources

- 📖 [README.md](README.md) - Complete tutorial
- 🚀 [QUICKSTART.md](QUICKSTART.md) - Fast track guide
- 🏆 [REFERENCE_EXAMPLE.md](REFERENCE_EXAMPLE.md) - Reference implementation
- 💬 **Discord Channel** - Join for real-time help and community support

### Support Channels

1. **Documentation** - Check guides first
2. **Discord Channel** - Ask questions, get real-time help, share ideas
3. **GitHub Issues** - Report bugs, request features
4. **PR Comments** - Ask for clarification on reviews

### When Asking for Help

Include:
- What you're trying to do
- What you've tried
- Full error messages
- Relevant code snippets
- Environment details (OS, Python version, etc.)

## 🎓 Learning Resources

### Understanding the Codebase

1. **Start with web_search domain**
   ```bash
   cd domains/web_search
   cat README.md
   cat config.yaml
   cat tasks/info_search_task_0001.json
   cat evaluators/functions.py
   ```

2. **Study the CLI**
   ```bash
   uv run alignerr_mcp --help
   uv run alignerr_mcp validate --help
   ```

3. **Read existing PRs**
   - See what was accepted
   - Learn from feedback
   - Understand patterns

### External Resources

- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit format
- [UV Documentation](https://github.com/astral-sh/uv) - Package manager

## 📊 Metrics and Goals

### Domain Quality Metrics

| Metric | Target   | Acceptable | Needs Work   |
|--------|--------  |------------|------------  |
| Pass@1 | 40-60%   | 30-70%     | <30% or >70% |
| Pass@3 | 60-80%   | 50-85%     | <50% or >85% |
| Zero score | 0%   | <5%        | >5%          |
| Task count | 5-6+ | 4          | <4           |

### Review Turnaround

- Initial CI feedback: < 5 minutes
- Maintainer review: 2-3 business days
- Follow-up reviews: 1-2 business days

## 🎉 After Your PR is Merged

### What Happens Next

1. **Auto-sync to mothership**
   - Your domain is automatically synced to the main repository
   - Becomes available in the central benchmark suite

2. **Recognition**
   - Added to contributors list
   - Credited in release notes
   - Featured in community updates

3. **Maintenance**
   - You're invited to maintain your domain
   - Notified of issues related to your domain
   - Can submit updates and improvements

### Future Contributions

- Add more tasks to your domain
- Improve existing evaluators
- Help others with reviews
- Create new domains
- Contribute to CLI tools

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## ❓ Questions?

- 💬 **Join Discord** - Ask in the project-specific channel for real-time help
- 🐛 [Report an Issue](https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template/issues/new) - For bugs and feature requests
- 📧 Contact maintainers (see README)

---

**Thank you for contributing to LBX MCP Universe!** 🙏

Your contributions help build better AI agent benchmarks and advance the field. We appreciate your time and effort! 🚀

