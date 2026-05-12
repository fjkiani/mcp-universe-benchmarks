# 🤖 Agent-Powered Demo Plan

## 🎯 **Goal**
Build demos that showcase AI agent capabilities, showing how agents work together, using test data (except telehealth which is real).

---

## 🏗️ **Architecture: Agent Layer on Top**

### **Current (Direct MCP Calls):**
```
Frontend → Backend API → MCP Server Tool → Response
```

### **New (Agent-Powered):**
```
Frontend → Backend API → AI Agent → Uses MCP Tools → Response
```

**Key Difference:** Agents add intelligence, routing, and coordination!

---

## 📋 **Demo Capabilities to Showcase**

### **1. Receptionist Agent** 👩‍💼
**Demo:** "Patient calls in, agent handles intake and routes"
- **Input:** Natural language request
- **Agent:** Receptionist Agent receives, processes, routes
- **MCP Tools Used:** `nexhealth.create_patient()` (test data)
- **Output:** Patient created, routed to appropriate next step

### **2. Scheduling Agent** 📅
**Demo:** "Agent books appointment intelligently"
- **Input:** "I need an appointment next week"
- **Agent:** Scheduling Agent checks availability, books
- **MCP Tools Used:** `nexhealth.check_provider_availability()`, `nexhealth.book_appointment()` (test data)
- **Output:** Appointment booked, confirmation sent

### **3. Insurance Agent** 💳
**Demo:** "Agent verifies insurance automatically"
- **Input:** Patient ID + procedure code
- **Agent:** Insurance Agent verifies eligibility
- **MCP Tools Used:** `nexhealth.verify_insurance_eligibility()` (test data)
- **Output:** Coverage status, benefits, prior auth requirements

### **4. Triage Agent** 🚨
**Demo:** "Agent assesses urgency and routes appropriately"
- **Input:** Patient symptoms
- **Agent:** Triage Agent assesses urgency
- **MCP Tools Used:** None (agent reasoning)
- **Output:** Urgency level, routing decision (911/ER vs routine)

### **5. Telehealth Coordinator** 📹 (REAL - Production)
**Demo:** "Agent coordinates video consultation"
- **Input:** Patient + Provider IDs
- **Agent:** Telehealth Coordinator creates room, manages session
- **MCP Tools Used:** `videosdk.create_room()`, `videosdk.start_recording()`, `assemblyai.transcribe_medical()` (REAL APIs)
- **Output:** Video room, recording, transcription stored

### **6. Communication Agent** 💬
**Demo:** "Agent sends HIPAA-compliant messages"
- **Input:** Message content + patient ID
- **Agent:** Communication Agent checks for PHI, sends
- **MCP Tools Used:** `twilio_hipaa.send_sms()` (test data)
- **Output:** Message sent, PHI filtered if detected

---

## 🔄 **Multi-Agent Workflows**

### **Workflow 1: Complete Patient Journey**
```
1. Patient calls → Receptionist Agent
2. Receptionist Agent → Creates patient (test data)
3. Receptionist Agent → Routes to Scheduling Agent
4. Scheduling Agent → Books appointment (test data)
5. Scheduling Agent → Routes to Insurance Agent
6. Insurance Agent → Verifies coverage (test data)
7. Insurance Agent → Routes to Communication Agent
8. Communication Agent → Sends confirmation (test data)
```

**Shows:** Agent coordination, routing, workflow orchestration

### **Workflow 2: Urgent Triage**
```
1. Patient reports symptoms → Receptionist Agent
2. Receptionist Agent → Routes to Triage Agent
3. Triage Agent → Assesses urgency (agent reasoning)
4. If urgent → Routes to Communication Agent → Sends 911 alert (test)
5. If routine → Routes to Scheduling Agent → Books appointment (test)
```

**Shows:** Agent decision-making, safety-critical routing

### **Workflow 3: Telehealth Session**
```
1. Appointment scheduled → Telehealth Coordinator
2. Telehealth Coordinator → Creates video room (REAL)
3. Telehealth Coordinator → Manages session (REAL)
4. Telehealth Coordinator → Transcribes recording (REAL)
5. Telehealth Coordinator → Stores in database (REAL)
```

**Shows:** Real production capability with agent orchestration

---

## 🛠️ **Implementation Plan**

### **Phase 1: Agent Integration Layer** (Backend)

**File:** `backend/services/agent_service.py` (NEW)

```python
from lbx_cli.mcpuniverse.agent.react import ReAct
from lbx_cli.mcpuniverse.workflows.router import Router
from lbx_cli.mcpuniverse.workflows.orchestrator import Orchestrator
from lbx_cli.mcpuniverse.llm import LabelboxModel as LiteLLMProxyClient  # YAML kind: llm → type: litellm
from lbx_cli.mcpuniverse.mcp.manager import MCPManager

class HealthcareAgentService:
    """Service to execute healthcare agents"""
    
    def __init__(self):
        # Load agent config from domain
        self.agent_config = self._load_agent_config()
        self.mcp_manager = MCPManager(config="central/mcp-config.yaml")
        
    async def execute_receptionist_agent(self, user_request: str):
        """Execute Receptionist Agent"""
        agent = ReAct(config=self.agent_config)
        response = await agent.execute(user_request)
        return response
    
    async def execute_scheduling_agent(self, user_request: str):
        """Execute Scheduling Agent"""
        # Agent uses nexhealth tools
        agent = ReAct(config=self.agent_config)
        response = await agent.execute(user_request)
        return response
    
    # ... other agents
```

### **Phase 2: Agent-Powered Demo Endpoints** (Backend)

**File:** `backend/api/routers/agent_demo.py` (NEW)

```python
@router.post("/agent/patient-journey")
async def complete_patient_journey(request: PatientJourneyRequest):
    """
    Complete patient journey using multiple agents
    
    Input:
    {
      "patient_name": "John Doe",
      "request": "I need to schedule an appointment for a checkup"
    }
    
    Flow:
    1. Receptionist Agent → Creates patient (test data)
    2. Scheduling Agent → Books appointment (test data)
    3. Insurance Agent → Verifies coverage (test data)
    4. Communication Agent → Sends confirmation (test data)
    
    Returns workflow trace showing agent coordination
    """
    # Use Orchestrator to coordinate multiple agents
    orchestrator = Orchestrator(agents=[...])
    result = await orchestrator.execute(request.request)
    return {"workflow": result, "agents_used": [...]}
```

### **Phase 3: Frontend Agent Demo Pages** (Frontend)

**File:** `frontend/src/pages/demo/AgentDemoPage.jsx` (NEW)

```jsx
// Show agent-powered workflows
// Display agent reasoning, tool calls, coordination
// Show test data vs real data clearly
```

---

## 📊 **Test Data Strategy**

### **What Uses Test Data:**
- ✅ Patient creation (NexHealth mock)
- ✅ Appointment booking (NexHealth mock)
- ✅ Insurance verification (NexHealth mock)
- ✅ SMS sending (Twilio mock)
- ✅ Agent routing and coordination (all test)

### **What Uses Real Data:**
- ✅ Video room creation (VideoSDK real)
- ✅ Video recording (VideoSDK real)
- ✅ Transcription (AssemblyAI real)
- ✅ Database storage (PostgreSQL real)

---

## 🎯 **Demo Showcases**

### **Demo 1: Single Agent - Scheduling**
**Page:** `/demo/agent-scheduling`
- User: "I need an appointment next Tuesday"
- **Scheduling Agent** processes request
- Shows: Agent reasoning, tool calls, result
- Uses: Test data (mock NexHealth)

### **Demo 2: Multi-Agent - Patient Journey**
**Page:** `/demo/agent-patient-journey`
- User: "I'm a new patient, need a checkup"
- **Receptionist Agent** → **Scheduling Agent** → **Insurance Agent** → **Communication Agent**
- Shows: Agent coordination, workflow trace
- Uses: Test data (all mocks)

### **Demo 3: Safety-Critical - Triage**
**Page:** `/demo/agent-triage`
- User: "I have chest pain"
- **Triage Agent** assesses urgency
- Shows: Agent decision-making, routing logic
- Uses: Agent reasoning (no tools needed)

### **Demo 4: Production - Telehealth**
**Page:** `/demo/agent-telehealth`
- User: Creates video consultation
- **Telehealth Coordinator** manages session
- Shows: Real video, real transcription
- Uses: Real APIs (VideoSDK, AssemblyAI)

---

## 🔧 **Technical Implementation**

### **Step 1: Integrate Agent Framework**
```python
# backend/services/agent_service.py
from lbx_cli.mcpuniverse.agent.react import ReAct
from domains.healthcare_receptionist.config import load_config

class HealthcareAgentService:
    def __init__(self):
        config = load_config("domains/healthcare_receptionist/config.yaml")
        self.agent = ReAct(config=config)
        self.mcp_manager = MCPManager(config="central/mcp-config.yaml")
```

### **Step 2: Create Agent Endpoints**
```python
# backend/api/routers/agent_demo.py
@router.post("/agent/schedule")
async def agent_schedule(request: ScheduleRequest):
    agent_service = HealthcareAgentService()
    response = await agent_service.execute_scheduling_agent(
        f"Schedule appointment for {request.patient_id} on {request.date}"
    )
    return {"agent_response": response, "tools_used": [...]}
```

### **Step 3: Frontend Integration**
```jsx
// frontend/src/pages/demo/AgentScheduling.jsx
const handleAgentRequest = async (userRequest) => {
  const response = await fetch('/api/v1/agent/schedule', {
    method: 'POST',
    body: JSON.stringify({ request: userRequest })
  })
  // Show agent reasoning, tool calls, result
}
```

---

## ✅ **What This Achieves**

### **Shows:**
- ✅ **Agent Intelligence** - How agents reason and make decisions
- ✅ **Agent Routing** - How Receptionist Agent routes to specialists
- ✅ **Agent Coordination** - How multiple agents work together
- ✅ **Tool Usage** - How agents use MCP tools intelligently
- ✅ **Workflow Orchestration** - Complete patient journeys

### **Uses:**
- ✅ **Test Data** - Safe, no real API costs for most demos
- ✅ **Real Data** - Telehealth is production-ready
- ✅ **Agent Framework** - Actual agent execution, not mocks

---

## 🚀 **Implementation Steps**

### **Week 1: Agent Integration**
1. Create `backend/services/agent_service.py`
2. Integrate domain agent config
3. Connect to MCP manager
4. Test single agent execution

### **Week 2: Agent Endpoints**
1. Create `backend/api/routers/agent_demo.py`
2. Build single-agent endpoints
3. Build multi-agent workflows
4. Add workflow tracing

### **Week 3: Frontend Demos**
1. Create agent demo pages
2. Show agent reasoning
3. Display tool calls
4. Visualize workflows

### **Week 4: Polish & Testing**
1. Test all workflows
2. Add error handling
3. Improve UI/UX
4. Document everything

---

## 📋 **File Structure**

```
backend/
├── services/
│   ├── agent_service.py          # NEW - Agent execution service
│   └── mcp_client_service.py     # Existing - MCP tool calls
├── api/routers/
│   ├── agent_demo.py              # NEW - Agent-powered endpoints
│   └── healthcare_demo.py        # Existing - Direct MCP calls (keep for comparison)

frontend/
├── src/pages/demo/
│   ├── AgentDemoPage.jsx         # NEW - Main agent demo hub
│   ├── AgentScheduling.jsx      # NEW - Scheduling agent demo
│   ├── AgentPatientJourney.jsx   # NEW - Multi-agent workflow
│   ├── AgentTriage.jsx           # NEW - Triage agent demo
│   └── VideoConsultation.jsx     # Existing - Keep (real telehealth)
```

---

## 🎯 **Success Criteria**

- ✅ Agents actually execute (not mocked)
- ✅ Agent reasoning visible to user
- ✅ Tool calls shown clearly
- ✅ Multi-agent workflows work
- ✅ Test data used safely
- ✅ Telehealth remains real/production
- ✅ Clear explanation of how everything connects

---

## 💡 **Key Insight**

**Current:** Direct MCP tool calls (tool showcase)  
**New:** Agent-powered workflows (intelligence showcase)

**The difference:** Agents add reasoning, routing, and coordination that direct tool calls don't have!

---

**This plan shows how agents work together, uses test data safely, and keeps telehealth real!** 🚀

