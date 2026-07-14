# Grant Application AI Pipeline - Task Breakdown

Detailed categorization and analysis of benchmark tasks.

## Overview

- **Total Tasks (Phase 1):** 10
- **Categories:** 3
- **Difficulty Distribution:** 30% Easy, 50% Medium, 20% Hard
- **Multi-Server Tasks:** 3 (30%)
- **Expected Pass@1:** 35-50%
- **Expected Pass@3:** 55-75%

## Task Categories

### Category 1: Grant Discovery & Matching (3 tasks)

**Purpose:** Test agent's ability to search, filter, and match grant opportunities using search APIs.

**MCP Servers:** google-search

**Complexity:** Medium

| Task ID | Description | Key Skills | Expected Pass@1 |
|---------|-------------|------------|-----------------|
| grant_search_task_0001 | Search NSF grants by research area and budget | Search API, filtering | 40-55% |
| grant_search_task_0002 | Match researcher profile to opportunities | Comparative analysis, reasoning | 30-45% |
| grant_search_task_0003 | Compare eligibility across programs | Structured extraction, comparison | 35-50% |

**Common Failure Patterns:**
- Incomplete filtering (missing budget/eligibility constraints)
- Search query formulation issues
- Result ranking errors
- Missing or incorrect fields in structured output

**Why These Tasks Matter:**
- Tests multi-constraint search capabilities
- Requires semantic understanding of grant requirements
- Exposes reasoning gaps in profile matching

---

### Category 2: Requirements Extraction (3 tasks)

**Purpose:** Test structured information extraction from complex policy documents.

**MCP Servers:** google-search, calendar (for deadlines)

**Complexity:** Medium-Hard

| Task ID | Description | Key Skills | Expected Pass@1 |
|---------|-------------|------------|-----------------|
| requirements_task_0001 | Extract NSF CAREER requirements | Document parsing, structure | 35-50% |
| requirements_task_0002 | Parse NIH R01 budget guidelines | Detailed extraction, rules | 30-45% |
| requirements_task_0003 | Track submission deadlines | Date handling, calculation | 40-55% |

**Common Failure Patterns:**
- Missing required fields
- Incorrect numeric extraction (page limits, budget caps)
- Date calculation errors
- Incomplete rule understanding

**Why These Tasks Matter:**
- Real-world document complexity
- Tests attention to detail
- Requires compliance checking capabilities
- Exposes structured extraction weaknesses

---

### Category 3: Document Generation (4 tasks)

**Purpose:** Test creation of compliant application materials with proper formatting and content.

**MCP Servers:** pdf-generator, google-sheets, calendar

**Complexity:** Medium-Hard

| Task ID | Description | Key Skills | Expected Pass@1 |
|---------|-------------|------------|-----------------|
| document_gen_task_0001 | Generate budget justification | Narrative generation, math | 35-50% |
| document_gen_task_0002 | Create project timeline | Planning, dates, dependencies | 30-45% |
| document_gen_task_0003 | Draft specific aims | Scientific writing, structure | 25-40% |
| document_gen_task_0004 | Compile submission checklist | Organization, completeness | 40-55% |

**Common Failure Patterns:**
- Budget calculation errors
- Missing justification details
- Poor timeline structure
- Incomplete checklists
- Formatting issues
- Missing required sections

**Why These Tasks Matter:**
- Tests generation + compliance simultaneously
- Requires domain knowledge application
- Exposes planning and structuring weaknesses
- Multi-step reasoning with calculations

---

## Difficulty Distribution

### Easy Tasks (30% - 3 tasks)
- grant_search_task_0001 (basic search)
- requirements_task_0003 (deadline tracking)
- document_gen_task_0004 (checklist compilation)

**Characteristics:**
- Single primary skill
- Clear success criteria
- Direct MCP server usage
- Limited reasoning depth

**Expected Pass@1:** 40-60%

---

### Medium Tasks (50% - 5 tasks)
- grant_search_task_0002 (profile matching)
- grant_search_task_0003 (eligibility comparison)
- requirements_task_0001 (requirement extraction)
- requirements_task_0002 (budget guidelines)
- document_gen_task_0001 (budget justification)

**Characteristics:**
- Multiple skills combined
- Requires interpretation
- Some reasoning required
- Structured output validation

**Expected Pass@1:** 30-50%

---

### Hard Tasks (20% - 2 tasks)
- document_gen_task_0002 (timeline with dependencies)
- document_gen_task_0003 (specific aims drafting)

**Characteristics:**
- Complex multi-step reasoning
- Domain knowledge application
- Quality assessment needed
- Multiple validation criteria

**Expected Pass@1:** 20-40%

---

## Multi-Server Orchestration

### Single Server Tasks (7 tasks)
- Pure search: grant_search_task_0001, 0002
- Pure extraction: requirements_task_0001, 0002
- Pure generation: document_gen_task_0001, 0003, 0004

### Multi-Server Tasks (3 tasks)
1. **grant_search_task_0003**
   - google-search → google-sheets (comparison table)
   - Tests: Sequential server usage

2. **requirements_task_0003**
   - google-search → calendar (deadline tracking)
   - Tests: Date calculation workflow

3. **document_gen_task_0002**
   - calendar → google-sheets (timeline generation)
   - Tests: Integrated planning workflow

**Multi-Server Complexity:**
- Requires proper sequencing
- Data transfer between servers
- Compound error potential
- Expected Pass@1: 25-40% (harder than single-server)

---

## Evaluation Strategy per Category

### Grant Discovery (Category 1)
**Primary Evaluator:** `validate_grant_search`

**Checks:**
- Minimum result count (3)
- Required fields present
- Data format validity
- Relevance to query

**Pass Threshold:** 70% of checks successful

---

### Requirements Extraction (Category 2)
**Primary Evaluator:** `validate_requirements_extraction`

**Checks:**
- Expected structure present
- Key values accurate
- Completeness score
- Field-by-field validation

**Pass Threshold:** 70% match with ground truth

---

### Document Generation (Category 3)
**Primary Evaluators:** 
- `validate_budget_justification` (for budgets)
- `validate_timeline` (for timelines)
- `validate_document_structure` (for general docs)

**Checks:**
- Required sections present
- Content completeness
- Format compliance
- Calculation accuracy
- Narrative quality

**Pass Threshold:** 75% of criteria met

---

## Expected Failure Analysis

### High-Failure Tasks (Expected <35% Pass@1)
1. **document_gen_task_0003** (specific aims)
   - Requires scientific writing quality
   - Domain knowledge needed
   - Structure + content both critical

2. **document_gen_task_0002** (timeline with dependencies)
   - Complex dependency tracking
   - Date calculations across 3 years
   - Milestone interconnections

3. **grant_search_task_0002** (profile matching)
   - Semantic reasoning required
   - Must justify matches
   - Multiple constraint satisfaction

**Why High Failure is Good:**
- Exposes reasoning limitations
- Tests complex planning
- Requires domain adaptation
- Perfect for capability gap identification

### Medium-Failure Tasks (35-50% Pass@1)
- Most tasks in this range
- Balanced difficulty
- Clear but challenging requirements

### Low-Failure Tasks (>50% Pass@1)
- Basic search and extraction
- Should be achievable
- Validates agent baseline capabilities

---

## Phase 2 Expansion Plan (20 additional tasks)

### New Categories to Add

**Category 4: Budget Creation (5 tasks)**
- Generate detailed budget tables
- Calculate indirect costs
- Justify equipment purchases
- Personnel cost calculations
- Multi-year budget projections

**Category 5: Compliance Checking (5 tasks)**
- Validate page limits
- Check formatting requirements
- Verify eligibility criteria
- Cross-reference budget caps
- Deadline compliance validation

**Category 6: Multi-Document Workflows (5 tasks)**
- Integrated application assembly
- Cross-document consistency checks
- Version control and tracking
- Collaborative editing simulation
- Final submission package creation

**Category 7: Advanced Scenarios (5 tasks)**
- Resubmission with reviewer responses
- Multi-PI coordination
- Budget revision scenarios
- Scope change management
- Deadline extension requests

**Expected Phase 2 Metrics:**
- Total tasks: 30
- Pass@1: 30-50% (maintained difficulty)
- Multi-server tasks: 50%
- Complex workflows: 40%

---

## Ground Truth Verification

### Data Sources
1. **NSF Official Documentation**
   - CAREER solicitation (verified annually)
   - Budget guidelines
   - Formatting requirements

2. **NIH Grant Information**
   - R01 RFP documents
   - Budget policies
   - Submission requirements

3. **DOE Programs**
   - Early Career Research Program guidelines
   - Eligibility criteria

4. **Institutional Resources**
   - University grant office materials
   - Successful application examples
   - Budget templates

### Verification Process
- All numeric values cross-referenced
- Requirements extracted from official sources
- Dates checked against current cycles
- Examples validated by grant professionals

---

## Success Metrics (Phase 1)

**Target Ranges:**
- **Pass@1:** 35-50% (appropriately challenging)
- **Pass@3:** 55-75% (achievable with retries)
- **Zero Score:** <5% (tasks are solvable)
- **Evaluation Errors:** 0% (clean execution)
- **Average Execution Time:** 30-45s per task

**Quality Indicators:**
- Consistent failure patterns across runs
- Clear capability gaps identified
- Reproducible results
- Meaningful error analysis possible

---

## Lessons for Contributors

### What We Learned
1. **Multi-server tasks are 30-40% harder** than single-server
2. **Document generation tasks need clear structure validation**
3. **LLM-as-judge needed for narrative quality**
4. **Ground truth must be 100% verifiable**
5. **Calculation tasks expose math weaknesses**

### Recommendations
- Start with clear, verifiable tasks
- Build complexity gradually
- Test evaluators thoroughly
- Use flexible matching where appropriate
- Document expected failure modes

---

**Status:** Phase 1 Complete (10 tasks)  
**Next:** Local validation and Pass@k testing  
**Last Updated:** 2025-01-19

