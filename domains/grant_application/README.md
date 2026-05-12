# Grant Application AI Pipeline - Benchmark Domain

AI agent benchmark for grant application workflow automation, testing multi-server orchestration and complex agentic reasoning.

## Overview

- **Category:** Business Process Automation / Research Support
- **Total Tasks:** 10 (Phase 1) → 50+ (Full Implementation)
- **MCP Servers:** google-search, google-sheets, pdf-generator, file-storage, calendar, email
- **Difficulty:** High (Multi-server workflows, complex reasoning)
- **Expected Pass@1:** 30-50%
- **Expected Pass@3:** 50-70%

## Domain Purpose

This domain tests AI agents' ability to:
- Navigate complex multi-step grant application workflows
- Orchestrate multiple MCP servers in sequence
- Extract and process structured requirements from documents
- Generate compliant, formatted application materials
- Manage deadlines and submission logistics
- Handle conditional branching based on funding agency rules

**Philosophy:** Grant applications are inherently complex, rule-bound, and multi-faceted. Models must demonstrate planning, compliance checking, document generation, and workflow coordination—exposing capability gaps in real-world automation scenarios.

## Domain Structure

```
grant_application/
├── README.md                           # This file
├── TASK_BREAKDOWN.md                   # Detailed task categorization
├── config.yaml                         # Benchmark configuration
├── tasks/                              # Task definitions (10→50+)
│   ├── grant_search_task_0001.json     # Search grants by research area
│   ├── grant_search_task_0002.json     # Match researcher to opportunities
│   ├── grant_search_task_0003.json     # Compare eligibility requirements
│   ├── requirements_task_0001.json     # Extract RFP requirements
│   ├── requirements_task_0002.json     # Parse budget constraints
│   ├── requirements_task_0003.json     # Identify submission deadlines
│   ├── document_gen_task_0001.json     # Generate budget justification
│   ├── document_gen_task_0002.json     # Create project timeline
│   ├── document_gen_task_0003.json     # Draft specific aims
│   └── document_gen_task_0004.json     # Compile application checklist
├── evaluators/                         # Evaluation logic
│   ├── __init__.py                     # Package initialization
│   └── functions.py                    # Evaluator implementations
└── test_data/                          # Sample data (not committed)
    ├── rfps/                           # Sample RFPs (NSF, NIH, etc.)
    ├── profiles/                       # Researcher profiles
    └── budgets/                        # Budget templates
```

## Task Categories (Phase 1: 10 Tasks)

### Category 1: Grant Discovery & Matching (3 tasks)

#### Task 1: `grant_search_task_0001` - NSF Grant Search by Research Area
**Objective:** Test agent's ability to search and filter grant opportunities based on multiple constraints.

**What the agent must do:**
- Search for active NSF grants in "machine learning for climate modeling"
- Apply filters: budget $500K-$1M, early-career researcher eligibility
- Return top 3 opportunities with grant numbers, deadlines, and budget limits
- Format results as structured JSON

**Why this is challenging:**
- Requires accurate search query formulation for technical domain
- Must apply multiple constraints simultaneously (budget range + eligibility)
- Tests filtering accuracy and result ranking
- Exposes failures in multi-constraint satisfaction

**MCP Servers:** `google-search`  
**Expected Pass@1:** 40-55%  
**Expected Failure Mode:** Missing budget filters, incorrect eligibility interpretation, incomplete result fields

---

#### Task 2: `grant_search_task_0002` - Researcher Profile Matching
**Objective:** Test agent's semantic reasoning and profile-to-opportunity matching capabilities.

**What the agent must do:**
- Given a researcher profile (expertise: NLP, healthcare applications; status: assistant professor)
- Search for relevant grant opportunities across NSF, NIH, DOE
- Match based on research area alignment, career stage, institution type
- Provide match reasoning for each recommendation

**Why this is challenging:**
- Requires semantic understanding of research areas (not just keyword matching)
- Must consider multiple eligibility dimensions (career stage, institution, citizenship)
- Tests reasoning ability: explain WHY each grant matches
- Exposes gaps in profile-based recommendation logic

**MCP Servers:** `google-search`  
**Expected Pass@1:** 30-45%  
**Expected Failure Mode:** Poor semantic matching, missing eligibility checks, weak justifications

---

#### Task 3: `grant_search_task_0003` - Cross-Program Eligibility Comparison
**Objective:** Test agent's ability to extract and compare structured eligibility requirements across multiple programs.

**What the agent must do:**
- Compare eligibility requirements for NSF CAREER, NIH R21, DOE Early Career
- Extract: minimum experience, institution requirements, budget caps, duration limits, citizenship
- Present as structured comparison (JSON or table format)
- Identify key differences that affect applicant choice

**Why this is challenging:**
- Requires extracting structured data from multiple unstructured sources
- Must normalize criteria across different agency terminology
- Tests comparative reasoning: what are the meaningful differences?
- Exposes failures in structured information extraction and alignment

**MCP Servers:** `google-search`  
**Expected Pass@1:** 35-50%  
**Expected Failure Mode:** Incomplete extraction, incorrect normalization, missing key differences

---

### Category 2: Requirements Extraction (3 tasks)

#### Task 4: `requirements_task_0001` - NSF CAREER Requirements Extraction
**Objective:** Test agent's ability to extract precise, structured requirements from complex policy documents.

**What the agent must do:**
- Search for and locate the NSF CAREER solicitation
- Extract: page limits (project description: 15 pages), required sections (5 sections), budget cap ($500K), PI eligibility (years from PhD, tenure-track)
- Format as structured JSON with exact values
- Ensure all critical constraints are captured

**Why this is challenging:**
- NSF documents are long (~30 pages) with requirements scattered throughout
- Requires precision: exact page numbers, dollar amounts, timeframes
- Must distinguish between required vs recommended elements
- Tests attention to detail and document comprehension

**MCP Servers:** `google-search`, `file-storage` (if RFP is provided)  
**Expected Pass@1:** 35-50%  
**Expected Failure Mode:** Missing fields, incorrect numeric values, incomplete section lists

---

#### Task 5: `requirements_task_0002` - NIH R01 Budget Guidelines Parsing
**Objective:** Test agent's ability to parse complex financial rules and constraints.

**What the agent must do:**
- Extract NIH R01 budget guidelines: max direct costs, modular budget threshold ($250K), allowable cost categories
- Identify: what's allowed (personnel, equipment, travel, etc.), what's restricted (e.g., equipment >$5K needs justification)
- Calculate: if indirect cost rate is 52%, what's the total budget cap?
- Format with clear categories and numerical accuracy

**Why this is challenging:**
- Budget rules have many conditional clauses (if X, then Y)
- Requires understanding of grant accounting terminology (direct vs indirect, modular vs detailed)
- Tests numerical reasoning: calculate derived values
- Exposes failures in rule extraction and financial logic

**MCP Servers:** `google-search`  
**Expected Pass@1:** 30-45%  
**Expected Failure Mode:** Missing cost categories, incorrect calculations, unclear restrictions

---

#### Task 6: `requirements_task_0003` - Submission Deadline Tracking
**Objective:** Test agent's ability to identify, calculate, and track time-sensitive information.

**What the agent must do:**
- Given NSF CAREER program info, extract: full proposal deadline, any preliminary deadlines, earliest submission date
- Calculate: days remaining from today's date to deadline
- Determine: notification timeline (when results are expected)
- Format as structured date objects with countdown

**Why this is challenging:**
- Dates may be mentioned in multiple formats (July 23, 2025; 07/23/25; third Thursday in July)
- Requires date arithmetic (days until deadline)
- Must understand academic calendars and review timelines
- Tests temporal reasoning and date handling

**MCP Servers:** `google-search`, `calendar` (for date calculations)  
**Expected Pass@1:** 40-55%  
**Expected Failure Mode:** Incorrect date parsing, wrong calculations, missing preliminary deadlines

---

### Category 3: Document Generation (4 tasks)

#### Task 7: `document_gen_task_0001` - Budget Justification Narrative
**Objective:** Test agent's ability to generate compliant, justified budget narratives with correct calculations.

**What the agent must do:**
- Given line items: PI summer salary ($12K), 2 grad students ($30K each), materials ($15K), travel ($8K)
- Generate narrative justification: 2-3 sentences per category explaining necessity and calculation basis
- Ensure all amounts are mentioned and justified
- Format as cohesive narrative suitable for grant application

**Why this is challenging:**
- Requires both calculation accuracy AND narrative quality
- Must justify why each expense is necessary (not just list amounts)
- Tests balance between technical precision and persuasive writing
- Exposes weaknesses in structured data → narrative generation

**MCP Servers:** `pdf-generator` (for formatted output)  
**Expected Pass@1:** 35-50%  
**Expected Failure Mode:** Missing justifications, calculation errors, poor narrative flow

---

#### Task 8: `document_gen_task_0002` - 3-Year Project Timeline with Dependencies
**Objective:** Test agent's ability to create structured, realistic project timelines with milestone dependencies.

**What the agent must do:**
- Create 3-year timeline (2025-2027) with 8+ milestones
- Include: month number, date, milestone name, description, deliverables, dependencies
- Ensure chronological ordering and realistic spacing
- Show how milestones build on each other (dependencies)

**Why this is challenging:**
- Requires project planning knowledge (what's realistic timeline?)
- Must manage dependencies: Milestone B can't start until Milestone A completes
- Tests temporal reasoning and project management logic
- Exposes failures in planning and dependency tracking

**MCP Servers:** `google-sheets` (timeline table), `calendar` (date management)  
**Expected Pass@1:** 30-45%  
**Expected Failure Mode:** Unrealistic timelines, missing dependencies, too few milestones

---

#### Task 9: `document_gen_task_0003` - Specific Aims Section for NSF CAREER
**Objective:** Test agent's ability to draft scientific proposal text with proper structure and content.

**What the agent must do:**
- Given project topic ("Machine learning for climate model uncertainty quantification")
- Draft Specific Aims section: opening paragraph (problem statement), 3 aims with objectives/approaches/outcomes, broader impacts statement
- Follow NSF CAREER structure: integrate research + education
- Ensure scientific rigor and proper formatting

**Why this is challenging:**
- Requires domain knowledge (climate science, ML) or ability to generate plausible content
- Must follow specific structural conventions of NSF proposals
- Tests scientific writing quality, not just formatting
- Exposes gaps in domain adaptation and narrative generation

**MCP Servers:** `pdf-generator` (formatted document)  
**Expected Pass@1:** 25-40%  
**Expected Failure Mode:** Poor structure, weak aims, missing broader impacts, generic content

---

#### Task 10: `document_gen_task_0004` - Application Submission Checklist
**Objective:** Test agent's ability to compile comprehensive, organized checklists from scattered requirements.

**What the agent must do:**
- Generate complete NSF CAREER submission checklist
- Include: core documents (project description, budget, etc.), supplementary documents, required approvals, submission platform requirements
- Organize by: document name, page limit, format requirements, deadline, status
- Ensure nothing is missing from official requirements

**Why this is challenging:**
- Requires synthesizing information from multiple sources (NSF guidelines, institutional policies)
- Must be exhaustively complete (missing one item = failed submission)
- Tests organizational ability and thoroughness
- Exposes failures in information aggregation and checklist logic

**MCP Servers:** `google-search` (find requirements), `file-storage` (checklist template)  
**Expected Pass@1:** 40-55%  
**Expected Failure Mode:** Missing items, incorrect page limits, incomplete formatting requirements

---

## Task Difficulty Summary

| Task | Category | Difficulty | Pass@1 | Key Challenge |
|------|----------|-----------|--------|---------------|
| 1 | Grant Search | Medium | 40-55% | Multi-constraint filtering |
| 2 | Grant Matching | Medium-Hard | 30-45% | Semantic reasoning + justification |
| 3 | Eligibility Comparison | Medium | 35-50% | Structured extraction across sources |
| 4 | NSF Requirements | Medium | 35-50% | Precision extraction from long docs |
| 5 | NIH Budget Rules | Medium-Hard | 30-45% | Financial logic + calculations |
| 6 | Deadline Tracking | Medium | 40-55% | Date parsing + arithmetic |
| 7 | Budget Justification | Medium | 35-50% | Calculation + narrative quality |
| 8 | Project Timeline | Hard | 30-45% | Dependencies + realistic planning |
| 9 | Specific Aims | Hard | 25-40% | Domain knowledge + scientific writing |
| 10 | Submission Checklist | Medium | 40-55% | Completeness + organization |

**Overall Expected Pass@1:** 35-50% (appropriately challenging)  
**Overall Expected Pass@3:** 55-75% (achievable with retries)

## Required Services

### MCP Servers

#### google-search
- **Purpose:** Search grant databases, research funding opportunities
- **Installation:** `uv run alignerr_mcp servers install google_search`
- **API Key:** `SERP_API_KEY` from [serpapi.com](https://serpapi.com/)
- **Free Tier:** 100 searches/month

#### google-sheets
- **Purpose:** Manage grant tracking spreadsheets, budget tables
- **Installation:** `uv run alignerr_mcp servers install google_sheets`
- **API Key:** `GOOGLE_CREDENTIALS_JSON` from [console.cloud.google.com](https://console.cloud.google.com/)
- **Free Tier:** Available

#### pdf-generator
- **Purpose:** Create formatted application documents, reports
- **Installation:** `uv run alignerr_mcp servers install pdf_generator`
- **API Key:** None required
- **Free Tier:** Unlimited (local generation)

#### file-storage
- **Purpose:** Store and retrieve application documents, RFPs
- **Installation:** `uv run alignerr_mcp servers install file_storage`
- **API Key:** None required
- **Free Tier:** Unlimited (local storage)

#### calendar
- **Purpose:** Track submission deadlines, milestone dates
- **Installation:** `uv run alignerr_mcp servers install calendar`
- **API Key:** None required (or Google Calendar API)
- **Free Tier:** Available

#### email
- **Purpose:** Simulate grant office correspondence (optional for Phase 1)
- **Installation:** `uv run alignerr_mcp servers install email`
- **API Key:** SMTP credentials
- **Free Tier:** Depends on provider

### API Keys Setup

```bash
# Create .env file
cat > .env << EOF
# LLM Providers (for evaluation)
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx

# MCP Servers
SERP_API_KEY=your_serpapi_key_here
GOOGLE_CREDENTIALS_JSON=/path/to/google-credentials.json

# Optional: Email
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EOF

# Setup via CLI
uv run alignerr_mcp env setup
```

## Usage

### Installation

```bash
# Clone repository with submodules
git clone --recurse-submodules <repo-url>
cd lbx_mcp_universe_template

# Install dependencies
uv sync

# Install required MCP servers
uv run alignerr_mcp servers install google_search
uv run alignerr_mcp servers install google_sheets
uv run alignerr_mcp servers install pdf_generator
uv run alignerr_mcp servers install file_storage
uv run alignerr_mcp servers install calendar

# Setup API keys
uv run alignerr_mcp env setup
```

### Running Validation

```bash
# Validate domain structure
uv run alignerr_mcp validate --domain grant_application

# Run with specific model
uv run alignerr_mcp validate --domain grant_application --model claude-3-5-sonnet-20241022

# Pass@k validation (3 runs)
uv run alignerr_mcp validate --domain grant_application --runs 3

# Parallel execution
uv run alignerr_mcp validate --domain grant_application --parallel 4
```

### Expected Results

**Phase 1 (10 tasks):**
- **Pass@1:** 30-50% (appropriately challenging)
- **Pass@3:** 50-70% (achievable with retries)
- **Zero score:** <5% (tasks are solvable)
- **Execution time:** ~30-45s per task
- **Total runtime:** ~5-8 minutes for full domain

**Target failure patterns:**
- Incomplete requirement extraction
- Budget calculation errors
- Missing compliance checks
- Poor document formatting
- Deadline management failures

## Example Tasks

### Example 1: Grant Search by Research Area

**Task:** `grant_search_task_0001.json`

```json
{
    "category": "grant_search",
    "question": "Search for active NSF grants in the area of 'machine learning for climate modeling' with budgets between $500K-$1M and eligibility for early-career researchers. List the top 3 opportunities with grant numbers, deadlines, and budget limits.",
    "output_format": {
        "grants": [
            {
                "grant_number": "[Grant ID]",
                "title": "[Grant Title]",
                "deadline": "[YYYY-MM-DD]",
                "budget_range": "[Min-Max]",
                "eligibility": "[Requirements]"
            }
        ]
    },
    "use_specified_server": true,
    "mcp_servers": [{"name": "google-search"}],
    "evaluators": [{
        "func": "raw",
        "op": "grant_application.validate_grant_search",
        "op_args": {
            "question": "Search for active NSF grants in the area of 'machine learning for climate modeling' with budgets between $500K-$1M and eligibility for early-career researchers.",
            "required_fields": ["grant_number", "title", "deadline", "budget_range"],
            "min_results": 3
        }
    }]
}
```

### Example 2: Extract Requirements from RFP

**Task:** `requirements_task_0001.json`

```json
{
    "category": "requirements_extraction",
    "question": "Given the NSF CAREER RFP document, extract and structure the following: (1) page limits for project description, (2) required sections, (3) budget cap, (4) eligibility requirements for PI. Format as structured JSON.",
    "output_format": {
        "page_limits": {"project_description": "[number]"},
        "required_sections": ["[section1]", "[section2]"],
        "budget_cap": "[amount]",
        "eligibility": {"pi_requirements": "[requirements]"}
    },
    "use_specified_server": true,
    "mcp_servers": [
        {"name": "file-storage"},
        {"name": "google-search"}
    ],
    "evaluators": [{
        "func": "raw",
        "op": "grant_application.validate_requirements_extraction",
        "op_args": {
            "question": "Extract requirements from NSF CAREER RFP",
            "expected_structure": {
                "page_limits": {"project_description": 15},
                "budget_cap": "$500,000",
                "required_sections_count": 5
            }
        }
    }]
}
```

### Example 3: Generate Budget Justification

**Task:** `document_gen_task_0001.json`

```json
{
    "category": "document_generation",
    "question": "Generate a budget justification narrative for the following items: Senior Personnel (PI, 1 month summer salary, $12,000), Graduate Student (2 students, 12 months each, $30,000 each), Materials & Supplies ($15,000), Travel ($8,000 for 2 conferences). Justify each line item in 2-3 sentences explaining necessity and calculation basis.",
    "output_format": {
        "budget_justification": "[narrative text with sections for each budget category]"
    },
    "use_specified_server": true,
    "mcp_servers": [{"name": "pdf-generator"}],
    "evaluators": [{
        "func": "raw",
        "op": "grant_application.validate_budget_justification",
        "op_args": {
            "question": "Generate budget justification narrative",
            "required_categories": ["Senior Personnel", "Graduate Student", "Materials & Supplies", "Travel"],
            "required_amounts": [12000, 60000, 15000, 8000],
            "min_sentences_per_category": 2
        }
    }]
}
```

## Evaluation Strategy

### Multi-Layered Evaluation Approach

1. **Structure Validation**
   - Check for required fields
   - Validate JSON format
   - Ensure minimum result counts

2. **Content Accuracy**
   - Verify extracted values match ground truth
   - Check calculations (budgets, dates)
   - Validate compliance with rules

3. **LLM-as-a-Judge**
   - Assess narrative quality
   - Check justification completeness
   - Evaluate formatting appropriateness

4. **Workflow Validation**
   - Verify correct MCP server usage
   - Check for proper sequencing
   - Validate error handling

## Known Challenges & Expected Failures

### Challenge Areas (Target for Model Failure)

1. **Multi-step Planning**
   - Models may search but fail to filter correctly
   - Expected failure: 30-40% on complex searches

2. **Structured Extraction**
   - Models struggle with precise field extraction
   - Expected failure: 20-30% on complex RFPs

3. **Budget Calculations**
   - Math errors, missing categories
   - Expected failure: 40-50% on multi-category budgets

4. **Compliance Checking**
   - Models miss subtle eligibility requirements
   - Expected failure: 30-40% on rule-heavy tasks

5. **Document Formatting**
   - Poor structure, missing sections
   - Expected failure: 25-35% on formatted outputs

## Troubleshooting

### Common Issues

**Issue:** Search returns no results
- **Solution:** Check SERP_API_KEY is valid and not rate-limited
- **Workaround:** Use mock search results for testing

**Issue:** Google Sheets connection fails
- **Solution:** Verify GOOGLE_CREDENTIALS_JSON path is correct
- **Workaround:** Use CSV files via file-storage instead

**Issue:** PDF generation fails
- **Solution:** Check pdf-generator server is installed
- **Workaround:** Generate text output instead of PDF

**Issue:** Tasks timeout
- **Solution:** Increase max_iterations in config.yaml (currently 20)
- **Workaround:** Break complex tasks into smaller subtasks

## Future Enhancements (Phase 2+)

### Phase 2: Expand to 30 Tasks
- Budget table generation with formulas
- Timeline with Gantt chart creation
- Multi-agency comparison workflows
- Compliance rule checking

### Phase 3: Expand to 50+ Tasks
- Full end-to-end application pipeline
- Reviewer response letter generation
- Resubmission workflow automation
- Grant portfolio management

### Phase 4: Advanced Features
- Multi-agent collaboration (PI + grant officer)
- Conditional branching based on agency rules
- Real-time deadline tracking with alerts
- Automated pre-submission validation

## Contributing

See main repository [CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines.

## License

Same as parent repository.

## Contact

For domain-specific questions, contact the domain maintainer or open an issue.

---

**Status:** Phase 1 - Initial Implementation (10 tasks)
**Last Updated:** 2025-01-19
**Maintainer:** Alpha (fahadkiani)

