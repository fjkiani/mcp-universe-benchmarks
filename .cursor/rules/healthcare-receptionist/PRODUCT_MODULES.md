# Product Modules - Healthcare Receptionist AI

**Purpose:** Modular structure for building and enhancing the Healthcare Receptionist AI product

**⚠️ IMPORTANT:** This document shows the PRODUCT architecture. For system architecture and agent workflows, see:
- `ARCHITECTURE.md` - Complete system overview
- `.cursor/rules/healthcare-receptionist/AGENT_WORKFLOW.md` - Agent responsibilities

---

## 🏗️ Module Architecture

```
product/
├── core/                    # Core AI agent capabilities
│   ├── receptionist-agent/  # Main AI agent
│   ├── triage-engine/       # Safety-critical triage
│   └── workflow-orchestrator/ # Multi-step workflows
│
├── integrations/           # External integrations
│   ├── ehr/                # EHR integrations
│   │   ├── nexhealth/      # NexHealth (80+ EHRs)
│   │   ├── epic/           # Epic FHIR
│   │   └── cerner/         # Cerner FHIR
│   ├── communication/      # Communication APIs
│   │   ├── twilio-hipaa/   # SMS/Voice
│   │   ├── videosdk/       # Video consultations
│   │   └── assemblyai/     # Transcription
│   ├── insurance/          # Insurance verification
│   │   ├── availity/       # Real-time eligibility
│   │   └── change-healthcare/ # Claims processing
│   └── identity/           # Identity verification
│       └── id-me/          # Patient identity
│
├── compliance/              # Compliance & security
│   ├── hipaa/              # HIPAA compliance
│   ├── phi-detection/      # PHI detection engine
│   └── audit-logging/      # Audit trail
│
├── frontend/               # User interfaces
│   ├── dashboard/          # Admin dashboard
│   ├── landing/            # Marketing site
│   └── patient-portal/     # Patient portal (future)
│
└── infrastructure/         # Infrastructure
    ├── api-gateway/        # Backend API
    ├── mcp-servers/        # MCP server wrappers
    └── monitoring/         # Observability
```

---

## 📦 Core Modules

### **1. Receptionist Agent** (`core/receptionist-agent/`)

**Purpose:** Main AI agent that handles patient interactions

**Capabilities:**
- Patient intake
- Appointment scheduling
- Multi-language support
- Context management
- Conversation flow

**Files:**
- `agent.py` - Main agent logic
- `prompts.py` - System prompts
- `context.py` - Conversation context
- `config.yaml` - Agent configuration

**Dependencies:**
- MCP servers (calendar, email, etc.)
- Triage engine (for safety-critical routing)
- Workflow orchestrator (for multi-step tasks)

---

### **2. Triage Engine** (`core/triage-engine/`)

**Purpose:** Safety-critical patient triage (100% accuracy required)

**Capabilities:**
- Emergent condition detection
- Urgency classification
- Routing logic (911/ER vs. routine)
- FHIR Observation creation

**Files:**
- `triage.py` - Triage logic
- `conditions.py` - Condition definitions
- `rules.py` - Safety rules
- `fhir.py` - FHIR integration

**Dependencies:**
- FHIR R4 schemas
- Task management (for clinical alerts)

---

### **3. Workflow Orchestrator** (`core/workflow-orchestrator/`)

**Purpose:** Multi-step workflow management

**Capabilities:**
- Workflow definition
- Step execution
- Error handling
- State management

**Files:**
- `orchestrator.py` - Main orchestrator
- `workflows.py` - Workflow definitions
- `state.py` - State management

**Dependencies:**
- All MCP servers
- Receptionist agent

---

## 🔌 Integration Modules

### **1. EHR Integration** (`integrations/ehr/`)

**NexHealth Module** (`integrations/ehr/nexhealth/`)
- Unified API for 80+ EHR systems
- Real-time appointment sync
- Provider availability
- Patient data access

**Files:**
- `client.py` - NexHealth API client
- `mappers.py` - EHR → FHIR mapping
- `sync.py` - Real-time sync logic

**Epic FHIR Module** (`integrations/ehr/epic/`)
- Epic FHIR R4 integration
- SMART on FHIR auth
- Patient resources
- Appointment resources

**Cerner FHIR Module** (`integrations/ehr/cerner/`)
- Cerner FHIR R4 integration
- Similar to Epic

---

### **2. Communication Integration** (`integrations/communication/`)

**Twilio HIPAA** (`integrations/communication/twilio-hipaa/`)
- SMS sending with PHI detection
- Voice calls
- HIPAA-compliant recording
- Call status tracking

**VideoSDK** (`integrations/communication/videosdk/`)
- Video room creation
- Token generation
- Recording management
- Room management

**AssemblyAI** (`integrations/communication/assemblyai/`)
- Medical transcription
- Entity extraction
- Medical accuracy (93.3%)

---

### **3. Insurance Integration** (`integrations/insurance/`)

**Availity** (`integrations/insurance/availity/`)
- Real-time eligibility verification
- Benefits lookup
- Coverage verification

**Change Healthcare** (`integrations/insurance/change-healthcare/`)
- Claims processing
- Prior authorization
- Benefits verification

---

### **4. Identity Integration** (`integrations/identity/`)

**ID.me** (`integrations/identity/id-me/`)
- Patient identity verification
- Multi-factor authentication
- Secure login

---

## 🛡️ Compliance Modules

### **1. HIPAA Compliance** (`compliance/hipaa/`)

**Purpose:** Ensure HIPAA compliance across all modules

**Files:**
- `baa-manager.py` - BAA tracking
- `encryption.py` - Encryption utilities
- `access-control.py` - Access control
- `audit-logger.py` - Audit logging

---

### **2. PHI Detection** (`compliance/phi-detection/`)

**Purpose:** Detect and handle PHI in communications

**Files:**
- `detector.py` - PHI detection engine
- `patterns.py` - PHI patterns (SSN, MRN, DOB, etc.)
- `sanitizer.py` - PHI sanitization
- `validator.py` - Message validation

---

### **3. Audit Logging** (`compliance/audit-logging/`)

**Purpose:** Track all actions for compliance

**Files:**
- `logger.py` - Audit logger
- `storage.py` - Log storage
- `reports.py` - Compliance reports

---

## 🖥️ Frontend Modules

### **1. Dashboard** (`frontend/dashboard/`)

**Purpose:** Admin dashboard for monitoring and management

**Components:**
- Sprint progress
- Server status
- Task metrics
- Real-time monitoring

**Pages:**
- Dashboard (overview)
- Servers (server status)
- Tasks (task progress)
- Analytics (metrics)

---

### **2. Landing** (`frontend/landing/`)

**Purpose:** Marketing landing page

**Components:**
- Hero section
- Problem statement
- Solution
- Features
- Pricing
- CTA

**Based on:** `LANDING_PAGE.md`

---

## 🏗️ Infrastructure Modules

### **1. API Gateway** (`infrastructure/api-gateway/`)

**Purpose:** Backend API server

**Endpoints:**
- `/api/v1/servers` - MCP server management
- `/api/v1/sprint` - Sprint metrics
- `/api/v1/tasks` - Task management
- `/api/v1/ehr` - EHR operations
- `/api/v1/communication` - Communication operations

**Technology:**
- FastAPI or Express.js
- MCP server connections
- Authentication/Authorization
- Rate limiting

---

### **2. MCP Servers** (`infrastructure/mcp-servers/`)

**Purpose:** MCP server wrappers for external APIs

**Servers:**
- `twilio_hipaa` - Twilio HIPAA
- `assemblyai` - AssemblyAI
- `videosdk` - VideoSDK
- `nexhealth` - NexHealth
- `calendar` - Calendar (existing)
- `email` - Email (existing)
- `task-management` - Task management (existing)

**Location:** `lbx_mcp_universe_mcp_servers_mothership/servers/`

---

### **3. Monitoring** (`infrastructure/monitoring/`)

**Purpose:** Observability and monitoring

**Components:**
- Metrics collection
- Log aggregation
- Error tracking
- Performance monitoring

---

## 📋 Module Development Guidelines

### **For Another Agent:**

1. **Start with Core Modules**
   - Build receptionist agent first
   - Add triage engine
   - Then workflow orchestrator

2. **Add Integrations Incrementally**
   - Start with one integration (NexHealth)
   - Test thoroughly
   - Add next integration

3. **Compliance First**
   - Build HIPAA compliance early
   - Add PHI detection
   - Set up audit logging

4. **Frontend Parallel**
   - Frontend can be built in parallel
   - Connect via API gateway
   - Use mock data initially

5. **Infrastructure Last**
   - API gateway after core modules
   - Monitoring after everything works
   - Deployment after testing

---

## 🔄 Module Dependencies

```
Receptionist Agent
    ├── Triage Engine
    ├── Workflow Orchestrator
    ├── EHR Integration (NexHealth)
    ├── Communication (Twilio, VideoSDK, AssemblyAI)
    ├── Insurance (Availity)
    ├── Identity (ID.me)
    └── Compliance (HIPAA, PHI Detection, Audit)

Workflow Orchestrator
    ├── All MCP Servers
    └── Receptionist Agent

Triage Engine
    ├── FHIR R4
    └── Task Management

EHR Integration
    ├── NexHealth API
    ├── Epic FHIR
    └── Cerner FHIR

Communication
    ├── Twilio HIPAA
    ├── VideoSDK
    └── AssemblyAI

Compliance
    ├── All Modules
    └── Audit Logging
```

---

## 🎯 Module Priority

### **Phase 1: Foundation** (Weeks 1-2)
1. ✅ Core: Receptionist Agent
2. ✅ Core: Triage Engine
3. ✅ Integration: NexHealth
4. ✅ Compliance: HIPAA basics

### **Phase 2: Communication** (Weeks 3-4)
5. ✅ Integration: Twilio HIPAA
6. ✅ Integration: AssemblyAI
7. ✅ Integration: VideoSDK
8. ✅ Compliance: PHI Detection

### **Phase 3: Expansion** (Weeks 5-6)
9. ✅ Integration: Availity
10. ✅ Integration: ID.me
11. ✅ Core: Workflow Orchestrator
12. ✅ Infrastructure: API Gateway

### **Phase 4: Polish** (Weeks 7-8)
13. ✅ Frontend: Dashboard
14. ✅ Frontend: Landing
15. ✅ Infrastructure: Monitoring
16. ✅ Compliance: Full audit logging

---

## 📝 Module Template

Each module should have:

```
module-name/
├── README.md           # Module documentation
├── requirements.txt    # Python dependencies
├── config.yaml        # Configuration
├── tests/             # Unit tests
│   └── test_module.py
├── src/               # Source code
│   ├── __init__.py
│   └── module.py
└── docs/              # Additional docs
    └── api.md
```

---

## 🔗 Module Communication

**Pattern:**
- Modules communicate via MCP protocol
- API Gateway handles routing
- Compliance modules intercept all operations
- Audit logging captures everything

**Example:**
```
Receptionist Agent
    → Calls MCP Tool: "nexhealth/book_appointment"
    → API Gateway routes to NexHealth MCP Server
    → PHI Detection checks message
    → Audit Logger records action
    → Response returned to Agent
```

---

**Last Updated:** 2025-11-04  
**Status:** Modular Architecture - Ready for Development

