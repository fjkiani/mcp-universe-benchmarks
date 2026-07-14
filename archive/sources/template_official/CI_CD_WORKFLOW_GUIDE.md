# Resolving CI/CD Issues: Domain Submission Workflow

**Author:** Fahad Kiani 
**Context:** Grant Application Domain - Phase 2A (50 tasks)  
**Issue:** CI/CD not running / Understanding the fork workflow  

---

## 🎯 Problem

When submitting a new domain to LBX MCP Universe, I encountered confusion about:
1. Where to push code (template repo vs dedicated repo)
2. How to trigger CI/CD evaluation
3. Understanding PR workflows and branch structure
4. Enabling GitHub Actions on forked repos

---

## ✅ Solution: The Correct Workflow

### Step 1: Understanding Repository Structure

**There are TWO types of repos:**

| Repo Type | Purpose | Example | Who Manages |
|-----------|---------|---------|-------------|
| **Template Repo** | Framework base | `lbx_mcp_universe_template` | Maintainers |
| **Dedicated Repo** | Your domain work | `lbx_mcp_universe_grant_application` | You (collaborator) |

---

### Step 2: The Correct Submission Flow

```
1. Get added as collaborator to dedicated repo
   └─> Maintainers create: lbx_mcp_universe_[YOUR_DOMAIN]

2. Clone the dedicated repo
   └─> git clone https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_grant_application.git

3. Create your domain in a branch
   └─> git checkout -b initial-implementation
   └─> Build tasks, evaluators, docs

4. Push to dedicated repo
   └─> git push origin initial-implementation

5. Create PR in dedicated repo
   └─> initial-implementation -> main

6. CI/CD runs automatically
   └─> Validation + Evaluation pipeline triggers
   └─> Results posted to PR
```

---

### Step 3: Enabling GitHub Actions (Critical!)

**Issue:** Forked repos have Actions disabled by default for security.

**Fix:**
1. Go to: `https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_[YOUR_DOMAIN]/settings/actions`
2. Click **"Actions"** → **"General"**
3. Enable **"Allow all actions and reusable workflows"**
4. Save

**Then trigger workflow:**
- Push a new commit, OR
- Go to Actions tab → Select "Domain Validation" → "Run workflow"

---

### Step 4: Understanding Branch Protection

**If you get:** "Changes must be made through a pull request"

**This means:**
- You can't push directly to `main`
- You MUST create a PR from a feature branch
- This is normal and expected!

**Correct workflow:**
```bash
# Work in a branch
git checkout -b initial-implementation

# Push to branch
git push origin initial-implementation

# Create PR via GitHub UI
# initial-implementation -> main
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "No available destinations to fork"
**Cause:** You don't have fork permissions  
**Solution:** Maintainers must add you as collaborator to a dedicated repo

---

### Issue 2: "Workflows aren't running on this forked repository"
**Cause:** GitHub disables Actions by default on forks  
**Solution:** Enable Actions in Settings (see Step 3 above)

---

### Issue 3: "CI/CD ran old tasks, not my new ones"
**Cause:** Looking at wrong repo or wrong branch  
**Solution:** 
- Check you're in the DEDICATED repo, not template
- Check the commit SHA matches your latest push
- Verify branch name in Actions tab

---

### Issue 4: "PR number: 0" in CI/CD logs
**Cause:** Workflow can't auto-detect PR number  
**Solution:**
```yaml
# In .github/workflows/ci.yml, add manual input:
workflow_dispatch:
  inputs:
    pr_number:
      description: 'PR number to post results to'
      required: false
      type: number
```

---

## 📊 My Results: Grant Application Domain

**Final Stats:**
- **50 tasks** across 7 categories
- **60% Pass@1** (perfect target range: 30-70%)
- **CI/CD working perfectly** after workflow fixes
- **PR approved** and running evaluation

**Key learnings:**
1. Template repo = community submissions
2. Dedicated repo = your working environment
3. CI/CD only runs in dedicated repo
4. Always enable Actions first!

---

## 🚀 Quick Reference Commands

```bash
# Clone dedicated repo
git clone https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_[DOMAIN].git
cd lbx_mcp_universe_[DOMAIN]

# Create feature branch
git checkout -b initial-implementation

# Build your domain
mkdir -p domains/[domain_name]/{tasks,evaluators}
# ... create tasks and evaluators ...

# Commit and push
git add domains/[domain_name]
git commit -m "feat: Add [domain_name] domain with X tasks"
git push origin initial-implementation

# Create PR via GitHub UI
# Then check: https://github.com/.../actions
```

---

## 🎯 Pro Tips

1. **Test locally first:** Use `alignerr_mcp validate` before pushing
2. **Commit incrementally:** Every 10 tasks for faster feedback
3. **Check Actions tab:** Monitor CI/CD runs in real-time
4. **Read the logs:** Even failures have useful info
5. **Ask maintainers:** Discord is very responsive!

---

## 📚 Related Resources

- **Main Docs:** `WORKFLOW.md` in template repo
- **Setup Guide:** `GETTING_STARTED.md`
- **My Domain:** https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_grant_application
- **PR Example:** https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template/pull/26

---

**Questions?** Drop them in #contributors on Discord! 🚀

**TL;DR:** Work in dedicated repo → Enable Actions → Push to branch → Create PR → CI/CD runs automatically ✅

