# Execution Flow Diagram - Domain Validation

## Complete Flow: CLI Command → Evaluation Result

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CLI COMMAND ENTRY                                            │
│    validate_command()                                            │
│    Location: lbx_cli/commands/validate.py:22                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. DOMAIN DISCOVERY                                              │
│    DomainRegistry.discover_domains()                            │
│    Location: lbx_cli/core/domain.py:187                         │
│                                                                  │
│    For each domain_dir in domains_root:                         │
│      ├─> Domain(domain_dir)                                     │
│      └─> domain.load()                                          │
│          ├─> Load config.yaml → DomainConfig                   │
│          ├─> Glob tasks/*.json → TaskConfig[]                  │
│          └─> Check evaluators/ directory                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. BENCHMARK RUNNER INITIALIZATION                              │
│    BenchmarkRunner(domain.path / "config.yaml",                  │
│                    base_dir=domain.path)                         │
│    Location: lbx_cli/core/runner.py:117                         │
│                                                                  │
│    ┌──────────────────────────────────────────────────────┐    │
│    │ MCPRunner.__init__()                                  │    │
│    │ Location: lbx_cli/mcpuniverse/benchmark/runner.py:240│    │
│    │                                                        │    │
│    │ ├─> _load_domain_evaluators(base_dir)                 │    │
│    │ │   └─> importlib.exec_module()                       │    │
│    │ │       └─> @compare_func decorators execute           │    │
│    │ │           └─> COMPARISON_FUNCTIONS[name] = func      │    │
│    │ │                                                      │    │
│    │ ├─> _discover_mcp_servers()                            │    │
│    │ │   └─> Scan servers directory                        │    │
│    │ │       └─> Build server configs                       │    │
│    │ │                                                      │    │
│    │ └─> Load config.yaml                                   │    │
│    │     └─> Parse LLM, Agent, Benchmark configs           │    │
│    └──────────────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. WORKFLOW BUILDING                                             │
│    WorkflowBuilder.build()                                       │
│    Location: lbx_cli/mcpuniverse/workflows/builder.py           │
│                                                                  │
│    ├─> Create LLM instances                                     │
│    ├─> Create Agent instances                                   │
│    └─> Configure MCP Manager                                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. TASK EXECUTION LOOP                                           │
│    benchmark.run()                                               │
│    Location: lbx_cli/mcpuniverse/benchmark/runner.py:396        │
│                                                                  │
│    For each benchmark in benchmark_configs:                     │
│      ├─> Get agent from workflow                               │
│      ├─> await agent.initialize()                               │
│      │                                                          │
│      └─> For each task_path in benchmark.tasks:                │
│            │                                                    │
│            ├─> Resolve task path                                │
│            │   ├─> Relative: base_dir + task_path              │
│            │   └─> Absolute: task_path                          │
│            │                                                    │
│            └─> evaluate_single_task()                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. SINGLE TASK EXECUTION                                         │
│    evaluate_single_task()                                        │
│    Location: lbx_cli/mcpuniverse/benchmark/runner.py:36         │
│                                                                  │
│    ├─> Task(task_filepath, context)                            │
│    │   ├─> TaskConfig.model_validate()                         │
│    │   └─> Evaluator(c, context) for each evaluator            │
│    │                                                           │
│    ├─> if task.use_specified_server():                          │
│    │     await agent.change_servers(task.get_mcp_servers())    │
│    │                                                           │
│    ├─> agent.execute(question, output_format, tracer)           │
│    │   └─> Agent makes tool calls via MCP servers              │
│    │                                                           │
│    ├─> task.evaluate(result)                                    │
│    │   └─> For each evaluator:                                 │
│    │       └─> evaluator.evaluate(result)                      │
│    │                                                           │
│    └─> task.reset(trace_records)                                │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. EVALUATION FLOW                                               │
│    evaluator.evaluate(result)                                    │
│    Location: lbx_cli/mcpuniverse/evaluator/evaluator.py:112     │
│                                                                  │
│    ├─> execute(x) - Run function chain                         │
│    │   └─> For each func in config.func:                       │
│    │       └─> EVALUATION_FUNCTIONS[name](res, *args)          │
│    │           (e.g., "raw" → raw_decode())                    │
│    │                                                           │
│    └─> Run comparison function                                  │
│        └─> COMPARISON_FUNCTIONS[op](r.result, value, op_args) │
│            (e.g., "gitlab_mlops.validate_project_creation")    │
│            └─> Returns (bool, str)                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. RESULT AGGREGATION                                            │
│    BenchmarkResult                                               │
│    Location: lbx_cli/mcpuniverse/benchmark/runner.py:156       │
│                                                                  │
│    ├─> task_results: Dict[str, Dict]                           │
│    │   └─> Key: task_path, Value: evaluation_results          │
│    │                                                           │
│    └─> task_trace_ids: Dict[str, str]                          │
│        └─> Key: task_path, Value: trace_id                     │
└─────────────────────────────────────────────────────────────────┘
```

## Key Decision Points

### Decision Point 1: Domain Loading
```
Domain Directory Exists?
├─ YES → Load config.yaml
│         ├─ EXISTS → Parse DomainConfig
│         └─ MISSING → FileNotFoundError (caught, domain skipped)
└─ NO → Warning printed, return
```

### Decision Point 2: Task Discovery
```
Tasks Directory Exists?
├─ YES → Glob all *.json files
│         └─ Load each as TaskConfig
└─ NO → No tasks loaded (validation will fail)
```

### Decision Point 3: Evaluator Loading
```
base_dir Provided?
├─ YES → _load_domain_evaluators(base_dir)
│         ├─ evaluators/functions.py EXISTS → Load module
│         │   └─ @compare_func decorators execute
│         └─ MISSING → Warning, continue
└─ NO → No domain evaluators loaded
```

### Decision Point 4: Task Path Resolution
```
Task Path Absolute?
├─ YES → Use as-is
└─ NO → Resolve relative to base_dir
        ├─ EXISTS → Use
        └─ MISSING → Try default folder
            ├─ EXISTS → Use
            └─ MISSING → FileNotFoundError
```

### Decision Point 5: Agent Server Configuration
```
task.use_specified_server() == True?
├─ YES → agent.change_servers(task.get_mcp_servers())
│         └─ Agent only uses specified servers
└─ NO → Agent uses all available servers
```

### Decision Point 6: Evaluator Function Lookup
```
op in COMPARISON_FUNCTIONS?
├─ YES → Call function
│         └─ Returns (bool, str)
└─ NO → AssertionError in Evaluator.__init__()
```

## Data Flow

### Domain Loading Phase
```
domains/{domain_name}/
├─ config.yaml → DomainConfig
│   ├─ llm_config
│   ├─ agent_config
│   └─ tasks: List[str]  # Execution order
│
├─ tasks/*.json → TaskConfig[]
│   └─ Each file → TaskConfig
│       ├─ task_id
│       ├─ question
│       ├─ mcp_servers
│       └─ evaluators
│
└─ evaluators/functions.py → COMPARISON_FUNCTIONS
    └─ @compare_func(name="domain.func") → Registered
```

### Task Execution Phase
```
Task JSON → TaskConfig
    │
    ├─> question → Agent.execute()
    │   └─> Agent Response (str)
    │
    ├─> mcp_servers → agent.change_servers()
    │   └─> MCP Clients initialized
    │
    └─> evaluators → Evaluator[]
        └─> evaluator.evaluate(response)
            └─> EvaluationResult
                ├─ passed: bool
                ├─ reason: str
                └─ error: str
```

## Error Handling Flow

```
Domain Loading Error
├─ FileNotFoundError (config.yaml missing)
│   └─> Caught in discover_domains()
│       └─> Warning printed, domain skipped
│
Task Loading Error
├─ JSONDecodeError
│   └─> Caught in Domain.load()
│       └─> Warning printed, task skipped
│
Task Path Resolution Error
├─ FileNotFoundError
│   └─> Raised in benchmark.run()
│       └─> Execution stops, error message shown
│
Evaluator Loading Error
├─ ImportError / SyntaxError
│   └─> Caught in _load_domain_evaluators()
│       └─> Warning printed, continue without evaluators
│
Evaluator Function Lookup Error
├─ AssertionError (op not in COMPARISON_FUNCTIONS)
│   └─> Raised in Evaluator.__init__()
│       └─> Task initialization fails
│
MCP Server Error
├─ RuntimeError (server not found)
│   └─> Raised in agent.initialize()
│       └─> Agent initialization fails
```

---

**End of Execution Flow Diagram**






