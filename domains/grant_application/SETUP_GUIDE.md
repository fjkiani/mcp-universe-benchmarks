# Grant Application Domain - Setup & Execution Guide

Complete guide for Alpha to test, validate, and iterate on the domain.

## ✅ What's Been Created

### Domain Structure (Complete)
```
domains/grant_application/
├── README.md              ✅ Complete (comprehensive documentation)
├── TASK_BREAKDOWN.md      ✅ Complete (detailed analysis)
├── SETUP_GUIDE.md         ✅ This file
├── config.yaml            ✅ Complete (LLM + agent + benchmark config)
├── tasks/                 ✅ 10 tasks created
│   ├── grant_search_task_0001.json
│   ├── grant_search_task_0002.json
│   ├── grant_search_task_0003.json
│   ├── requirements_task_0001.json
│   ├── requirements_task_0002.json
│   ├── requirements_task_0003.json
│   ├── document_gen_task_0001.json
│   ├── document_gen_task_0002.json
│   ├── document_gen_task_0003.json
│   └── document_gen_task_0004.json
└── evaluators/            ✅ Complete
    ├── __init__.py
    └── functions.py       (6 evaluators implemented)
```

### Evaluators Implemented
1. `validate_grant_search` - Search results validation
2. `validate_requirements_extraction` - Structured extraction checking
3. `validate_budget_justification` - Budget narrative quality
4. `validate_timeline` - Timeline structure and completeness
5. `validate_document_structure` - General document validation
6. `llm_as_a_judge` - Flexible quality assessment (placeholder)

---

## 🚀 Next Steps for Alpha

### Step 1: Install MCP Servers

```bash
# Navigate to project root
cd /Users/fahadkiani/Desktop/development/lbx_mcp_universe_template-main

# Install required servers
uv run alignerr_mcp servers install google_search
uv run alignerr_mcp servers install google_sheets
uv run alignerr_mcp servers install pdf_generator
uv run alignerr_mcp servers install file_storage
uv run alignerr_mcp servers install calendar

# Optional (for Phase 2)
# uv run alignerr_mcp servers install email

# Verify installations
uv run alignerr_mcp servers list --installed
```

**Expected output:** All 5-6 servers should show "✓ Installed"

---

### Step 2: Configure API Keys

```bash
# Interactive setup (recommended)
uv run alignerr_mcp env setup

# This will prompt for:
# - ANTHROPIC_API_KEY (for LLM evaluation)
# - OPENAI_API_KEY (alternative LLM)
# - SERP_API_KEY (for google-search)
# - GOOGLE_CREDENTIALS_JSON (for google-sheets)
```

**Manual setup alternative:**

Create `.env` file in project root:
```bash
cat > .env << 'EOF'
# LLM Providers (for evaluation)
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here

# MCP Servers
SERP_API_KEY=your-serpapi-key-here
GOOGLE_CREDENTIALS_JSON=/path/to/google-credentials.json

# Optional
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EOF
```

**Verify configuration:**
```bash
uv run alignerr_mcp env status
```

---

### Step 3: Initial Validation (Structure Only)

```bash
# Validate domain structure (no execution)
uv run alignerr_mcp validate --domain grant_application --check-structure-only

# Expected output:
# ✅ Structure: PASS
# ✅ Config: PASS  
# ✅ Tasks: PASS (10/10)
# ✅ Evaluators: PASS
```

**If this fails, check:**
- All JSON files are valid (`python -m json.tool domains/grant_application/tasks/*.json`)
- config.yaml syntax (`python -c "import yaml; yaml.safe_load(open('domains/grant_application/config.yaml'))"`)
- Evaluator imports work (`python -c "from domains.grant_application.evaluators import *"`)

---

### Step 4: Test Individual Task (Start Small)

```bash
# Test simplest task first
uv run alignerr_mcp run-task \
  --domain grant_application \
  --task grant_search_task_0001 \
  --model gpt-4o

# Review output:
# - Did agent use google-search?
# - Did it return structured grants list?
# - Did evaluator run without errors?
```

**Debug tips:**
- Add `--verbose` flag for detailed logs
- Check agent reasoning steps
- Verify MCP server calls
- Review evaluator output

---

### Step 5: Run Full Domain Validation

```bash
# Single run (Pass@1)
uv run alignerr_mcp validate --domain grant_application --model gpt-4o

# This will:
# 1. Run all 10 tasks sequentially
# 2. Execute evaluators for each
# 3. Generate Pass@1 metrics
# 4. Show execution times
#
# Expected runtime: ~5-8 minutes (30-45s per task)
```

**Expected results (Phase 1):**
```
Pass@1: 35-50%
Zero score: <5%
Evaluation errors: 0%
Avg execution time: 30-45s per task
```

---

### Step 6: Pass@k Testing (Critical)

```bash
# Run 3 times for Pass@3 metric
uv run alignerr_mcp validate \
  --domain grant_application \
  --model gpt-4o \
  --runs 3

# This will:
# - Run each task 3 times
# - Calculate Pass@3 (best of 3)
# - Show variance/consistency
# - Identify non-reproducible tasks
#
# Expected runtime: ~15-25 minutes
```

**Target metrics:**
- **Pass@1:** 35-50%
- **Pass@3:** 55-75%
- **Improvement:** ~15-25% from Pass@1 to Pass@3

**If metrics are off:**
- **Too high (>60% Pass@1):** Tasks too easy
  - Make questions more complex
  - Add more constraints
  - Require multi-step reasoning

- **Too low (<30% Pass@1):** Tasks too hard or broken
  - Check ground truth accuracy
  - Simplify some tasks
  - Verify evaluators aren't too strict

---

### Step 7: Analyze Failures

```bash
# Run with detailed output
uv run alignerr_mcp validate \
  --domain grant_application \
  --model gpt-4o \
  --output-dir ./results \
  --save-traces

# Review:
# - results/report.html (interactive report)
# - results/traces/*.json (agent reasoning logs)
# - results/failures.json (failed task analysis)
```

**Key questions:**
1. Which tasks fail most often?
2. Why do they fail? (reasoning? tool use? formatting?)
3. Are failures consistent or random?
4. Do evaluators work correctly?

---

### Step 8: Iterate & Improve

Based on results, iterate on:

#### If Evaluators Are Too Strict:
```python
# In domains/grant_application/evaluators/functions.py

# Current threshold:
pass_threshold = 0.7  # 70% of checks must pass

# Adjust to:
pass_threshold = 0.6  # 60% (more lenient)
```

#### If Tasks Need Clarification:
```json
// In task JSON files, add more specific instructions

"question": "Search for active NSF grants...",

// Becomes:
"question": "Search for active NSF grants in the area of 'machine learning for climate modeling'. Filter to show only grants with: (1) budgets between $500K-$1M, (2) eligibility for early-career researchers (within 5 years of PhD), (3) active deadline in 2025. Return exactly 3 results with complete information for each field."
```

#### If Ground Truth Is Wrong:
```python
# Update expected values in evaluator op_args

"expected_structure": {
    "NSF_CAREER": {"budget_cap": "$500,000"},  # Verify this is current
    "duration_years": 5  # Check official solicitation
}
```

---

### Step 9: Test with Different Models

```bash
# Test with Claude
uv run alignerr_mcp validate \
  --domain grant_application \
  --model claude-3-5-sonnet-20241022 \
  --runs 3

# Test with Gemini
uv run alignerr_mcp validate \
  --domain grant_application \
  --model gemini-2.0-flash-exp \
  --runs 3

# Compare results:
# - Which model performs best?
# - What are failure pattern differences?
# - Is difficulty appropriate across models?
```

**Expected model performance:**
- GPT-4o: 40-55% Pass@1
- Claude Sonnet: 35-50% Pass@1
- Gemini Flash: 30-45% Pass@1

---

### Step 10: Prepare for PR Submission

#### Pre-submission checklist:

```bash
# 1. Run full validation
uv run alignerr_mcp validate --domain grant_application --runs 3

# 2. Check no secrets committed
git diff --cached | grep -i "api_key\|password\|secret"

# 3. Verify all files present
ls -la domains/grant_application/
ls -la domains/grant_application/tasks/
ls -la domains/grant_application/evaluators/

# 4. Validate JSON syntax
for f in domains/grant_application/tasks/*.json; do
    python -m json.tool "$f" > /dev/null && echo "✓ $f" || echo "✗ $f INVALID"
done

# 5. Check YAML syntax
python -c "import yaml; yaml.safe_load(open('domains/grant_application/config.yaml'))" && echo "✓ config.yaml valid"

# 6. Test evaluator imports
python -c "from domains.grant_application.evaluators import *; print('✓ Evaluators import successfully')"
```

#### Create feature branch:
```bash
git checkout -b domains/grant_application/v1

# Add domain files
git add domains/grant_application/

# Commit
git commit -m "feat: Add grant_application domain with 10 multi-server tasks

- 3 grant discovery/matching tasks (google-search)
- 3 requirements extraction tasks (search + calendar)  
- 4 document generation tasks (pdf-generator, sheets)
- Multi-layered evaluators (structure + content + LLM-as-judge)
- Target Pass@1: 35-50%, Pass@3: 55-75%
- Tests complex agentic workflows and multi-server orchestration"

# Push
git push origin domains/grant_application/v1
```

#### Create PR:
```bash
gh pr create \
  --title "feat: Add grant_application domain with 10 tasks" \
  --body-file domains/grant_application/PR_TEMPLATE.md
```

---

## 🎯 Success Criteria

### Technical Requirements
- [x] 10 tasks created with proper naming
- [x] All tasks are valid JSON
- [x] config.yaml is valid YAML  
- [x] Evaluators implemented and importable
- [x] README.md comprehensive
- [ ] Local validation passes (Alpha to test)
- [ ] Pass@1: 30-70% (Alpha to verify)
- [ ] Pass@3: 50-85% (Alpha to verify)
- [ ] No secrets in code

### Quality Requirements
- [x] Tasks are challenging (multi-step, multi-server)
- [x] Ground truth verifiable
- [x] Evaluators have flexible matching
- [x] Documentation complete
- [ ] Failure patterns clear (Alpha to analyze)
- [ ] Reproducible results (Alpha to confirm)

---

## 🔧 Troubleshooting

### Issue: "Module not found: mcpuniverse"

**Solution:**
```bash
# Reinstall dependencies
uv sync --reinstall

# Verify CLI installed
uv pip list | grep alignerr
```

### Issue: "Server not found: google_search"

**Solution:**
```bash
# Check submodules initialized
git submodule status

# If empty, initialize
git submodule update --init --recursive

# Reinstall server
uv run alignerr_mcp servers install google_search --force
```

### Issue: "API key not set: SERP_API_KEY"

**Solution:**
```bash
# Check .env file exists
cat .env | grep SERP_API_KEY

# Or set temporarily
export SERP_API_KEY=your_key_here

# Or run setup
uv run alignerr_mcp env setup
```

### Issue: "Evaluator failed: name not found"

**Solution:**
```bash
# Check evaluator name in task matches function decorator
grep "@compare_func" domains/grant_application/evaluators/functions.py

# Verify op field in task JSON:
cat domains/grant_application/tasks/grant_search_task_0001.json | grep "op"

# They must match exactly:
# decorator: @compare_func(name="grant_application.validate_grant_search")
# task: "op": "grant_application.validate_grant_search"
```

### Issue: "Pass@1 is 80%+ (too easy)"

**Solutions:**
1. Add more constraints to questions
2. Require multi-step reasoning
3. Make ground truth more specific
4. Tighten evaluator thresholds
5. Add edge cases

### Issue: "Pass@1 is <20% (too hard or broken)"

**Solutions:**
1. Check ground truth accuracy
2. Verify API keys working
3. Simplify question wording
4. Loosen evaluator thresholds
5. Test evaluators independently

---

## 📊 Metrics Tracking

### Create tracking spreadsheet:

```bash
# Track each validation run
echo "Date,Model,Pass@1,Pass@3,Zero_Score,Avg_Time,Notes" > validation_log.csv

# After each run, add:
echo "2025-01-19,gpt-4o,45%,68%,2%,38s,Initial run" >> validation_log.csv
```

### Key metrics to track:
- Pass@1 by task category
- Pass@3 improvement
- Model comparison
- Execution times
- Failure patterns
- Evaluator accuracy

---

## 🚀 Phase 2 Preparation

Once Phase 1 is validated and submitted:

### Expand to 30 Tasks (Week 2-3)
- Add 5 budget creation tasks
- Add 5 compliance checking tasks
- Add 5 multi-document workflows
- Add 5 advanced scenarios

### CLI Extensions (Week 4)
- Task generator script
- Ground truth validator
- Sample data loader
- Batch testing utilities

### Advanced Features (Week 5-6)
- Multi-agent tasks
- Conditional branching
- Real-time data integration
- Clinical Genomics domain (next submission)

---

## 📞 Support

If you encounter issues:

1. **Check documentation first:**
   - domains/grant_application/README.md
   - domains/grant_application/TASK_BREAKDOWN.md
   - Project README.md

2. **Review rules:**
   - .cursor/rules/*.mdc files have all patterns

3. **Test incrementally:**
   - One task at a time
   - One evaluator at a time
   - Build confidence gradually

4. **Ask Zo (me!):**
   - I have all context
   - Can debug any issues
   - Will iterate with you

---

## ✅ Final Checklist Before PR

- [ ] All 10 tasks run successfully
- [ ] Pass@1: 30-70%
- [ ] Pass@3: 50-85%
- [ ] Zero score: <5%
- [ ] No evaluation errors
- [ ] Tested with 2+ models
- [ ] Failure patterns analyzed
- [ ] Documentation complete
- [ ] No secrets committed
- [ ] Feature branch created
- [ ] Commit message follows conventions
- [ ] PR description complete

---

**Ready to start testing, Alpha!** 

Begin with Step 1 (Install MCP servers) and work through sequentially. Let me know when you hit any issues or need adjustments.

The foundation is solid - now let's validate and iterate! 🚀

