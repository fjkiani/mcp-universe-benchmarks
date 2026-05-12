---
name: Domains Directory - Complete Understanding (Code-Based Analysis)
overview: ""
todos:
  - id: 939cf546-c043-4a0d-aca9-2fe4b08af47b
    content: Understand base domain structure (base.py, file-based domains, CLI discovery)
    status: completed
  - id: 4d8f9ed0-969d-41ae-9461-f8cdd728ef9e
    content: Understand task JSON format (question, output_format, mcp_servers, evaluators)
    status: completed
  - id: bcb49f07-7aa7-4695-851a-75b15b1e0ebc
    content: Trace evaluator loading and registration (importlib, @compare_func timing)
    status: pending
  - id: bf32ce74-bb8a-4d62-9b6e-8570ff862efe
    content: Trace task path resolution (base_dir, relative paths, fallbacks)
    status: pending
  - id: 5dda6fd1-be9b-45a2-9930-e56d7c48773e
    content: Trace MCP server discovery and configuration
    status: pending
  - id: a204e794-c101-4606-ad6f-bd2b2149021c
    content: Map complete execution flow (CLI → Domain → Task → Agent → Evaluator)
    status: pending
  - id: 51ce7525-ffd5-4a8d-9873-69c57929b060
    content: Validate integration points with code references
    status: pending
  - id: aeccda83-20a4-4f1e-9b3c-2718dbf35933
    content: Identify gaps and inconsistencies
    status: pending
isProject: false
---

# Domains Directory - Complete Understanding (Code-Based Analysis)

## Architecture Overview

The `domains/` directory contains self-contained benchmark domains that test AI agents on specific problem domains. Each domain is a complete benchmark with tasks, evaluators, and configuration.

### System Components

1. **Domains** (`domains/`) - Benchmark implementations (file-based, not class-based)
2. **CLI** (`lbx_mcp_universe_cli/`) - Domain discovery, validation, and execution
3. **MCP Servers** (`lbx_mcp_universe_mcp_servers_mothership/servers/`) - Tool providers for agents
4. **Base Classes** (`domains/base.py`) - Abstract domain interface (NOT USED by current domains)

## CRITICAL FINDING: BaseDomain Class is NOT Used

**Code Evidence:**

- `domains/base.py` defines `BaseDomain` abstract class
- `domains/__init__.py` only exports version string
- CLI uses `DomainRegistry` and `Domain` classes from `lbx_cli/core/domain.py`
- Current domains are **file-based**, not class-based

**Actual Domain Loading:**

```python
# lbx_cli/core/domain.py:187-200
def discover_domains(self) -> None:
    for domain_dir in self.domains_root.iterdir():
        if domain_dir.is_dir() and not domain_dir.name.startswith("."):
            domain = Domain(domain_dir)  # Creates Domain object
            domain.load()  # Loads config.yaml and tasks
            self.domains[domain.name] = domain
```

**Domain.load() Implementation:**

```python
# lbx_cli/core/domain.py:107-129
def load(self) -> None:
    # Load config.yaml
    config_path = self.path / "config.yaml"
    self.config = DomainConfig.from_yaml(config_path, self.name)
    
    # Load tasks from tasks/ directory
    tasks_dir = self.path / "tasks"
    for task_file in sorted(tasks_dir.glob("*.json")):
        task = TaskConfig.from_file(task_file)
        self.tasks[task.task_id] = task
    
    # Check for evaluators directory
    evaluators_dir = self.path / "evaluators"
    if evaluators_dir.exists():
        self.evaluators_path = evaluators_dir
```

## Domain Structure

Each domain follows this structure:

```
domains/{domain_name}/
├── config.yaml              # Benchmark configuration (LLM, agent, tasks)
├── tasks/                   # Task definition files (JSON)
│   ├── task_0001.json
│   ├── task_0002.json
│   └── ...
├── evaluators/             # Evaluation functions
│   ├── __init__.py
│   └── functions.py        # Custom evaluator functions
└── README.md               # Domain documentation
```

### Key Files

**config.yaml** - Defines:

- LLM configurations (model, provider)
- Agent configuration (type, instructions, max_iterations)
- Benchmark specification (tasks list, agent reference)

**tasks/*.json** - Task definitions with:

- `question` - Task prompt
- `output_format` - Expected response structure
- `mcp_servers` - Required MCP servers (array of `{"name": "server-name"}`)
- `use_specified_server` - Boolean (restrict to specified servers)
- `evaluators` - Evaluation criteria (array of evaluator configs)

**evaluators/functions.py** - Custom evaluation functions:

- Decorated with `@compare_func(name="domain.function_name")`
- Return `(bool, str)` tuple (pass/fail, error message)
- Access agent response via `llm_response` parameter

## Current Domains

### 1. web_search (Reference Implementation)

- **Status:** Production-ready reference
- **Tasks:** 50 tasks (info_search_task_0001 to _0050)
- **MCP Servers:** google-search, fetch
- **Evaluator:** LLM-as-a-judge (flexible answer matching)
- **Purpose:** Tests web search and information retrieval

### 2. gitlab_mlops

- **Status:** 6 tasks (Module 1 - GitLab Orchestrator)
- **MCP Servers:** gitlab
- **Tasks:** Project creation, MR creation, reviewer assignment, issue linking, pipeline status, release/milestone
- **Evaluator:** Structured JSON validation with error types

### 3. identity_service

- **Status:** 15 tasks across 3 categories
- **MCP Servers:** task-management, calendar, date (zero-API servers)
- **Categories:** Identity Verification, Access Control, Audit & Compliance
- **Purpose:** Tests MCP integration without external dependencies

### 4. investments

- **Status:** 15 tasks
- **MCP Servers:** yahoo_finance, stock_portfolio, etc.
- **Purpose:** Financial analysis and portfolio management

### 5. grant_application

- **Status:** 50+ tasks
- **Categories:** Document generation, grant search, multi-server tasks, agentic tasks, edge cases
- **Purpose:** Complex grant application workflows

### 6. google_slides

- **Status:** 3 tasks
- **MCP Servers:** google_slides, google_docs, google_sheets
- **Purpose:** Google Workspace automation

### 7. currency_converter

- **Status:** 1 task (minimal example)
- **MCP Servers:** currency_converter

### 8. flight_delay

- **Status:** 1 task
- **MCP Servers:** flight_delay

### 9. healthcare_receptionist

- **Status:** Incomplete (evaluators directory exists)

### 10. ai_receptionist

- **Status:** Incomplete (evaluators directory exists)

## Base Domain Interface

**Location:** `domains/base.py`

**Classes:**

- `BaseDomain` (ABC) - Abstract base class
  - `load_data()` - Load domain data (abstract)
  - `validate_structure()` - Validate structure (abstract)
  - `add_variation()` - Add domain variation
  - `get_variation()` - Get variation by ID
  - `validate_completeness()` - Check minimum task count (default: 100)

- `DomainTask` (Pydantic) - Task model
  - `task_id`, `description`, `difficulty`, `metadata`

- `DomainVariation` (Pydantic) - Variation model
  - `variation_id`, `name`, `description`, `tasks`

**Note:** Current domains don't use `BaseDomain` class - they use file-based structure with CLI discovery.

## CLI Integration

**Location:** `lbx_mcp_universe_cli/lbx_cli/core/domain.py`

**Key Classes:**

- `DomainRegistry` - Discovers and manages domains
  - `discover_domains()` - Scans `domains/` directory
  - `get_domain(name)` - Get domain by name
  - `list_domains()` - List all domain names

- `Domain` - Represents a single domain
  - `load()` - Loads config.yaml, tasks, evaluators
  - `validate_structure()` - Validates domain structure

- `TaskConfig` - Task configuration model
  - Loads from JSON files in `tasks/` directory

- `DomainConfig` - Domain configuration model
  - Loads from `config.yaml` using YAML parsing

## Task Execution Flow

1. **Discovery:** CLI scans `domains/` directory
2. **Loading:** Loads `config.yaml` and all task JSON files
3. **Task Execution:** For each task:

   - Creates `Task` object from JSON
   - Initializes MCP servers specified in task
   - Executes agent with question
   - Collects agent response
   - Runs evaluators on response
   - Resets task state

4. **Evaluation:** Custom evaluator functions validate response
5. **Reporting:** Results aggregated and reported

## MCP Server Integration

**Task Configuration:**

```json
{
  "mcp_servers": [
    {"name": "google-search"},
    {"name": "fetch"}
  ],
  "use_specified_server": true
}
```

**Server Discovery:**

- CLI manages server installation via `alignerr_mcp servers install`
- Servers located in `lbx_mcp_universe_mcp_servers_mothership/servers/`
- Each server has `server.py`, `pyproject.toml`, `server_config.json`

**Server Naming:**

- CLI uses underscore: `google_search`
- Tasks use hyphen: `google-search`
- CLI handles conversion automatically

## Evaluation System

**Evaluator Types:**

1. **Raw evaluators** - Custom Python functions
   ```json
   {
     "func": "raw",
     "op": "domain.function_name",
     "op_args": {}
   }
   ```

2. **Built-in evaluators** - Standard comparison functions

**Evaluator Function Pattern:**

```python
@compare_func(name="domain.function_name")
async def evaluate_function(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    # Parse response
    # Validate structure
    # Check business logic
    return (True, "") or (False, "error message")
```

**Error Types** (from gitlab_mlops example):

- `PARSE_ERROR` - JSON parsing failures
- `VALIDATION_ERROR` - Missing fields, wrong types, invalid values

## Domain Creation Workflow

1. **Create domain structure:**
   ```bash
   uv run alignerr_mcp create-domain --name my_domain
   ```

2. **Implement domain:**

   - Create `config.yaml` with LLM, agent, benchmark specs
   - Create task JSON files in `tasks/`
   - Implement evaluator functions in `evaluators/functions.py`
   - Write `README.md` documentation

3. **Test locally:**
   ```bash
   uv run alignerr_mcp validate --domain my_domain
   ```

4. **Install required servers:**
   ```bash
   uv run alignerr_mcp servers install server_name
   ```

5. **Configure API keys:**
   ```bash
   uv run alignerr_mcp env setup
   ```


## Best Practices

### Task Design

- Clear, unambiguous questions
- Verifiable answers (ground truth)
- Appropriate difficulty (target 40-60% pass rate)
- Structured output formats
- Proper MCP server specification

### Evaluation

- Use LLM-as-a-judge for flexible matching (web_search pattern)
- Use structured validation for deterministic checks (gitlab_mlops pattern)
- Handle Pydantic response unwrapping
- Provide clear error messages with error types

### Configuration

- Use LiteLLM or your provider’s OpenAI-compatible endpoint in `config.yaml`
- Configure ReAct agents with appropriate max_iterations
- Specify all required MCP servers
- Document API key requirements

### Documentation

- Include comprehensive README
- Document task categories
- Explain evaluation strategy
- List required MCP servers and API keys
- Provide usage examples

## Integration Points

1. **CLI → Domains:** Discovery, validation, execution
2. **Domains → MCP Servers:** Tool access during task execution
3. **Domains → Evaluators:** Response validation
4. **MCP Servers → External APIs:** Actual tool functionality
5. **CLI → MCP Universe:** Benchmark execution framework

## File Locations

- **Domain base:** `domains/base.py`
- **Domain implementations:** `domains/{domain_name}/`
- **CLI domain management:** `lbx_mcp_universe_cli/lbx_cli/core/domain.py`
- **CLI commands:** `lbx_mcp_universe_cli/lbx_cli/commands/`
- **MCP servers:** `lbx_mcp_universe_mcp_servers_mothership/servers/`
- **Documentation:** `docs/`, domain-specific `README.md` files

## Key Insights

1. **Domains are self-contained** - Each domain has everything needed (config, tasks, evaluators)

2. **File-based structure** - Domains don't use Python classes, they use YAML/JSON files discovered by CLI

3. **MCP servers are shared** - Multiple domains can use the same servers (e.g., google-search used by web_search)

4. **Evaluators are domain-specific** - Each domain implements custom evaluation logic

5. **Reference implementation** - `web_search` domain is the gold standard for new domains

6. **Zero-API pattern** - `identity_service` demonstrates using built-in servers (task-management, calendar, date) without external APIs

7. **Complex workflows** - Domains like `grant_application` test multi-server orchestration

8. **CI/CD integration** - GitLab domain has CI/CD testing patterns documented in `.cursor/rules/`

## Next Steps for Understanding

1. Study `web_search` domain as reference implementation
2. Review `gitlab_mlops` for structured validation patterns
3. Examine `identity_service` for zero-API server usage
4. Check CLI code for domain discovery and execution flow
5. Review MCP server structure in mothership repository
6. Understand evaluator function patterns and error handling

## Fail-First Questions (Critical Validation)

These questions reveal gaps if answered incorrectly:

### 1. Domain Loading & Discovery

**Q: What happens if a domain has no `config.yaml`?**

- **Expected:** `FileNotFoundError` raised in `Domain.load()` (line 112)
- **Fail condition:** Silent skip or wrong error handling
- **Code:** `lbx_cli/core/domain.py:110-112`

**Q: How are task files discovered vs. config.yaml task list?**

- **Expected:** Tasks loaded from `tasks/*.json` glob, config.yaml `tasks` list is for execution order
- **Fail condition:** Tasks only loaded from config.yaml list (missing files)
- **Code:** `lbx_cli/core/domain.py:117-124` (glob) vs `DomainConfig.from_yaml:88` (config list)

### 2. Evaluator Loading

**Q: When are domain evaluators loaded and registered?**

- **Expected:** Loaded when `BenchmarkRunner` initialized with `base_dir` pointing to domain
- **Fail condition:** Evaluators not loaded, `@compare_func` decorators not executed
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:289-313` (`_load_domain_evaluators`)

**Q: What happens if evaluator function name doesn't match task config `op`?**

- **Expected:** `AssertionError` in `Evaluator.__init__` if op not in `COMPARISON_FUNCTIONS`
- **Fail condition:** Silent failure or wrong evaluator called
- **Code:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:79-80`

### 3. Task Path Resolution

**Q: How are relative task paths resolved?**

- **Expected:** Resolved relative to `base_dir` (domain path), fallback to default folder
- **Fail condition:** Tasks not found, wrong paths used
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:467-489`

**Q: What if config.yaml lists tasks that don't exist?**

- **Expected:** `FileNotFoundError` raised with search paths shown
- **Fail condition:** Silent skip or wrong error
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:482-489`

### 4. MCP Server Integration

**Q: How are MCP servers discovered and configured?**

- **Expected:** Auto-discovered from `lbx_mcp_universe_mcp_servers_mothership/servers/` directory
- **Fail condition:** Servers not found, wrong paths
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:315-394` (`_discover_mcp_servers`)

**Q: What happens when task specifies server not in discovered list?**

- **Expected:** Runtime error when agent tries to use server
- **Fail condition:** Silent failure or wrong server used
- **Code:** `lbx_cli/mcpuniverse/agent/base.py:209-220` (`change_servers`)

### 5. Agent Execution

**Q: When does agent get MCP servers from task?**

- **Expected:** After task created, before execution, if `use_specified_server=True`
- **Fail condition:** Agent uses wrong servers or all servers
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:93-95` (`evaluate_single_task`)

**Q: How is agent response converted to evaluator input?**

- **Expected:** `response.get_response_str()` returns string, evaluator receives it
- **Fail condition:** Wrong format passed to evaluator
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:115,119`

---

## Detailed Execution Flow (Code-Based)

### Complete Task Execution Path

```python
# 1. CLI Command Entry
validate_command()  # lbx_cli/commands/validate.py:22
  → DomainRegistry.discover_domains()  # lbx_cli/core/domain.py:187
    → Domain.load()  # lbx_cli/core/domain.py:107
      → DomainConfig.from_yaml()  # lbx_cli/core/domain.py:63
      → TaskConfig.from_file() for each task  # lbx_cli/core/domain.py:121

# 2. Benchmark Runner Initialization
BenchmarkRunner(domain.path / "config.yaml", base_dir=domain.path)  # lbx_cli/core/runner.py:117
  → MCPRunner.__init__()  # lbx_cli/mcpuniverse/benchmark/runner.py:240
    → _load_domain_evaluators(base_dir)  # lbx_cli/mcpuniverse/benchmark/runner.py:266
      → importlib.util.spec_from_file_location("domain_evaluators", evaluators_path)
      → spec.loader.exec_module(module)  # Executes @compare_func decorators
    → _discover_mcp_servers()  # lbx_cli/mcpuniverse/benchmark/runner.py:315
      → Scans servers directory, builds config dict

# 3. Task Execution Loop
for task_path in benchmark.tasks:  # lbx_cli/mcpuniverse/benchmark/runner.py:452
  → Resolve task path: os.path.join(self._config_dir, task_path)  # Line 469
  → evaluate_single_task(task_filepath, agent, ...)  # lbx_cli/mcpuniverse/benchmark/runner.py:36
    → Task(task_filepath, context)  # lbx_cli/mcpuniverse/benchmark/task.py:91
      → TaskConfig.model_validate()  # Parses JSON
      → Evaluator(c, context) for each evaluator  # lbx_cli/mcpuniverse/benchmark/task.py:100
    → if task.use_specified_server():  # Line 94
        agent.change_servers(task.get_mcp_servers())  # lbx_cli/mcpuniverse/agent/base.py:209
    → agent.execute(question, output_format, tracer)  # lbx_cli/mcpuniverse/agent/base.py:226
    → task.evaluate(result)  # lbx_cli/mcpuniverse/benchmark/task.py:138
      → evaluator.evaluate(result) for each evaluator  # lbx_cli/mcpuniverse/evaluator/evaluator.py:112
        → execute(x)  # Runs func chain (e.g., "raw")
        → COMPARISON_FUNCTIONS[op](r.result, value, op_args)  # Line 136
          → Domain evaluator function (e.g., "gitlab_mlops.validate_project_creation")
    → task.reset(trace_records)  # Cleanup
```

### Evaluator Registration Flow

```python
# Domain evaluators/functions.py
@compare_func(name="gitlab_mlops.validate_project_creation")
async def validate_project_creation(llm_response, *args, **kwargs):
    ...

# Registration happens when module is loaded:
# 1. BenchmarkRunner.__init__(base_dir=domain_path)  # runner.py:266
# 2. _load_domain_evaluators(domain_path)  # runner.py:289
# 3. spec.loader.exec_module(module)  # runner.py:308
#    → Executes all @compare_func decorators
#    → Functions registered in COMPARISON_FUNCTIONS dict  # functions.py:54

# Usage:
# Task JSON: {"func": "raw", "op": "gitlab_mlops.validate_project_creation"}
# Evaluator.__init__() checks: self._config.op in COMPARISON_FUNCTIONS  # evaluator.py:79
# Evaluator.evaluate() calls: COMPARISON_FUNCTIONS[op](...)  # evaluator.py:136
```

### MCP Server Discovery Flow

```python
# BenchmarkRunner._discover_mcp_servers()  # runner.py:315
# Searches for servers in:
possible_paths = [
    # Template repo with mothership as sibling
    os.path.join(module_dir, "..", "..", "..", "..", "lbx_mcp_universe_mcp_servers_mothership", "servers"),
    # Standalone CLI repo
    os.path.join(module_dir, "..", "..", "..", "..", "lbx_mcp_universe_mcp_servers_mothership", "servers"),
]

# For each server directory:
if os.path.exists(os.path.join(server_path, "__main__.py")):
    servers[server_name.replace("_", "-")] = {
        "stdio": {
            "command": sys.executable,
            "args": ["-m", f"servers.{server_name}"],
        },
        "env": {"PYTHONPATH": servers_parent_dir},
    }

# MCPManager uses this config to build clients
MCPManager(config=server_configs, context=context)  # runner.py:419
```

---

## Integration Points (Code References)

### 1. CLI → Domain Discovery

- **Entry:** `validate_command()` → `DomainRegistry.discover_domains()`
- **Code:** `lbx_cli/commands/validate.py:65-66`
- **Implementation:** `lbx_cli/core/domain.py:187-200`

### 2. Domain → Benchmark Runner

- **Entry:** `BenchmarkRunner(domain=domain, ...)`
- **Code:** `lbx_cli/core/runner.py:146`
- **Passes:** `domain.path` as `base_dir` to `MCPRunner` (line 117)

### 3. Benchmark Runner → Evaluator Loading

- **Entry:** `BenchmarkRunner.__init__(base_dir=domain_path)`
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:262-266`
- **Loads:** `{domain_path}/evaluators/functions.py` via `importlib`

### 4. Task → Agent Server Configuration

- **Entry:** `task.use_specified_server()` check
- **Code:** `lbx_cli/mcpuniverse/benchmark/runner.py:94-95`
- **Calls:** `agent.change_servers(task.get_mcp_servers())`
- **Implementation:** `lbx_cli/mcpuniverse/agent/base.py:209-220`

### 5. Agent → MCP Manager

- **Entry:** `agent.initialize(mcp_servers)`
- **Code:** `lbx_cli/mcpuniverse/agent/base.py:172`
- **Uses:** `MCPManager` to build clients for each server

### 6. Evaluator → Comparison Functions

- **Entry:** `evaluator.evaluate(result)`
- **Code:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:112`
- **Resolves:** `COMPARISON_FUNCTIONS[op]` (includes domain evaluators)

---

## Iteration Plan

### Iteration 1: Validate Core Assumptions (Fail-First)

**Goal:** Answer all fail-first questions with code evidence

1. **Domain Loading**

   - [ ] Trace `DomainRegistry.discover_domains()` execution
   - [ ] Verify task loading (glob vs config.yaml)
   - [ ] Test missing config.yaml error handling

2. **Evaluator Loading**

   - [ ] Trace `_load_domain_evaluators()` execution
   - [ ] Verify `@compare_func` registration timing
   - [ ] Test evaluator name resolution

3. **Task Path Resolution**

   - [ ] Trace task path resolution logic
   - [ ] Test relative vs absolute paths
   - [ ] Verify fallback behavior

**Deliverable:** Code trace document with line numbers

### Iteration 2: Execution Flow Mapping

**Goal:** Complete execution path from CLI command to evaluation result

1. **CLI Command Flow**

   - [ ] Map `validate_command()` → `BenchmarkRunner`
   - [ ] Trace domain discovery and loading
   - [ ] Verify config preparation

2. **Task Execution Flow**

   - [ ] Map task creation from JSON
   - [ ] Trace agent initialization with servers
   - [ ] Verify evaluator instantiation

3. **Evaluation Flow**

   - [ ] Map evaluator function chain execution
   - [ ] Trace comparison function lookup
   - [ ] Verify result aggregation

**Deliverable:** Complete execution flow diagram with code references

### Iteration 3: Integration Point Validation

**Goal:** Verify all integration points work correctly

1. **MCP Server Integration**

   - [ ] Trace server discovery
   - [ ] Verify server config building
   - [ ] Test server name conversion (underscore ↔ hyphen)

2. **Evaluator Integration**

   - [ ] Verify domain evaluator loading
   - [ ] Test evaluator function registration
   - [ ] Verify evaluator lookup in task execution

3. **Error Handling**

   - [ ] Test missing file errors
   - [ ] Test invalid config errors
   - [ ] Test server connection errors

**Deliverable:** Integration test checklist

### Iteration 4: Gap Analysis

**Goal:** Identify what's missing or unclear

1. **Documentation Gaps**

   - [ ] Compare docs vs actual code
   - [ ] Identify missing explanations
   - [ ] Note inconsistencies

2. **Code Gaps**

   - [ ] Find unused code (e.g., `BaseDomain`)
   - [ ] Identify missing error handling
   - [ ] Note TODO comments or incomplete features

3. **Testing Gaps**

   - [ ] Identify untested paths
   - [ ] Note missing test coverage
   - [ ] Suggest test scenarios

**Deliverable:** Gap analysis report