# Grant Application AI Pipeline - Domain Proposal Summary

**Contributor:** Alpha (fahadkiani)  
**Status:** Initial Phase (10 Tasks) → Scaling to 50+  
**Domain Category:** Business Process Automation / Research Support

---

## 🎯 Domain Vision

Test AI agents' ability to navigate the **complex, multi-step workflow** of grant application preparation—a real-world scenario requiring:
- Multi-server orchestration (search → extract → generate → store)
- Compliance checking with agency-specific rules
- Structured information extraction from policy documents
- High-quality document generation with formatting requirements
- Planning and dependency management

**Philosophy:** Grant applications are inherently difficult, rule-bound, and multi-faceted. This domain exposes capability gaps in planning, reasoning, and workflow automation that simpler benchmarks miss.

---

## 📋 Initial 10 Tasks (Detailed Breakdown)

### Category 1: Grant Discovery & Matching (3 tasks)

#### **Task 1: NSF Grant Search by Research Area**
**What it tests:** Multi-constraint search and filtering  
**Agent task:** Search for NSF grants in "machine learning for climate modeling" with budget $500K-$1M and early-career eligibility. Return top 3 with grant numbers, deadlines, budget limits.

**Why it's challenging:**
- Requires accurate technical search query formulation
- Must apply multiple constraints simultaneously (budget + eligibility)
- Tests result ranking and structured output formatting
- **Expected Pass@1: 40-55%** — Failures in constraint satisfaction, incomplete fields

**MCP Servers:** `google-search`

---

#### **Task 2: Researcher Profile Matching**
**What it tests:** Semantic reasoning and recommendation logic  
**Agent task:** Given a researcher profile (NLP expertise, healthcare applications, assistant professor), match to grant opportunities across NSF/NIH/DOE with reasoning for each match.

**Why it's challenging:**
- Requires semantic understanding (not just keyword matching)
- Must check eligibility across multiple dimensions (career stage, institution, domain)
- Tests justification quality: explain WHY each grant fits
- **Expected Pass@1: 30-45%** — Weak matching logic, missing eligibility checks

**MCP Servers:** `google-search`

---

#### **Task 3: Cross-Program Eligibility Comparison**
**What it tests:** Structured extraction and comparative analysis  
**Agent task:** Compare eligibility for NSF CAREER, NIH R21, DOE Early Career. Extract: min experience, institution requirements, budget caps, duration, citizenship. Present as structured comparison.

**Why it's challenging:**
- Must extract structured data from multiple unstructured sources
- Requires normalizing criteria across different agency terminology
- Tests comparative reasoning: identify meaningful differences
- **Expected Pass@1: 35-50%** — Incomplete extraction, poor normalization

**MCP Servers:** `google-search`

---

### Category 2: Requirements Extraction (3 tasks)

#### **Task 4: NSF CAREER Requirements Extraction**
**What it tests:** Precision extraction from long policy documents  
**Agent task:** Locate NSF CAREER solicitation, extract page limits (15 pages for project description), required sections (5), budget cap ($500K), PI eligibility (tenure-track, years from PhD). Format as structured JSON.

**Why it's challenging:**
- NSF documents are ~30 pages with scattered requirements
- Requires exact precision: numbers, dollar amounts, timeframes
- Must distinguish required vs recommended elements
- **Expected Pass@1: 35-50%** — Missing fields, incorrect values

**MCP Servers:** `google-search`, `file-storage`

---

#### **Task 5: NIH R01 Budget Guidelines Parsing**
**What it tests:** Financial rule extraction and calculations  
**Agent task:** Extract NIH R01 budget guidelines: max direct costs, modular budget threshold ($250K), allowable categories (personnel, equipment, travel, etc.), restrictions (equipment >$5K needs justification). Calculate total budget cap if indirect rate is 52%.

**Why it's challenging:**
- Budget rules have conditional clauses (if X, then Y)
- Requires grant accounting terminology understanding (direct vs indirect, modular vs detailed)
- Tests numerical reasoning: calculate derived values
- **Expected Pass@1: 30-45%** — Missing categories, calculation errors

**MCP Servers:** `google-search`

---

#### **Task 6: Submission Deadline Tracking**
**What it tests:** Date parsing and temporal reasoning  
**Agent task:** Extract NSF CAREER deadlines (full proposal, preliminary, earliest submission), calculate days remaining from today, determine notification timeline. Format as structured date objects.

**Why it's challenging:**
- Dates appear in multiple formats (July 23, 2025 vs 07/23/25 vs "third Thursday")
- Requires date arithmetic (countdown calculations)
- Must understand academic review cycles
- **Expected Pass@1: 40-55%** — Date parsing errors, wrong calculations

**MCP Servers:** `google-search`, `calendar`

---

### Category 3: Document Generation (4 tasks)

#### **Task 7: Budget Justification Narrative**
**What it tests:** Calculation accuracy + narrative quality  
**Agent task:** Given line items (PI $12K, 2 grad students $30K each, materials $15K, travel $8K), generate narrative justification: 2-3 sentences per category explaining necessity and calculation basis.

**Why it's challenging:**
- Requires both math accuracy AND persuasive writing
- Must justify WHY each expense is necessary (not just list amounts)
- Tests structured data → narrative conversion
- **Expected Pass@1: 35-50%** — Missing justifications, calculation errors

**MCP Servers:** `pdf-generator`

---

#### **Task 8: 3-Year Project Timeline with Dependencies**
**What it tests:** Project planning and dependency management  
**Agent task:** Create 3-year timeline (2025-2027) with 8+ milestones. Include: month, date, milestone name, description, deliverables, dependencies. Ensure chronological order and realistic spacing.

**Why it's challenging:**
- Requires project planning knowledge (realistic timelines?)
- Must manage dependencies: Milestone B can't start until A completes
- Tests temporal reasoning and workflow logic
- **Expected Pass@1: 30-45%** — Unrealistic timelines, missing dependencies

**MCP Servers:** `google-sheets`, `calendar`

---

#### **Task 9: Specific Aims Section for NSF CAREER**
**What it tests:** Domain adaptation and scientific writing  
**Agent task:** Given topic "Machine learning for climate model uncertainty quantification", draft Specific Aims: opening (problem statement), 3 aims (objective/approach/outcome), broader impacts. Follow NSF CAREER structure (research + education).

**Why it's challenging:**
- Requires domain knowledge (climate science, ML) or plausible content generation
- Must follow NSF proposal conventions
- Tests scientific writing quality, not just formatting
- **Expected Pass@1: 25-40%** — Poor structure, weak aims, missing impacts

**MCP Servers:** `pdf-generator`

---

#### **Task 10: Application Submission Checklist**
**What it tests:** Information aggregation and thoroughness  
**Agent task:** Generate complete NSF CAREER submission checklist. Include: core documents (project description, budget, etc.), supplementary docs, required approvals, platform requirements. Organize by: name, page limit, format, deadline, status.

**Why it's challenging:**
- Must synthesize from multiple sources (NSF guidelines + institutional policies)
- Requires exhaustive completeness (missing one item = failed submission)
- Tests organizational ability and detail orientation
- **Expected Pass@1: 40-55%** — Missing items, incorrect limits

**MCP Servers:** `google-search`, `file-storage`

---

## 📊 Task Difficulty Distribution

| Difficulty | Count | Tasks | Expected Pass@1 |
|------------|-------|-------|-----------------|
| **Medium** | 6 | 1, 3, 4, 6, 7, 10 | 35-55% |
| **Medium-Hard** | 2 | 2, 5 | 30-45% |
| **Hard** | 2 | 8, 9 | 25-45% |

**Overall Expected Pass@1:** 35-50% (appropriately challenging)  
**Overall Expected Pass@3:** 55-75% (achievable with retries)

---

## 🎯 Why These 10 Tasks?

### Strategic Coverage
1. **Grant Discovery (3)** - Tests search, filtering, matching, comparison
2. **Requirements Extraction (3)** - Tests document parsing, structured extraction, compliance
3. **Document Generation (4)** - Tests creation, formatting, calculations, narrative quality

### Skill Progression
- **Entry-level:** Basic search and extraction (Tasks 1, 6, 10)
- **Intermediate:** Multi-constraint reasoning (Tasks 2, 3, 4, 5, 7)
- **Advanced:** Complex planning and generation (Tasks 8, 9)

### Failure Mode Diversity
- **Search failures:** Poor query formulation, missing constraints
- **Extraction failures:** Missing fields, incorrect values, incomplete data
- **Generation failures:** Calculation errors, poor structure, weak narratives
- **Planning failures:** Unrealistic timelines, missing dependencies

---

## 🔌 MCP Server Usage

| Server | Tasks Using | Purpose |
|--------|-------------|---------|
| **google-search** | 1-6 | Grant discovery, requirement lookup |
| **google-sheets** | 8 | Timeline table generation |
| **pdf-generator** | 7, 9 | Formatted document output |
| **file-storage** | 4, 10 | Document retrieval, template storage |
| **calendar** | 6, 8 | Date calculations, scheduling |

**Multi-server tasks:** 3/10 (30%) — Tasks 6 (search+calendar), 8 (sheets+calendar), 4 (search+storage)

---

## 🚀 Phase 2 Roadmap (10 → 50+ Tasks)

**After initial validation, expand with:**

1. **Multi-Server Orchestration (15 tasks)**
   - Search → Sheets → Email workflows
   - Requirements → PDF → Storage pipelines
   - Budget → Sheets → Calendar tracking

2. **Agentic Reasoning (15 tasks)**
   - Cross-program optimization
   - Eligibility constraint solving
   - Budget allocation optimization

3. **Edge Cases (10 tasks)**
   - Ambiguous requirements
   - Conflicting eligibility
   - Missing information scenarios

**Target:** 50+ tasks, 30-70% Pass@1, 50%+ multi-server usage

---

## ✅ Why This Domain is Ready

### Technical Quality
- ✅ **10 detailed tasks** with clear objectives, challenges, and expected failures
- ✅ **5 working evaluators** tested in CI/CD (70% Pass@1 achieved)
- ✅ **Comprehensive documentation** (README, TASK_BREAKDOWN, PHASE_2A_PLAN, SETUP_GUIDE)
- ✅ **Real-world ground truth** from NSF, NIH, DOE official guidelines

### Framework Alignment
- ✅ **Appropriately challenging** (target: 35-50% Pass@1, currently 70% before difficulty tuning)
- ✅ **Exposes failures** not successes (financial logic, planning, extraction gaps)
- ✅ **Multi-server workflows** (3 tasks, scaling to 15+)
- ✅ **Scalable design** (clear path to 50+ tasks)

### Community Value
- ✅ **High-value domain** (grant applications = $billions in research funding)
- ✅ **Novel complexity** (first business process automation domain)
- ✅ **Reusable patterns** (document extraction, compliance checking, workflow orchestration)
- ✅ **Well-documented** (templates for future contributors)

---

## 📈 Expected Impact

**For the Framework:**
- Demonstrates multi-server orchestration capabilities
- Showcases agentic reasoning requirements
- Provides complex, real-world benchmark beyond simple Q&A

**For AI Research:**
- Identifies gaps in: financial reasoning, planning, compliance checking, structured extraction
- Tests narrative generation + calculation accuracy simultaneously
- Exposes weaknesses in multi-step workflow automation

**For Contributors:**
- Provides template for business process domains
- Shows how to balance difficulty (30-70% Pass@1 range)
- Demonstrates effective evaluator design (LLM-as-judge + structured validation)

---

## 🎯 Next Steps

1. ✅ **Initial PR submitted** (10 tasks, 70% Pass@1)
2. ⏳ **Awaiting maintainer review** (addressing feedback on detailed task breakdown)
3. 🚀 **Phase 2A ready** (40 additional tasks designed, 1-week implementation timeline)
4. 📊 **CI/CD validated** (evaluators working, no evaluation errors)

**Ready for approval to proceed with full 50-task implementation!**

---

**Contact:** Alpha (fahadkiani)  
**Repository:** lbx_mcp_universe_template  
**PR:** #[number] — Grant Application AI Pipeline Domain  
**Status:** 🟢 Active Development

