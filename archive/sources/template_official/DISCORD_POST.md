# 🎯 CI/CD Workflow Guide (Quick Reference)

**Problem:** CI/CD not running on my Grant Application domain PR

**Root Cause:** Confusion between template repo vs dedicated repo workflow

---

## ✅ The Correct Flow

### 1️⃣ **Two Repositories, Two Purposes**

| Repo | Purpose | When to Use |
|------|---------|-------------|
| `lbx_mcp_universe_template` | Submit to community | Final PR for maintainers |
| `lbx_mcp_universe_[YOUR_DOMAIN]` | Your workspace | Active development + CI/CD |

### 2️⃣ **The Right Workflow**

```
1. Maintainers create dedicated repo for you
   → lbx_mcp_universe_grant_application

2. Clone & work in dedicated repo
   → git checkout -b initial-implementation
   → Build tasks, evaluators, docs

3. Push to branch in dedicated repo
   → git push origin initial-implementation

4. Create PR in dedicated repo
   → CI/CD runs automatically here!

5. (Later) Submit to template repo
   → For community benchmark inclusion
```

### 3️⃣ **Enable GitHub Actions (CRITICAL!)**

**Forked repos have Actions disabled by default.**

**Fix:**
1. Settings → Actions → General
2. Enable "Allow all actions"
3. Save

**Without this, CI/CD won't run!**

---

## 🐛 Common Issues

**Issue:** "Workflows aren't running"  
**Fix:** Enable Actions (see above)

**Issue:** "No PR to fork to"  
**Fix:** Maintainers must add you as collaborator

**Issue:** "CI/CD shows old tasks"  
**Fix:** Check you're in dedicated repo, not template

---

## 📊 My Results

**Grant Application Domain:**
- ✅ 50 tasks, 60% Pass@1 (perfect!)
- ✅ CI/CD working after enabling Actions
- ✅ PR: https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template/pull/26

**Key Insight:** Dedicated repo = where CI/CD runs. Template repo = community submission.

---

## 🚀 TL;DR

1. Work in **dedicated repo** (not template)
2. **Enable Actions** in Settings
3. Push to **branch** → Create **PR**
4. CI/CD runs automatically ✅

Full guide: [attached CI_CD_WORKFLOW_GUIDE.md]

---

Hope this helps others avoid the confusion I hit! 💪

