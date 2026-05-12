# Documentation Index

**Single Source of Truth for All Project Documentation**

**Last Updated:** 2025-01-XX

---

## 🎯 Quick Start

### **Current Status & Progress:**
- **[STATUS.md](../STATUS.md)** ⭐ Main status tracker (root level)

### **System Overview:**
- **[ARCHITECTURE.md](architecture/ARCHITECTURE.md)** Complete system architecture

### **Frontend:**
- **[FRONTEND_ARCHITECTURE.md](../frontend/FRONTEND_ARCHITECTURE.md)** Frontend structure, integration, development
- **[COMPONENT_ARCHITECTURE.md](../frontend/COMPONENT_ARCHITECTURE.md)** Component patterns & design
- **[DESIGN_SYSTEM.md](../frontend/DESIGN_SYSTEM.md)** Visual design system

---

## 📚 Documentation Structure

### **🏗️ Architecture** (`docs/architecture/`)

| File | Purpose |
|------|---------|
| **[ARCHITECTURE.md](architecture/ARCHITECTURE.md)** | Complete system architecture, data flow, component connections |

**Location:** `docs/architecture/`

---

### **💻 Development Guides** (`docs/development/`)

| File | Purpose |
|------|---------|
| **[CENTRAL_WORKFLOW.md](development/CENTRAL_WORKFLOW.md)** | Central workflow: API registry, test runner, frontend sync |
| **[GIT_WORKFLOW.md](development/GIT_WORKFLOW.md)** | Git workflow: what gets pushed vs. stays local |
| **[AUTO_UPDATE_BACKEND.md](development/AUTO_UPDATE_BACKEND.md)** | Automatic backend updates from test results |
| **[FRONTEND_BACKEND_SYNC_STATUS.md](development/FRONTEND_BACKEND_SYNC_STATUS.md)** | Frontend-backend sync status |

**Location:** `docs/development/`

**Also See:**
- **[FRONTEND_ARCHITECTURE.md](../frontend/FRONTEND_ARCHITECTURE.md)** - Complete frontend guide
- **[HOW_TO_CREATE_NEW_LANDING_PAGE.md](../frontend/HOW_TO_CREATE_NEW_LANDING_PAGE.md)** - Landing page guide

---

### **🏥 Healthcare Receptionist Domain** (`docs/healthcare-receptionist/`)

| File | Purpose |
|------|---------|
| **[MASTER.md](healthcare-receptionist/MASTER.md)** | Domain master documentation |
| **[LANDING_PAGE.md](healthcare-receptionist/LANDING_PAGE.md)** | Landing page copy & content |
| **[AGENT_WORKFLOW.md](healthcare-receptionist/AGENT_WORKFLOW.md)** | Agent responsibilities & workflow |
| **[PRODUCT_MODULES.md](healthcare-receptionist/PRODUCT_MODULES.md)** | Product module architecture |
| **[NEXHEALTH_RESEARCH_REPORT.md](healthcare-receptionist/NEXHEALTH_RESEARCH_REPORT.md)** | NexHealth integration research |

**Location:** `docs/healthcare-receptionist/`

**Also in:** `.cursor/rules/healthcare-receptionist/` (original location, kept for reference)

**Organized Subfolders:**
- **[demo/](healthcare-receptionist/demo/)** - Demo documentation (5 files)
- **[telehealth/](healthcare-receptionist/telehealth/)** - Telehealth features (3 files)
- **[setup/](healthcare-receptionist/setup/)** - API keys and setup (3 files)
- **[status/](healthcare-receptionist/status/)** - Status and PR docs (3 files)
- **[testing/](healthcare-receptionist/testing/)** - Testing guides (1 file)

**See:** [healthcare-receptionist/README.md](healthcare-receptionist/README.md) for complete index

---

### **📋 Reference** (`docs/reference/`)

**Location:** `docs/reference/`

**Currently empty** - Add reference docs here as needed.

---

## 🔍 Root-Level Documentation

### **Status & Progress:**
- **[STATUS.md](../STATUS.md)** - Main status tracker ⭐
- **[CURRENT_STATUS_REPORT.md](../CURRENT_STATUS_REPORT.md)** - Detailed status report
- **[FRONTEND_BACKEND_SYNC_STATUS.md](../FRONTEND_BACKEND_SYNC_STATUS.md)** - Sync status (duplicate in docs/development/)

### **Setup & Running:**
- **[HOW_TO_RUN.md](../HOW_TO_RUN.md)** - How to run frontend & backend
- **[FIX_TERMINAL_AND_SETUP.md](../FIX_TERMINAL_AND_SETUP.md)** - Terminal fix & setup guide

### **Project-Specific:**
- **[LANDING_PAGE_ITERATION_SUMMARY.md](../LANDING_PAGE_ITERATION_SUMMARY.md)** - Landing page iterations
- **[MODULAR_CONFIG_COMPLETE.md](../MODULAR_CONFIG_COMPLETE.md)** - Modular config system
- **[DASHBOARD_ENHANCEMENTS.md](../DASHBOARD_ENHANCEMENTS.md)** - Dashboard enhancements
- **[ERROR_CLASSIFICATION_SUMMARY.md](../ERROR_CLASSIFICATION_SUMMARY.md)** - Error classification
- **[DUAL_PROJECT_PLAN.md](../DUAL_PROJECT_PLAN.md)** - Dual project management
- **[CONVERSATION_ANALYSIS.md](../CONVERSATION_ANALYSIS.md)** - Conversation analysis

### **General Project Docs:**
- **[README.md](../README.md)** - Main project README
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines
- **[GETTING_STARTED.md](../GETTING_STARTED.md)** - Getting started guide
- **[DOCUMENTATION_INDEX.md](../DOCUMENTATION_INDEX.md)** - Documentation index
- **[MCP_SERVERS_GUIDE.md](../MCP_SERVERS_GUIDE.md)** - MCP servers guide

---

## 🎯 Quick Links by Role

### **Frontend Developer:**
1. **[STATUS.md](../STATUS.md)** - Current status
2. **[FRONTEND_ARCHITECTURE.md](../frontend/FRONTEND_ARCHITECTURE.md)** - Complete frontend guide
3. **[COMPONENT_ARCHITECTURE.md](../frontend/COMPONENT_ARCHITECTURE.md)** - Component patterns
4. **[DESIGN_SYSTEM.md](../frontend/DESIGN_SYSTEM.md)** - Design system
5. **[HOW_TO_CREATE_NEW_LANDING_PAGE.md](../frontend/HOW_TO_CREATE_NEW_LANDING_PAGE.md)** - Landing page guide

### **Backend Developer:**
1. **[STATUS.md](../STATUS.md)** - Current status
2. **[ARCHITECTURE.md](architecture/ARCHITECTURE.md)** - System architecture
3. **[CENTRAL_WORKFLOW.md](development/CENTRAL_WORKFLOW.md)** - Central workflow
4. **[AUTO_UPDATE_BACKEND.md](development/AUTO_UPDATE_BACKEND.md)** - Backend auto-updates

### **Domain Developer (Zo):**
1. **[STATUS.md](../STATUS.md)** - Current progress
2. **[MASTER.md](healthcare-receptionist/MASTER.md)** - Domain master doc
3. **[LANDING_PAGE.md](healthcare-receptionist/LANDING_PAGE.md)** - Landing page content
4. **[PRODUCT_MODULES.md](healthcare-receptionist/PRODUCT_MODULES.md)** - Product modules

---

## 📁 File Locations Reference

### **Documentation:**
- `docs/` - Organized documentation
- `frontend/` - Frontend-specific docs
- Root level - Status, setup, general docs

### **Runtime Files (Not Documentation):**
- `central/api-registry.yaml` - API registry (runtime data)
- `central/test-runner.py` - Test runner (runtime script)
- `frontend/src/` - Frontend code
- `backend/api/` - Backend code
- `domains/healthcare_receptionist/` - Domain code

---

## 🔄 Documentation Maintenance

**When adding new docs:**
1. Place in appropriate `docs/` subfolder
2. Update this README
3. Update [STATUS.md](../STATUS.md) if relevant

**When updating docs:**
1. Update the doc file
2. Update "Last Updated" date
3. Update [STATUS.md](../STATUS.md) "Recent Updates" section if significant

---

**Last Updated:** 2025-01-XX  
**Status:** Documentation organized and indexed
