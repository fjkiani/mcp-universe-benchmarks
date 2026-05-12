# Git Workflow - What Gets Pushed

**Purpose:** Clear guide on what gets pushed to remote vs. kept local

**Last Updated:** 2025-11-04

---

## 🎯 What Gets Pushed

### **✅ Pushed to Remote (Previously & Now)**

1. **Domain Tasks & Evaluators**
   - `domains/**/` - All domain code
   - `domains/**/tasks/*.json` - Task definitions
   - `domains/**/evaluators/*.py` - Evaluator functions
   - `domains/**/config.yaml` - Domain configuration
   - `domains/**/README.md` - Domain documentation

2. **MCP Servers**
   - `lbx_mcp_universe_mcp_servers_mothership/servers/**` - All MCP servers
   - Server code, configs, documentation

3. **CLI Submodule**
   - `lbx_mcp_universe_cli/` - CLI submodule reference

4. **Documentation (Plans Only)**
   - `ARCHITECTURE.md` - System architecture
   - `CENTRAL_WORKFLOW.md` - Central workflow guide
   - `frontend/FRONTEND_DEVELOPMENT_PLAN.md` - Frontend plan
   - `backend/API_GATEWAY_PLAN.md` - Backend plan
   - `central/README.md` - Central workflow README
   - `.cursor/rules/**/*.md` - Documentation files

5. **CI/CD Configuration**
   - `.github/workflows/` - GitHub Actions workflows

---

## 🚫 What Stays Local (Not Pushed)

### **❌ Excluded from Git**

1. **Frontend Code**
   - `frontend/src/` - React components, pages
   - `frontend/node_modules/` - Dependencies
   - `frontend/dist/` - Build artifacts
   - `frontend/src/data/*.json` - Auto-generated data

2. **Backend Code**
   - `backend/api/` - FastAPI implementation
   - `backend/mcp/` - MCP client code
   - `backend/services/` - Service logic

3. **Central Workflow Runtime**
   - `central/*.py` - Python scripts (test-runner, frontend-sync)
   - `central/api-registry.yaml` - Runtime registry (has local API keys, test results)

4. **Tests**
   - `tests/` - All test files (local development only)

5. **Environment Files**
   - `.env` - API keys, credentials
   - `*.log` - Log files

---

## 🔍 CI/CD Impact Analysis

### **Current CI/CD Workflow**

**File:** `.github/workflows/ci.yml`

**Triggers On:**
```yaml
paths:
  - "domains/**"  # Only triggers on changes to domains folder
```

**What It Does:**
1. Checks out code
2. Detects changed domains
3. Runs validation (`alignerr_mcp lint-domain`)
4. Runs evaluation (Pass@K testing)
5. Posts results as PR comment

### **✅ Our Changes Don't Affect CI/CD**

**Why:**
- CI/CD only watches `domains/**` folder
- Frontend, backend, central are excluded
- No dependencies on frontend/backend for domain validation
- Existing workflows continue to work

---

## 📋 Git Status Check

### **Before Committing**

```bash
# Check what will be committed
git status

# Should show:
# ✅ domains/** (all domain files)
# ✅ lbx_mcp_universe_mcp_servers_mothership/** (MCP servers)
# ✅ Documentation plans (ARCHITECTURE.md, CENTRAL_WORKFLOW.md, etc.)
# ❌ Should NOT show: frontend/, backend/, central/*.py, tests/
```

---

## 🔄 Workflow: Making Changes

### **1. Domain Changes (Pushed)**

```bash
# Edit domain files
vim domains/healthcare_receptionist/tasks/new_task.json

# Commit
git add domains/
git commit -m "Add new healthcare task"
git push  # ✅ This gets pushed
```

---

### **2. Frontend Changes (Local Only)**

```bash
# Edit frontend
vim frontend/src/pages/Dashboard.tsx

# Check status
git status
# Should show: frontend/ is ignored

# If it shows up, check .gitignore
cat .gitignore | grep frontend
```

---

### **3. Central Workflow Changes (Local Only)**

```bash
# Edit central workflow
vim central/test-runner.py

# Check status
git status
# Should show: central/*.py is ignored

# Only push documentation
git add central/README.md
git commit -m "Update central workflow docs"
git push
```

---

## 🛠️ Troubleshooting

### **Issue 1: Frontend files showing in git status**

**Solution:**
```bash
# Check .gitignore
cat .gitignore | grep frontend

# If frontend/ is not ignored, add it
echo "frontend/" >> .gitignore

# Remove from staging if already added
git rm -r --cached frontend/

# Commit .gitignore
git add .gitignore
git commit -m "Exclude frontend from git"
```

---

### **Issue 2: CI/CD failing after changes**

**Check:**
- Did you modify `domains/**` folder?
- Did you modify `.github/workflows/ci.yml`?
- Are there syntax errors in domain files?

**Solution:**
```bash
# Test locally first
uv run alignerr_mcp lint-domain --domain healthcare_receptionist

# If passes locally, CI/CD should pass
```

---

### **Issue 3: Accidentally committed frontend**

**Solution:**
```bash
# Remove from git but keep locally
git rm -r --cached frontend/

# Commit removal
git add .gitignore
git commit -m "Remove frontend from git tracking"

# Push (removes from remote)
git push
```

---

## ✅ Verification Checklist

Before pushing, verify:

- [ ] `git status` shows only domain files and docs
- [ ] No `frontend/` files in staging
- [ ] No `backend/` implementation files in staging
- [ ] No `central/*.py` files in staging
- [ ] No `tests/` files in staging
- [ ] `.gitignore` is up to date
- [ ] Documentation plans are included (if updated)

---

## 📊 What CI/CD Sees

**When you push:**

```
CI/CD receives:
✅ domains/healthcare_receptionist/tasks/*.json
✅ domains/healthcare_receptionist/evaluators/*.py
✅ domains/healthcare_receptionist/config.yaml
✅ ARCHITECTURE.md (docs)
✅ CENTRAL_WORKFLOW.md (docs)

CI/CD does NOT see:
❌ frontend/src/
❌ backend/api/
❌ central/*.py
❌ tests/
```

**Result:** CI/CD works exactly as before, only validates domains.

---

## 🎯 Summary

**Pushed:**
- ✅ Domain code (tasks, evaluators, configs)
- ✅ MCP servers
- ✅ Documentation plans
- ✅ CI/CD workflows

**Local Only:**
- ❌ Frontend implementation
- ❌ Backend implementation
- ❌ Central workflow scripts
- ❌ Tests
- ❌ API keys, credentials

**CI/CD:**
- ✅ Only watches `domains/**` folder
- ✅ Unaffected by frontend/backend changes
- ✅ Continues to work as before

---

**Last Updated:** 2025-11-04  
**Status:** Git Workflow - Ready for Use


