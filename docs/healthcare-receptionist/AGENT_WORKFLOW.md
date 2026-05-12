# Agent Workflow Guide - Healthcare Receptionist AI

**Purpose:** Clear separation of responsibilities so multiple agents can work in parallel

**Last Updated:** 2025-11-04

---

## 🎯 Agent Roles

### **Zo (Current Agent) - Tasks & Domain Specialist**

**Focus:** Domain development, MCP servers, tasks, evaluators

**Responsibilities:**
- ✅ Create domain tasks (`domains/healthcare_receptionist/tasks/`)
- ✅ Write evaluators (`domains/healthcare_receptionist/evaluators/`)
- ✅ Build MCP servers (`lbx_mcp_universe_mcp_servers_mothership/servers/`)
- ✅ Domain configuration (`domains/healthcare_receptionist/config.yaml`)
- ✅ Sprint planning & documentation
- ✅ Product architecture decisions

**What Zo Should NOT Do:**
- ❌ Build complex frontend UI (except basic structure)
- ❌ Implement backend API (except planning)
- ❌ Design landing page (except copy)

**Key Files:**
- `domains/healthcare_receptionist/` - Domain tasks & evaluators
- `lbx_mcp_universe_mcp_servers_mothership/servers/` - MCP servers
- `.cursor/rules/healthcare-receptionist/SPRINT_PLAN.md` - Sprint planning
- `.cursor/rules/healthcare-receptionist/PRODUCT_MODULES.md` - Architecture

---

### **Frontend Agent - UI & UX Specialist**

**Focus:** Frontend development, user experience, visualizations

**Responsibilities:**
- ✅ Build React components (`frontend/src/components/`)
- ✅ Create pages (`frontend/src/pages/`)
- ✅ Connect to backend API (`frontend/src/api/mcp-client.ts`)
- ✅ Implement landing page from `LANDING_PAGE.md`
- ✅ Add charts/visualizations (Recharts)
- ✅ Make it responsive & beautiful
- ✅ Add loading states, error handling

**Can Work Independently:**
- ✅ Uses mock data initially (no backend needed)
- ✅ Follows `frontend/FRONTEND_DEVELOPMENT_PLAN.md`
- ✅ Backend API contract defined in `backend/API_GATEWAY_PLAN.md`

**Key Files:**
- `frontend/` - Frontend application
- `frontend/FRONTEND_DEVELOPMENT_PLAN.md` - Development guide
- `.cursor/rules/healthcare-receptionist/LANDING_PAGE.md` - Landing page copy

**First Steps:**
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

**Development Order:**
1. Build common components (Button, Card, Badge)
2. Build chart components (ProgressBar, MetricsChart)
3. Build dashboard components (ServerStatus, SprintMetrics)
4. Create pages (Dashboard, Landing, Servers, Tasks)
5. Connect to backend API (replace mock data)

---

### **Backend Agent - API & Integration Specialist**

**Focus:** Backend API, MCP server integration, data aggregation

**Responsibilities:**
- ✅ Implement FastAPI backend (`backend/`)
- ✅ Connect to MCP servers (`backend/mcp/client.py`)
- ✅ Implement API endpoints (`backend/api/routers/`)
- ✅ Aggregate sprint metrics (`backend/services/`)
- ✅ Handle errors & logging
- ✅ Security (API keys, CORS)

**Can Work Independently:**
- ✅ API contract defined in `backend/API_GATEWAY_PLAN.md`
- ✅ MCP server locations known (`lbx_mcp_universe_mcp_servers_mothership/servers/`)
- ✅ Data sources identified (markdown files, task JSONs)

**Key Files:**
- `backend/` - Backend API
- `backend/API_GATEWAY_PLAN.md` - Implementation guide
- `ARCHITECTURE.md` - System overview

**First Steps:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx python-dotenv
# Create main.py, implement endpoints
uvicorn main:app --reload
# API at http://localhost:8000
```

**Development Order:**
1. Set up FastAPI app (`main.py`)
2. Create basic server endpoints (`api/routers/servers.py`)
3. Implement MCP client (`mcp/client.py`)
4. Connect to one MCP server (test)
5. Add sprint metrics endpoint
6. Add task endpoints
7. Add error handling & logging

---

## 🔄 Workflow: How Agents Work Together

### **Phase 1: Foundation (Current)**

**Zo (Tasks):**
1. ✅ Created domain structure
2. ✅ Built 4 MCP servers
3. ✅ Created 13 tasks
4. ✅ Created frontend skeleton
5. ✅ Created backend plan

**Frontend Agent:**
1. ✅ Frontend structure exists
2. ⏳ Build components (can use mock data)
3. ⏳ Build landing page
4. ⏳ Connect to backend when ready

**Backend Agent:**
1. ⏳ Implement FastAPI backend
2. ⏳ Connect to MCP servers
3. ⏳ Implement API endpoints

---

### **Phase 2: Integration**

**Frontend Agent:**
1. Replace mock data with API calls
2. Test with backend
3. Add error handling
4. Polish UI

**Backend Agent:**
1. Test API endpoints
2. Fix CORS issues
3. Add error handling
4. Optimize performance

**Zo (Tasks):**
1. Add more tasks as needed
2. Test domain with integrations
3. Update documentation

---

## 📋 Communication Protocol

### **How Frontend Agent Knows What to Build:**

1. **Read `ARCHITECTURE.md`**
   - Understand system overview
   - See component connections
   - Understand data flow

2. **Read `frontend/FRONTEND_DEVELOPMENT_PLAN.md`**
   - Component architecture
   - Development guidelines
   - API integration steps

3. **Read `backend/API_GATEWAY_PLAN.md`**
   - API endpoint specifications
   - Request/response formats
   - Know what backend will provide

4. **Read `.cursor/rules/healthcare-receptionist/LANDING_PAGE.md`**
   - Landing page copy
   - Component breakdown
   - Design requirements

---

### **How Backend Agent Knows What to Build:**

1. **Read `ARCHITECTURE.md`**
   - System overview
   - Data flow
   - Component connections

2. **Read `backend/API_GATEWAY_PLAN.md`**
   - FastAPI setup
   - Endpoint specifications
   - MCP integration

3. **Check MCP Server Locations:**
   - `lbx_mcp_universe_mcp_servers_mothership/servers/`
   - Each server has `server.py`, `pyproject.toml`, `server_config.json`

4. **Check Data Sources:**
   - Server status: `lbx_mcp_universe_mcp_servers_mothership/servers/SPRINT_P1_TEST_RESULTS.md`
   - Tasks: `domains/healthcare_receptionist/tasks/*.json`

---

### **How Zo Knows What to Focus On:**

1. **Domain Tasks:**
   - `domains/healthcare_receptionist/tasks/` - Add more tasks
   - `domains/healthcare_receptionist/evaluators/` - Improve evaluators

2. **MCP Servers:**
   - `lbx_mcp_universe_mcp_servers_mothership/servers/` - Build new servers
   - Test existing servers

3. **Documentation:**
   - Update sprint plans
   - Update architecture docs
   - Create new guides as needed

---

## 🚫 What NOT to Do

### **Frontend Agent Should NOT:**
- ❌ Modify domain tasks
- ❌ Modify MCP servers
- ❌ Modify backend code (except if fixing frontend integration)

### **Backend Agent Should NOT:**
- ❌ Modify domain tasks
- ❌ Modify frontend code
- ❌ Modify MCP servers (except integration fixes)

### **Zo Should NOT:**
- ❌ Build complex frontend UI (except basic structure)
- ❌ Implement backend API (except planning)
- ❌ Design landing page (except copy)

---

## ✅ Checklist for Each Agent

### **Frontend Agent Checklist:**

**Setup:**
- [ ] Read `ARCHITECTURE.md`
- [ ] Read `frontend/FRONTEND_DEVELOPMENT_PLAN.md`
- [ ] Run `npm install` in `frontend/`
- [ ] Run `npm run dev` and verify it works

**Components:**
- [ ] Build common components (Button, Card, Badge)
- [ ] Build chart components (ProgressBar, MetricsChart)
- [ ] Build dashboard components (ServerStatus, SprintMetrics)

**Pages:**
- [ ] Build Dashboard page
- [ ] Build Landing page (from `LANDING_PAGE.md`)
- [ ] Build Servers page
- [ ] Build Tasks page

**Integration:**
- [ ] Update API client to use backend URL
- [ ] Replace mock data with API calls
- [ ] Add error handling
- [ ] Add loading states

---

### **Backend Agent Checklist:**

**Setup:**
- [ ] Read `ARCHITECTURE.md`
- [ ] Read `backend/API_GATEWAY_PLAN.md`
- [ ] Set up Python virtual environment
- [ ] Install dependencies (fastapi, uvicorn, etc.)

**Implementation:**
- [ ] Create FastAPI app (`main.py`)
- [ ] Create server endpoints (`api/routers/servers.py`)
- [ ] Create sprint endpoints (`api/routers/sprint.py`)
- [ ] Create task endpoints (`api/routers/tasks.py`)

**MCP Integration:**
- [ ] Implement MCP client (`mcp/client.py`)
- [ ] Connect to one MCP server (test)
- [ ] Connect to all MCP servers
- [ ] Test tool calls

**Polish:**
- [ ] Add error handling
- [ ] Add logging
- [ ] Add CORS configuration
- [ ] Test with frontend

---

### **Zo (Tasks) Checklist:**

**Domain:**
- [ ] Add more tasks to domain
- [ ] Improve evaluators
- [ ] Test domain with CI/CD
- [ ] Update domain documentation

**MCP Servers:**
- [ ] Build new MCP servers as needed
- [ ] Test existing servers
- [ ] Update server documentation

**Documentation:**
- [ ] Update sprint plans
- [ ] Update architecture docs
- [ ] Create guides for other agents

---

## 🔗 Key Integration Points

### **Frontend ↔ Backend**

**Contract:** REST API
- Frontend calls: `http://localhost:8000/api/v1/*`
- Backend serves: FastAPI endpoints
- Protocol: HTTP/JSON

**Frontend Agent:**
- Update `frontend/src/api/mcp-client.ts` to use backend URL
- Handle API responses
- Display data in components

**Backend Agent:**
- Implement endpoints as specified in `API_GATEWAY_PLAN.md`
- Return data in expected format
- Handle CORS for frontend

---

### **Backend ↔ MCP Servers**

**Contract:** MCP Protocol
- Backend spawns MCP servers as subprocesses
- Communicates via stdio
- Protocol: JSON-RPC over stdio

**Backend Agent:**
- Implement MCP client in `backend/mcp/client.py`
- Connect to servers in `lbx_mcp_universe_mcp_servers_mothership/servers/`
- Handle tool calls

**Zo (Tasks):**
- Ensure MCP servers are properly structured
- Update server documentation
- Test servers independently

---

## 📚 Reference Documents

| Document | Purpose | For Who |
|----------|---------|---------|
| `ARCHITECTURE.md` | System overview | Everyone |
| `frontend/FRONTEND_DEVELOPMENT_PLAN.md` | Frontend guide | Frontend Agent |
| `backend/API_GATEWAY_PLAN.md` | Backend guide | Backend Agent |
| `.cursor/rules/healthcare-receptionist/LANDING_PAGE.md` | Landing page copy | Frontend Agent |
| `.cursor/rules/healthcare-receptionist/SPRINT_PLAN.md` | Sprint planning | Zo |
| `.cursor/rules/healthcare-receptionist/PRODUCT_MODULES.md` | Module architecture | Zo |

---

**Last Updated:** 2025-11-04  
**Status:** Agent Workflow Guide - Ready for Multi-Agent Development

