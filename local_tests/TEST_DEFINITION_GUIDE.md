# Test Definition Guide

**Purpose:** How to define and structure tests for the local testing framework

---

## 🎯 Test Types

### **1. MCP Server Tests** (`test_mcp_servers.py`)

**What it tests:**
- Server file structure (server.py, pyproject.toml, etc.)
- Tool definitions (@mcp.tool() decorators)
- Architecture (FastMCP pattern)
- Required files presence

**How to define:**
```python
# Automatic discovery - no manual definition needed
# Tests all servers in: lbx_mcp_universe_mcp_servers_mothership/servers/

# Test specific server:
python3 local_tests/test_mcp_servers.py --server twilio_hipaa

# Test all servers:
python3 local_tests/test_mcp_servers.py
```

**Test Structure:**
- Checks for `server.py` existence
- Counts `@mcp.tool()` decorators
- Validates FastMCP pattern
- Checks required files (pyproject.toml, __init__.py, etc.)

---

### **2. Task Validation Tests** (`test_tasks.py`)

**What it tests:**
- Task JSON structure
- Required fields (question, evaluators)
- Field types and formats
- MCP server references

**How to define:**
Tasks are defined in `domains/{domain}/tasks/*.json`

**Example Task Definition:**
```json
{
  "category": "patient_intake",
  "question": "A new patient calls: 'Hi, I'd like to schedule...'",
  "output_format": {
    "patient": {
      "resourceType": "Patient",
      "identifier": [{"value": "MRN-12345"}]
    }
  },
  "use_specified_server": true,
  "mcp_servers": [
    {"name": "calendar"},
    {"name": "email"}
  ],
  "evaluators": [
    {
      "func": "raw",
      "op": "healthcare_receptionist.validate_patient_intake",
      "op_args": {}
    }
  ]
}
```

**Required Fields:**
- `question` (string) - Task prompt
- `evaluators` (array) - List of evaluator configs

**Optional Fields:**
- `category` (string) - Task category
- `output_format` (object) - Expected output structure
- `mcp_servers` (array) - Required MCP servers
- `use_specified_server` (boolean) - Restrict to specified servers

**Test Execution:**
```bash
# Test all tasks in domain:
python3 local_tests/test_tasks.py --domain healthcare_receptionist

# Test specific task:
python3 local_tests/test_tasks.py --domain healthcare_receptionist --task patient_intake_basic_001
```

---

### **3. Evaluator Tests** (`test_evaluators.py`)

**What it tests:**
- Evaluator function execution
- Pydantic response unwrapping
- Pass/fail logic
- Error handling

**How to define:**
Evaluators are defined in `domains/{domain}/evaluators/functions.py`

**Example Evaluator Definition:**
```python
from lbx_cli.mcpuniverse.evaluator.functions import compare_func
from typing import Tuple, Any

@compare_func(name="healthcare_receptionist.validate_patient_intake")
async def validate_patient_intake(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validates basic patient intake workflow
    
    Returns: (passed: bool, message: str)
    """
    success, data, error = unwrap_pydantic_and_parse_json(llm_response)
    if not success:
        return False, f"Parse error: {error}"
    
    # Validation logic...
    if not data.get('patient'):
        return False, "Missing 'patient' in response"
    
    return True, "Patient intake validated successfully"
```

**Evaluator Requirements:**
- Must be async function
- Must use `@compare_func` decorator
- Must return `Tuple[bool, str]`
- First parameter: `llm_response: Any`
- Use `unwrap_pydantic_and_parse_json` helper for parsing

**Mock Responses:**
The test framework automatically creates mock responses:
- `simple` - Plain dict
- `pydantic_wrapped` - Pydantic FunctionResult object
- `json_string` - JSON string

**Test Execution:**
```bash
# Test all evaluators in domain:
python3 local_tests/test_evaluators.py --domain healthcare_receptionist

# Test specific evaluator:
python3 local_tests/test_evaluators.py --domain healthcare_receptionist --evaluator validate_patient_intake
```

---

### **4. Custom Test Definitions**

**Creating Custom Test Files:**

You can create custom test files in `local_tests/` directory:

**Example: `test_custom_workflow.py`**
```python
#!/usr/bin/env python3
"""Custom workflow tests"""

import asyncio
import json
from pathlib import Path

async def test_end_to_end_workflow():
    """Test complete workflow from task to evaluation."""
    
    # 1. Load task
    task_path = Path("domains/healthcare_receptionist/tasks/patient_intake_basic_001.json")
    with open(task_path) as f:
        task = json.load(f)
    
    # 2. Create mock agent response
    mock_response = {
        "patient": {
            "resourceType": "Patient",
            "identifier": [{"value": "MRN-12345"}],
            "name": [{"family": "Doe", "given": ["John"]}],
            "birthDate": "1985-03-15",
            "telecom": [{"system": "phone", "value": "555-1234"}]
        },
        "appointment": {
            "provider": "Dr. Smith",
            "date": "2025-11-10",
            "time": "14:00"
        },
        "intake_form_sent": True
    }
    
    # 3. Run evaluator
    from domains.healthcare_receptionist.evaluators.functions import validate_patient_intake
    
    passed, message = await validate_patient_intake(mock_response)
    
    # 4. Assert result
    assert passed, f"Evaluator failed: {message}"
    print(f"✅ Test passed: {message}")

if __name__ == "__main__":
    asyncio.run(test_end_to_end_workflow())
```

---

## 📋 Test Definition Patterns

### **Pattern 1: Structure Validation Tests**

**Purpose:** Validate file structure, syntax, required fields

**Example:**
```python
def test_task_structure(task_path):
    """Validate task JSON structure."""
    with open(task_path) as f:
        task = json.load(f)
    
    assert "question" in task, "Missing 'question' field"
    assert "evaluators" in task, "Missing 'evaluators' field"
    assert isinstance(task["evaluators"], list), "evaluators must be list"
```

---

### **Pattern 2: Functional Tests**

**Purpose:** Test actual functionality with mock data

**Example:**
```python
async def test_evaluator_functionality():
    """Test evaluator with various response formats."""
    
    evaluator = validate_patient_intake
    
    # Test 1: Valid response
    valid_response = {"patient": {...}, "appointment": {...}}
    passed, msg = await evaluator(valid_response)
    assert passed, f"Valid response failed: {msg}"
    
    # Test 2: Missing field
    invalid_response = {"appointment": {...}}  # Missing patient
    passed, msg = await evaluator(invalid_response)
    assert not passed, "Should fail on missing patient"
```

---

### **Pattern 3: Integration Tests**

**Purpose:** Test multiple components working together

**Example:**
```python
async def test_task_evaluator_integration():
    """Test task + evaluator integration."""
    
    # Load task
    task = load_task("patient_intake_basic_001")
    
    # Simulate agent response
    agent_response = simulate_agent(task["question"])
    
    # Run evaluator
    evaluator = load_evaluator(task["evaluators"][0])
    passed, msg = await evaluator(agent_response)
    
    return passed
```

---

### **Pattern 4: Mock Data Definitions**

**Create mock data files: `local_tests/fixtures/mock_responses.py`**

```python
"""Mock agent responses for testing"""

MOCK_PATIENT_INTAKE_RESPONSE = {
    "patient": {
        "resourceType": "Patient",
        "identifier": [{"value": "MRN-12345"}],
        "name": [{"family": "Doe", "given": ["John"]}],
        "birthDate": "1985-03-15",
        "telecom": [{"system": "phone", "value": "555-1234"}]
    },
    "appointment": {
        "provider": "Dr. Smith",
        "date": "2025-11-10",
        "time": "14:00"
    },
    "intake_form_sent": True
}

MOCK_APPOINTMENT_RESPONSE = {
    "appointment": {
        "resourceType": "Appointment",
        "status": "booked",
        "start": "2025-11-11T14:00:00-05:00",
        "end": "2025-11-11T14:30:00-05:00"
    },
    "confirmation_sent": True
}

# Usage in tests:
from fixtures.mock_responses import MOCK_PATIENT_INTAKE_RESPONSE
```

---

## 🎯 Test Definition Best Practices

### **1. Test Naming Convention**
```
test_<component>_<what>_<expected_result>.py

Examples:
- test_task_json_structure_validation.py
- test_evaluator_pydantic_unwrapping.py
- test_mcp_server_tool_discovery.py
```

### **2. Test Organization**
```
local_tests/
├── test_mcp_servers.py          # MCP server tests
├── test_tasks.py                 # Task validation tests
├── test_evaluators.py            # Evaluator tests
├── test_custom_*.py              # Custom tests
├── fixtures/                     # Test data
│   ├── mock_responses.py
│   └── sample_data.py
└── utils/                        # Test utilities
    ├── mcp_client.py
    └── evaluator_runner.py
```

### **3. Test Assertions**
```python
# Good: Clear assertion messages
assert "patient" in data, "Missing 'patient' field in response"
assert data["patient"]["resourceType"] == "Patient", "Invalid resourceType"

# Bad: Unclear failure messages
assert "patient" in data
assert data["patient"]["resourceType"] == "Patient"
```

### **4. Error Handling**
```python
try:
    result = await evaluator(response)
    assert result[0], f"Evaluator failed: {result[1]}"
except Exception as e:
    pytest.fail(f"Evaluator raised exception: {str(e)}")
```

---

## 🚀 Adding New Tests

### **Step 1: Create Test File**
```bash
touch local_tests/test_<your_test>.py
chmod +x local_tests/test_<your_test>.py
```

### **Step 2: Define Test Structure**
```python
#!/usr/bin/env python3
"""Your test description"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

async def test_your_feature():
    """Test description."""
    # Your test logic
    pass

if __name__ == "__main__":
    asyncio.run(test_your_feature())
```

### **Step 3: Add to Test Suite**
Update `run_all_tests.py` to include your test:

```python
from test_your_test import test_your_feature

async def run_all_tests():
    # ... existing tests ...
    
    # Your test
    await test_your_feature()
```

---

## 📊 Test Results Format

**JSON Results:**
```json
{
  "timestamp": "2025-11-05T12:00:00",
  "test_type": "tasks",
  "domain": "healthcare_receptionist",
  "results": [
    {
      "task": "patient_intake_basic_001",
      "status": "valid",
      "errors": [],
      "warnings": []
    }
  ],
  "summary": {
    "total_tasks": 13,
    "valid": 13,
    "errors": 0,
    "pass_rate": 100.0
  }
}
```

---

## 🔧 Test Configuration

**Environment Variables:**
```bash
export MCP_SERVERS_PATH="/path/to/servers"
export DOMAINS_PATH="/path/to/domains"
export TEST_RESULTS_DIR="./local_tests/results"
```

**Config File: `local_tests/config.json`**
```json
{
  "mcp_servers_path": "../lbx_mcp_universe_mcp_servers_mothership/servers",
  "domains_path": "../domains",
  "test_results_dir": "./results",
  "test_timeout": 30,
  "parallel_workers": 4
}
```

---

## 📊 Test Tracking & Status

**Last Updated:** 2025-11-05  
**Status:** Active Development

### **Test Suite Status**

| Test File | Status | Last Run | Pass Rate | Notes |
|-----------|--------|----------|-----------|-------|
| `test_mcp_servers.py` | ✅ Working | 2025-11-05 | 100% | Validates 33 servers, all passing |
| `test_tasks.py` | ✅ Working | 2025-11-05 | 100% | 13/13 tasks validated |
| `test_evaluators.py` | ✅ Fixed | 2025-11-05 | TBD | Error handling fixed, ready for testing |
| `run_all_tests.py` | ✅ Working | - | - | Full test suite runner |

---

### **Test Results History**

#### **2025-11-05 - Initial Test Run**

**Task Validation Tests:**
- ✅ **13/13 tasks valid (100%)**
- Domain: `healthcare_receptionist`
- Errors: 0
- Warnings: 0
- All required fields present
- All evaluator references valid

**MCP Server Structure Tests:**
- ✅ **33/33 servers valid (100%)**
- Healthcare servers tested:
  - `twilio_hipaa`: 5 tools, FastMCP ✅
  - `assemblyai`: 5 tools, FastMCP ✅
  - `videosdk`: 7 tools, FastMCP ✅
  - `nexhealth`: 6 tools, FastMCP ✅
- All servers: FastMCP architecture
- All required files present

**Evaluator Tests:**
- ⚠️ Initial run had error handling issue
- ✅ Fixed: Added error checking for missing summary
- Status: Ready for full testing

---

### **Test Coverage**

**Current Coverage:**
- ✅ MCP Server Structure: 100% (33/33 servers)
- ✅ Task JSON Validation: 100% (13/13 tasks)
- ⏳ Evaluator Function Testing: Pending full run
- ⏳ End-to-End Workflow: Not yet implemented
- ⏳ MCP Server Tool Execution: Not yet implemented (requires MCP client)

**Planned Coverage:**
- [ ] MCP Server Tool Execution Tests
- [ ] End-to-End Task Execution Tests
- [ ] Mock LLM Response Tests
- [ ] Integration Tests (Task + Evaluator + MCP)
- [ ] Performance Tests

---

### **Known Issues & Fixes**

**Issue 1: Evaluator Test Error Handling**
- **Status:** ✅ Fixed
- **Date:** 2025-11-05
- **Problem:** `test_evaluators.py` crashed when results didn't have 'summary' key
- **Fix:** Added error checking before accessing summary
- **File:** `local_tests/test_evaluators.py`

**Issue 2: MCP Client Library Dependency**
- **Status:** ⚠️ Known Limitation
- **Problem:** Full MCP server tool execution requires `mcp` library
- **Workaround:** Structure-only testing works without MCP library
- **Note:** Tests work with structure validation only

---

### **Test Execution Log**

```bash
# 2025-11-05 - Task Validation
$ python3 local_tests/test_tasks.py --domain healthcare_receptionist
Result: 13/13 tasks valid (100%)

# 2025-11-05 - MCP Server Structure
$ python3 local_tests/test_mcp_servers.py --server twilio_hipaa
Result: ✅ Valid (5 tools, FastMCP)

# 2025-11-05 - All MCP Servers
$ python3 local_tests/test_mcp_servers.py
Result: 33/33 servers valid (100%)

# 2025-11-05 - Evaluator Tests (Fixed)
$ python3 local_tests/test_evaluators.py --domain healthcare_receptionist
Status: Fixed, ready for full testing
```

---

### **Test Metrics**

**Total Tests Created:** 4
- `test_mcp_servers.py` - MCP server structure validation
- `test_tasks.py` - Task JSON validation
- `test_evaluators.py` - Evaluator function testing
- `run_all_tests.py` - Full test suite runner

**Total Test Files:** 4
**Total Test Fixtures:** 1 (`mock_responses.py`)
**Total Test Utilities:** 0 (planned)

**Test Execution Time:**
- Task validation: ~2 seconds (13 tasks)
- MCP server structure: ~5 seconds (33 servers)
- Evaluator tests: TBD (pending full run)

---

### **Next Test Priorities**

1. **Complete Evaluator Testing** (High Priority)
   - Run full evaluator test suite
   - Test with all mock response formats
   - Document pass rates

2. **Add MCP Tool Execution Tests** (Medium Priority)
   - Install MCP library if needed
   - Test actual tool calls
   - Validate tool responses

3. **Create End-to-End Tests** (Medium Priority)
   - Test task → evaluator → result flow
   - Mock agent responses
   - Validate complete workflows

4. **Add Performance Tests** (Low Priority)
   - Measure test execution time
   - Identify bottlenecks
   - Optimize slow tests

---

**Last Updated:** 2025-11-05  
**Status:** Active Development - Tests Passing ✅

