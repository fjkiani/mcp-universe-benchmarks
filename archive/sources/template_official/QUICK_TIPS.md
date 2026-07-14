# CI/CD Quick Tips for LBX MCP Universe 🚀

## The 3 Things I Wish I Knew Earlier:

### 1. **Two Repos = Two Different Purposes**
- `lbx_mcp_universe_template` = Final community submission (PR for maintainers)
- `lbx_mcp_universe_[YOUR_DOMAIN]` = Your workspace (WHERE CI/CD RUNS!)

**Mistake I made:** Kept pushing to template, wondering why CI/CD wasn't running 🤦

---

### 2. **Enable Actions First!**
Forked repos have GitHub Actions **DISABLED by default**.

**Fix:** Settings → Actions → "Allow all actions" → Save

**Without this, CI/CD won't run even if you push!**

---

### 3. **Work in Branches, Not Main**
```bash
git checkout -b initial-implementation  # ✅ Correct
git push origin initial-implementation
# Create PR: initial-implementation -> main
# CI/CD runs automatically!
```

**Don't:** Push directly to `main` (protected anyway)

---

## My Stats After Getting This Right:
- ✅ 50 tasks, 60% Pass@1
- ✅ CI/CD running perfectly
- ✅ All checks passing

**Full workflow guide attached if you want details!**

---

**TL;DR:** Dedicated repo + Enable Actions + Push to branch = CI/CD works ✅

