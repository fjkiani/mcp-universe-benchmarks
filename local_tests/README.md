# Local Testing Framework

**Purpose:** Rigorous local testing of MCP servers, tasks, and evaluators without calling paid model APIs.

**Location:** `local_tests/` (gitignored, local-only)

---

## 🎯 What This Tests

### **1. MCP Server Connectivity**
- ✅ Server startup and initialization
- ✅ Tool discovery and registration
- ✅ Tool execution with real/mock inputs
- ✅ Error handling and validation

### **2. Task Execution**
- ✅ Task JSON parsing and validation
- ✅ MCP server integration
- ✅ End-to-end workflow execution
- ✅ Response format validation

### **3. Evaluator Validation**
- ✅ Evaluator function execution
- ✅ Response parsing (Pydantic unwrapping)
- ✅ Pass/fail logic
- ✅ Error handling

### **4. Mock LLM Responses**
- ✅ Simulates agent responses
- ✅ Tests without live LLM credentials
- ✅ Fast iteration cycles

---

## 🚀 Quick Start

```bash
# Test all MCP servers (structure validation)
python3 local_tests/test_mcp_servers.py

# Test specific server
python3 local_tests/test_mcp_servers.py --server twilio_hipaa

# Test task execution
python3 local_tests/test_tasks.py --domain healthcare_receptionist

# Test evaluators
python3 local_tests/test_evaluators.py --domain healthcare_receptionist

# Full test suite
python3 local_tests/run_all_tests.py --domain healthcare_receptionist
```

**Note:** Tests work without MCP library installed (structure-only testing). For full MCP client testing, install: `pip install mcp`

---

## 📋 Test Structure

```
local_tests/
├── README.md                 # This file
├── test_mcp_servers.py      # MCP server connectivity tests
├── test_tasks.py            # Task execution tests
├── test_evaluators.py       # Evaluator validation tests
├── test_mock_llm.py         # Mock LLM response tests
├── run_all_tests.py         # Full test suite runner
├── fixtures/                # Test fixtures
│   ├── mock_responses.py    # Mock LLM responses
│   └── sample_data.py       # Sample test data
├── utils/                   # Testing utilities
│   ├── mcp_client.py       # MCP client wrapper
│   └── evaluator_runner.py # Evaluator test runner
└── results/                 # Test results (gitignored)
    └── *.json
```

---

## 🔧 Configuration

**Environment Variables:**
- `MCP_SERVERS_PATH`: Path to MCP servers (default: `../lbx_mcp_universe_mcp_servers_mothership/servers`)
- `DOMAINS_PATH`: Path to domains (default: `../domains`)
- `TEST_RESULTS_DIR`: Results directory (default: `./results`)

**API Keys (for real API testing):**
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` (for twilio_hipaa)
- `ASSEMBLYAI_API_KEY` (for assemblyai)
- `VIDEOSDK_API_KEY`, `VIDEOSDK_SECRET_KEY` (for videosdk)
- `NEXHEALTH_API_KEY` (for nexhealth)

**Note:** Tests can run with or without API keys (mock mode vs real API mode)

---

## 📊 Test Output

All tests generate:
- ✅ Console output (pass/fail per test)
- ✅ JSON results file (`results/test_results_YYYY-MM-DD.json`)
- ✅ Summary report (`results/test_summary.md`)

---

## 🎯 Use Cases

1. **Rapid Iteration:** Test MCP servers without waiting for CI/CD
2. **Debugging:** Isolate issues with specific servers or tasks
3. **Development:** Validate new features before pushing
4. **Integration:** Test real API connectivity (when keys available)

---

**Last Updated:** 2025-11-05

