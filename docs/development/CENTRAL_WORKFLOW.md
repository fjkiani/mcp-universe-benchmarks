# Central Development Workflow - SaaS-First Approach

**Purpose:** One central place to manage APIs, tests, and frontend integration - building real SaaS products, not just assignments

**Last Updated:** 2025-11-04

---

## 🎯 Core Principle: Showcase Real Work

**Goal:** Every feature we build should be:
1. ✅ **Tested** (automated tests)
2. ✅ **Visible** (frontend dashboard)
3. ✅ **Documented** (clear API docs)
4. ✅ **Production-Ready** (SaaS quality)

**No More:**
- ❌ Buried code in test files
- ❌ Hidden API integrations
- ❌ Tests that don't connect to frontend
- ❌ Features that exist but aren't visible

---

## 🏗️ Central Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              CENTRAL API & TEST MANAGER                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Registry (api-registry.yaml)                    │   │
│  │  - All APIs, endpoints, credentials                    │   │
│  │  - Test status, coverage, results                     │   │
│  │  - Frontend integration status                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Test Runner (test-runner.py)                         │   │
│  │  - Runs all tests automatically                       │   │
│  │  - Updates test results in registry                   │   │
│  │  - Triggers frontend updates                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Frontend Sync (frontend-sync.py)                     │   │
│  │  - Syncs test results → frontend                      │   │
│  │  - Updates dashboard automatically                    │   │
│  │  - Shows real-time progress                           │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬───────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌──────────────┐   ┌──────────────┐
│   Backend     │   │   Frontend  │   │  MCP Servers │
│   (FastAPI)   │   │   (Vite.js) │   │   (Wrappers) │
│               │   │             │   │              │
│  - API        │   │  - Dashboard│   │  - Twilio    │
│  - Tests      │   │  - Real-time│   │  - AssemblyAI│
│  - Registry   │   │  - Progress │   │  - VideoSDK  │
│               │   │             │   │  - NexHealth │
└───────────────┘   └──────────────┘   └──────────────┘
```

---

## 📁 Central Structure

```
lbx_mcp_universe_template-main/
├── central/                          # 🎯 CENTRAL WORKFLOW
│   ├── api-registry.yaml            # Single source of truth for all APIs
│   ├── test-runner.py                # Automated test runner
│   ├── frontend-sync.py              # Sync test results → frontend
│   ├── api-manager.py                # API connection manager
│   └── README.md                     # This workflow guide
│
├── backend/                          # Backend API
│   ├── api/
│   │   └── routers/
│   │       ├── apis.py              # API registry endpoints
│   │       ├── tests.py               # Test endpoints
│   │       └── sync.py                # Frontend sync endpoints
│   └── services/
│       ├── api_registry_service.py   # API registry logic
│       └── test_service.py           # Test execution logic
│
├── frontend/                         # Frontend Dashboard
│   ├── src/
│   │   ├── components/
│   │   │   └── showcase/            # Showcase components
│   │   │       ├── APIShowcase.tsx   # Real API status
│   │   │       ├── TestShowcase.tsx  # Real test results
│   │   │       └── ProgressShowcase.tsx # Real progress
│   │   └── pages/
│   │       └── Showcase.tsx          # Main showcase page
│
└── tests/                           # Centralized Tests
    ├── api/                          # API integration tests
    │   ├── test_twilio.py
    │   ├── test_assemblyai.py
    │   ├── test_videosdk.py
    │   └── test_nexhealth.py
    ├── mcp/                          # MCP server tests
    └── e2e/                          # End-to-end tests
```

---

## 📋 API Registry (`central/api-registry.yaml`)

**Purpose:** Single source of truth for all APIs, tests, and frontend integration

```yaml
apis:
  twilio_hipaa:
    name: "Twilio HIPAA"
    category: "communication"
    status: "active"
    mcp_server: "twilio_hipaa"
    location: "lbx_mcp_universe_mcp_servers_mothership/servers/twilio_hipaa/"
    credentials:
      env_file: ".env"
      keys: ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"]
    endpoints:
      - name: "send_hipaa_sms"
        tested: true
        last_test: "2025-11-04T10:00:00Z"
        test_result: "passed"
        frontend_showcase: true
        showcase_component: "APIShowcase"
      - name: "make_voice_call"
        tested: true
        last_test: "2025-11-04T10:00:00Z"
        test_result: "passed"
        frontend_showcase: true
      - name: "check_phi_in_message"
        tested: true
        last_test: "2025-11-04T10:00:00Z"
        test_result: "passed"
        frontend_showcase: true
    tests:
      total: 5
      passed: 5
      failed: 0
      coverage: 100%
    frontend:
      integrated: true
      showcase_page: "/showcase/twilio"
      last_synced: "2025-11-04T10:00:00Z"

  assemblyai:
    name: "AssemblyAI"
    category: "transcription"
    status: "active"
    mcp_server: "assemblyai"
    location: "lbx_mcp_universe_mcp_servers_mothership/servers/assemblyai/"
    credentials:
      env_file: ".env"
      keys: ["ASSEMBLYAI_API_KEY"]
    endpoints:
      - name: "transcribe_medical"
        tested: true
        last_test: "2025-11-04T10:00:00Z"
        test_result: "passed"
        frontend_showcase: true
    tests:
      total: 5
      passed: 5
      failed: 0
      coverage: 100%
    frontend:
      integrated: true
      showcase_page: "/showcase/assemblyai"

  videosdk:
    name: "VideoSDK.live"
    category: "video"
    status: "active"
    mcp_server: "videosdk"
    location: "lbx_mcp_universe_mcp_servers_mothership/servers/videosdk/"
    credentials:
      env_file: ".env"
      keys: ["VIDEOSDK_API_KEY", "VIDEOSDK_SECRET_KEY"]
    endpoints:
      - name: "create_video_room"
        tested: true
        test_result: "passed"
        frontend_showcase: true
    tests:
      total: 7
      passed: 7
      failed: 0
    frontend:
      integrated: true

  nexhealth:
    name: "NexHealth"
    category: "ehr"
    status: "active"
    mcp_server: "nexhealth"
    location: "lbx_mcp_universe_mcp_servers_mothership/servers/nexhealth/"
    credentials:
      env_file: ".env"
      keys: ["NEXHEALTH_API_KEY"]
    endpoints:
      - name: "book_appointment"
        tested: true
        test_result: "passed"
        frontend_showcase: true
    tests:
      total: 6
      passed: 6
      failed: 0
    frontend:
      integrated: true

# Test Results Summary
test_summary:
  total_apis: 4
  total_endpoints: 23
  total_tests: 23
  tests_passed: 23
  tests_failed: 0
  overall_coverage: 100%
  last_updated: "2025-11-04T10:00:00Z"

# Frontend Integration Status
frontend_integration:
  total_showcases: 4
  integrated_apis: 4
  showcase_pages:
    - "/showcase/twilio"
    - "/showcase/assemblyai"
    - "/showcase/videosdk"
    - "/showcase/nexhealth"
  last_synced: "2025-11-04T10:00:00Z"
```

---

## 🔄 Workflow: Build → Test → Showcase

### **Step 1: Build API Integration**

**Developer builds:**
- MCP server (`lbx_mcp_universe_mcp_servers_mothership/servers/twilio_hipaa/`)
- Backend endpoint (`backend/api/routers/apis.py`)
- Frontend component (`frontend/src/components/showcase/APIShowcase.tsx`)

**Then registers in `central/api-registry.yaml`:**

```yaml
apis:
  new_api:
    name: "New API"
    status: "active"
    frontend_showcase: true  # ← This triggers frontend integration
```

---

### **Step 2: Write Tests**

**Developer creates:**
- Test file (`tests/api/test_new_api.py`)

**Test automatically:**
- Runs via `test-runner.py`
- Updates `api-registry.yaml` with results
- Triggers frontend sync

---

### **Step 3: Frontend Auto-Sync**

**`frontend-sync.py` automatically:**
1. Reads `api-registry.yaml`
2. Updates frontend data files
3. Regenerates showcase components
4. Updates dashboard

**Frontend shows:**
- ✅ Real API status
- ✅ Real test results
- ✅ Real progress
- ✅ Interactive demos

---

## 🛠️ Implementation

### **1. API Registry (`central/api-registry.yaml`)**

**Purpose:** Single source of truth

**Contains:**
- All APIs and their status
- All endpoints and test results
- Frontend integration status
- Test coverage

**Updated by:**
- `test-runner.py` (test results)
- `api-manager.py` (API status)
- Manual (new APIs)

---

### **2. Test Runner (`central/test-runner.py`)**

**Purpose:** Run all tests and update registry

**What it does:**
```python
# 1. Discover all tests
tests = discover_tests("tests/api/")

# 2. Run tests
results = run_tests(tests)

# 3. Update registry
update_registry("central/api-registry.yaml", results)

# 4. Trigger frontend sync
sync_frontend()
```

**Run:**
```bash
cd central
python test-runner.py
```

---

### **3. Frontend Sync (`central/frontend-sync.py`)**

**Purpose:** Sync test results → frontend

**What it does:**
```python
# 1. Read registry
registry = load_yaml("central/api-registry.yaml")

# 2. Generate frontend data
frontend_data = generate_frontend_data(registry)

# 3. Write to frontend
write_json("frontend/src/data/api-status.json", frontend_data)

# 4. Update showcase components
update_showcase_components(registry)
```

**Run:**
```bash
cd central
python frontend-sync.py
```

---

### **4. API Manager (`central/api-manager.py`)**

**Purpose:** Manage API connections and status

**What it does:**
- Check API health
- Verify credentials
- Test endpoints
- Update registry

**Run:**
```bash
cd central
python api-manager.py --check-all
```

---

## 📊 Frontend Showcase Components

### **1. APIShowcase Component**

**Purpose:** Show real API status and test results

**Location:** `frontend/src/components/showcase/APIShowcase.tsx`

**Shows:**
- ✅ API status (active/inactive)
- ✅ Endpoint test results
- ✅ Test coverage
- ✅ Interactive demo (if available)

**Data Source:** `frontend/src/data/api-status.json` (synced from registry)

---

### **2. TestShowcase Component**

**Purpose:** Show real test results

**Location:** `frontend/src/components/showcase/TestShowcase.tsx`

**Shows:**
- ✅ Test pass/fail status
- ✅ Test coverage percentage
- ✅ Last test run time
- ✅ Test history

---

### **3. ProgressShowcase Component**

**Purpose:** Show overall progress

**Location:** `frontend/src/components/showcase/ProgressShowcase.tsx`

**Shows:**
- ✅ Total APIs integrated
- ✅ Total tests passing
- ✅ Overall coverage
- ✅ Progress timeline

---

### **4. Showcase Page**

**Purpose:** Main showcase page

**Location:** `frontend/src/pages/Showcase.tsx`

**Shows:**
- All APIs with real status
- All tests with real results
- Interactive demos
- Progress metrics

---

## 🔄 Development Cycle

### **Every Feature:**

```
1. Build API Integration
   ↓
2. Register in api-registry.yaml
   ↓
3. Write Tests
   ↓
4. Run test-runner.py
   ↓
5. Auto-update api-registry.yaml
   ↓
6. Run frontend-sync.py
   ↓
7. Frontend shows real status
   ↓
8. Deploy & Showcase
```

---

## 🎯 Example: Adding New API

### **Step 1: Build MCP Server**

```bash
# Create MCP server
cd lbx_mcp_universe_mcp_servers_mothership/servers/
mkdir new_api
# ... build server
```

---

### **Step 2: Register in Registry**

```yaml
# central/api-registry.yaml
apis:
  new_api:
    name: "New API"
    status: "active"
    frontend_showcase: true  # ← Enable showcase
```

---

### **Step 3: Write Tests**

```python
# tests/api/test_new_api.py
def test_new_api_endpoint():
    # Test implementation
    assert result == expected
```

---

### **Step 4: Run Test Runner**

```bash
cd central
python test-runner.py
# Updates api-registry.yaml automatically
```

---

### **Step 5: Sync Frontend**

```bash
cd central
python frontend-sync.py
# Updates frontend automatically
```

---

### **Step 6: Frontend Shows**

- ✅ API status
- ✅ Test results
- ✅ Interactive demo

---

## 📋 Backend API Endpoints

### **GET `/api/v1/central/apis`**

**Returns:** All APIs from registry

**Response:**
```json
{
  "apis": [
    {
      "name": "twilio_hipaa",
      "status": "active",
      "tests": {
        "total": 5,
        "passed": 5,
        "failed": 0
      },
      "frontend": {
        "integrated": true,
        "showcase_page": "/showcase/twilio"
      }
    }
  ]
}
```

---

### **GET `/api/v1/central/tests`**

**Returns:** All test results

**Response:**
```json
{
  "summary": {
    "total_tests": 23,
    "passed": 23,
    "failed": 0,
    "coverage": "100%"
  },
  "results": [...]
}
```

---

### **POST `/api/v1/central/sync`**

**Purpose:** Trigger frontend sync

**Response:**
```json
{
  "status": "synced",
  "apis_updated": 4,
  "frontend_updated": true
}
```

---

## 🚀 Quick Start

### **1. Setup Central Workflow**

```bash
# Create central directory
mkdir -p central tests/api tests/mcp tests/e2e

# Create api-registry.yaml
touch central/api-registry.yaml

# Create scripts
touch central/test-runner.py
touch central/frontend-sync.py
touch central/api-manager.py
```

---

### **2. Run Test Runner**

```bash
cd central
python test-runner.py
# Discovers tests, runs them, updates registry
```

---

### **3. Sync Frontend**

```bash
cd central
python frontend-sync.py
# Syncs registry → frontend
```

---

### **4. View Showcase**

```bash
cd frontend
npm run dev
# Open http://localhost:3000/showcase
```

---

## ✅ Benefits

**1. DRY (Don't Repeat Yourself)**
- Single source of truth (`api-registry.yaml`)
- No duplicate API definitions
- No duplicate test results

**2. Real Work Showcase**
- Every API is visible on frontend
- Every test result is shown
- Real progress is tracked

**3. Automated**
- Tests run automatically
- Frontend syncs automatically
- No manual updates needed

**4. Production-Ready**
- Tests → Frontend → Showcase
- Everything is connected
- Real SaaS quality

---

## 📚 File Reference

| File | Purpose | Updated By |
|------|---------|------------|
| `central/api-registry.yaml` | Single source of truth | test-runner.py, api-manager.py |
| `central/test-runner.py` | Run all tests | Developer |
| `central/frontend-sync.py` | Sync to frontend | test-runner.py, Developer |
| `central/api-manager.py` | Manage APIs | Developer |
| `frontend/src/data/api-status.json` | Frontend data | frontend-sync.py |
| `tests/api/` | API tests | Developer |

---

**Last Updated:** 2025-11-04  
**Status:** Central Workflow - Ready for Implementation

