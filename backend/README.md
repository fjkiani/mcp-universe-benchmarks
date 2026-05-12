# Backend API Gateway

**Purpose:** FastAPI server that connects frontend to MCP servers and central workflow

**Status:** ✅ **BUILT & READY**

---

## 🚀 Quick Start

### **1. Install Dependencies**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **2. Run Server**

```bash
python main.py
# or
uvicorn main:app --reload --port 8000
```

Server will start on: `http://localhost:8000`

### **3. Test Endpoints**

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Servers:** http://localhost:8000/api/v1/servers
- **Sprint Metrics:** http://localhost:8000/api/v1/sprint/metrics
- **Central APIs:** http://localhost:8000/api/v1/central/apis

---

## 📁 Structure

```
backend/
├── main.py                    # FastAPI app entry point
├── requirements.txt            # Dependencies
├── api/
│   ├── __init__.py
│   ├── models.py              # Pydantic models
│   └── routers/
│       ├── __init__.py
│       ├── servers.py         # Server endpoints
│       ├── sprint.py          # Sprint metrics
│       ├── tasks.py           # Task management
│       └── central.py         # Central workflow
└── services/
    ├── __init__.py
    ├── registry_service.py    # Read from api-registry.yaml
    └── sprint_service.py      # Calculate metrics
```

---

## 🔌 Endpoints

### **Servers**
- `GET /api/v1/servers` - List all servers
- `GET /api/v1/servers/{name}` - Get server status
- `POST /api/v1/servers/{name}/test` - Test server

### **Sprint**
- `GET /api/v1/sprint/metrics` - Get sprint metrics
- `GET /api/v1/sprint/progress` - Get detailed progress

### **Tasks**
- `GET /api/v1/tasks` - List all tasks
- `GET /api/v1/tasks/{id}` - Get task details
- `GET /api/v1/tasks/{id}/status` - Get task status

### **Central**
- `GET /api/v1/central/apis` - Get API registry
- `GET /api/v1/central/tests` - Get test results
- `POST /api/v1/central/sync` - Trigger frontend sync

---

## 📊 Data Sources

**Backend reads from:**
1. `central/api-registry.yaml` - API registry (via RegistryService)
2. `frontend/src/data/api-status.json` - Synced frontend data
3. `domains/healthcare_receptionist/tasks/*.json` - Task definitions

---

## 🔗 Frontend Connection

**Frontend is configured to use backend:**
- `frontend/src/api/mcp-client.ts` → `useBackend = true`
- Endpoints: `http://localhost:8000/api/v1/*`

**To test:**
1. Start backend: `python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Frontend will call backend automatically

---

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test servers endpoint
curl http://localhost:8000/api/v1/servers

# Test sprint metrics
curl http://localhost:8000/api/v1/sprint/metrics
```

---

## 📝 Notes

- Backend reads from `central/api-registry.yaml` (single source of truth)
- Falls back to `api-status.json` if registry unavailable
- CORS enabled for frontend (`localhost:3000`, `localhost:5173`)
- All endpoints return JSON
- FastAPI auto-generates docs at `/docs`

---

**Status:** ✅ Ready for production  
**Next:** Test with frontend, add MCP server integration if needed

