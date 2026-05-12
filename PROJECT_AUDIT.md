# MCP Universe benchmarks — project audit

**Date:** 2025-12-20  
**Updated:** 2026-05-12 — consolidated layout for `mcp-universe-benchmarks`; product apps called out as optional.

**Purpose:** Record structure, architecture, and how this template extends the scaffolded MCP benchmark stack (CLI + mothership submodules + `domains/`).

**Architecture:** Hub-and-spoke architecture with:
- **CLI Tools** (shared submodule) - Domain management, validation, evaluation
- **Template Repository** (this repo) - Blueprint for new domain repos
- **Domain Repos** (per domain) - Individual domain implementations
- **Mothership** (aggregator) - Central repository syncing all domains

**Current Status:** Active development with multiple domains in progress

---

## 🏗️ Architecture Overview

### Hub-and-Spoke Model

```
lbx_mcp_universe_cli (shared CLI tools)
└── Git submodule in all repos
    └── Domain management CLI
    └── Validation and evaluation tools

lbx_mcp_universe_template (this repo - blueprint)
└── Starting point for new domain repos
    └── Contains .github/workflows/
    └── Contains base domain classes
    └── Includes CLI as submodule

domain-specific-repos (per domain)
├── lbx-mcp-domain-{your-domain}
    ├── domains/{your-domain}/          # Domain implementation
    ├── lbx_mcp_universe_cli/           # Git submodule
    └── .github/workflows/
        ├── ci.yml                       # Validation & evaluation
        ├── sync-to-mother.yml           # Auto-sync to mothership
        └── secret-scan.yml              # Secret scanning

lbx_mcp_universe_mothership (aggregator)
└── Central repository
    └── domains/
        ├── domain1/    # Synced from domain repos
        ├── domain2/
        └── ...
```

### Key Components

1. **CLI Tools** (`lbx_mcp_universe_cli/`)
   - Domain management commands
   - Validation tools
   - Evaluation framework
   - LLM-as-a-judge evaluation

2. **MCP Servers** (`lbx_mcp_universe_mcp_servers_mothership/`)
   - 25+ MCP servers (Google Search, Email, PDF Generator, etc.)
   - Healthcare-specific servers (Twilio HIPAA, AssemblyAI, VideoSDK, NexHealth)
   - Git submodule

3. **Domain Implementations** (`domains/`)
   - Reference: `web_search` (complete, production-ready)
   - Active: `healthcare_receptionist`, `gitlab_mlops`, `grant_application`, etc.
   - Each domain contains:
     - `config.yaml` - Benchmark configuration
     - `tasks/` - 50+ task JSON files
     - `evaluators/` - Evaluation logic

4. **Frontend** (`frontend/`)
   - React/TypeScript application
   - Dashboard for sprint metrics
   - Server status visualization
   - Task progress tracking

5. **Backend** (`backend/`)
   - API gateway (planned)
   - Database layer
   - Services layer

6. **Central** (`central/`)
   - API registry (`api-registry.yaml`)
   - Test runner (`test-runner.py`)
   - Frontend sync (`frontend-sync.py`)

---

## 📂 Directory Structure Analysis

### Core Directories

| Directory | Purpose | Status | Key Files |
|-----------|---------|--------|-----------|
| `domains/` | Domain implementations | ✅ Active | `web_search/`, `healthcare_receptionist/`, `gitlab_mlops/` |
| `lbx_mcp_universe_cli/` | CLI tools (submodule) | ✅ Active | CLI commands, validation, evaluation |
| `lbx_mcp_universe_mcp_servers_mothership/` | MCP servers (submodule) | ✅ Active | 25+ servers |
| `frontend/` | React frontend | ✅ Active | Dashboard, components, pages |
| `backend/` | API backend | ⏳ In Progress | API gateway plan, services |
| `central/` | Central registry | ✅ Active | API registry, test runner |
| `docs/` | Documentation | ✅ Active | Guides, architecture docs |
| `tests/` | Test suites | ✅ Active | API, e2e, MCP tests |

### Key Files

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Main documentation | ✅ Complete |
| `STRUCTURE_GUIDE.md` | Structure guide | ✅ Complete |
| `STATUS.md` | Healthcare receptionist status | ✅ Active |
| `pyproject.toml` | Python project config | ✅ Active |
| `uv.lock` | Dependency lock file | ✅ Active |
| `.github/workflows/` | CI/CD workflows | ✅ Active |

---

## 🎯 Domain Analysis

### Reference Domain: `web_search`

**Status:** ✅ Complete, production-ready reference

**Structure:**
- `config.yaml` - Benchmark configuration
- `tasks/` - 53+ task files
- `evaluators/` - Evaluation logic
- `README.md` - Complete documentation

**Purpose:** Reference implementation showing best practices

### Active Domains

#### 1. `healthcare_receptionist`

**Status:** ✅ Active Development (20% complete - Priority 1 done)

**Components:**
- **MCP Servers:** 4/4 built ✅
  - `twilio_hipaa` - 5 tools (SMS/Voice/PHI detection)
  - `assemblyai` - 5 tools (Medical transcription)
  - `videosdk` - 7 tools (Video consultations)
  - `nexhealth` - 6 tools (EHR integration, 80+ systems)

- **Domain Tasks:** 13 tasks created ✅
  - Patient Intake: 5 tasks
  - Appointment Scheduling: 5 tasks
  - Clinical Triage: 1 task
  - Real API Integration: 2 tasks

- **API Keys:** 7/7 configured ✅

**Frontend Integration:**
- ✅ Server status cards ready
- ✅ Test results visualization (structure ✅, API ⏳ pending)
- ⏳ API test results (awaiting environment setup)

**Next Steps:**
- Run `python central/test-runner.py` to populate test results
- Run `python central/frontend-sync.py` to update frontend data
- Build showcase components

#### 2. `gitlab_mlops`

**Status:** ⏳ In Progress (uncommitted changes detected)

**Components:**
- Tasks: 6+ tasks created
- Evaluators: Error types infrastructure
- Documentation: Sprint summaries, CI/CD setup

**Current Branch:** `feature/gitlab-mlops-domain`

#### 3. Other Domains

- `grant_application` - Grant application domain
- `identity_service` - Identity service domain
- `investments` - Investments domain
- `currency_converter` - Currency conversion
- `flight_delay` - Flight delay information
- `web_search` - Reference implementation

---

## 🔧 Technology Stack

### Backend
- **Language:** Python
- **Package Manager:** UV (modern Python package manager)
- **Framework:** FastAPI (planned)
- **Dependencies:** Managed via `pyproject.toml` and `uv.lock`

### Frontend
- **Language:** TypeScript
- **Framework:** React
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Package Manager:** npm

### Infrastructure
- **CI/CD:** GitHub Actions
- **Workflows:**
  - `ci.yml` - Validation & evaluation
  - `sync-to-mother.yml` - Auto-sync to mothership
  - `secret-scan.yml` - Secret scanning

### MCP (Model Context Protocol)
- **Servers:** 25+ MCP servers
- **Integration:** Git submodule
- **Purpose:** Provide tools/context to LLM agents

---

## 📊 Current State Assessment

### ✅ Strengths

1. **Well-Structured Architecture**
   - Clear separation of concerns
   - Hub-and-spoke model enables scalability
   - Submodule pattern for shared code

2. **Comprehensive Documentation**
   - README.md with quick start
   - STRUCTURE_GUIDE.md with templates
   - STATUS.md for progress tracking
   - Domain-specific READMEs

3. **Reference Implementation**
   - `web_search` domain as complete example
   - Best practices demonstrated
   - 5-6 high-quality tasks

4. **Active Development**
   - Multiple domains in progress
   - Frontend/backend infrastructure
   - Central registry system

### ⚠️ Areas of Concern

1. **Uncommitted Changes**
   - `gitlab_mlops` domain has uncommitted changes
   - Need to commit or stash before switching branches

2. **Incomplete Integration**
   - Frontend awaiting test results
   - Backend API not fully built
   - Some MCP servers need dependency fixes

3. **Documentation Fragmentation**
   - Multiple status files
   - Some docs may be outdated
   - Need consolidation

### 🔄 Active Workflows

1. **Domain Creation Workflow**
   ```bash
   uv run alignerr_mcp create-domain --name {your-domain}
   ```

2. **Validation Workflow**
   ```bash
   uv run alignerr_mcp validate --domain {your-domain}
   ```

3. **Frontend Sync Workflow**
   ```bash
   python central/frontend-sync.py
   ```

4. **Test Runner Workflow**
   ```bash
   python central/test-runner.py
   ```

---

## 🎯 Key Insights

### Project Purpose

This is a **benchmark framework** for evaluating LLM agents on domain-specific tasks. The goal is to create **challenging benchmarks** that expose model limitations, not showcase successes.

**Key Principle:**
> Model failures are the goal. We're building a benchmark to identify where models struggle, not to showcase their successes.

### Evaluation Metrics

**Good Signs:**
- ✅ High model failure rate (50-90% failure) - tasks are appropriately challenging
- ✅ Zero evaluation errors - all tasks execute cleanly
- ✅ 100% ground truth confidence - every expected output is verified
- ✅ Consistent failure patterns - same tasks fail reliably

**Warning Signs:**
- ⚠️ Pass@1 > 70% - tasks may be too easy
- ⚠️ Inconsistent results - non-reproducible
- ⚠️ Evaluation errors > 5-10% - infrastructure issues

**Critical Issues:**
- ❌ Pass@1 > 85% - benchmark not challenging enough
- ❌ Evaluation errors > 15% - broken tasks
- ❌ Ground truth confidence < 95% - ambiguous outputs

### Development Workflow

1. **Create Domain Structure**
   ```bash
   uv run alignerr_mcp create-domain --name {your-domain}
   ```

2. **Implement Domain**
   - Edit `config.yaml`
   - Create tasks in `tasks/`
   - Implement evaluators in `evaluators/`

3. **Test Locally**
   ```bash
   uv run alignerr_mcp validate --domain {your-domain}
   ```

4. **Create PR**
   - Feature branch: `domains/{domain-name}/v{version}`
   - CI automatically validates
   - Sync to mothership on merge

---

## 📋 Recommendations

### Immediate Actions

1. **Handle Uncommitted Changes**
   ```bash
   # Option 1: Commit changes
   git add .
   git commit -m "WIP: gitlab_mlops domain progress"
   
   # Option 2: Stash changes
   git stash
   
   # Then switch to main
   git checkout main
   ```

2. **Verify Main Branch State**
   ```bash
   git checkout main
   git status
   git pull origin main
   ```

3. **Review Active Domains**
   - Check `STATUS.md` for healthcare_receptionist
   - Review `gitlab_mlops` progress
   - Identify other active domains

### Short-Term Improvements

1. **Consolidate Documentation**
   - Merge status files
   - Update outdated docs
   - Create single source of truth

2. **Complete Frontend Integration**
   - Run test runner
   - Sync frontend data
   - Build showcase components

3. **Fix MCP Server Dependencies**
   - Resolve httpx issues
   - Fix twilio library dependencies
   - Verify all servers work

### Long-Term Enhancements

1. **Backend API Development**
   - Complete API gateway
   - Connect frontend to backend
   - Real-time updates

2. **Test Coverage**
   - Increase test coverage
   - Add integration tests
   - Validate all domains

3. **Documentation**
   - Create architecture diagrams
   - Document all workflows
   - Update examples

---

## 🔍 Key Files to Review

### Must Read
- ✅ `README.md` - Complete tutorial
- ✅ `STRUCTURE_GUIDE.md` - Structure guide
- ✅ `STATUS.md` - Healthcare receptionist status
- ✅ `GETTING_STARTED.md` - Learning paths

### Should Read
- `docs/README.md` - Documentation index
- `domains/web_search/README.md` - Reference example
- `central/api-registry.yaml` - API registry
- `.github/workflows/ci.yml` - CI configuration

### Reference
- `domains/web_search/` - Complete reference implementation
- `domains/healthcare_receptionist/` - Active domain example
- `frontend/src/` - Frontend structure
- `backend/` - Backend structure

---

## 📝 Summary

**Project Type:** Template repository for domain-specific LLM agent benchmarks

**Architecture:** Hub-and-spoke with CLI submodule, MCP servers, domain repos, and mothership aggregator

**Current State:** Active development with multiple domains in progress, frontend/backend infrastructure being built

**Key Insight:** This is a benchmark framework designed to expose model limitations, not showcase successes. High failure rates are expected and desired.

**Next Steps:**
1. Handle uncommitted changes
2. Switch to main branch
3. Review active domains
4. Complete frontend integration
5. Continue domain development

---

**Audit Complete:** 2025-12-20  
**Status:** Ready for development on main branch


