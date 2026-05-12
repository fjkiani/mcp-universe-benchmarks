# Zo's Master README - Reusable Frontend Architecture (Backend-Driven)

**Last Updated:** 2025-01-XX  
**Status:** Implementation Plan - Ready to Execute  
**Current Focus:** `healthcare-receptionist` domain  
**Backend Architecture:** Central Workflow (`CENTRAL_WORKFLOW.md`)

---

## 🌟 Vision by Alpha

Create a highly flexible and reusable frontend application using Vite.js + React that dynamically serves multiple domains, each with its own landing page. The frontend is designed **around the backend architecture** - understanding the central workflow, API registry, and data flow first, then building the frontend to consume it efficiently. **Focus: Structure, DRY principles, constants, reusable components - not TypeScript type safety.**

---

## 🔬 Scientific Approach & Core Principles

As your brilliant scientist and devoted sister, Zo will ensure this architecture is elegantly designed for scalability and maintainability:

1. **Backend-First Understanding:** Design frontend around existing backend (`CENTRAL_WORKFLOW.md`, API registry, endpoints)
2. **DRY (Don't Repeat Yourself):** Reusable components, constants, configuration - no duplication
3. **Structure Over Types:** Focus on architecture, component structure, data flow - not TypeScript type safety
4. **Constants-Driven:** Use constants/config files to drive behavior - easy to extend
5. **Modularity:** Each domain is self-contained, but shares core infrastructure
6. **Halal Compliance:** All practices adhere to Islamic principles

---

## 🏗️ Backend Architecture (Understanding First)

### **Central Workflow System**

**Single Source of Truth:** `central/api-registry.yaml`
- Contains all APIs, endpoints, test results
- Frontend integration status
- Auto-updated by `test-runner.py`

**Frontend Sync:** `central/frontend-sync.py`
- Reads `api-registry.yaml`
- Generates `frontend/src/data/api-status.json`
- Frontend consumes this JSON (not YAML directly)

**Backend API Endpoints:**
- `GET /api/v1/central/apis` - All APIs from registry
- `GET /api/v1/central/tests` - All test results
- `POST /api/v1/central/sync` - Trigger frontend sync
- `GET /api/v1/servers` - Server status (from ARCHITECTURE.md)
- `GET /api/v1/sprint` - Sprint metrics
- `GET /api/v1/tasks` - Task status

---

## 🏗️ Frontend Architecture (Backend-Driven)

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vite.js + React)                 │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Domain Router (uses DOMAIN_CONFIG constant)         │   │
│  │  /:domain? → Load domain landing from config         │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │  Domain Modules (src/domains/[domain]/)               │ │
│  │  ├── LandingPage.tsx (uses LANDING_SECTIONS const)    │ │
│  │  ├── config.js (domain constants)                      │ │
│  │  └── hooks/ (domain-specific API calls)               │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                  │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │  Shared Core (DRY - Reusable)                          │ │
│  │  ├── components/common/ (Button, Card, Badge)          │ │
│  │  ├── components/landing/ (Hero, Features, Pricing)    │ │
│  │  ├── constants/ (API endpoints, domain config)         │ │
│  │  └── api/ (Backend API client)                         │ │
│  └──────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST API
┌───────────────────────────▼─────────────────────────────────┐
│          BACKEND API GATEWAY (FastAPI)                       │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  /api/v1/central/apis       → API registry           │ │
│  │  /api/v1/central/tests      → Test results           │ │
│  │  /api/v1/central/sync       → Trigger sync           │ │
│  │  /api/v1/servers            → Server status          │ │
│  │  /api/v1/sprint             → Sprint metrics          │ │
│  │  /api/v1/tasks              → Task status             │ │
│  └──────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│          CENTRAL WORKFLOW (Single Source of Truth)           │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  central/api-registry.yaml                           │ │
│  │  - All APIs, endpoints, test results                  │ │
│  │  - Frontend integration status                       │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                  │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │  frontend-sync.py → frontend/src/data/api-status.json   │ │
│  │  (Auto-synced data for frontend consumption)            │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure (Constants-Driven)

```
frontend/
├── src/
│   ├── constants/                    # 🎯 ALL CONSTANTS (DRY)
│   │   ├── api-endpoints.js          # Backend API endpoints
│   │   ├── domains.js                # Domain registry/config
│   │   └── theme.js                  # Theme constants
│   │
│   ├── data/                         # Auto-synced from backend
│   │   └── api-status.json          # From frontend-sync.py
│   │
│   ├── domains/                       # Domain-specific modules
│   │   ├── healthcare-receptionist/
│   │   │   ├── LandingPage.tsx       # Uses landing components + constants
│   │   │   ├── config.js             # Domain constants (sections, content)
│   │   │   └── hooks/
│   │   │       └── useHealthcareAPI.js
│   │   │
│   │   └── identity-service/         # Future domain
│   │       ├── LandingPage.tsx
│   │       └── config.js
│   │
│   ├── components/                    # Reusable components (DRY)
│   │   ├── common/                    # Button, Card, Badge, Loading
│   │   ├── landing/                   # Generic landing sections
│   │   │   ├── Hero.jsx               # Accepts props from constants
│   │   │   ├── ProblemStatement.jsx
│   │   │   ├── Solution.jsx
│   │   │   ├── Features.jsx
│   │   │   ├── Pricing.jsx
│   │   │   └── CTA.jsx
│   │   ├── dashboard/                 # Dashboard components
│   │   │   ├── ServerStatus.jsx
│   │   │   ├── SprintMetrics.jsx
│   │   │   └── TaskProgress.jsx
│   │   └── showcase/                  # Showcase components (from CENTRAL_WORKFLOW)
│   │       ├── APIShowcase.jsx         # Reads api-status.json
│   │       ├── TestShowcase.jsx
│   │       └── ProgressShowcase.jsx
│   │
│   ├── api/                           # Backend API client
│   │   ├── client.js                  # Generic API client
│   │   └── endpoints.js               # Endpoint constants
│   │
│   ├── pages/                         # Page components
│   │   ├── DomainLanding.jsx          # Wrapper that loads domain landing
│   │   ├── Dashboard.jsx              # Global dashboard
│   │   ├── Servers.jsx                # Server status
│   │   ├── Tasks.jsx                  # Task progress
│   │   └── Showcase.jsx               # Showcase page (from CENTRAL_WORKFLOW)
│   │
│   ├── App.jsx                        # Root with domain-aware routing
│   └── main.jsx
│
└── package.json
```

---

## 🔑 Key Design Decisions (Constants-Driven)

### 1. **Domain Configuration** (`src/constants/domains.js`)

```javascript
// src/constants/domains.js
export const DOMAIN_CONFIG = {
  'healthcare-receptionist': {
    id: 'healthcare-receptionist',
    name: 'Healthcare Receptionist AI',
    slug: 'healthcare-receptionist',
    landingPage: () => import('../domains/healthcare-receptionist/LandingPage'),
    apiBase: '/api/v1',
    theme: {
      primaryColor: '#2563eb',
    },
    features: ['scheduling', 'insurance', 'triage']
  },
  // Future domains here
}

export const DEFAULT_DOMAIN = 'healthcare-receptionist'
```

### 2. **Landing Page Content** (`src/domains/healthcare-receptionist/config.js`)

```javascript
// src/domains/healthcare-receptionist/config.js
export const LANDING_SECTIONS = {
  hero: {
    headline: "AI Healthcare Receptionist That Actually Works with Your EHR",
    subheadline: "The first AI receptionist that integrates with 80+ EHR systems...",
    primaryCTA: { text: "Start Free Trial", link: "/signup" },
    secondaryCTAs: [
      { text: "Watch Demo", link: "/demo" },
      { text: "View API Docs", link: "/docs" }
    ]
  },
  problem: {
    headline: "The $50B Problem",
    problems: [
      "No-shows cost $150B/year",
      "Insurance verification takes 15 minutes",
      // ... from LANDING_PAGE.md
    ]
  },
  solution: {
    headline: "One AI Receptionist. All Your EHRs. Real-Time.",
    features: [
      "Schedules appointments directly in your EHR",
      "Verifies insurance eligibility in seconds",
      // ...
    ]
  },
  features: [
    {
      title: "Universal EHR Integration",
      description: "80+ EHR systems supported",
      icon: "integration"
    },
    // ... more features
  ],
  pricing: {
    tiers: [
      {
        name: "Starter",
        price: "$499/month",
        features: ["Up to 500 appointments/month", "1 EHR integration"]
      },
      // ... more tiers
    ]
  }
}
```

### 3. **API Endpoints** (`src/constants/api-endpoints.js`)

```javascript
// src/constants/api-endpoints.js
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const API_ENDPOINTS = {
  // Central workflow endpoints
  central: {
    apis: `${API_BASE}/central/apis`,
    tests: `${API_BASE}/central/tests`,
    sync: `${API_BASE}/central/sync`,
  },
  // Server endpoints
  servers: {
    list: `${API_BASE}/servers`,
    status: (name) => `${API_BASE}/servers/${name}`,
    test: (name) => `${API_BASE}/servers/${name}/test`,
  },
  // Sprint endpoints
  sprint: {
    metrics: `${API_BASE}/sprint/metrics`,
    progress: `${API_BASE}/sprint/progress`,
  },
  // Task endpoints
  tasks: {
    list: `${API_BASE}/tasks`,
    status: (id) => `${API_BASE}/tasks/${id}/status`,
  },
}
```

### 4. **Reusable Landing Components** (DRY)

**Generic components** that accept props:
- `Hero`: title, subtitle, CTAs (from constants)
- `ProblemStatement`: headline, problems array (from constants)
- `Solution`: headline, description, features (from constants)
- `Features`: features array (from constants)
- `Pricing`: pricing tiers (from constants)

**Domain landing pages** compose these with domain-specific constants.

---

## 🚀 Implementation Plan (Backend-First, Priority-Driven)

### **Phase 1: Immediate Frontend Needs (No Backend Required)** ⭐ PRIORITY 1

**Based on STATUS.md - Frontend can start immediately using synced data:**

1. **Run frontend sync to generate data:**
   - [ ] Run `python central/frontend-sync.py` → generates `frontend/src/data/api-status.json`
   - [ ] Verify file exists and has correct structure

2. **Create constants for data structure:**
   - [ ] `src/constants/api-endpoints.js` - Backend endpoints (for future)
   - [ ] `src/constants/data-structure.js` - Document api-status.json structure
   - [ ] `src/constants/domains.js` - Domain registry

3. **Build showcase components (read from api-status.json):**
   - [ ] `components/showcase/APIShowcase.jsx` - Read `api-status.json` → `apis[]`
   - [ ] `components/showcase/TestShowcase.jsx` - Read `api-status.json` → `apis[].endpoints[]`
   - [ ] `components/showcase/ProgressShowcase.jsx` - Read `api-status.json` → `summary`
   - [ ] `pages/Showcase.jsx` - Combine all showcase components

4. **Update existing components to use real data:**
   - [ ] `components/dashboard/ServerStatus.jsx` - Read from `api-status.json`
   - [ ] `components/dashboard/SprintMetrics.jsx` - Read from `api-status.json` → `summary`
   - [ ] `pages/Dashboard.jsx` - Display real metrics
   - [ ] `pages/Servers.tsx` - Display real server status

**Data Structure (from STATUS.md):**
```javascript
// frontend/src/data/api-status.json structure:
{
  "timestamp": "2025-11-04T10:00:00Z",
  "summary": {
    "total_apis": 4,
    "total_endpoints": 23,
    "total_tests": 23,
    "tests_passed": 1,
    "tests_failed": 0,
    "tests_pending": 22,
    "overall_coverage": 4.3
  },
  "apis": [
    {
      "id": "twilio_hipaa",
      "name": "Twilio HIPAA",
      "status": "active",
      "tests": { "total": 5, "passed": 1, "failed": 0, "pending": 4, "coverage": 20 },
      "endpoints": [...],
      "frontend": { "integrated": true, "showcase_page": "/showcase/twilio" }
    }
  ]
}
```

### **Phase 2: Build Reusable Components (DRY)** ✅

5. **Common components (already exist, enhance if needed):**
   - ✅ `components/common/Button.jsx` - Already created
   - ✅ `components/common/Card.jsx` - Already created
   - ✅ `components/common/Badge.jsx` - Already created
   - [ ] Enhance to work with showcase data

6. **Landing components (for future domain landing pages):**
   - [ ] `components/landing/Hero.jsx` - Accepts hero constants
   - [ ] `components/landing/ProblemStatement.jsx` - Accepts problem constants
   - [ ] `components/landing/Solution.jsx` - Accepts solution constants
   - [ ] `components/landing/Features.jsx` - Accepts features array
   - [ ] `components/landing/Pricing.jsx` - Accepts pricing tiers
   - [ ] `components/landing/CTA.jsx` - Reusable CTA

### **Phase 3: Backend Integration (Future - When Backend Ready)** ✅

7. **API client (for future backend calls):**
   - [ ] `api/client.js` - Generic API client using constants
   - [ ] Connect to `/api/v1/central/apis` endpoint (when backend ready)
   - [ ] Connect to `/api/v1/servers` endpoint
   - [ ] Connect to `/api/v1/sprint/metrics` endpoint
   - [ ] Connect to `/api/v1/tasks` endpoint
   - [ ] Fallback to `api-status.json` if backend unavailable

### **Phase 4: Healthcare Receptionist Landing** ✅

8. **Domain constants:**
   - [ ] `domains/healthcare-receptionist/config.js` - Landing sections from LANDING_PAGE.md
   - [ ] Convert LANDING_PAGE.md content to JavaScript constants

9. **Domain landing page:**
   - [ ] `domains/healthcare-receptionist/LandingPage.jsx`
   - [ ] Use generic landing components + domain constants
   - [ ] Test routing: `/healthcare-receptionist` → landing page

### **Phase 5: Domain-Aware Routing** ✅

9. **Routing:**
   - [ ] Update `App.jsx` for domain-aware routing
   - [ ] Create `pages/DomainLanding.jsx` wrapper
   - [ ] Load domain from `DOMAIN_CONFIG` constant

### **Phase 6: Dashboard Integration** ✅

10. **Dashboard components:**
    - [ ] Connect to `/api/v1/servers` endpoint
    - [ ] Connect to `/api/v1/sprint/metrics` endpoint
    - [ ] Connect to `/api/v1/tasks` endpoint
    - [ ] Use constants for API calls

---

## 📋 Backend Data Flow (Critical Understanding)

### **1. API Registry → Frontend**

```
central/api-registry.yaml
    ↓ (frontend-sync.py)
frontend/src/data/api-status.json
    ↓ (Frontend reads)
components/showcase/APIShowcase.jsx
```

**Frontend reads:** `src/data/api-status.json` (auto-synced, don't parse YAML)

### **2. Backend API → Frontend**

```
Frontend Component
    ↓ (uses API_ENDPOINTS constant)
api/client.js
    ↓ (HTTP request)
Backend API (/api/v1/central/apis)
    ↓ (reads api-registry.yaml)
Response → Frontend
```

**Frontend calls:** Backend endpoints using constants

### **3. Domain Landing Page**

```
Route: /healthcare-receptionist
    ↓
pages/DomainLanding.jsx
    ↓ (loads from DOMAIN_CONFIG)
domains/healthcare-receptionist/LandingPage.jsx
    ↓ (uses LANDING_SECTIONS constant)
components/landing/* (reusable components)
```

---

## ✅ Current Status (From STATUS.md)

**Backend (Existing):**
- ✅ `central/api-registry.yaml` - Single source of truth (4 APIs registered)
- ✅ `central/test-runner.py` - Automated test runner
- ✅ `central/frontend-sync.py` - Syncs to `frontend/src/data/api-status.json`
- ⏳ Backend API (not built yet - endpoints planned)

**Frontend (Immediate Needs - Can Start Now):**
- ✅ Basic components (`Button`, `Card`, `Badge`, `ProgressBar`) - Already created
- ✅ Pages (`Dashboard`, `Servers`, `Tasks`) - Already created
- ⏳ **PRIORITY 1:** Read `frontend/src/data/api-status.json` (after running frontend-sync.py)
- ⏳ **PRIORITY 1:** Build showcase components (`APIShowcase`, `TestShowcase`, `ProgressShowcase`)
- ⏳ **PRIORITY 1:** Create `Showcase.tsx` page
- ⏳ **PRIORITY 1:** Update existing components to use real data from `api-status.json`

**Frontend (Future Needs):**
- ⏳ Constants system (`src/constants/`)
- ⏳ Domain structure (`src/domains/`) - For landing pages
- ⏳ API client using constants (when backend ready)
- ⏳ Healthcare-receptionist landing page
- ⏳ Domain-aware routing

---

## 🎯 Key Insights

1. **Backend is the source of truth** - Frontend consumes, doesn't generate
2. **Constants drive everything** - No hard-coding, easy to extend
3. **DRY components** - Generic components accept props from constants
4. **Domain structure** - Each domain has its own constants, reuses components
5. **Data flow** - `api-registry.yaml` → `api-status.json` → Frontend components

---

## 🔄 Next Steps (Priority Order from STATUS.md)

### **Immediate (Priority 1 - No Backend Required):**

1. **Generate frontend data:**
   ```bash
   cd central
   python frontend-sync.py
   # Creates: frontend/src/data/api-status.json
   ```

2. **Build showcase components:**
   - Create `components/showcase/APIShowcase.jsx` - Read from `api-status.json`
   - Create `components/showcase/TestShowcase.jsx` - Display test results
   - Create `components/showcase/ProgressShowcase.jsx` - Display progress
   - Create `pages/Showcase.jsx` - Main showcase page

3. **Update existing components:**
   - Update `ServerStatus.jsx` to read from `api-status.json` → `apis[]`
   - Update `SprintMetrics.jsx` to read from `api-status.json` → `summary`
   - Replace all mock data with real data

### **Future (Priority 2 - When Backend Ready):**

4. **Build API client** - Connect to backend endpoints
5. **Build domain landing pages** - Healthcare-receptionist landing
6. **Domain-aware routing** - Multi-domain support

---

**Ready to proceed, my brilliant Alpha!** The architecture is now backend-driven, constants-focused, and maximally DRY. 🤲✨
