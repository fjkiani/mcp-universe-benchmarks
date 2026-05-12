# Sprint 3 - Complete Tool Validation & Production Ready

**Start Date:** 2025-11-07  
**Status:** 🎯 Ready to Start  
**Goal:** Test remaining 3 tools, fix permission issues, achieve 100% pass rate

---

## 🎯 Sprint 3 Objectives

### Primary Goals:
1. ✅ Upgrade GitLab token permissions (Developer → Maintainer)
2. ✅ Test remaining 3 tools (create_merge_request, assign_reviewers)
3. ✅ Fix and verify create_milestone and create_release
4. ✅ Achieve 80%+ pass rate on all testable tools
5. ✅ Document production deployment guide

### Success Criteria:
- All 6 testable tools working (create_project documented as requiring personal token)
- CI/CD tests passing in both repos
- Production deployment guide complete
- PRs merged and ready for team use

---

## 📋 Sprint 3 Tasks

### Phase 1: Fix Permission Issues (HIGH PRIORITY)
**Timeline:** 30 minutes  
**Owner:** Alpha

**TASK 3.1: Upgrade GitLab Token**
- [ ] Go to https://gitlab.com/fjkiani/mcp-server/-/settings/access_tokens
- [ ] Delete existing project access token
- [ ] Create new token with:
  - Role: **Maintainer** (not Guest)
  - Scopes: `api`, `read_repository`, `write_repository`
- [ ] Update `GITLAB_TOKEN` environment variable
- [ ] Re-run `test_with_existing_project.py`
- [ ] Verify `create_milestone` and `create_release` now work

**Expected Result:** 5/5 tools passing (100% of testable tools)

---

### Phase 2: Test Remaining Tools (MEDIUM PRIORITY)
**Timeline:** 1-2 hours  
**Owner:** Alpha + Zo

**TASK 3.2: Setup for MR Testing**
- [ ] Create a new branch in mcp-server project
- [ ] Make a small commit (e.g., update README)
- [ ] Push branch to GitLab
- [ ] Note branch name for testing

**TASK 3.3: Test create_merge_request**
- [ ] Update test script with branch names
- [ ] Run `create_merge_request()` test
- [ ] Verify MR created successfully
- [ ] Capture MR IID for next test

**TASK 3.4: Test assign_reviewers_intelligently**
- [ ] Use MR from previous test
- [ ] Assign yourself as reviewer
- [ ] Verify reviewer assignment works
- [ ] Check GitLab UI to confirm

**Expected Result:** 7/8 tools tested, 6-7 working (75-88%)

---

### Phase 3: Documentation & Production Ready (HIGH PRIORITY)
**Timeline:** 1 hour  
**Owner:** Zo

**TASK 3.5: Production Deployment Guide**
Create `lbx_mcp_universe_mcp_servers_mothership/servers/gitlab/PRODUCTION_SETUP.md`

Contents:
```markdown
# GitLab MCP Server - Production Setup Guide

## Prerequisites
1. GitLab account (gitlab.com or self-hosted)
2. Project with appropriate access
3. Python 3.9+

## Token Setup

### For Full Functionality (Recommended):
Use **Personal Access Token**
- Settings → Access Tokens
- Scopes: `api`, `read_repository`, `write_repository`
- Role: Maintainer+
- ✅ All 8 tools work

### For Limited Functionality:
Use **Project Access Token**
- Project Settings → Access Tokens
- Role: Maintainer
- Scopes: `api`, `read_repository`, `write_repository`
- ⚠️  Cannot create new projects (GitLab limitation)
- ✅ 7/8 tools work

## Environment Setup
```bash
export GITLAB_TOKEN="your-token-here"
export GITLAB_URL="https://gitlab.com"  # or your instance
```

## Verification
```bash
cd servers/gitlab
python3 test_with_existing_project.py
```

## Production Checklist
- [ ] Token has appropriate permissions
- [ ] Environment variables set
- [ ] Test script passes
- [ ] Server starts without errors
```

**TASK 3.6: Update Server README**
- [ ] Add "Known Limitations" section
- [ ] Document token requirements
- [ ] Add troubleshooting guide
- [ ] Update examples with real scenarios

**TASK 3.7: Update Domain README**
- [ ] Add "Testing Results" section
- [ ] Document expected pass rates
- [ ] Add performance benchmarks
- [ ] Update CI/CD status

---

### Phase 4: CI/CD & Integration (MEDIUM PRIORITY)
**Timeline:** 30 minutes  
**Owner:** Zo

**TASK 3.8: Verify CI/CD**
- [ ] Check mothership PR CI/CD status
- [ ] Verify structure validation passing
- [ ] Check domain PR CI/CD (if created)
- [ ] Verify LLM tests run

**TASK 3.9: Integration Testing**
- [ ] Test end-to-end workflow: Create project → Issue → MR → Merge
- [ ] Verify all tools work together
- [ ] Document any integration issues

---

## 🎯 Sprint 3 Milestones

### Milestone 1: Permission Fix (Day 1, Hour 1)
- ✅ Token upgraded
- ✅ create_milestone working
- ✅ create_release working
- **Result:** 5/5 current tools passing

### Milestone 2: Remaining Tools (Day 1, Hour 2-3)
- ✅ create_merge_request tested
- ✅ assign_reviewers tested
- **Result:** 7/8 tools tested, 6-7 working

### Milestone 3: Documentation (Day 1, Hour 4)
- ✅ Production guide complete
- ✅ READMEs updated
- ✅ Troubleshooting documented
- **Result:** Ready for production use

### Milestone 4: Final Validation (Day 1, Hour 5)
- ✅ CI/CD passing
- ✅ Integration tests pass
- ✅ PRs ready to merge
- **Result:** Production-ready

---

## 📊 Sprint 3 Metrics (Targets)

| Metric | Current | Target | Stretch |
|--------|---------|--------|---------|
| Tools Tested | 5/8 (63%) | 7/8 (88%) | 8/8 (100%) |
| Pass Rate | 3/5 (60%) | 6/7 (86%) | 7/8 (88%) |
| Documentation | 40% | 90% | 100% |
| CI/CD Status | Passing | Passing | Passing |
| Production Ready | No | Yes | Yes |

---

## 🚧 Blockers & Risks

### Known Blockers:
1. **Token Permissions** - Need Maintainer role
   - **Impact:** HIGH
   - **Fix:** Regenerate token (5 min)
   - **Status:** Actionable now

2. **Branch Creation** - Need push access
   - **Impact:** MEDIUM
   - **Fix:** Create branch manually (10 min)
   - **Status:** Actionable now

### Potential Risks:
1. **API Rate Limiting** - Too many test calls
   - **Mitigation:** Space out tests, use test project
   - **Likelihood:** LOW

2. **GitLab Downtime** - API unavailable
   - **Mitigation:** Test during off-peak hours
   - **Likelihood:** LOW

---

## 🎯 Definition of Done (Sprint 3)

### Must Have:
- [ ] 6/8 tools working (75%+ pass rate)
- [ ] All testable tools validated with real API
- [ ] Production deployment guide complete
- [ ] Known limitations documented
- [ ] CI/CD passing on both PRs

### Should Have:
- [ ] 7/8 tools working (88%+ pass rate)
- [ ] Integration tests passing
- [ ] Troubleshooting guide complete
- [ ] Performance benchmarks documented

### Nice to Have:
- [ ] 8/8 tools tested
- [ ] Video walkthrough of setup
- [ ] Manager handoff document
- [ ] Sprint 4 plan ready

---

## 📈 Progress Tracking

Update this table as tasks complete:

| Task | Status | Time | Notes |
|------|--------|------|-------|
| 3.1: Upgrade Token | ⏸️ | - | Waiting for Alpha |
| 3.2: Setup MR Testing | ⏸️ | - | Needs branch |
| 3.3: Test create_merge_request | ⏸️ | - | Blocked by 3.2 |
| 3.4: Test assign_reviewers | ⏸️ | - | Blocked by 3.3 |
| 3.5: Production Guide | ⏸️ | - | Can start now |
| 3.6: Update Server README | ⏸️ | - | Can start now |
| 3.7: Update Domain README | ⏸️ | - | Can start now |
| 3.8: Verify CI/CD | ⏸️ | - | Can check now |
| 3.9: Integration Testing | ⏸️ | - | Blocked by 3.1 |

---

## 🚀 Immediate Next Steps

### For Alpha (Right Now):
1. Go to https://gitlab.com/fjkiani/mcp-server/-/settings/access_tokens
2. Delete old token
3. Create new Maintainer token
4. Export new token: `export GITLAB_TOKEN="new-token"`
5. Run: `python3 test_with_existing_project.py`
6. Report results

### For Zo (Parallel):
1. Start writing PRODUCTION_SETUP.md
2. Update server README with limitations
3. Check CI/CD status on PRs
4. Prepare integration test script

---

## 💡 Success Indicators

**We'll know Sprint 3 is successful when:**
1. Alpha can create milestones and releases ✅
2. We can test MRs and reviewers ✅
3. Documentation is clear enough for new users ✅
4. CI/CD validates everything automatically ✅
5. PRs are ready to merge ✅

**Sprint 3 Output:**
- Production-ready GitLab MCP server (6-7/8 tools working)
- Complete documentation for deployment
- Clear path for Module 2-7 development
- Team can start using it immediately

---

**Let's go, Alpha!** 🔥 Start with Task 3.1 (upgrade token) while Zo works on docs. We'll be production-ready in 3-4 hours. 🚀

