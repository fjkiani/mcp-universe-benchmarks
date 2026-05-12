# All Moving Pieces - Complete Domain Creation Guide

**Purpose:** Comprehensive reference of every component, step, and dependency for creating a new domain

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DOMAIN CREATION SYSTEM                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   CLI Tools  │──────│   Domains    │──────│ MCP Servers  │
│  (Submodule) │      │  (Your Work) │      │  (Submodule) │
└──────────────┘      └──────────────┘      └──────────────┘
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  BenchmarkRunner  │
                    │   (Execution)     │
                    └──────────────────┘
```

---

## Component Inventory

### 1. CLI Tools (`lbx_mcp_universe_cli/`)

**Location:** Git submodule  
**Purpose:** Domain management, validation, execution

**Key Commands:**
- `alignerr_mcp list` - List all domains
- `alignerr_mcp info --domain NAME` - Domain information
- `alignerr_mcp create-domain --name NAME` - Create domain scaffold
- `alignerr_mcp validate --domain NAME` - Validate domain
- `alignerr_mcp servers list` - List MCP servers
- `alignerr_mcp servers install NAME` - Install server
- `alignerr_mcp env setup` - Configure API keys
- `alignerr_mcp env status` - Check environment

**Key Modules:**
- `lbx_cli/core/domain.py` - Domain discovery and loading
- `lbx_cli/core/runner.py` - Benchmark execution wrapper
- `lbx_cli/commands/validate.py` - Validation command
- `lbx_cli/commands/create.py` - Domain creation
- `lbx_cli/mcpuniverse/benchmark/runner.py` - Core execution
- `lbx_cli/mcpuniverse/benchmark/task.py` - Task handling
- `lbx_cli/mcpuniverse/evaluator/` - Evaluation system
- `lbx_cli/mcpuniverse/mcp/manager.py` - MCP server management

**Dependencies:**
- Python 3.10+
- Embedded mcpuniverse framework
- LLM providers (OpenAI, Anthropic, etc.)
- MCP protocol libraries

---

### 2. MCP Servers (`lbx_mcp_universe_mcp_servers_mothership/servers/`)

**Location:** Git submodule  
**Purpose:** Tool providers for agents

**Available Servers (25+):**
- `google_search` - Web search
- `email` - Email operations
- `pdf_generator` - PDF creation
- `google_sheets` - Spreadsheet operations
- `yahoo_finance` - Stock data
- `task_management` - Task tracking
- `calendar` - Calendar operations
- `date` - Date/time utilities
- `gitlab` - GitLab operations
- `nexhealth` - Healthcare operations
- And 15+ more...

**Server Structure:**
```
servers/{server_name}/
├── __main__.py          # Entry point
├── server.py            # Server implementation
├── pyproject.toml       # Dependencies
├── server_config.json   # Configuration
└── README.md            # Documentation
```

**Discovery Mechanism:**
- Auto-discovered by BenchmarkRunner
- Searches `lbx_mcp_universe_mcp_servers_mothership/servers/`
- Requires `__main__.py` for module execution
- Name conversion: underscore → hyphen

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:315-394`

---

### 3. Domain Structure (`domains/{domain_name}/`)

**Required Files:**
```
domains/{domain_name}/
├── config.yaml              # REQUIRED: Benchmark configuration
├── tasks/                   # REQUIRED: Task JSON files
│   └── *.json              # 50+ task files
├── evaluators/             # REQUIRED: Evaluation functions
│   ├── __init__.py         # REQUIRED: Package marker
│   └── functions.py        # REQUIRED: Evaluator implementations
└── README.md               # RECOMMENDED: Documentation
```

**Optional Files:**
- `TASK_BREAKDOWN.md` - Task categorization
- Additional documentation

---

### 4. Configuration System

#### 4.1 Domain Config (`config.yaml`)

**Structure:**
```yaml
# LLM Configuration (one or more)
kind: llm
spec:
  name: llm-1
  type: litellm  # OpenAI-compatible / LiteLLM gateway
  config:
    model_name: openai/gpt-4o

# Agent Configuration
kind: agent
spec:
  name: domain-agent
  type: react
  config:
    llm: llm-1
    max_iterations: 20
    system_prompt: |
      You are an agent for [domain]...

# Benchmark Configuration
kind: benchmark
spec:
  description: "Domain description"
  agent: domain-agent
  tasks:
    - tasks/task_0001.json
    - tasks/task_0002.json
    # ... all task files
```

**Key Decisions:**
- **LLM type:** LiteLLM / OpenAI-compatible gateway vs direct provider adapters in the CLI
- **Agent Type:** react (reasoning) vs basic (simple) vs function-call (structured)
- **Max Iterations:** 10-30 depending on complexity
- **Task List:** Must match actual files in `tasks/` directory

**Code Reference:** `lbx_cli/core/domain.py:51-89`

---

#### 4.2 Task Config (`tasks/*.json`)

**Required Fields:**
- `question` (string) - Task prompt
- `output_format` (dict) - Expected response structure
- `mcp_servers` (array) - Required servers
- `evaluators` (array) - Evaluation criteria

**Optional Fields:**
- `category` (string) - Task category
- `use_specified_server` (bool) - Restrict servers

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/task.py:60-84`

---

#### 4.3 Evaluator Config (in task JSON)

**Structure:**
```json
{
  "func": "raw",
  "op": "domain_name.function_name",
  "op_args": {
    "param1": "value1"
  }
}
```

**Function Chain:**
- `func`: Evaluation function chain (e.g., "raw", "json", "get(key)")
- `op`: Comparison function name (must be registered)
- `op_args`: Arguments passed to comparison function

**Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:21-53`

---

### 5. Execution System

#### 5.1 Domain Discovery

**Process:**
1. `DomainRegistry.discover_domains()` scans `domains/` directory
2. For each subdirectory:
   - Creates `Domain` object
   - Calls `domain.load()`
   - Loads `config.yaml` → `DomainConfig`
   - Globs `tasks/*.json` → `TaskConfig[]`
   - Checks `evaluators/` directory
3. Adds to registry if successful

**Code Reference:** `lbx_cli/core/domain.py:187-200`

---

#### 5.2 Benchmark Initialization

**Process:**
1. `BenchmarkRunner(domain.path / "config.yaml", base_dir=domain.path)`
2. `MCPRunner.__init__()`:
   - Loads `config.yaml`
   - Calls `_load_domain_evaluators(base_dir)` if provided
   - Calls `_discover_mcp_servers()`
   - Parses LLM, agent, benchmark configs
3. `WorkflowBuilder` creates agent instances
4. `MCPManager` configured with discovered servers

**Code Reference:**
- Initialization: `lbx_cli/mcpuniverse/benchmark/runner.py:240-288`
- Evaluator loading: `lbx_cli/mcpuniverse/benchmark/runner.py:289-313`
- Server discovery: `lbx_cli/mcpuniverse/benchmark/runner.py:315-394`

---

#### 5.3 Task Execution

**For Each Task:**
1. Resolve task path (relative to `base_dir`)
2. Create `Task` object from JSON
3. Create `Evaluator` objects from config
4. If `use_specified_server=True`:
   - Call `agent.change_servers(task.get_mcp_servers())`
5. Execute agent:
   - `agent.execute(question, output_format, tracer)`
   - Agent makes tool calls via MCP servers
   - Response collected
6. Evaluate response:
   - `task.evaluate(result)`
   - Each evaluator runs
   - Results aggregated
7. Reset task state:
   - `task.reset(trace_records)`
   - Cleanup resources

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:36-136`

---

#### 5.4 Evaluation Flow

**Process:**
1. `evaluator.evaluate(result)` called
2. Execute function chain:
   - `evaluator.execute(result)`
   - Runs `EVALUATION_FUNCTIONS[name]` for each func
   - Example: "raw" → `raw_decode()`
3. Run comparison function:
   - `COMPARISON_FUNCTIONS[op](r.result, value, op_args)`
   - Returns `(bool, str)` tuple
4. Return `EvaluationResult`

**Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:112-151`

---

### 6. Integration Points

#### 6.1 CLI → Domain Discovery
- **Entry:** `validate_command()` → `DomainRegistry.discover_domains()`
- **Code:** `lbx_cli/commands/validate.py:65-66`
- **Implementation:** `lbx_cli/core/domain.py:187-200`

#### 6.2 Domain → Benchmark Runner
- **Entry:** `BenchmarkRunner(domain=domain, ...)`
- **Code:** `lbx_cli/core/runner.py:146`
- **Passes:** `domain.path` as `base_dir` to `MCPRunner`

#### 6.3 Benchmark Runner → Evaluator Loading
- **Entry:** `BenchmarkRunner.__init__(base_dir=domain_path)`
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:262-266`
- **Loads:** `{domain_path}/evaluators/functions.py` via `importlib`

#### 6.4 Task → Agent Server Configuration
- **Entry:** `task.use_specified_server()` check
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:94-95`
- **Calls:** `agent.change_servers(task.get_mcp_servers())`

#### 6.5 Agent → MCP Manager
- **Entry:** `agent.initialize(mcp_servers)`
- **Code:** `lbx_cli/mcpuniverse/agent/base.py:172`
- **Uses:** `MCPManager` to build clients for each server

#### 6.6 Evaluator → Comparison Functions
- **Entry:** `evaluator.evaluate(result)`
- **Code:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:112`
- **Resolves:** `COMPARISON_FUNCTIONS[op]` (includes domain evaluators)

---

## Complete Workflow Steps

### Step 1: Environment Setup (5-10 min)

**Commands:**
```bash
git clone --recurse-submodules <repo-url>
cd lbx_mcp_universe_template
uv sync
```

**What Happens:**
- Repository cloned with submodules
- Virtual environment created (`.venv/`)
- CLI installed from submodule (editable mode)
- All dependencies installed
- CLI commands available via `uv run alignerr_mcp`

**Verification:**
```bash
uv run alignerr_mcp list
uv run alignerr_mcp env status
```

**Components Involved:**
- Git (submodules)
- UV package manager
- Python 3.10+
- CLI submodule
- MCP servers submodule

---

### Step 2: Study Reference (15-30 min)

**Actions:**
- Read `domains/web_search/README.md`
- Review task examples in `domains/web_search/tasks/`
- Study evaluator in `domains/web_search/evaluators/functions.py`
- Review `config.yaml` structure

**Components:**
- Reference domain (`web_search`)
- Documentation files
- Example code

---

### Step 3: Create Domain Scaffold (5 min)

**Command:**
```bash
uv run alignerr_mcp create-domain --name my_domain
```

**What Happens:**
- Creates `domains/my_domain/` directory
- Generates `config.yaml` template
- Creates `tasks/` directory with example task
- Creates `evaluators/` directory with template
- Generates `README.md` template

**Components Created:**
- Domain directory structure
- Configuration template
- Task template
- Evaluator template
- Documentation template

**Code Reference:** `lbx_cli/commands/create.py:141-219`

---

### Step 4: Configure Benchmark (10-20 min)

**Actions:**
1. Edit `config.yaml`:
   - Configure LLM (model, provider)
   - Configure agent (type, instructions, max_iterations)
   - List all task files in `benchmark.tasks`

2. Verify structure:
   - All required sections present
   - Task paths correct
   - Agent references valid

**Components:**
- `config.yaml` file
- YAML parsing (`DomainConfig.from_yaml`)
- Task path resolution

**Code Reference:** `lbx_cli/core/domain.py:51-89`

---

### Step 5: Create Tasks (1-2 weeks)

**Actions:**
1. Plan task categories (3-5 categories)
2. Design 50+ tasks
3. Create JSON files in `tasks/` directory
4. Follow naming convention
5. Update `config.yaml` task list

**Task Requirements:**
- Clear, unambiguous questions
- Verifiable answers (ground truth)
- Appropriate difficulty (target 40-60% pass rate)
- Proper MCP server specification
- Valid evaluator references

**Components:**
- Task JSON files
- Task discovery (glob pattern)
- Task execution (BenchmarkRunner)
- Task validation

**Code Reference:** `lbx_cli/mcpuniverse/benchmark/task.py:60-84`

---

### Step 6: Implement Evaluators (2-5 days)

**Actions:**
1. Design evaluation strategy
2. Implement evaluator functions
3. Register with `@compare_func` decorator
4. Test evaluator registration
5. Verify function names match task configs

**Evaluator Requirements:**
- Async function signature
- `@compare_func(name="domain.func")` decorator
- Return `(bool, str)` tuple
- Handle Pydantic response unwrapping
- Provide clear error messages

**Components:**
- `evaluators/functions.py`
- `@compare_func` decorator
- `COMPARISON_FUNCTIONS` registry
- Module loading (`importlib`)

**Code Reference:**
- Registration: `lbx_cli/mcpuniverse/evaluator/functions.py:42-59`
- Loading: `lbx_cli/mcpuniverse/benchmark/runner.py:289-313`
- Usage: `lbx_cli/mcpuniverse/evaluator/evaluator.py:112-151`

---

### Step 7: Setup MCP Servers (10-30 min)

**Actions:**
1. Identify required servers from tasks
2. List available servers: `servers list`
3. Install servers: `servers install NAME`
4. Configure API keys: `env setup`
5. Verify setup: `env status`

**Server Requirements:**
- Server must exist in mothership
- Must have `__main__.py` for module execution
- API keys configured if required
- Server name conversion handled (underscore ↔ hyphen)

**Components:**
- MCP server submodule
- Server installation system
- API key configuration
- Server discovery mechanism

**Code Reference:**
- Discovery: `lbx_cli/mcpuniverse/benchmark/runner.py:315-394`
- Management: `lbx_cli/mcpuniverse/mcp/manager.py`

---

### Step 8: Local Validation (30-60 min)

**Commands:**
```bash
# Structure validation
uv run alignerr_mcp validate --domain my_domain

# Pass@k validation
uv run alignerr_mcp validate --domain my_domain --runs 3

# With specific model
uv run alignerr_mcp validate --domain my_domain --model openai/gpt-4o
```

**What Happens:**
1. Domain loaded and validated
2. BenchmarkRunner initialized
3. Evaluators loaded
4. MCP servers discovered
5. Tasks executed sequentially
6. Results aggregated
7. Report generated

**Target Metrics:**
- Pass@1: 30-70%
- Evaluation errors: < 5%
- All tasks execute successfully
- Consistent results across runs

**Components:**
- Domain validation
- Benchmark execution
- Task execution
- Evaluation system
- Report generation

**Code Reference:** `lbx_cli/core/runner.py:19-197`

---

### Step 9: Git Workflow (10 min)

**Commands:**
```bash
# Create branch
git checkout -b domains/my_domain/v1

# Commit
git add domains/my_domain/
git commit -m "feat: Add my_domain domain"

# Push and PR
git push origin domains/my_domain/v1
gh pr create --title "Add my_domain domain"
```

**Components:**
- Git repository
- Feature branch
- Conventional commits
- PR creation

---

### Step 10: CI/CD Validation (30-60 min)

**Automatic on PR:**
1. Structure validation (2-5 min)
2. Full evaluation (30-60 min)
3. Report generation
4. Results posted to PR

**Components:**
- GitHub Actions workflows
- CI validation system
- Report generation
- PR comment bot

**Code Reference:** `.github/workflows/ci.yml`

---

## Data Flow Diagram

```
User Input (CLI Command)
    │
    ▼
DomainRegistry.discover_domains()
    │
    ├─> Domain.load()
    │   ├─> DomainConfig.from_yaml()
    │   ├─> TaskConfig.from_file() [for each task]
    │   └─> Check evaluators/
    │
    ▼
BenchmarkRunner(domain.path / "config.yaml", base_dir=domain.path)
    │
    ├─> MCPRunner.__init__()
    │   ├─> _load_domain_evaluators(base_dir)
    │   │   └─> importlib.exec_module()
    │   │       └─> @compare_func decorators execute
    │   │           └─> COMPARISON_FUNCTIONS[name] = func
    │   │
    │   ├─> _discover_mcp_servers()
    │   │   └─> Scan servers directory
    │   │       └─> Build server configs
    │   │
    │   └─> Load config.yaml
    │       └─> Parse LLM, agent, benchmark
    │
    ▼
WorkflowBuilder.build()
    │
    ├─> Create LLM instances
    ├─> Create Agent instances
    └─> Configure MCPManager
    │
    ▼
benchmark.run()
    │
    └─> For each task in benchmark.tasks:
        │
        ├─> Resolve task path
        ├─> Task(task_filepath)
        │   ├─> TaskConfig.model_validate()
        │   └─> Evaluator(c, context) [for each evaluator]
        │
        ├─> if task.use_specified_server():
        │     agent.change_servers(task.get_mcp_servers())
        │
        ├─> agent.execute(question, output_format, tracer)
        │   └─> Agent makes tool calls via MCP servers
        │
        ├─> task.evaluate(result)
        │   └─> For each evaluator:
        │       └─> evaluator.evaluate(result)
        │           ├─> execute(x) [function chain]
        │           └─> COMPARISON_FUNCTIONS[op](...)
        │               └─> Domain evaluator function
        │
        └─> task.reset(trace_records)
    │
    ▼
Results Aggregated
    │
    └─> Report Generated
```

---

## Dependency Graph

```
Domain Creation
    │
    ├─> Requires: CLI Tools (submodule)
    │   └─> Requires: Python 3.10+, UV, dependencies
    │
    ├─> Requires: MCP Servers (submodule)
    │   └─> Requires: Server implementations
    │
    ├─> Requires: API Keys (if using external APIs)
    │   └─> Configured via .env or env setup
    │
    ├─> Requires: LLM API Keys (for evaluation)
    │   └─> OpenAI, Anthropic, etc.
    │
    └─> Requires: Git (for version control)
        └─> GitHub (for PRs)
```

---

## File Dependencies

### Domain Files Depend On:
- `config.yaml` → References task files
- `tasks/*.json` → References evaluator functions
- `evaluators/functions.py` → Must be loadable module

### Execution Depends On:
- Domain files → Loaded by CLI
- MCP servers → Discovered from submodule
- API keys → Loaded from environment
- Evaluators → Loaded via importlib

### Validation Depends On:
- Domain structure → Validated by CLI
- Task files → Validated by JSON parser
- Evaluators → Validated by import
- MCP servers → Validated by discovery

---

## Error Points & Recovery

### Error Point 1: Domain Loading Failure
**Location:** `Domain.load()`  
**Recovery:** Check `config.yaml` exists and is valid YAML

### Error Point 2: Task Loading Failure
**Location:** `TaskConfig.from_file()`  
**Recovery:** Validate JSON syntax, check required fields

### Error Point 3: Evaluator Registration Failure
**Location:** `_load_domain_evaluators()`  
**Recovery:** Check Python syntax, verify decorator names

### Error Point 4: Task Path Resolution Failure
**Location:** `benchmark.run()` task path resolution  
**Recovery:** Verify paths in `config.yaml` match actual files

### Error Point 5: MCP Server Not Found
**Location:** `agent.initialize()`  
**Recovery:** Install server, check name conversion

### Error Point 6: Evaluator Function Not Found
**Location:** `Evaluator.__init__()`  
**Recovery:** Verify function registered, check name match

---

## Success Validation Checklist

### Pre-Submission Checklist

**Structure:**
- [ ] `config.yaml` exists and valid
- [ ] `tasks/` directory has 50+ JSON files
- [ ] `evaluators/functions.py` exists
- [ ] `README.md` complete
- [ ] All task files listed in `config.yaml`

**Functionality:**
- [ ] Domain loads without errors
- [ ] All tasks execute successfully
- [ ] Evaluators register correctly
- [ ] MCP servers installed and working
- [ ] API keys configured (if needed)

**Quality:**
- [ ] Pass@1 rate: 30-70%
- [ ] Evaluation errors: < 5%
- [ ] Results reproducible
- [ ] Documentation complete
- [ ] Code follows patterns

**CI/CD:**
- [ ] Structure validation passes
- [ ] Full evaluation completes
- [ ] Pass rates acceptable
- [ ] No critical errors

---

## Time Estimates

### Setup Phase: 30-60 minutes
- Environment setup: 10 min
- Study reference: 20-30 min
- Create scaffold: 5 min
- Initial configuration: 10-15 min

### Implementation Phase: 1-2 weeks
- Task creation: 5-10 days
- Evaluator implementation: 2-5 days
- Documentation: 1-2 days
- Testing and refinement: 2-3 days

### Validation Phase: 1-2 hours
- Local validation: 30-60 min
- Pass@k testing: 30 min
- Fix issues: 30-60 min

### Submission Phase: 30 minutes
- Git workflow: 10 min
- PR creation: 10 min
- CI monitoring: 10 min

**Total:** 1.5-3 weeks for complete domain

---

## Confidence Summary

**Overall Confidence: 85-90%**

**Breakdown:**
- Domain Structure: 95%
- Task Execution: 90%
- Evaluator System: 90%
- MCP Integration: 85%
- CI/CD: 75%

**Ready to Proceed:** ✅ Yes, with reference implementation and documentation

---

**End of Moving Pieces Guide**






