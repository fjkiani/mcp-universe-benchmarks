# CI/CD Setup for Mothership Repo

**Purpose:** Create automated tests that trigger when server code changes in the mothership repo

---

## 🎯 What We're Building

**GitHub Actions Workflow** that:
- ✅ Triggers on `servers/**` path changes (PRs)
- ✅ Auto-detects changed servers
- ✅ Runs structure validation tests
- ✅ Posts results as PR comments
- ✅ Fails PR if validation fails

---

## 📁 Files Created

### **1. `.github/workflows/ci.yml`**
**Location:** `lbx_mcp_universe_mcp_servers_mothership/.github/workflows/ci.yml`

**What it does:**
- Triggers on PRs with `servers/**` changes
- Detects which servers changed
- Runs `test_structure.py` (if exists) or `validate_servers.py`
- Posts results to PR
- Fails if any server validation fails

**Key Features:**
- Auto-detects changed servers from git diff
- Supports manual dispatch with server name
- Skips draft PRs
- Cancels older runs

---

## 🔧 How It Works

### **Trigger:**
```yaml
on:
  pull_request:
    paths:
      - "servers/**"  # Triggers on server changes
```

### **Detection:**
```bash
# Auto-detects servers from changed files
git diff --name-only $BASE_SHA HEAD | grep '^servers/' | cut -d'/' -f2
```

### **Validation:**
```bash
# For each changed server:
if [ -f "$SERVER/test_structure.py" ]; then
  python3 "$SERVER/test_structure.py"
else
  python3 validate_servers.py "$SERVER"
fi
```

### **Results:**
- ✅ Success: All servers pass → PR can merge
- ❌ Failure: Any server fails → PR blocked
- 📝 Comment: Results posted to PR

---

## 🧪 Test Scripts

### **Option 1: Server-Specific Test**
**File:** `servers/{server_name}/test_structure.py`

**Example:** `servers/gitlab/test_structure.py`
- Tests that specific server
- Custom validation logic
- Returns exit code 0 (pass) or 1 (fail)

### **Option 2: Generic Validation**
**File:** `servers/validate_servers.py`

**Usage:**
```bash
python3 validate_servers.py gitlab
python3 validate_servers.py gitlab nexhealth twilio_hipaa
```

**What it tests:**
- File structure (server.py, pyproject.toml, etc.)
- Python syntax
- FastMCP pattern
- Tool definitions
- Config validation

---

## 📊 Workflow Steps

1. **Checkout** - Get code
2. **Set up Python** - Python 3.12
3. **Detect servers** - From changed files
4. **Validate** - Run tests for each server
5. **Comment** - Post results to PR

---

## ✅ What Gets Tested

**Structure Validation:**
- ✅ All required files present
- ✅ Python syntax valid
- ✅ FastMCP pattern used
- ✅ Tools defined correctly
- ✅ Config valid
- ✅ Dependencies listed

**No API Tests:**
- ⏸️ API tests require tokens (manual)
- ⏸️ Structure tests are sufficient for CI/CD

---

## 🚀 How to Use

### **Automatic (PR):**
1. Create PR with server changes
2. CI/CD automatically runs
3. Check PR comments for results

### **Manual (Workflow Dispatch):**
1. Go to Actions tab
2. Select "Server Validation"
3. Click "Run workflow"
4. Enter server name (or "all")
5. Run

---

## 📝 Example Output

**PR Comment:**
```
## 🔍 Server Validation Results

✅ All 1 server(s) validated successfully

### Results:
✅ **gitlab**: PASSED

---
*Validated servers: gitlab*
```

---

## 🔄 Integration with Template Repo

**Current Flow:**
1. Server code → Mothership repo → CI/CD runs structure tests ✅
2. Domain code → Template repo → CI/CD runs domain tests ✅

**Both workflows:**
- Run automatically on PRs
- Post results to PRs
- Block merge on failure

---

## 🎯 Next Steps

1. **Push workflow file:**
   ```bash
   cd lbx_mcp_universe_mcp_servers_mothership
   git add .github/workflows/ci.yml
   git commit -m "ci: Add server validation workflow"
   git push
   ```

2. **Test it:**
   - Create PR with server changes
   - CI/CD should trigger automatically
   - Check PR comments for results

3. **Add test_structure.py to other servers:**
   - Copy `servers/gitlab/test_structure.py` pattern
   - Customize for each server
   - Or rely on generic `validate_servers.py`

---

**Status:** ✅ Workflow created, ready to push and test!




