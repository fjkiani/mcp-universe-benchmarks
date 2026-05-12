# Integration Test Checklist

**Purpose:** Verify all integration points work correctly based on code analysis

---

## Test Category 1: Domain Loading & Discovery

### Test 1.1: Domain Discovery with Valid Domain
- [ ] **Setup:** Create domain with `config.yaml`, `tasks/`, `evaluators/`
- [ ] **Action:** `DomainRegistry.discover_domains()`
- [ ] **Expected:** Domain loaded successfully, added to registry
- [ ] **Code Reference:** `lbx_cli/core/domain.py:187-200`

### Test 1.2: Domain Discovery with Missing config.yaml
- [ ] **Setup:** Create domain directory without `config.yaml`
- [ ] **Action:** `DomainRegistry.discover_domains()`
- [ ] **Expected:** `FileNotFoundError` caught, warning printed, domain NOT added to registry
- [ ] **Code Reference:** `lbx_cli/core/domain.py:111-112, 199-200`

### Test 1.3: Task Discovery via Glob
- [ ] **Setup:** Domain with 5 task JSON files in `tasks/` directory
- [ ] **Action:** `Domain.load()`
- [ ] **Expected:** All 5 tasks loaded via glob, regardless of `config.yaml` task list
- [ ] **Code Reference:** `lbx_cli/core/domain.py:117-124`

### Test 1.4: Task Loading with Invalid JSON
- [ ] **Setup:** Domain with one invalid JSON file in `tasks/`
- [ ] **Action:** `Domain.load()`
- [ ] **Expected:** Warning printed for invalid file, other tasks still loaded
- [ ] **Code Reference:** `lbx_cli/core/domain.py:120-124`

---

## Test Category 2: Evaluator Loading & Registration

### Test 2.1: Evaluator Loading with base_dir
- [ ] **Setup:** Domain with `evaluators/functions.py` containing `@compare_func` decorators
- [ ] **Action:** `BenchmarkRunner.__init__(base_dir=domain_path)`
- [ ] **Expected:** Evaluators loaded, functions registered in `COMPARISON_FUNCTIONS`
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:262-266, 289-313`

### Test 2.2: Evaluator Loading without base_dir
- [ ] **Setup:** Domain with evaluators, but `base_dir` not provided
- [ ] **Action:** `BenchmarkRunner.__init__(config_path)` (no base_dir)
- [ ] **Expected:** Evaluators NOT loaded, no error
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:267-269`

### Test 2.3: Evaluator Function Registration Timing
- [ ] **Setup:** Domain with evaluator function `@compare_func(name="test.func")`
- [ ] **Action:** Load module, then check `COMPARISON_FUNCTIONS`
- [ ] **Expected:** Function registered immediately when module executed
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/evaluator/functions.py:42-59`

### Test 2.4: Evaluator Name Mismatch
- [ ] **Setup:** Task with evaluator `op="nonexistent.func"` (not registered)
- [ ] **Action:** `Task(task_filepath)` → `Evaluator.__init__()`
- [ ] **Expected:** `AssertionError` raised: "Unknown comparison op: nonexistent.func"
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:79-80`

---

## Test Category 3: Task Path Resolution

### Test 3.1: Relative Task Path Resolution
- [ ] **Setup:** Domain with `config.yaml` listing `tasks/task_001.json`
- [ ] **Action:** `BenchmarkRunner.run()` with `base_dir=domain_path`
- [ ] **Expected:** Task resolved to `domain_path/tasks/task_001.json`
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:467-471`

### Test 3.2: Absolute Task Path
- [ ] **Setup:** Domain with `config.yaml` listing absolute path
- [ ] **Action:** `BenchmarkRunner.run()`
- [ ] **Expected:** Task path used as-is, no resolution
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:470-471`

### Test 3.3: Task Path Fallback
- [ ] **Setup:** Task listed in `config.yaml` but not in domain directory
- [ ] **Action:** `BenchmarkRunner.run()`
- [ ] **Expected:** Falls back to default folder, then `FileNotFoundError` if not found
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:473-489`

### Test 3.4: Missing Task File
- [ ] **Setup:** `config.yaml` lists `tasks/nonexistent.json`
- [ ] **Action:** `BenchmarkRunner.run()`
- [ ] **Expected:** `FileNotFoundError` with search paths shown
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:482-489`

---

## Test Category 4: MCP Server Integration

### Test 4.1: Server Discovery
- [ ] **Setup:** MCP servers in `lbx_mcp_universe_mcp_servers_mothership/servers/`
- [ ] **Action:** `BenchmarkRunner._discover_mcp_servers()`
- [ ] **Expected:** All servers with `__main__.py` discovered and configured
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:315-394`

### Test 4.2: Server Name Conversion
- [ ] **Setup:** Server directory named `google_search` (underscore)
- [ ] **Action:** `_discover_mcp_servers()`
- [ ] **Expected:** Registered as `google-search` (hyphen) in server configs
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:375`

### Test 4.3: Task Server Specification
- [ ] **Setup:** Task with `mcp_servers: [{"name": "google-search"}]` and `use_specified_server: true`
- [ ] **Action:** `evaluate_single_task()`
- [ ] **Expected:** `agent.change_servers()` called with task servers only
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:94-95`

### Test 4.4: Missing Server in Task
- [ ] **Setup:** Task specifies server not in discovered list
- [ ] **Action:** `agent.change_servers([{"name": "nonexistent"}])`
- [ ] **Expected:** Runtime error when agent tries to initialize server
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/agent/base.py:172-207`

---

## Test Category 5: Agent Execution

### Test 5.1: Agent Initialization
- [ ] **Setup:** Valid agent config in `config.yaml`
- [ ] **Action:** `workflow.get_component(benchmark.agent)`
- [ ] **Expected:** Agent instance created and initialized
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:429-431`

### Test 5.2: Agent Server Change
- [ ] **Setup:** Agent initialized, then task specifies different servers
- [ ] **Action:** `agent.change_servers(task.get_mcp_servers())`
- [ ] **Expected:** Old servers cleaned up, new servers initialized
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/agent/base.py:209-220`

### Test 5.3: Agent Response Format
- [ ] **Setup:** Agent executes task
- [ ] **Action:** `response.get_response_str()`
- [ ] **Expected:** Returns string representation of response
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:115`

---

## Test Category 6: Evaluation Flow

### Test 6.1: Function Chain Execution
- [ ] **Setup:** Evaluator with `func: "raw"`
- [ ] **Action:** `evaluator.execute(x)`
- [ ] **Expected:** `raw_decode()` called, returns `FunctionResult`
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:98-110`

### Test 6.2: Comparison Function Lookup
- [ ] **Setup:** Evaluator with `op: "gitlab_mlops.validate_project_creation"`
- [ ] **Action:** `evaluator.evaluate(result)`
- [ ] **Expected:** Domain evaluator function called from `COMPARISON_FUNCTIONS`
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:136`

### Test 6.3: Evaluation Result Format
- [ ] **Setup:** Evaluator evaluates agent response
- [ ] **Action:** `evaluator.evaluate(result)`
- [ ] **Expected:** Returns `EvaluationResult` with `passed`, `reason`, `error`
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:112-151`

### Test 6.4: Evaluation Error Handling
- [ ] **Setup:** Evaluator function raises exception
- [ ] **Action:** `evaluator.evaluate(result)`
- [ ] **Expected:** Exception caught, `EvaluationResult` with `passed=False` and error message
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/evaluator/evaluator.py:145-151`

---

## Test Category 7: Error Handling

### Test 7.1: Missing config.yaml Error
- [ ] **Setup:** Domain directory without `config.yaml`
- [ ] **Action:** `Domain.load()`
- [ ] **Expected:** `FileNotFoundError` with path shown
- [ ] **Code Reference:** `lbx_cli/core/domain.py:111-112`

### Test 7.2: Invalid YAML Error
- [ ] **Setup:** Domain with malformed `config.yaml`
- [ ] **Action:** `DomainConfig.from_yaml()`
- [ ] **Expected:** YAML parsing error raised
- [ ] **Code Reference:** `lbx_cli/core/domain.py:65-66`

### Test 7.3: Missing Task Directory
- [ ] **Setup:** Domain with `config.yaml` but no `tasks/` directory
- [ ] **Action:** `Domain.load()`
- [ ] **Expected:** No tasks loaded, `validate_structure()` returns False
- [ ] **Code Reference:** `lbx_cli/core/domain.py:117-118, 147-149`

### Test 7.4: Server Connection Error
- [ ] **Setup:** Task requires server that fails to connect
- [ ] **Action:** `agent.initialize(mcp_servers)`
- [ ] **Expected:** Connection error raised, agent initialization fails
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/mcp/manager.py:180-221`

---

## Test Category 8: Integration Scenarios

### Test 8.1: Complete Domain Execution
- [ ] **Setup:** Valid domain with config, tasks, evaluators, required servers
- [ ] **Action:** `validate_command(domain="test_domain")`
- [ ] **Expected:** All tasks execute, evaluations run, results returned
- [ ] **Code Reference:** Full flow from `validate.py:22` to `runner.py:544`

### Test 8.2: Multi-Domain Execution
- [ ] **Setup:** Multiple valid domains
- [ ] **Action:** `validate_command(all_domains=True)`
- [ ] **Expected:** All domains discovered, executed in parallel, results aggregated
- [ ] **Code Reference:** `lbx_cli/commands/validate.py:76-77, 168-187`

### Test 8.3: Domain with Missing Evaluators
- [ ] **Setup:** Domain with tasks but no `evaluators/functions.py`
- [ ] **Action:** `BenchmarkRunner.run()`
- [ ] **Expected:** Warning logged, execution continues (if using built-in evaluators)
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/runner.py:297-299`

### Test 8.4: Task with Multiple Evaluators
- [ ] **Setup:** Task with multiple evaluator configs
- [ ] **Action:** `task.evaluate(result)`
- [ ] **Expected:** All evaluators run, results aggregated
- [ ] **Code Reference:** `lbx_cli/mcpuniverse/benchmark/task.py:138-145`

---

## Test Execution Notes

### Prerequisites
- All MCP servers installed and configured
- API keys set in environment
- Test domains created in `domains/` directory

### Test Data Setup
- Create test domains with various configurations
- Include both valid and invalid scenarios
- Test edge cases (missing files, invalid JSON, etc.)

### Expected Outcomes
- All tests should pass for valid configurations
- Error handling tests should verify proper error messages
- Integration tests should verify end-to-end functionality

---

**End of Integration Test Checklist**






