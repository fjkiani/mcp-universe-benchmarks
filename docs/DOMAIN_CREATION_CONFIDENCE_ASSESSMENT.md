# Domain Creation Confidence Assessment

**Date:** 2025-01-XX  
**Purpose:** Complete assessment of confidence level and all moving pieces for creating a new domain

---

## Confidence Level: **HIGH (85-90%)**

### Why High Confidence?

✅ **Complete Code Understanding:**
- Domain loading mechanism fully traced
- Task execution flow completely mapped
- Evaluator registration system understood
- MCP server integration documented
- Error handling patterns identified

✅ **Reference Implementation Available:**
- `web_search` domain is production-ready reference
- `gitlab_mlops` shows structured validation pattern
- `identity_service` demonstrates zero-API pattern
- Multiple working examples to study

✅ **CLI Tools Available:**
- `create-domain` command scaffolds structure
- `validate` command tests locally
- `servers install` manages dependencies
- `env setup` configures API keys

✅ **Documentation Complete:**
- Step-by-step guides available
- Code trace analysis completed
- Execution flow diagrammed
- Integration points validated

### Remaining Uncertainties (10-15%)

⚠️ **Edge Cases:**
- Complex multi-server orchestration scenarios
- Advanced evaluator patterns not yet seen
- Error recovery in production runs
- Performance optimization for large task sets

⚠️ **CI/CD Specifics:**
- Exact CI workflow behavior
- Report generation details
- Secret management in CI
- Mothership sync process

---

## All Moving Pieces for New Domain Creation

### Phase 1: Setup & Discovery (5-10 minutes)

#### 1.1 Environment Setup
```bash
# Prerequisites
- Python 3.10+ installed
- UV package manager installed
- Git configured
- GitHub access (for PRs)

# Commands
git clone --recurse-submodules <repo-url>
cd lbx_mcp_universe_template
uv sync
```

**Components:**
- **Virtual Environment:** `.venv/` created by UV
- **CLI Submodule:** `lbx_mcp_universe_cli/` (git submodule)
- **MCP Servers Submodule:** `lbx_mcp_universe_mcp_servers_mothership/` (git submodule)
- **Dependencies:** Installed via `uv sync` from `pyproject.toml`

**Verification:**
```bash
uv run alignerr_mcp list  # Should show existing domains
uv run alignerr_mcp env status  # Check environment
```

---

### Phase 2: Domain Structure Creation (5 minutes)

#### 2.1 Create Domain Scaffold
```bash
uv run alignerr_mcp create-domain --name my_domain
```

**What This Creates:**
```
domains/my_domain/
├── config.yaml              # Benchmark configuration template
├── tasks/                   # Empty directory
│   └── task_0001.json      # Example task template
├── evaluators/              # Evaluation functions
│   ├── __init__.py          # Package marker
│   └── functions.py         # Template with example evaluator
└── README.md                # Domain documentation template
```

**Components Created:**
- **config.yaml:** YAML with LLM, agent, benchmark sections
- **tasks/:** Directory for task JSON files
- **evaluators/:** Python package for evaluation functions
- **README.md:** Documentation template

**Code Reference:** `lbx_cli/commands/create.py:141-219`

---

### Phase 3: Domain Implementation (1-2 weeks)

#### 3.1 Configure Benchmark (config.yaml)

**Required Sections:**
```yaml
# LLM Configuration
kind: llm
spec:
  name: llm-1
  type: litellm
  config:
    model_name: openai/gpt-4o

# Agent Configuration
kind: agent
spec:
  name: my-domain-agent
  type: react
  config:
    llm: llm-1
    max_iterations: 20
    system_prompt: |
      You are an agent for [domain description]...

# Benchmark Configuration
kind: benchmark
spec:
  description: "[Domain description]"
  agent: my-domain-agent
  tasks:
    - tasks/task_0001.json
    - tasks/task_0002.json
    # ... list all task files
```

**Key Decisions:**
- **LLM provider:** LiteLLM-compatible gateway or direct provider config in `config.yaml`
- **Agent Type:** `react` (reasoning), `basic` (simple), `function-call` (structured)
- **Max Iterations:** 20-30 for complex tasks, 10-15 for simple
- **Task List:** Must match actual task files in `tasks/` directory

**Code Reference:** `lbx_cli/core/domain.py:51-89` (DomainConfig.from_yaml)

---

#### 3.2 Create Task Files (tasks/*.json)

**Task Structure:**
```json
{
  "category": "general",
  "question": "Clear, unambiguous task question...",
  "output_format": {
    "field1": "expected_type",
    "field2": "expected_type"
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "server-name-1"},
    {"name": "server-name-2"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "domain_name.evaluator_function",
      "op_args": {
        "param1": "value1"
      }
    }
  ]
}
```

**Required Fields:**
- `question` (string): Task prompt
- `output_format` (dict): Expected response structure
- `mcp_servers` (array): Required MCP servers
- `evaluators` (array): Evaluation criteria

**Optional Fields:**
- `category` (string): Task category
- `use_specified_server` (bool): Restrict to specified servers

**Naming Convention:**
- Pattern: `{category}_task_{number}.json`
- Example: `info_search_task_0001.json`
- Sequential numbering: `0001`, `0002`, etc.

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/task.py:60-84` (TaskConfig)

**Best Practices:**
- Clear, unambiguous questions
- Verifiable answers (ground truth)
- Appropriate difficulty (target 40-60% pass rate)
- Consistent structure across tasks
- Proper MCP server specification

---

#### 3.3 Implement Evaluators (evaluators/functions.py)

**Evaluator Function Pattern:**
```python
from lbx_cli.mcpuniverse.evaluator.functions import compare_func
from typing import Tuple, Any

@compare_func(name="domain_name.function_name")
async def evaluate_function(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Evaluate agent response.
    
    Args:
        llm_response: Agent response (may be Pydantic FunctionResult)
        *args: Positional arguments from op_args
        **kwargs: Keyword arguments (includes context)
    
    Returns:
        (bool, str): (passed, error_message)
    """
    # Parse response
    # Validate structure
    # Check business logic
    return (True, "") or (False, "error message")
```

**Registration:**
- Functions registered when module loaded via `importlib`
- Must be loaded before task execution (during BenchmarkRunner init)
- Registered in `COMPARISON_FUNCTIONS` dict

**Code Reference:**
- Registration: `lbx_cli/mcpuniverse/evaluator/functions.py:42-59`
- Loading: `lbx_cli/mcpuniverse/benchmark/runner.py:289-313`
- Usage: `lbx_cli/mcpuniverse/evaluator/evaluator.py:112-151`

**Common Patterns:**

**Pattern 1: LLM-as-a-Judge (web_search)**
```python
@compare_func(name="web_search.llm_as_a_judge")
async def llm_as_a_judge(llm_response, *args, **kwargs):
    question = kwargs['op_args']['question']
    correct_answer = kwargs['op_args']['correct_answer']
    # Use LLM to judge if response matches answer
    # Handles variations in phrasing
```

**Pattern 2: Structured Validation (gitlab_mlops)**
```python
@compare_func(name="gitlab_mlops.validate_project_creation")
async def validate_project_creation(llm_response, *args, **kwargs):
    # Parse JSON from response
    # Check required fields
    # Validate field types
    # Check business logic
    # Return (True, "") or (False, "[ERROR_TYPE] message")
```

**Pattern 3: Exact Match**
```python
@compare_func(name="domain.exact_match")
async def exact_match(llm_response, *args, **kwargs):
    expected = kwargs['op_args']['expected']
    actual = extract_answer(llm_response)
    return (actual == expected, "")
```

---

#### 3.4 Write Documentation (README.md)

**Required Sections:**
- Overview (domain purpose)
- Task Categories
- MCP Servers Required
- API Keys Needed
- Usage Examples
- Expected Results

**Code Reference:** Study `domains/web_search/README.md` as template

---

### Phase 4: MCP Server Setup (10-30 minutes)

#### 4.1 Identify Required Servers

**From Task Analysis:**
- Review all task JSON files
- List unique `mcp_servers` entries
- Check server availability

**Server Discovery:**
```bash
uv run alignerr_mcp servers list
uv run alignerr_mcp servers capabilities
```

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:315-394` (_discover_mcp_servers)

---

#### 4.2 Install Servers

```bash
# Install individual servers
uv run alignerr_mcp servers install server_name

# Example
uv run alignerr_mcp servers install google_search
uv run alignerr_mcp servers install email
```

**What Happens:**
- Server installed from `lbx_mcp_universe_mcp_servers_mothership/servers/`
- Registered in MCPManager config
- Available for agent tool calls

**Code Reference:** CLI server management in `lbx_cli/commands/servers.py`

---

#### 4.3 Configure API Keys

**Interactive Setup:**
```bash
uv run alignerr_mcp env setup
```

**Manual Setup (.env file):**
```bash
# Create .env file in project root
SERP_API_KEY=your_key_here
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
# ... other keys
```

**Code Reference:** `lbx_cli/commands/env.py`

**Verification:**
```bash
uv run alignerr_mcp env status
```

---

### Phase 5: Local Validation (30-60 minutes)

#### 5.1 Structure Validation

```bash
uv run alignerr_mcp validate --domain my_domain
```

**What This Checks:**
- `config.yaml` exists and is valid
- `tasks/` directory exists
- Task files are valid JSON
- Evaluator functions are registered
- Task paths in config.yaml match actual files

**Code Reference:** `lbx_cli/core/domain.py:131-151` (validate_structure)

---

#### 5.2 Functional Testing

**Run Single Task:**
```bash
# Not directly supported, but can validate entire domain
uv run alignerr_mcp validate --domain my_domain --tasks task_0001
```

**Run All Tasks:**
```bash
uv run alignerr_mcp validate --domain my_domain
```

**What Happens:**
1. Domain loaded and validated
2. BenchmarkRunner initialized
3. Evaluators loaded
4. MCP servers discovered
5. Each task executed:
   - Agent initialized with specified servers
   - Question sent to agent
   - Agent makes tool calls
   - Response collected
   - Evaluators run
   - Results aggregated
6. Report generated

**Code Reference:** Full flow in `docs/EXECUTION_FLOW_DIAGRAM.md`

---

#### 5.3 Pass@k Validation (Quality Check)

```bash
# Run 3 times with same model
uv run alignerr_mcp validate --domain my_domain --runs 3

# Run with multiple models
uv run alignerr_mcp validate --domain my_domain \
  --runs 3 \
  --models openai/gpt-4o,anthropic/claude-sonnet-4-5
```

**Target Metrics:**
- **Pass@1:** 30-70% (challenging but solvable)
- **Pass@3:** 40-80% (reasonable improvement)
- **Evaluation Errors:** < 5%
- **Consistency:** Same tasks fail reliably

**Code Reference:** `lbx_cli/core/runner.py:200-319` (ValidationRunner)

---

### Phase 6: Git Workflow (10 minutes)

#### 6.1 Create Feature Branch

```bash
git checkout -b domains/my_domain/v1
```

**Naming Convention:**
- Pattern: `domains/{domain_name}/v{version}`
- Example: `domains/email_automation/v1`

---

#### 6.2 Commit Changes

```bash
# Add domain files
git add domains/my_domain/

# Commit with conventional format
git commit -m "feat: Add my_domain domain with 50 tasks"
```

**Conventional Commits:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring

---

#### 6.3 Push and Create PR

```bash
# Push branch
git push origin domains/my_domain/v1

# Create PR
gh pr create --title "Add my_domain domain" --body "..."
```

**PR Template Should Include:**
- Domain description
- Number of tasks
- MCP servers used
- Expected pass rate
- Local validation results

---

### Phase 7: CI/CD Validation (30-60 minutes)

#### 7.1 Automatic Checks

**On PR Creation:**
1. **Structure Validation** (2-5 min)
   - Validates file structure
   - Checks config.yaml format
   - Verifies task files

2. **Full Evaluation** (30-60 min)
   - Runs all tasks
   - Generates HTML report
   - Posts results to PR

**Code Reference:** `.github/workflows/ci.yml`

---

#### 7.2 Review Results

**Check PR Comments:**
- Bot posts evaluation results
- HTML report link provided
- Pass rates shown
- Error summary included

**Acceptable Results:**
- Pass@1: 30-70%
- Evaluation errors: < 5%
- All tasks execute successfully
- Consistent failure patterns

---

### Phase 8: Merge & Sync (Automatic)

**On PR Merge:**
1. Domain synced to mothership
2. CLI submodule updated
3. Domain available in central repo

**Code Reference:** `.github/workflows/sync-to-mother.yml`

---

## Complete Checklist for New Domain

### Pre-Development
- [ ] Read GETTING_STARTED.md
- [ ] Study web_search reference domain
- [ ] Understand MCP server capabilities
- [ ] Review REFERENCE_EXAMPLE.md

### Setup
- [ ] Clone repository with submodules
- [ ] Run `uv sync`
- [ ] Verify CLI works: `uv run alignerr_mcp list`
- [ ] Explore existing domains

### Domain Creation
- [ ] Run `create-domain --name my_domain`
- [ ] Review generated structure
- [ ] Plan task categories (3-5 categories)
- [ ] Identify required MCP servers

### Implementation
- [ ] Configure `config.yaml` (LLM, agent, benchmark)
- [ ] Create 50+ task JSON files
- [ ] Implement evaluator functions
- [ ] Write domain README.md
- [ ] Update config.yaml task list

### MCP Server Setup
- [ ] List available servers: `servers list`
- [ ] Install required servers: `servers install`
- [ ] Configure API keys: `env setup`
- [ ] Verify server status: `env status`

### Validation
- [ ] Structure validation: `validate --domain my_domain`
- [ ] Fix any structure issues
- [ ] Run full validation
- [ ] Check pass rates (target: 30-70%)
- [ ] Run Pass@k validation (3 runs)
- [ ] Review evaluation errors
- [ ] Test reproducibility

### Submission
- [ ] Create feature branch: `domains/my_domain/v1`
- [ ] Commit changes with conventional format
- [ ] Push branch
- [ ] Create PR with description
- [ ] Monitor CI/CD results
- [ ] Address any CI failures
- [ ] Respond to review feedback

---

## Critical Dependencies

### Required Components

1. **CLI Submodule** (`lbx_mcp_universe_cli/`)
   - Must be initialized: `git submodule update --init --recursive`
   - Contains domain management, validation, execution
   - Installed in editable mode via UV

2. **MCP Servers Submodule** (`lbx_mcp_universe_mcp_servers_mothership/`)
   - Must be initialized
   - Contains 25+ MCP servers
   - Auto-discovered by BenchmarkRunner

3. **Python Environment**
   - Python 3.10+
   - UV package manager
   - Virtual environment (`.venv/`)

4. **API Keys** (if using external APIs)
   - Configured via `.env` file
   - Or via `env setup` command
   - Never committed to git

### Optional Components

- **LLM API Keys:** For evaluation (if using LLM-as-a-judge)
- **External Services:** Depends on domain requirements
- **CI/CD Secrets:** For automated testing (organization-level)

---

## Common Pitfalls & Solutions

### Pitfall 1: Tasks Not Executed

**Symptom:** Domain validates but no tasks run

**Cause:** Tasks listed in `config.yaml` don't match files in `tasks/` directory

**Solution:**
- Ensure all task files listed in `config.yaml` `benchmark.tasks` array
- Verify file paths are relative to domain directory
- Check file names match exactly

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:467-489`

---

### Pitfall 2: Evaluator Not Found

**Symptom:** `AssertionError: Unknown comparison op: domain.func`

**Cause:** Evaluator function not loaded or name mismatch

**Solution:**
- Ensure `evaluators/functions.py` exists
- Verify `@compare_func(name="domain.func")` matches task `op`
- Check BenchmarkRunner initialized with `base_dir=domain_path`
- Verify module loads without syntax errors

**Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:79-80`

---

### Pitfall 3: MCP Server Not Found

**Symptom:** Runtime error when agent tries to use server

**Cause:** Server not installed or name mismatch

**Solution:**
- Install server: `servers install server_name`
- Check server name conversion (underscore ↔ hyphen)
- Verify server has `__main__.py` in mothership
- Check server discovery logs

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:315-394`

---

### Pitfall 4: Task Path Resolution Error

**Symptom:** `FileNotFoundError: Task file not found`

**Cause:** Task path in `config.yaml` doesn't resolve correctly

**Solution:**
- Use relative paths: `tasks/task_0001.json`
- Ensure `base_dir` set to domain path
- Verify file exists in domain directory
- Check path separators (use `/` not `\`)

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:467-489`

---

### Pitfall 5: High Pass Rate (>85%)

**Symptom:** All or most tasks pass

**Cause:** Tasks too easy or trivial

**Solution:**
- Increase task complexity
- Add multi-step reasoning
- Require multiple tool calls
- Add edge cases
- Test with weaker models

**Target:** 30-70% Pass@1 rate

---

### Pitfall 6: Low Pass Rate (<10%)

**Symptom:** Almost no tasks pass

**Cause:** Tasks too difficult or broken

**Solution:**
- Simplify task requirements
- Provide clearer instructions
- Check evaluator logic (may be too strict)
- Verify MCP servers work correctly
- Test with stronger models

**Target:** 30-70% Pass@1 rate

---

## Documentation Recovery

### Documentation Files Status

**Core Documentation (10 files):**
1. ✅ GETTING_STARTED.md - Present
2. ✅ README.md - Present
3. ❓ QUICKSTART.md - Not found in root (check lbx_mcp_universe_cli/)
4. ✅ STRUCTURE_GUIDE.md - Present
5. ✅ MCP_SERVERS_GUIDE.md - Present
6. ✅ WORKFLOW.md - Present
7. ✅ CONTRIBUTING.md - Present
8. ✅ REFERENCE_EXAMPLE.md - Present
9. ✅ SETUP_NOTES.md - Present
10. ✅ UV_SETUP.md - Present
11. ✅ README_UV_SYNC.md - Present

**Additional Documentation:**
- ✅ DOCUMENTATION_INDEX.md - Present
- ✅ DOCUMENTATION_STRUCTURE.md - Present
- ✅ DOMAIN_REPO_WORKFLOW.md - Present
- ✅ TESTING_GUIDE.md - Present

**New Analysis Documents:**
- ✅ docs/CODE_TRACE_ANALYSIS.md - Created
- ✅ docs/EXECUTION_FLOW_DIAGRAM.md - Created
- ✅ docs/INTEGRATION_TEST_CHECKLIST.md - Created
- ✅ docs/DOMAIN_CREATION_CONFIDENCE_ASSESSMENT.md - This file

**Total:** 15+ documentation files available

---

## Confidence Breakdown by Component

### Domain Structure (95% Confidence)
- ✅ File structure understood
- ✅ config.yaml format known
- ✅ Task JSON format documented
- ✅ Evaluator pattern clear
- ⚠️ Advanced patterns may exist

### Task Execution (90% Confidence)
- ✅ Execution flow mapped
- ✅ Agent initialization understood
- ✅ MCP server integration clear
- ✅ Evaluation process documented
- ⚠️ Edge cases in error handling

### MCP Server Integration (85% Confidence)
- ✅ Server discovery mechanism known
- ✅ Server installation process clear
- ✅ Name conversion understood
- ⚠️ Complex server configurations
- ⚠️ Server error handling

### Evaluator System (90% Confidence)
- ✅ Registration mechanism understood
- ✅ Function patterns documented
- ✅ Common patterns identified
- ⚠️ Advanced evaluation strategies

### CI/CD Integration (75% Confidence)
- ✅ Workflow files present
- ✅ Basic structure understood
- ⚠️ Exact CI behavior
- ⚠️ Report generation details
- ⚠️ Secret management

---

## Recommended Approach for New Domain

### Step-by-Step with Confidence Levels

1. **Setup Environment** (100% confidence)
   - Follow README.md steps 1-2
   - Verified working process

2. **Study Reference** (100% confidence)
   - Review web_search domain
   - Study task examples
   - Review evaluator patterns

3. **Create Domain Scaffold** (100% confidence)
   - Use `create-domain` command
   - Verified working

4. **Implement Tasks** (90% confidence)
   - Follow task JSON format
   - Use web_search as template
   - Test incrementally

5. **Implement Evaluators** (90% confidence)
   - Follow documented patterns
   - Test registration
   - Verify function names

6. **Configure MCP Servers** (85% confidence)
   - Install required servers
   - Configure API keys
   - Test server availability

7. **Local Validation** (90% confidence)
   - Run validation commands
   - Check pass rates
   - Fix issues iteratively

8. **Submit PR** (100% confidence)
   - Follow git workflow
   - Monitor CI results
   - Address feedback

---

## Risk Assessment

### Low Risk Areas (High Confidence)
- ✅ Domain structure creation
- ✅ Task file format
- ✅ Basic evaluator implementation
- ✅ Local validation process
- ✅ Git workflow

### Medium Risk Areas (Moderate Confidence)
- ⚠️ Complex evaluator patterns
- ⚠️ Multi-server orchestration
- ⚠️ Advanced task design
- ⚠️ CI/CD specifics

### High Risk Areas (Lower Confidence)
- ⚠️ Performance optimization
- ⚠️ Edge case handling
- ⚠️ Production deployment
- ⚠️ Advanced error recovery

---

## Success Criteria

### Domain is Ready When:

✅ **Structure:**
- All required files present
- config.yaml valid
- Tasks load successfully
- Evaluators register correctly

✅ **Functionality:**
- All tasks execute without errors
- Evaluators return correct results
- MCP servers work as expected
- Pass rates in target range (30-70%)

✅ **Quality:**
- Documentation complete
- Code follows patterns
- Tasks are challenging but solvable
- Results are reproducible

✅ **CI/CD:**
- Structure validation passes
- Full evaluation completes
- Pass rates acceptable
- No critical errors

---

## Next Steps for Implementation

1. **Choose Domain Topic**
   - Identify problem domain
   - Research required MCP servers
   - Plan task categories

2. **Create Scaffold**
   - Run `create-domain` command
   - Review generated structure

3. **Implement Incrementally**
   - Start with 5-10 tasks
   - Test evaluators
   - Validate early
   - Expand to 50+ tasks

4. **Iterate on Quality**
   - Adjust task difficulty
   - Refine evaluators
   - Improve documentation
   - Test with multiple models

5. **Submit When Ready**
   - All validation passes
   - Pass rates acceptable
   - Documentation complete
   - Ready for review

---

**End of Confidence Assessment**






