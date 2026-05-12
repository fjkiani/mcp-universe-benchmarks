# Healthcare Receptionist AI - Complete Architecture

**Purpose:** Unified guide showing how all components connect and work together

**Last Updated:** 2025-11-04

---

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vite.js + React)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Dashboard   │  │   Landing    │  │   Servers    │         │
│  │   (Sprint    │  │   (Marketing)│  │   (Status)   │         │
│  │   Metrics)   │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/REST API
                           │ (Port 3000 → 8000)
┌──────────────────────────▼──────────────────────────────────────┐
│              BACKEND API GATEWAY (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  /api/v1/servers  →  Server Status & MCP Management    │   │
│  │  /api/v1/sprint   →  Sprint Metrics & Progress          │   │
│  │  /api/v1/tasks    →  Task Status & Results             │   │
│  │  /api/v1/ehr      →  EHR Operations (Future)           │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ MCP Protocol (stdio/subprocess)
┌──────────────────────────▼──────────────────────────────────────┐
│              MCP SERVERS (FastMCP Wrappers)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ twilio_hipaa │  │  assemblyai  │  │   videosdk   │         │
│  │  (SMS/Voice) │  │ (Transcribe) │  │  (Video)     │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐         │
│  │    nexhealth │  │   calendar    │  │    email     │         │
│  │   (EHR API)  │  │  (Existing)   │  │  (Existing)  │         │
│  └──────┬───────┘  └───────────────┘  └──────────────┘         │
└─────────┼────────────────────────────────────────────────────────┘
          │ HTTP/REST API Calls
┌─────────▼────────────────────────────────────────────────────────┐
│              EXTERNAL APIs                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Twilio    │  │ AssemblyAI   │  │  VideoSDK    │          │
│  │  (SMS/Voice) │  │ (Transcribe) │  │   (Video)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │  NexHealth   │  │   Availity   │                             │
│  │  (80+ EHRs)  │  │  (Insurance) │                             │
│  └──────────────┘  └──────────────┘                             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
lbx_mcp_universe_template-main/
├── frontend/                          # Frontend (Vite.js + React)
│   ├── src/
│   │   ├── components/               # Reusable UI components
│   │   │   ├── common/               # Button, Card, Badge
│   │   │   ├── charts/               # ProgressBar, MetricsChart
│   │   │   ├── dashboard/            # ServerStatus, SprintMetrics
│   │   │   └── landing/              # Hero, Features, Pricing
│   │   ├── pages/                    # Page components
│   │   │   ├── Dashboard.tsx        # Sprint dashboard
│   │   │   ├── Landing.tsx           # Marketing landing page
│   │   │   ├── Servers.tsx           # Server status page
│   │   │   └── Tasks.tsx             # Task progress page
│   │   ├── api/                      # API client
│   │   │   ├── mcp-client.ts         # Backend API client
│   │   │   └── types.ts              # TypeScript types
│   │   └── hooks/                    # React hooks
│   │       └── useSprintData.ts       # Sprint data fetching
│   ├── package.json
│   └── FRONTEND_DEVELOPMENT_PLAN.md  # Frontend dev guide
│
├── backend/                          # Backend API Gateway (FastAPI)
│   ├── api/
│   │   ├── routers/                  # API route handlers
│   │   │   ├── servers.py            # Server endpoints
│   │   │   ├── sprint.py              # Sprint endpoints
│   │   │   └── tasks.py               # Task endpoints
│   │   └── models.py                 # Pydantic models
│   ├── mcp/
│   │   ├── client.py                 # MCP client connection
│   │   └── servers.py                # Server registry
│   ├── services/
│   │   ├── sprint_service.py         # Sprint logic
│   │   └── task_service.py           # Task logic
│   ├── main.py                       # FastAPI app entry
│   └── API_GATEWAY_PLAN.md           # Backend dev guide
│
├── lbx_mcp_universe_mcp_servers_mothership/
│   └── servers/                      # MCP Server Wrappers
│       ├── twilio_hipaa/             # Twilio HIPAA MCP server
│       │   ├── server.py             # FastMCP server implementation
│       │   ├── pyproject.toml        # Dependencies
│       │   └── server_config.json    # Server config
│       ├── assemblyai/               # AssemblyAI MCP server
│       ├── videosdk/                 # VideoSDK MCP server
│       ├── nexhealth/                # NexHealth MCP server
│       ├── calendar/                 # Calendar (existing)
│       ├── email/                    # Email (existing)
│       └── task-management/          # Task management (existing)
│
├── domains/
│   └── healthcare_receptionist/      # Domain Tasks & Evaluators
│       ├── config.yaml               # Domain configuration
│       ├── tasks/                     # Task JSON files
│       │   ├── patient_intake_basic_001.json
│       │   ├── appointment_basic_009.json
│       │   └── ...
│       ├── evaluators/               # Python evaluators
│       │   └── functions.py          # Validation functions
│       └── README.md
│
└── .cursor/rules/
    └── healthcare-receptionist/
        ├── MASTER.md                 # Consolidated docs
        ├── PRODUCT_MODULES.md        # Module architecture
        ├── SPRINT_PLAN.md            # Sprint planning
        └── LANDING_PAGE.md           # Landing page copy
```

---

## 🔄 Data Flow

### **1. Frontend → Backend → MCP Servers**

**Example: Dashboard Loading Server Status**

```
1. Frontend (Dashboard.tsx)
   ↓ useQuery hook
2. API Client (mcp-client.ts)
   ↓ axios.get('/api/v1/servers')
3. Backend API Gateway (servers.py)
   ↓ MCP Client (mcp/client.py)
4. MCP Server (twilio_hipaa/server.py)
   ↓ HTTP API call
5. External API (Twilio)
   ↓ Response
6. Back through chain → Frontend renders ServerStatus component
```

### **2. Sprint Metrics Flow**

```
Frontend Dashboard
  → GET /api/v1/sprint/metrics
  → Backend sprint_service.py
  → Reads: SPRINT_P1_TEST_RESULTS.md (or calculates from data)
  → Aggregates: server status, task completion, pass rates
  → Returns JSON
  → Frontend displays metrics cards
```

### **3. Task Status Flow**

```
Frontend Tasks Page
  → GET /api/v1/tasks
  → Backend task_service.py
  → Reads: domains/healthcare_receptionist/tasks/*.json
  → Gets test results from CI/CD (or local)
  → Returns task list with status
  → Frontend displays task cards
```

---

## 🎯 Why We Created Backend API Gateway

### **Problem Without Backend:**
1. **Frontend can't directly call MCP servers**
   - MCP uses stdio/subprocess, not HTTP
   - Frontend runs in browser, can't spawn processes

2. **No centralized data aggregation**
   - Sprint metrics scattered across files
   - Server status in markdown files
   - Task results in CI/CD

3. **Security concerns**
   - API keys in frontend = exposed
   - Need server-side credential management

### **Solution: Backend API Gateway**

**Benefits:**
- ✅ **Unified API** - Frontend calls REST endpoints
- ✅ **Data aggregation** - Backend reads/calculates metrics
- ✅ **Security** - API keys stay on server
- ✅ **MCP integration** - Backend connects to MCP servers
- ✅ **Caching** - Backend can cache responses
- ✅ **Error handling** - Centralized error management

---

## 🔌 MCP Servers Location & Purpose

**Location:** `lbx_mcp_universe_mcp_servers_mothership/servers/`

**Purpose:** Wrap external APIs in MCP protocol so AI agents can use them

**Why separate folder?**
- MCP servers are reusable across domains
- Isolated from domain-specific code
- Follows MCP server contribution guidelines

**How they connect:**
1. Backend API Gateway spawns MCP servers as subprocesses
2. Communicates via stdio (MCP protocol)
3. MCP servers call external APIs (Twilio, AssemblyAI, etc.)
4. Results returned to backend → frontend

---

## 📋 Agent Responsibilities

### **Zo (Current Agent) - Focus: Tasks & Domain**

**Responsibilities:**
- ✅ Domain task creation (`domains/healthcare_receptionist/tasks/`)
- ✅ Evaluator development (`domains/healthcare_receptionist/evaluators/`)
- ✅ Domain configuration (`domains/healthcare_receptionist/config.yaml`)
- ✅ MCP server development (`lbx_mcp_universe_mcp_servers_mothership/servers/`)
- ✅ Sprint planning & documentation
- ✅ Product architecture

**Not Responsible For:**
- ❌ Frontend UI development (except basic structure)
- ❌ Backend API implementation (except planning)
- ❌ Landing page design

---

### **Frontend Agent - Focus: UI & User Experience**

**Responsibilities:**
- ✅ Build React components (`frontend/src/components/`)
- ✅ Create pages (`frontend/src/pages/`)
- ✅ Connect to backend API (`frontend/src/api/mcp-client.ts`)
- ✅ Implement landing page from `LANDING_PAGE.md`
- ✅ Add charts/visualizations (Recharts)
- ✅ Make it responsive & beautiful
- ✅ Add loading states, error handling

**Can Work Independently:**
- ✅ Uses mock data initially
- ✅ Follows `FRONTEND_DEVELOPMENT_PLAN.md`
- ✅ Backend API contract defined in `API_GATEWAY_PLAN.md`

---

### **Backend Agent - Focus: API & Integration**

**Responsibilities:**
- ✅ Implement FastAPI backend (`backend/`)
- ✅ Connect to MCP servers (`backend/mcp/client.py`)
- ✅ Implement API endpoints (`backend/api/routers/`)
- ✅ Aggregate sprint metrics (`backend/services/`)
- ✅ Handle errors & logging

**Can Work Independently:**
- ✅ API contract defined in `API_GATEWAY_PLAN.md`
- ✅ MCP server locations known
- ✅ Data sources identified

---

## 🚀 Development Workflow

### **Phase 1: Foundation (Current)**

**Zo (Tasks):**
- ✅ Created 13 tasks in `domains/healthcare_receptionist/`
- ✅ Created evaluators for all tasks
- ✅ Built 4 MCP servers (twilio_hipaa, assemblyai, videosdk, nexhealth)
- ✅ Created sprint plan

**Frontend Agent:**
- ✅ Vite.js app structure created
- ✅ Basic components (Button, Card, Badge, ProgressBar)
- ✅ Basic pages (Dashboard, Servers, Tasks)
- ⏳ **Next:** Connect to backend API (mock data for now)

**Backend Agent:**
- ⏳ **Next:** Implement FastAPI backend
- ⏳ **Next:** Connect to MCP servers
- ⏳ **Next:** Implement API endpoints

---

### **Phase 2: Integration**

**Frontend Agent:**
1. Update `mcp-client.ts` to use real backend URL
2. Replace mock data with API calls
3. Add error handling
4. Add loading states

**Backend Agent:**
1. Implement all API endpoints
2. Connect to MCP servers
3. Implement data aggregation
4. Add error handling

**Zo (Tasks):**
1. Add more tasks as needed
2. Test domain with new integrations
3. Update documentation

---

## 📊 Component Connections

### **Frontend Components → Backend Endpoints**

| Frontend Component | Backend Endpoint | Data Source |
|-------------------|------------------|-------------|
| `ServerStatus` | `GET /api/v1/servers` | MCP server status, `SPRINT_P1_TEST_RESULTS.md` |
| `SprintMetrics` | `GET /api/v1/sprint/metrics` | Calculated from server/task data |
| `TaskProgress` | `GET /api/v1/tasks` | `domains/healthcare_receptionist/tasks/*.json` |
| `ServerStatus` detail | `GET /api/v1/servers/:name` | MCP server + test results |

---

### **Backend → MCP Servers**

| Backend Endpoint | MCP Server | External API |
|-----------------|------------|--------------|
| `POST /api/v1/servers/:name/tools/send_hipaa_sms` | `twilio_hipaa` | Twilio API |
| `POST /api/v1/servers/:name/tools/transcribe_medical` | `assemblyai` | AssemblyAI API |
| `POST /api/v1/servers/:name/tools/create_video_room` | `videosdk` | VideoSDK API |
| `POST /api/v1/servers/:name/tools/book_appointment` | `nexhealth` | NexHealth API |

---

## 📝 Documentation Structure

### **For Frontend Agent:**

1. **`frontend/FRONTEND_DEVELOPMENT_PLAN.md`**
   - Component architecture
   - Development guidelines
   - API integration steps

2. **`backend/API_GATEWAY_PLAN.md`**
   - API endpoint specifications
   - Request/response formats
   - Integration examples

3. **`.cursor/rules/healthcare-receptionist/LANDING_PAGE.md`**
   - Landing page copy
   - Component breakdown
   - Design requirements

---

### **For Backend Agent:**

1. **`backend/API_GATEWAY_PLAN.md`**
   - FastAPI setup
   - MCP client integration
   - Endpoint implementation

2. **`ARCHITECTURE.md`** (this file)
   - System overview
   - Data flow
   - Component connections

---

### **For Zo (Tasks Agent):**

1. **`.cursor/rules/healthcare-receptionist/PRODUCT_MODULES.md`**
   - Module architecture
   - Development priorities

2. **`.cursor/rules/healthcare-receptionist/SPRINT_PLAN.md`**
   - Sprint priorities
   - Task breakdown

3. **`ARCHITECTURE.md`** (this file)
   - Overall system understanding

---

## 🔗 Key Integration Points

### **1. Frontend ↔ Backend**

**Contract:** REST API
- Frontend: `frontend/src/api/mcp-client.ts`
- Backend: `backend/api/routers/`
- Protocol: HTTP/JSON
- Port: Frontend 3000 → Backend 8000

---

### **2. Backend ↔ MCP Servers**

**Contract:** MCP Protocol
- Backend: `backend/mcp/client.py`
- MCP Servers: `lbx_mcp_universe_mcp_servers_mothership/servers/`
- Protocol: stdio/subprocess
- Communication: JSON-RPC over stdio

---

### **3. MCP Servers ↔ External APIs**

**Contract:** HTTP/REST
- MCP Servers: `servers/*/server.py`
- External APIs: Twilio, AssemblyAI, VideoSDK, NexHealth
- Protocol: HTTP/REST
- Authentication: API keys (stored in `.env`)

---

### **4. Domain Tasks ↔ Evaluators**

**Contract:** JSON task files + Python evaluators
- Tasks: `domains/healthcare_receptionist/tasks/*.json`
- Evaluators: `domains/healthcare_receptionist/evaluators/functions.py`
- Connection: Task JSON references evaluator function names

---

## 🎯 Quick Start for Each Agent

### **Frontend Agent:**

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

**First Steps:**
1. Read `FRONTEND_DEVELOPMENT_PLAN.md`
2. Update `mcp-client.ts` to use mock data initially
3. Build landing page components from `LANDING_PAGE.md`
4. Connect to backend API when ready

---

### **Backend Agent:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# API at http://localhost:8000
```

**First Steps:**
1. Read `API_GATEWAY_PLAN.md`
2. Implement basic FastAPI app
3. Create server endpoints
4. Connect to MCP servers (start with one)

---

### **Zo (Tasks Agent):**

```bash
# Continue working on domain tasks
cd domains/healthcare_receptionist
# Add new tasks, evaluators, update config.yaml
```

**Focus Areas:**
1. Domain task development
2. Evaluator improvements
3. MCP server enhancements
4. Documentation updates

---

## ✅ Current Status

**Completed:**
- ✅ Frontend structure (Vite.js + React)
- ✅ Basic components (Button, Card, Badge, ProgressBar)
- ✅ Basic pages (Dashboard, Servers, Tasks)
- ✅ 4 MCP servers built (twilio_hipaa, assemblyai, videosdk, nexhealth)
- ✅ 13 domain tasks created
- ✅ Documentation structure

**In Progress:**
- ⏳ Backend API implementation
- ⏳ Frontend-backend integration
- ⏳ Landing page development

**Next:**
- 📋 Backend agent implements FastAPI
- 📋 Frontend agent builds landing page
- 📋 Zo continues domain task development

---

## 📚 Key Files Reference

| File | Purpose | For Who |
|------|---------|---------|
| `ARCHITECTURE.md` | System overview (this file) | Everyone |
| `frontend/FRONTEND_DEVELOPMENT_PLAN.md` | Frontend dev guide | Frontend Agent |
| `backend/API_GATEWAY_PLAN.md` | Backend dev guide | Backend Agent |
| `.cursor/rules/healthcare-receptionist/PRODUCT_MODULES.md` | Module architecture | Zo |
| `.cursor/rules/healthcare-receptionist/LANDING_PAGE.md` | Landing page copy | Frontend Agent |
| `lbx_mcp_universe_mcp_servers_mothership/servers/` | MCP servers | Zo, Backend Agent |

---

**Last Updated:** 2025-11-04  
**Status:** Complete Architecture - Ready for Multi-Agent Development

