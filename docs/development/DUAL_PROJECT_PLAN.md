# Dual Project Management Plan - Healthcare Receptionist + GitLab MLOps

**Purpose:** Manage both projects simultaneously while keeping frontend/backend synced

**Last Updated:** 2025-11-05  
**Status:** Planning phase

---

## 📊 Current Status: Healthcare Receptionist

### **Sprint Progress**

| Sprint | Status | Deliverables | Next Steps |
|--------|--------|--------------|------------|
| **Sprint 1** | ✅ Complete | Local testing framework, 13 tasks validated | - |
| **Sprint 2** | ✅ Complete | NexHealth integrated into 8 tasks | - |
| **Sprint 3** | 🟡 In Progress | Need 27 more tasks (7 triage done, 20 remaining) | Continue task expansion |
| **Sprint 4** | ⏳ Pending | Hardening, CI/CD, production readiness | After Sprint 3 |

### **Current Deliverables**

**Tasks:** 20/40 (50% complete)
- ✅ 13 foundation tasks (Sprint 1)
- ✅ 7 triage tasks (Sprint 3 - partial)
- ⏳ 8 insurance tasks (Sprint 3 - pending)
- ⏳ 6 orchestration tasks (Sprint 3 - pending)
- ⏳ 6 advanced tasks (Sprint 3 - pending)

**MCP Servers:** 4/4 ✅ Complete
- ✅ `twilio_hipaa` (5 tools)
- ✅ `assemblyai` (5 tools)
- ✅ `videosdk` (7 tools)
- ✅ `nexhealth` (6 tools)

**Evaluators:** 20/40 (50% complete)
- ✅ 13 foundation evaluators
- ✅ 7 triage evaluators
- ⏳ 20 more needed

**Frontend/Backend:** ✅ Architecture exists
- ✅ Backend API structure (`backend/api/routers/`)
- ✅ Frontend components (`frontend/src/components/`)
- ✅ Central workflow (`central/api-registry.yaml`)
- ✅ Sync mechanism (`central/frontend-sync.py`)

---

## 🎯 GitLab MLOps Project: New

### **Proposed Structure**

**1 GitLab MCP Server** with 7 capability modules (~46 tools):
1. GitLab Orchestrator Module (8 tools)
2. Code Intelligence Module (6 tools)
3. CI/CD Intelligence Module (8 tools)
4. MLOps Automation Module (8 tools)
5. Data Pipeline Module (6 tools)
6. Resource Optimization Module (5 tools)
7. Collaboration Intelligence Module (5 tools)

**40 Tasks** across 7 categories (target 35-40% pass rate)

**Timeline:** 10 weeks (as per proposal)

---

## 🔄 Dual Project Management Strategy

### **Option 1: Sequential (Recommended)**
**Approach:** Finish Healthcare Sprint 3, then start GitLab

**Timeline:**
- **Week 1-2:** Complete Healthcare Sprint 3 (20 remaining tasks)
- **Week 3:** Complete Healthcare Sprint 4 (hardening, CI/CD)
- **Week 4-13:** Start GitLab project (10 weeks)

**Pros:**
- ✅ Focus on one project at a time
- ✅ Clean handoff between projects
- ✅ Healthcare project complete before starting new one

**Cons:**
- ❌ GitLab project starts later
- ❌ Manager wants to proceed now

---

### **Option 2: Parallel (If Manager Insists)**
**Approach:** Work on both projects simultaneously

**Timeline:**
- **Healthcare:** Continue Sprint 3 (20 tasks remaining)
- **GitLab:** Start Phase 1 (GitLab Orchestrator + Code Intelligence modules)

**Resource Allocation:**
- **70% time:** Healthcare (finish Sprint 3)
- **30% time:** GitLab (Phase 1 foundation)

**Pros:**
- ✅ Both projects progress
- ✅ Manager happy (GitLab started)
- ✅ Healthcare continues

**Cons:**
- ❌ Context switching overhead
- ❌ Risk of incomplete work on both
- ❌ More complex to manage

---

### **Option 3: Hybrid (Recommended if Manager Wants GitLab Now)**
**Approach:** Finish Healthcare Sprint 3 quickly, then parallel

**Timeline:**
- **Week 1:** Complete Healthcare Sprint 3 (20 tasks - focused sprint)
- **Week 2:** Healthcare Sprint 4 (hardening) + GitLab Phase 1 start
- **Week 3-12:** Parallel work (Healthcare maintenance + GitLab development)

**Pros:**
- ✅ Healthcare Sprint 3 complete (clean milestone)
- ✅ GitLab starts quickly (manager happy)
- ✅ Both projects progress

**Cons:**
- ❌ Intense Week 1 (20 tasks)
- ❌ Still some parallel work

---

## 🏗️ Frontend/Backend Sync Strategy

### **Current Architecture**

**Backend:**
- `backend/api/routers/` - API endpoints
- `backend/services/` - Business logic
- `central/api-registry.yaml` - Single source of truth
- `central/frontend-sync.py` - Syncs to frontend

**Frontend:**
- `frontend/src/components/` - Reusable components
- `frontend/src/pages/` - Page components
- `frontend/src/data/api-status.json` - Auto-synced from backend
- `frontend/src/api/mcp-client.ts` - API client

**Sync Mechanism:**
```
central/api-registry.yaml
    ↓ (frontend-sync.py)
frontend/src/data/api-status.json
    ↓ (Frontend reads)
React Components
```

---

### **Multi-Domain Frontend Architecture**

**Current:** Single domain (healthcare-receptionist)  
**Future:** Multi-domain (healthcare-receptionist + gitlab-mlops)

**Proposed Structure:**
```
frontend/
├── src/
│   ├── domains/
│   │   ├── healthcare-receptionist/
│   │   │   ├── config/
│   │   │   │   ├── problem-config.js
│   │   │   │   ├── pricing-config.js
│   │   │   │   ├── mcp-servers-config.js
│   │   │   │   └── integration-stack-config.js
│   │   │   └── LandingPage.jsx
│   │   └── gitlab-mlops/
│   │       ├── config/
│   │       │   ├── problem-config.js
│   │       │   ├── pricing-config.js
│   │       │   ├── mcp-servers-config.js
│   │       │   └── integration-stack-config.js
│   │       └── LandingPage.jsx
│   ├── components/
│   │   └── landing/ (reusable across domains)
│   └── pages/
│       ├── Dashboard.jsx (multi-domain)
│       └── DomainLanding.jsx (dynamic routing)
```

**Backend Updates:**
```
backend/
├── api/
│   └── routers/
│       ├── healthcare.py (healthcare endpoints)
│       ├── gitlab.py (gitlab endpoints)
│       └── central.py (shared endpoints)
├── services/
│   ├── healthcare_service.py
│   ├── gitlab_service.py
│   └── sprint_service.py (shared)
└── central/
    └── api-registry.yaml (both domains)
```

---

### **Sync Workflow for Dual Projects**

**1. API Registry Updates:**
```yaml
# central/api-registry.yaml
apis:
  healthcare-receptionist:
    - name: nexhealth
      status: active
      tests: [...]
  gitlab-mlops:
    - name: gitlab
      status: active
      tests: [...]
```

**2. Frontend Sync:**
```bash
# Run sync for both domains
python3 central/frontend-sync.py

# Generates:
# frontend/src/data/api-status.json (both domains)
```

**3. Frontend Consumption:**
```javascript
// frontend/src/pages/Dashboard.jsx
import apiStatus from '../data/api-status.json';

// Filter by domain
const healthcareAPIs = apiStatus.apis['healthcare-receptionist'];
const gitlabAPIs = apiStatus.apis['gitlab-mlops'];
```

---

## 📋 Implementation Plan

### **Phase 1: Healthcare Sprint 3 Completion (Week 1)**

**Goal:** Complete remaining 20 tasks

**Tasks:**
- [ ] Add 8 insurance tasks + evaluators
- [ ] Add 6 orchestration tasks + evaluators
- [ ] Add 6 advanced tasks + evaluators
- [ ] Update config.yaml with all 40 tasks
- [ ] Test all 40 tasks locally
- [ ] Measure pass rate

**Deliverable:** Healthcare domain with 40 tasks complete

---

### **Phase 2: GitLab Foundation (Week 2-3)**

**Goal:** Build GitLab server foundation

**Tasks:**
- [ ] Create `gitlab` server structure
- [ ] Implement Module 1 (GitLab Orchestrator) - 8 tools
- [ ] Implement Module 2 (Code Intelligence) - 6 tools
- [ ] Test GitLab API integration
- [ ] Create 12 initial tasks (6 GitLab + 6 Code Intelligence)

**Deliverable:** GitLab server with 2 modules, 12 tasks

---

### **Phase 3: Parallel Development (Week 4+)**

**Healthcare:**
- [ ] Sprint 4: Hardening, CI/CD integration
- [ ] Production readiness
- [ ] Documentation

**GitLab:**
- [ ] Phase 2: CI/CD + MLOps modules
- [ ] Phase 3: Data + Optimization modules
- [ ] Phase 4: Hardening

---

## 🔧 Frontend/Backend Sync Updates

### **Backend Changes Needed**

**1. Multi-Domain Support:**
```python
# backend/api/routers/central.py
@router.get("/api/v1/central/apis")
async def get_apis(domain: Optional[str] = None):
    """Get APIs for domain(s)."""
    if domain:
        return api_registry.get_domain_apis(domain)
    return api_registry.get_all_apis()
```

**2. Domain-Specific Endpoints:**
```python
# backend/api/routers/healthcare.py
@router.get("/api/v1/healthcare/servers")
async def get_healthcare_servers():
    """Get healthcare MCP servers."""
    ...

# backend/api/routers/gitlab.py
@router.get("/api/v1/gitlab/servers")
async def get_gitlab_servers():
    """Get GitLab MCP servers."""
    ...
```

---

### **Frontend Changes Needed**

**1. Domain Configuration:**
```javascript
// frontend/src/constants/domains.js
export const DOMAINS = {
  'healthcare-receptionist': {
    name: 'Healthcare Receptionist',
    route: '/healthcare-receptionist',
    configPath: 'domains/healthcare-receptionist/config'
  },
  'gitlab-mlops': {
    name: 'GitLab MLOps',
    route: '/gitlab-mlops',
    configPath: 'domains/gitlab-mlops/config'
  }
};
```

**2. Dynamic Routing:**
```javascript
// frontend/src/pages/DomainLanding.jsx
import { useParams } from 'react-router-dom';
import { DOMAINS } from '../constants/domains';

function DomainLanding() {
  const { domain } = useParams();
  const domainConfig = DOMAINS[domain];
  const LandingPage = require(`../domains/${domain}/LandingPage.jsx`).default;
  
  return <LandingPage config={domainConfig} />;
}
```

---

## ✅ Recommendation

**Option 3: Hybrid Approach**

**Week 1:** Complete Healthcare Sprint 3 (20 tasks - focused sprint)  
**Week 2:** Healthcare Sprint 4 + GitLab Phase 1 start  
**Week 3+:** Parallel development

**Why:**
1. ✅ Healthcare Sprint 3 complete (clean milestone)
2. ✅ GitLab starts quickly (manager happy)
3. ✅ Both projects progress
4. ✅ Frontend/backend can handle multi-domain

**Frontend/Backend Sync:**
- ✅ Architecture already supports multi-domain
- ✅ Just need to add GitLab domain config
- ✅ API registry already supports multiple domains
- ✅ Frontend sync script works for all domains

---

## 📝 Next Steps

1. **Confirm with Manager:** Hybrid approach (Week 1 finish Healthcare, then parallel)
2. **Week 1 Focus:** Complete Healthcare Sprint 3 (20 tasks)
3. **Week 2 Start:** Begin GitLab Phase 1 while finishing Healthcare Sprint 4
4. **Frontend/Backend:** Update for multi-domain support (minimal changes needed)

---

**Ready to proceed?** 🚀

