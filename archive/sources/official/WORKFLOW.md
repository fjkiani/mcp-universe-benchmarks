# Contribution Workflow

Visual guide to the complete contribution workflow.

## 📊 Process Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CONTRIBUTION WORKFLOW                        │
└─────────────────────────────────────────────────────────────────────┘

1. SETUP (5 minutes)
   ┌──────────────┐
   │ Fork & Clone │ --→ Clone with submodules
   │   Repository │     git clone --recurse-submodules
   └──────────────┘
          ↓
   ┌──────────────┐
   │  Install     │ --→ uv sync
   │ Dependencies │     Installs CLI + deps
   └──────────────┘
          ↓
   ┌──────────────┐
   │   Explore    │ --→ uv run alignerr_mcp list
   │  Reference   │     Study web_search domain
   └──────────────┘

2. DEVELOPMENT (1-2 weeks)
   ┌──────────────┐
   │ Create       │ --→ uv run alignerr_mcp create-domain
   │ Domain       │     Choose domain name
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Create 50+   │ --→ Write JSON task files
   │ Tasks        │     Follow naming convention
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Implement    │ --→ Write evaluation functions
   │ Evaluators   │     Use @compare_func decorator
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Configure    │ --→ Update config.yaml
   │ & Document   │     Write README.md
   └──────────────┘

3. LOCAL VALIDATION (10-30 minutes)
   ┌──────────────┐
   │ Structure    │ --→ uv run alignerr_mcp validate
   │ Validation   │     Check file structure
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Test Tasks   │ --→ Run sample tasks
   │ (Optional)   │     Verify functionality
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Pass@k       │ --→ Check quality metrics
   │ Check        │     Target: 30-70% Pass@1
   └──────────────┘
          ↓
        Pass? ──No──→ Fix issues and retry
          ↓ Yes

4. SUBMIT PR (5 minutes)
   ┌──────────────┐
   │ Create       │ --→ git checkout -b domains/name/v1
   │ Branch       │     Follow naming convention
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Commit       │ --→ git commit -m "feat: Add domain"
   │ Changes      │     Use conventional commits
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Push &       │ --→ gh pr create --title "..."
   │ Create PR    │     Fill out template
   └──────────────┘

5. CI VALIDATION (5-60 minutes)
   ┌──────────────┐
   │ Structure    │ --→ Validates files & config
   │ Check        │     (2-5 minutes)
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Full         │ --→ Runs all tasks
   │ Evaluation   │     (30-60 minutes)
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Bot Posts    │ --→ Results + HTML report link
   │ Results      │     Review metrics
   └──────────────┘
          ↓
        Pass? ──No──→ Review errors, fix, push
          ↓ Yes

6. CODE REVIEW (2-3 days)
   ┌──────────────┐
   │ Maintainer   │ --→ Reviews code quality
   │ Review       │     Checks task quality
   └──────────────┘     Validates docs
          ↓
   ┌──────────────┐
   │ Address      │ --→ Make requested changes
   │ Feedback     │     Re-request review
   └──────────────┘
          ↓
      Approved?
          ↓ Yes

7. MERGE & SYNC (automatic)
   ┌──────────────┐
   │ PR Merged    │ --→ Merged to main branch
   └──────────────┘
          ↓
   ┌──────────────┐
   │ Auto-sync    │ --→ Syncs to mothership
   │ to Mother    │     Domain now available
   └──────────────┘
          ↓
   ┌──────────────┐
   │ 🎉 Done!     │ --→ Your domain is live!
   │ Celebrate    │     Thank you! 🙏
   └──────────────┘
```

## 🔄 Iteration Loops

### Local Development Loop

```
┌─────────────┐
│   Write     │
│   Task      │
└─────┬───────┘
      ↓
┌─────────────┐
│  Validate   │ ←─────┐
│   Locally   │       │
└─────┬───────┘       │
      ↓               │
   Failed? ──Yes─→ Fix Issues
      ↓ No            │
   Continue           │
```

**Typical iterations:** 5-10 times
**Time per iteration:** 2-5 minutes

### CI Feedback Loop

```
┌─────────────┐
│  Push to    │
│     PR      │
└─────┬───────┘
      ↓
┌─────────────┐
│   CI Runs   │ ←─────┐
│  Validation │       │
└─────┬───────┘       │
      ↓               │
   Failed? ──Yes─→ Fix & Push
      ↓ No            │
   Continue           │
```

**Typical iterations:** 1-3 times
**Time per iteration:** 30-60 minutes (CI) + fix time

### Review Feedback Loop

```
┌─────────────┐
│ Maintainer  │
│   Review    │
└─────┬───────┘
      ↓
┌─────────────┐
│  Address    │ ←─────┐
│  Feedback   │       │
└─────┬───────┘       │
      ↓               │
More changes? ──Yes──→ Make Changes
      ↓ No            │
   Approved           │
```

**Typical iterations:** 1-2 times
**Time per iteration:** 1-2 days (review) + fix time

## ⏱️ Timeline Expectations

### Typical First Contribution

| Phase | Duration | Notes |
|-------|----------|-------|
| **Setup** | 5-15 minutes | Includes clone + install |
| **Learning** | 2-4 hours | Study reference domain |
| **Domain Design** | 1-2 days | Plan tasks and categories |
| **Implementation** | 1-2 weeks | Write 50+ tasks + evaluators |
| **Local Testing** | 1-2 hours | Validate and fix issues |
| **PR Submission** | 10 minutes | Create and submit PR |
| **CI Validation** | 30-60 minutes | Automated checks |
| **Code Review** | 2-3 days | Maintainer review |
| **Revisions** | 1-3 days | Address feedback |
| **Merge** | Immediate | Once approved |

**Total:** 1-3 weeks for first contribution

### Subsequent Contributions

With experience, timeline reduces to:
- Implementation: 3-5 days
- Testing: 30 minutes
- Total: 5-7 days

## 🚦 Decision Points

### Should I Submit Now?

```
Are there 50+ tasks? ────No────→ Add more tasks
       ↓ Yes
Does local validation pass? ──No──→ Fix issues
       ↓ Yes
Is Pass@1 between 30-70%? ────No──→ Adjust difficulty
       ↓ Yes
Is documentation complete? ────No──→ Write docs
       ↓ Yes
Any secrets committed? ────Yes────→ Remove secrets
       ↓ No
       ↓
  ✅ SUBMIT PR!
```

### Should I Ask for Help?

```
Stuck for > 30 minutes? ──Yes──→ Check documentation
       ↓ No
Stuck for > 2 hours? ────Yes──→ Search issues
       ↓ No
Stuck for > 4 hours? ────Yes──→ Ask in Discussions
       ↓ No
Keep trying!
```

## 📋 Checklist Progress

Track your progress:

### Phase 1: Setup ☐
- [ ] Repository forked
- [ ] Repository cloned with submodules
- [ ] Dependencies installed (`uv sync`)
- [ ] CLI working (`uv run alignerr_mcp list`)
- [ ] Reference domain explored

### Phase 2: Development ☐
- [ ] Domain structure created
- [ ] 50+ tasks written
- [ ] Tasks follow naming convention
- [ ] Evaluators implemented
- [ ] Config.yaml complete
- [ ] README.md written
- [ ] Task breakdown documented

### Phase 3: Validation ☐
- [ ] Structure validation passes
- [ ] All tasks are valid JSON
- [ ] Evaluators are importable
- [ ] Pass@1 in range (30-70%)
- [ ] Pass@3 in range (50-85%)
- [ ] Zero score < 5%

### Phase 4: Pre-Submission ☐
- [ ] No secrets committed
- [ ] No personal data included
- [ ] .gitignore working correctly
- [ ] Feature branch created
- [ ] Commits follow convention
- [ ] PR description prepared

### Phase 5: PR & Review ☐
- [ ] PR created
- [ ] CI validation passed
- [ ] HTML report reviewed
- [ ] Maintainer feedback addressed
- [ ] Tests passing
- [ ] Documentation approved

### Phase 6: Post-Merge ☐
- [ ] PR merged
- [ ] Auto-sync completed
- [ ] Domain available in mothership
- [ ] Celebrated! 🎉

## 🎯 Success Metrics

### Your Domain is Ready When:

**Technical ✓**
- ✅ 50+ tasks
- ✅ All validations pass
- ✅ Pass@1: 30-70%
- ✅ Pass@3: 50-85%
- ✅ Zero score: <5%

**Quality ✓**
- ✅ Clear task instructions
- ✅ Verifiable answers
- ✅ Robust evaluators
- ✅ Comprehensive docs

**Community ✓**
- ✅ No secrets
- ✅ Follows conventions
- ✅ Responsive to feedback
- ✅ Helpful to others

## 🆘 Common Blockers

### Blocker 1: Can't Get Started

**Symptoms:**
- Don't know what domain to create
- Overwhelmed by process

**Solution:**
1. Read [README.md](README.md) section by section
2. Study `web_search` domain thoroughly
3. Start with a domain you understand well
4. Ask in Discord channel for ideas and guidance

---

### Blocker 2: Local Validation Fails

**Symptoms:**
- Structure validation errors
- Import errors
- JSON syntax errors

**Solution:**
1. Check error message carefully
2. Compare with `web_search` structure
3. Validate JSON with `jq` or online tool
4. See [Troubleshooting](README.md#troubleshooting) section

---

### Blocker 3: Pass Rates Wrong

**Symptoms:**
- Pass@1 > 80% (too easy)
- Pass@1 < 20% (too hard)

**Solution:**
1. Review task difficulty
2. Test with different models
3. Adjust task complexity
4. Check if ground truth is correct
5. Verify evaluators work correctly

---

### Blocker 4: CI Keeps Failing

**Symptoms:**
- Validation passes locally
- Fails in CI

**Solution:**
1. Check CI logs carefully
2. Look for environment differences
3. Verify all dependencies specified
4. Check for hardcoded paths
5. Test in clean environment

---

### Blocker 5: Slow Review

**Symptoms:**
- Waiting > 5 days for review
- No maintainer response

**Solution:**
1. Ensure PR is not in draft mode
2. Check that CI passed
3. Ping maintainers politely
4. Check GitHub notifications settings

## 📊 Example Timeline (Real PR)

Here's a real example timeline:

```
Day 1 (Monday)
  09:00 - Fork and clone ✓
  09:15 - Install dependencies ✓
  10:00 - Finish studying web_search ✓
  14:00 - Plan email_automation domain ✓

Day 2-8 (Tuesday-Monday)
  - Write 50 tasks (7 tasks/day)
  - Implement evaluators
  - Write documentation

Day 9 (Tuesday)
  09:00 - Local validation ✓
  10:30 - Fix 3 JSON errors
  11:00 - Local validation ✓ (Pass@1: 45%)
  14:00 - Create PR
  14:30 - CI validation passes ✓
  15:00 - Full evaluation starts
  16:00 - Bot posts results ✓

Day 10 (Wednesday)
  10:00 - Maintainer posts review
  15:00 - Address feedback (improve 2 tasks)
  16:00 - Push changes
  16:30 - CI runs again ✓

Day 11 (Thursday)
  11:00 - Maintainer approves ✅
  11:05 - PR merged 🎉
  11:10 - Auto-sync to mothership ✓

Total: 11 days
```

## 🎓 Learning Path

### For Absolute Beginners

1. **Week 1:** Setup and exploration
   - Install tools
   - Clone repository
   - Study web_search domain
   - Read all documentation

2. **Week 2:** Simple domain
   - Create domain with 10 tasks
   - Get comfortable with structure
   - Test locally
   - Don't submit yet

3. **Week 3:** Full domain
   - Expand to 50+ tasks
   - Implement all evaluators
   - Complete documentation
   - Submit PR!

### For Experienced Developers

1. **Day 1:** Setup and design
   - Quick setup
   - Review reference
   - Design domain

2. **Days 2-5:** Implementation
   - Write all tasks
   - Implement evaluators
   - Test locally

3. **Day 6:** Submit
   - Create PR
   - Address feedback

## 💡 Pro Tips

1. **Start small, iterate fast**
   - Begin with 10 tasks locally
   - Validate the pattern
   - Scale to 50+

2. **Use reference domain heavily**
   - Copy structure
   - Adapt, don't reinvent
   - Learn patterns

3. **Test continuously**
   - Validate after each task batch
   - Catch issues early
   - Faster overall

4. **Document as you go**
   - Write README alongside tasks
   - Easier than retrofitting
   - Better quality

5. **Ask early**
   - Don't spend days stuck
   - Community is helpful
   - Discussions are for questions

## 📞 Support at Each Stage

| Stage | Need Help With | Resource |
|-------|----------------|----------|
| Setup | Installation, tools | [README Setup](README.md#prerequisites) |
| Learning | Understanding structure | [Reference Example](REFERENCE_EXAMPLE.md) |
| Development | Task design, evaluators | **Discord Channel** - Real-time help |
| Validation | Local testing | [Troubleshooting](README.md#troubleshooting) |
| PR | Submission process | [Contributing](CONTRIBUTING.md) |
| CI | Understanding results | [Section 8 of README](README.md#8-review-ci-results) |
| Review | Feedback interpretation | PR comments, Discord |

---

## 🎉 You're Ready!

Follow this workflow and you'll successfully contribute to LBX MCP Universe!

**Next Steps:**
1. Bookmark this page
2. Start with [README.md](README.md)
3. Follow the steps
4. Ask questions when stuck
5. Celebrate when merged! 🎊

---

**Questions about the workflow?** Ask in the Discord channel for real-time help!

