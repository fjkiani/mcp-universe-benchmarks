# Backend API Gateway - Development Plan

**Purpose:** Create backend API server that connects frontend to MCP servers

**Technology:** FastAPI (Python) or Express.js (Node.js)

---

## 🏗️ Architecture

```
Frontend (Vite.js)
    ↓ HTTP/REST
API Gateway (FastAPI/Express)
    ↓ MCP Protocol
MCP Servers (twilio_hipaa, assemblyai, videosdk, nexhealth)
    ↓ HTTP/REST
External APIs (Twilio, AssemblyAI, VideoSDK, NexHealth)
```

---

## 📋 API Endpoints

### **1. Server Management**

**GET `/api/v1/servers`**
- List all MCP servers
- Return server status, tools, capabilities

**Response:**
```json
{
  "servers": [
    {
      "name": "twilio_hipaa",
      "status": "ready",
      "structure": true,
      "syntax": true,
      "apiKeys": true,
      "dependencies": true,
      "testsPassed": 5,
      "testsFailed": 0,
      "tools": ["send_hipaa_sms", "make_voice_call", "get_call_status", "check_phi_in_message", "validate_phone_number"],
      "lastTested": "2025-11-04T10:00:00Z"
    }
  ]
}
```

**GET `/api/v1/servers/:name`**
- Get specific server details
- Return status, tools, test results

**POST `/api/v1/servers/:name/test`**
- Test a specific server
- Run structure, syntax, API key checks
- Return test results

**POST `/api/v1/servers/:name/tools/:tool`**
- Call a specific MCP tool
- Forward to MCP server
- Return response

---

### **2. Sprint Metrics**

**GET `/api/v1/sprint/metrics`**
- Get overall sprint metrics
- Pass rate, task completion, server status

**Response:**
```json
{
  "currentSprint": "P1",
  "passRate": 75.5,
  "tasksCompleted": 8,
  "tasksTotal": 13,
  "serversTested": 4,
  "serversTotal": 4,
  "priorities": [
    {
      "id": "p1-test-servers",
      "name": "Test & Validate Servers",
      "status": "completed",
      "tasks": 5,
      "completed": 5
    }
  ]
}
```

**GET `/api/v1/sprint/progress`**
- Get detailed sprint progress
- Timeline, milestones, blockers

---

### **3. Task Management**

**GET `/api/v1/tasks`**
- List all tasks
- Filter by category, status, server

**Response:**
```json
{
  "tasks": [
    {
      "id": "patient_intake_basic_001",
      "name": "Basic Patient Intake",
      "category": "patient_intake",
      "status": "completed",
      "servers": ["calendar", "email"],
      "passRate": 100,
      "lastTested": "2025-11-04T10:00:00Z"
    }
  ]
}
```

**GET `/api/v1/tasks/:id`**
- Get specific task details
- Return task definition, test results, evaluators

**GET `/api/v1/tasks/:id/status`**
- Get task status
- Last test result, pass/fail, metrics

---

### **4. EHR Operations** (Future)

**GET `/api/v1/ehr/appointments`**
- List appointments
- Filter by provider, date, status

**POST `/api/v1/ehr/appointments`**
- Book appointment
- Via NexHealth MCP server

**GET `/api/v1/ehr/providers/:id/availability`**
- Check provider availability
- Via NexHealth MCP server

---

### **5. Communication Operations** (Future)

**POST `/api/v1/communication/sms`**
- Send SMS
- Via Twilio HIPAA MCP server

**POST `/api/v1/communication/call`**
- Make voice call
- Via Twilio HIPAA MCP server

**POST `/api/v1/communication/transcribe`**
- Transcribe audio
- Via AssemblyAI MCP server

---

## 🔧 Implementation

### **Option A: FastAPI (Python)** ⭐ Recommended

**Why:**
- Python ecosystem (matches MCP servers)
- Easy MCP server integration
- Fast development
- Good documentation

**Structure:**
```
backend/
├── main.py                 # FastAPI app
├── api/
│   ├── __init__.py
│   ├── routers/
│   │   ├── servers.py     # Server endpoints
│   │   ├── sprint.py       # Sprint endpoints
│   │   ├── tasks.py        # Task endpoints
│   │   └── ehr.py          # EHR endpoints (future)
│   └── models.py          # Pydantic models
├── mcp/
│   ├── __init__.py
│   ├── client.py          # MCP client
│   └── servers.py         # Server registry
├── services/
│   ├── __init__.py
│   ├── sprint_service.py  # Sprint logic
│   └── task_service.py    # Task logic
├── requirements.txt
└── README.md
```

**Dependencies:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
httpx==0.25.0
python-dotenv==1.0.0
```

---

### **Option B: Express.js (Node.js)**

**Why:**
- JavaScript ecosystem
- Fast development
- Good for real-time features

**Structure:**
```
backend/
├── index.js               # Express app
├── routes/
│   ├── servers.js
│   ├── sprint.js
│   ├── tasks.js
│   └── ehr.js
├── services/
│   ├── mcp-client.js
│   ├── sprint-service.js
│   └── task-service.js
├── package.json
└── README.md
```

---

## 🔌 MCP Server Integration

### **MCP Client**

**Purpose:** Connect to MCP servers and call tools

**Implementation:**
```python
# mcp/client.py
from mcp import ClientSession, StdioServerParameters
import asyncio

class MCPClient:
    def __init__(self):
        self.servers = {}
    
    async def connect_server(self, server_name: str, command: list):
        """Connect to an MCP server"""
        params = StdioServerParameters(
            command=command[0],
            args=command[1:]
        )
        session = await ClientSession.create(params)
        self.servers[server_name] = session
        return session
    
    async def call_tool(self, server_name: str, tool_name: str, params: dict):
        """Call an MCP tool"""
        session = self.servers[server_name]
        result = await session.call_tool(tool_name, params)
        return result
```

---

## 📊 Data Sources

### **1. Server Status**
- Read from `SPRINT_P1_TEST_RESULTS.md`
- Parse markdown or JSON
- Cache in memory, update on request

### **2. Sprint Metrics**
- Calculate from server status
- Aggregate task completion
- Compute pass rates

### **3. Task Status**
- Read from domain task files
- Parse JSON task definitions
- Get test results from CI/CD

---

## 🚀 Quick Start

### **1. Create FastAPI App**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx python-dotenv
```

### **2. Create `main.py`**

```python
from fastapi import FastAPI
from api.routers import servers, sprint, tasks

app = FastAPI(title="Healthcare Receptionist AI API")

app.include_router(servers.router, prefix="/api/v1/servers", tags=["servers"])
app.include_router(sprint.router, prefix="/api/v1/sprint", tags=["sprint"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Healthcare Receptionist AI API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **3. Run Server**

```bash
python main.py
# or
uvicorn main:app --reload
```

---

## 🔒 Security

### **Authentication**
- JWT tokens for API access
- API keys for MCP server access
- Environment variables for secrets

### **CORS**
- Allow frontend origin
- Configure in FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Example Endpoint

```python
# api/routers/servers.py
from fastapi import APIRouter, HTTPException
from api.models import ServerStatus
from services.sprint_service import get_server_statuses

router = APIRouter()

@router.get("", response_model=list[ServerStatus])
async def list_servers():
    """List all MCP servers"""
    servers = await get_server_statuses()
    return servers

@router.get("/{server_name}", response_model=ServerStatus)
async def get_server(server_name: str):
    """Get specific server status"""
    server = await get_server_status(server_name)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.post("/{server_name}/test")
async def test_server(server_name: str):
    """Test a server"""
    result = await test_server_internal(server_name)
    return result
```

---

## 🧪 Testing

### **Unit Tests**
- Test each endpoint
- Mock MCP server responses
- Test error handling

### **Integration Tests**
- Test with real MCP servers (sandbox)
- Test end-to-end flows
- Test error scenarios

---

## 📋 Development Checklist

### **Phase 1: Basic API**
- [ ] Set up FastAPI project
- [ ] Create server endpoints
- [ ] Connect to MCP servers
- [ ] Return server status

### **Phase 2: Sprint Metrics**
- [ ] Create sprint endpoints
- [ ] Calculate metrics
- [ ] Return sprint data

### **Phase 3: Task Management**
- [ ] Create task endpoints
- [ ] Parse task files
- [ ] Return task status

### **Phase 4: Frontend Integration**
- [ ] Test with frontend
- [ ] Fix CORS issues
- [ ] Add error handling
- [ ] Add logging

---

## 🔗 Integration with Frontend

**Frontend calls:**
```typescript
// Frontend API client
const response = await axios.get('http://localhost:8000/api/v1/servers')
```

**Backend responds:**
```json
{
  "servers": [...]
}
```

**Frontend renders:**
- Server status cards
- Sprint metrics
- Task progress

---

**Last Updated:** 2025-11-04  
**Status:** API Gateway Plan - Ready for Implementation

