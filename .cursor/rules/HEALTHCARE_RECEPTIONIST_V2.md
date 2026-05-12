# Healthcare Receptionist & Clinical Operations - Domain Proposal

**Proposed Domain:** Healthcare-specific receptionist testing HIPAA-compliant workflows, clinical appointment scheduling, patient intake, insurance verification, and care coordination.

---

## 🎯 Overview

Multi-server domain testing AI agents on **real-world healthcare operations**. Focuses on:
- **HIPAA-compliant** patient communication
- **FHIR R4** patient data integration
- **HL7 v2.x** appointment messaging
- **Clinical scheduling** with provider availability, insurance verification, and care coordination
- **Multi-channel orchestration** across phone, SMS, email, and patient portals

**Market Context:** 
- $4.5 trillion US healthcare market
- 70% of healthcare providers struggling with patient no-shows
- AI medical assistants market projected to reach $40B by 2028
- Epic, Cerner, Athena Health all racing to add AI front-desk automation

**Key Differentiator:** Unlike Emma Lee's education proposal (which uses external APIs like Temporal, OPA, GraphQL), we **use existing MCP servers** but add **healthcare-specific complexity** through standards compliance (FHIR, HL7, HIPAA) and clinical workflows.

---

## 📋 Task Structure

**Phase 1 (Initial Release):** 40 high-quality tasks across 5 categories

### 1. Patient Intake & Registration (8 tasks)
- **Basic intake:** Collect demographics, insurance, chief complaint
- **HIPAA consent:** Verify identity, obtain consent, log compliance
- **Insurance verification:** Check eligibility via FHIR Coverage resource
- **New patient onboarding:** Create patient record in FHIR Patient resource format
- **Existing patient lookup:** Search by MRN, name, DOB (fuzzy matching)
- **Multi-language intake:** Spanish/Chinese/Vietnamese language detection and routing
- **Emergency contact registration:** Store and validate emergency contacts
- **Pharmacy preference:** Capture preferred pharmacy with FHIR Location reference

**Complexity:** Moderate-High (HIPAA compliance, data validation, FHIR resource creation)

### 2. Clinical Appointment Scheduling (10 tasks)
- **Basic scheduling:** Book appointment with provider availability check
- **Specialist referrals:** Schedule with referral authorization check
- **Follow-up scheduling:** Post-discharge appointments with care plan integration
- **Urgent same-day:** Triage urgency, find same-day slots
- **Recurring appointments:** Schedule series (e.g., 6 weeks of physical therapy)
- **Rescheduling with insurance:** Check new date covered by authorization
- **Provider preference matching:** Match patient preference with provider specialties
- **Timezone handling:** Multi-location clinics with timezone conversion
- **Wait-list management:** Add patient to cancellation list, auto-notify when available
- **Appointment reminders:** Send HIPAA-compliant SMS/email reminders 24h before

**Complexity:** High (clinical triage, authorization checks, FHIR Appointment resources)

### 3. Insurance & Authorization (8 tasks)
- **Eligibility verification:** Query insurance coverage via FHIR Coverage
- **Prior authorization check:** Verify procedure requires authorization
- **Authorization status lookup:** Check existing authorization status
- **Out-of-network detection:** Warn patient if provider not in network
- **Copay calculation:** Estimate patient responsibility based on coverage
- **Benefits explanation:** Explain deductible, out-of-pocket max
- **Secondary insurance:** Handle dual coverage coordination of benefits
- **Uninsured patient routing:** Route to financial assistance programs

**Complexity:** Very High (insurance logic, FHIR Coverage/ClaimResponse resources)

### 4. Clinical Triage & Routing (8 tasks)
- **Chief complaint classification:** Classify into clinical categories (ICD-10 mapping)
- **Urgency assessment:** Triage into routine/urgent/emergent
- **Symptom-based routing:** Route chest pain → cardiology, cough → primary care
- **Telehealth eligibility:** Determine if visit can be virtual
- **Nurse triage handoff:** When to escalate to RN triage line
- **After-hours protocol:** Route to on-call provider or ER
- **Pharmacy routing:** Refill requests to pharmacy, new Rx to provider
- **Lab result inquiry:** Check if results available, notify provider if critical

**Complexity:** Very High (clinical decision logic, safety-critical routing)

### 5. HIPAA-Compliant Multi-Channel Orchestration (6 tasks)
- **Appointment confirmation workflow:** Schedule → send encrypted confirmation → add to calendar
- **Test result notification:** Lab results ready → secure patient portal notification → SMS alert
- **Referral coordination:** PCP referral → schedule specialist → send medical records (FHIR DocumentReference)
- **Post-discharge follow-up:** Hospital discharge → schedule follow-up → send care instructions (FHIR CarePlan)
- **Prescription refill:** Patient requests refill → check last fill date → route to pharmacy or provider
- **Billing inquiry escalation:** Billing question → create support ticket → send summary to billing dept

**Complexity:** Extreme (multi-step workflows, FHIR resource coordination, HIPAA compliance)

**Planned Expansion:** Scale to 60+ tasks (telemedicine integration, prescription management, care plan adherence)

---

## 🔧 MCP Servers Required (All Existing!)

| Server | Healthcare Use Case | Status |
|--------|---------------------|--------|
| `calendar` | Appointment scheduling, provider availability | ✅ Ready |
| `email` | HIPAA-compliant patient communication | ✅ Ready |
| `sms-messaging` | Appointment reminders, test result alerts | ✅ Ready |
| `task-management` | Care coordination tasks, follow-ups | ✅ Ready |
| `google-search` | Look up pharmacy, clinic, insurance provider info | ✅ Ready |
| `pdf-generator` | Generate patient consent forms, care instructions | ✅ Ready |
| `date` | Age calculation, appointment date logic | ✅ Ready |

**Key Innovation:** 
- **No external APIs required** 
- **Complexity comes from healthcare standards** (FHIR, HL7, HIPAA) and clinical workflows
- **Existing MCP servers used in healthcare-specific ways** (e.g., `pdf-generator` for consent forms, `sms-messaging` with HIPAA-compliant templates)

---

## 📊 Difficulty & Metrics

**Target Pass@1:** 35-55% (high complexity due to clinical logic and compliance)

| Category | Tasks | Difficulty | Expected Pass@1 | Challenge |
|----------|-------|-----------|-----------------|-----------|
| **Patient Intake** | 8 | Medium | 60-70% | FHIR resource creation, validation |
| **Appointment Scheduling** | 10 | Hard | 45-55% | Provider logic, insurance checks |
| **Insurance & Authorization** | 8 | Very Hard | 25-35% | Complex insurance rules, FHIR Coverage |
| **Clinical Triage** | 8 | Extreme | 20-30% | Safety-critical decisions, ICD-10 |
| **Multi-Channel** | 6 | Extreme | 15-25% | Complex workflows, HIPAA compliance |
| **Overall** | **40** | **High** | **35-45%** | **Clinical complexity + compliance** |

**Why this difficulty?**
- **Harder than Grant Application:** Clinical decision logic, safety-critical
- **Similar to Emma Lee's education proposal:** Real-world standards (FHIR ≈ Ed-Fi, HIPAA ≈ FERPA)
- **Uses existing servers:** No new external APIs, complexity from domain logic

---

## 🎯 Sample Tasks (Detailed)

### Task 1: Basic Patient Intake
**Scenario:** New patient calls to schedule first appointment

**Agent receives:**
```
Patient: "Hi, I'd like to schedule my first appointment with Dr. Smith"
```

**Expected workflow:**
1. Collect demographics (name, DOB, address, phone)
2. Collect insurance info (carrier, member ID, group number)
3. Ask chief complaint ("What brings you in today?")
4. Use `calendar` to check Dr. Smith's availability
5. Use `email` to send appointment confirmation
6. Generate patient intake form via `pdf-generator`
7. Return FHIR Patient resource

**Expected output (simplified):**
```json
{
  "resourceType": "Patient",
  "identifier": [{"value": "MRN-12345"}],
  "name": [{"family": "Doe", "given": ["John"]}],
  "birthDate": "1985-03-15",
  "telecom": [{"system": "phone", "value": "555-1234"}],
  "appointment_scheduled": {
    "provider": "Dr. Smith",
    "date": "2025-11-10",
    "time": "14:00",
    "reason": "Annual physical"
  },
  "consent_obtained": true,
  "intake_form_sent": true
}
```

**Evaluator:** Validate FHIR Patient resource structure, appointment created, consent documented

---

### Task 2: Insurance Verification with Prior Authorization
**Scenario:** Patient needs MRI, requires prior authorization

**Agent receives:**
```json
{
  "patient_mrn": "MRN-12345",
  "procedure_code": "CPT-70553",  // MRI brain with contrast
  "insurance": {
    "carrier": "Blue Cross",
    "member_id": "ABC123456",
    "group": "GRP999"
  }
}
```

**Expected workflow:**
1. Query insurance eligibility (simulate FHIR Coverage resource lookup)
2. Check if CPT-70553 requires prior authorization (it does)
3. Check existing authorization status (none found)
4. Create task for clinical staff: "Prior auth needed for MRI"
5. Notify patient: "Your insurance requires authorization, we'll submit and call you"
6. Generate FHIR CoverageEligibilityRequest

**Expected output:**
```json
{
  "coverage_active": true,
  "requires_prior_auth": true,
  "auth_status": "pending_submission",
  "task_created": {
    "assigned_to": "authorization_team",
    "priority": "high",
    "due_date": "2025-11-05"
  },
  "patient_notified": true,
  "estimated_patient_cost": "$50 copay (if approved)"
}
```

**Evaluator:** Validate prior auth detection, task creation, patient notification, FHIR resource accuracy

---

### Task 3: Clinical Triage - Chest Pain (Safety-Critical)
**Scenario:** Patient calls with chest pain

**Agent receives:**
```
Patient: "I've been having chest pain for the last 2 hours, it's getting worse"
```

**Expected workflow:**
1. **IMMEDIATE ESCALATION** - chest pain is emergent
2. Ask key triage questions:
   - "Is the pain radiating to your arm or jaw?"
   - "Are you short of breath?"
   - "Do you have a history of heart disease?"
3. Based on answers:
   - **If yes to any:** "Call 911 immediately, don't wait"
   - **If no but worsening:** "Go to ER now, I'll notify them you're coming"
   - **If mild/stable:** "I'm connecting you to our triage nurse right now"
4. Create urgent task for clinical staff
5. Document triage in FHIR Observation (chief complaint + urgency)

**Expected output:**
```json
{
  "triage_category": "EMERGENT",
  "recommended_action": "call_911",
  "escalated_to": "emergency_services",
  "patient_advised": "Call 911 immediately for chest pain evaluation",
  "clinical_note": {
    "chief_complaint": "chest pain x 2 hours, worsening",
    "onset": "2 hours ago",
    "severity": "8/10",
    "associated_symptoms": ["shortness of breath", "left arm pain"]
  },
  "FHIR_observation_created": true,
  "safety_protocol_followed": true
}
```

**Evaluator:** 
- **PASS ONLY IF:** Correctly identified as emergent, advised 911/ER
- **FAIL IF:** Scheduled routine appointment, offered telehealth, any delay in care
- Validate FHIR Observation structure

---

### Task 4: Multi-Channel Post-Discharge Coordination
**Scenario:** Patient discharged from hospital, needs follow-up

**Agent receives (FHIR Encounter + CarePlan):**
```json
{
  "patient_mrn": "MRN-12345",
  "discharge_date": "2025-11-03",
  "discharge_diagnosis": "CHF exacerbation",
  "care_plan": {
    "follow_up_in": "7_days",
    "follow_up_with": "cardiologist",
    "medications": ["Furosemide 40mg daily", "Metoprolol 25mg BID"],
    "activity": "Limit sodium to 2g/day, weigh daily",
    "warning_signs": "Call if weight increases >3lbs in 24h or SOB worsens"
  }
}
```

**Expected workflow:**
1. Use `calendar` to schedule cardiology follow-up within 7 days
2. Use `pdf-generator` to create discharge summary with care plan
3. Use `email` to send discharge summary (HIPAA-compliant)
4. Use `sms-messaging` to send medication reminder
5. Use `task-management` to create "Check-in call on day 3" task for nurse
6. Generate FHIR Appointment + CarePlan resources

**Expected output:**
```json
{
  "follow_up_scheduled": {
    "provider": "Dr. Jones (Cardiology)",
    "date": "2025-11-10",
    "time": "09:00"
  },
  "discharge_summary_sent": true,
  "medication_reminders_scheduled": [
    "2025-11-04 08:00 - Take Furosemide",
    "2025-11-04 08:00 - Take Metoprolol"
  ],
  "check_in_task_created": {
    "assigned_to": "nurse_coordinator",
    "date": "2025-11-06",
    "reason": "Post-discharge check-in for CHF patient"
  },
  "patient_education_sent": {
    "topics": ["CHF management", "Daily weight monitoring", "Sodium restriction"],
    "format": "PDF via encrypted email"
  },
  "FHIR_resources_updated": ["Appointment", "CarePlan", "Task"]
}
```

**Evaluator:** Validate all 5 actions completed, FHIR resource integrity, timing correctness (within 7 days)

---

## 💡 Why This Domain Matters

### 1. **Massive Healthcare Market**
- $4.5T US healthcare market
- 70% of providers struggle with patient access and no-shows
- AI medical assistants: $40B market by 2028
- Epic, Cerner, Athena Health all investing heavily in AI automation

### 2. **Tests Unique Capabilities**
- **Clinical decision logic:** Triage, urgency assessment, safety protocols
- **Healthcare standards compliance:** FHIR R4, HL7 v2.x, HIPAA
- **Insurance complexity:** Authorization, eligibility, coordination of benefits
- **Safety-critical reasoning:** Wrong decision = patient harm
- **Multi-channel care coordination:** Hospital → PCP → specialist → pharmacy

### 3. **Differentiated from Emma Lee's Proposal**

| Aspect | Emma Lee (Education) | Our Domain (Healthcare) |
|--------|---------------------|-------------------------|
| **External APIs** | ✅ (Temporal, OPA, GraphQL) | ❌ (uses existing MCP servers) |
| **Complexity Source** | External integrations | Clinical logic + standards |
| **Standards** | Ed-Fi, xAPI, IMS | FHIR R4, HL7, HIPAA |
| **Safety-Critical** | No | ✅ (patient safety) |
| **Market Readiness** | Emerging | Established ($4.5T) |
| **Task Count** | ~30 | 40 |
| **Difficulty** | High | Very High |

### 4. **Production-Ready Use Cases**
- Primary care clinics (60% of US physicians)
- Specialty practices (cardiology, orthopedics, dermatology)
- Urgent care centers (10,000+ locations in US)
- Hospital outpatient departments
- Telemedicine platforms (Teladoc, Amwell, MDLive)

---

## 🧪 Ground Truth & Evaluation

### Patient Intake
- **FHIR validation:** Schema compliance for Patient, Coverage resources
- **Data completeness:** Required fields present (name, DOB, insurance)
- **Consent documentation:** HIPAA consent obtained and logged

### Appointment Scheduling
- **Provider availability:** Correct availability check, no double-booking
- **Insurance validation:** Authorization requirements detected
- **Appointment resource:** FHIR Appointment resource correctly formatted

### Insurance & Authorization
- **Eligibility accuracy:** Correct coverage status determination
- **Prior auth detection:** Accurately identify procedures requiring authorization
- **Cost estimation:** Reasonable copay/deductible calculation

### Clinical Triage (Safety-Critical)
- **Emergent detection:** 100% accuracy required on chest pain, stroke, severe bleeding
- **Appropriate escalation:** Correct routing to ER, nurse triage, or routine care
- **ICD-10 mapping:** Chief complaint mapped to appropriate diagnosis code

### Multi-Channel Orchestration
- **Workflow completeness:** All required steps executed in correct order
- **HIPAA compliance:** No PHI in unencrypted channels
- **FHIR resource integrity:** Resources correctly linked (Patient → Appointment → CarePlan)

---

## 🔬 Technical Innovation

### 1. **FHIR R4 Resource Generation**
All patient data structured as FHIR R4 resources:
```python
# Agent must generate valid FHIR resources:
Patient, Appointment, Coverage, Observation, CarePlan, Task
```

### 2. **HL7 v2.x Appointment Messages**
Appointment confirmations formatted as HL7 messages:
```
MSH|^~\&|SCHEDULE|CLINIC|EMR|HOSPITAL|20251103120000||SIU^S12|123456|P|2.5
PID|1||MRN-12345||DOE^JOHN||19850315|M
SCH|1||||||Routine Office Visit|||||20251110140000
```

### 3. **HIPAA-Compliant Communication Templates**
All SMS/email must follow HIPAA guidelines:
- ✅ "Your appointment is confirmed for Nov 10"
- ❌ "Your diabetes appointment is Nov 10"
- ✅ "Your test results are ready in the patient portal"
- ❌ "Your cholesterol is 250, please call us"

### 4. **Clinical Triage Decision Trees**
Safety-critical logic for emergent conditions:
```
Chest pain → 
  Radiating pain OR SOB OR diaphoresis → CALL 911
  Worse with exertion, better with rest → ER NOW
  Mild, stable, no risk factors → Urgent same-day
```

### 5. **Insurance Authorization Logic**
Complex rules for prior authorization:
```python
# Example: MRI requires auth, X-ray doesn't
if procedure_code in HIGH_COST_IMAGING:
    check_prior_auth()
if insurance_type == "Medicare" and procedure_code in MEDICARE_PA_LIST:
    check_prior_auth()
```

---

## 📈 Expected Results by Task Category

| Category | Tasks | Target Pass@1 | Why Hard |
|----------|-------|---------------|----------|
| **Patient Intake** | 8 | 65% | FHIR resource creation, validation |
| **Appointment Scheduling** | 10 | 50% | Provider logic, insurance checks |
| **Insurance & Authorization** | 8 | 30% | Complex insurance rules, edge cases |
| **Clinical Triage** | 8 | 25% | Safety-critical, requires clinical reasoning |
| **Multi-Channel** | 6 | 20% | 5+ step workflows, FHIR orchestration |
| **Overall** | **40** | **40%** | **Discriminative, production-ready** |

**Why 40% overall pass rate is ideal:**
- Too easy (>70%) = not testing real capabilities
- Too hard (<20%) = agents can't learn
- **40% = discriminative benchmark** that separates strong from weak agents
- Matches Emma Lee's complexity but uses existing infrastructure

---

## 🆚 Comparison with Existing Domains

| Metric | Grant App | Investments | Emma Lee (Education) | **Healthcare Receptionist** |
|--------|-----------|-------------|----------------------|----------------------------|
| **Pass@1 Target** | 50% | 27% | ~40% (est.) | **40%** |
| **Task Count** | 50 | 15 | ~30 (est.) | **40** |
| **Complexity** | High | Moderate | Very High | **Very High** |
| **MCP Servers** | 6 | 1 | N/A (external APIs) | **7 (all existing)** |
| **External APIs** | None | Alpha Vantage | Temporal, OPA, GraphQL | **None** |
| **Standards Compliance** | None | None | Ed-Fi, xAPI | **FHIR, HL7, HIPAA** |
| **Safety-Critical** | No | No | No | **Yes** |
| **Market Size** | $50B | $50B | $3T (education) | **$4.5T (healthcare)** |

**Key Advantages:**
1. ✅ **Uses existing MCP servers** (no new infrastructure)
2. ✅ **Real-world healthcare standards** (FHIR, HL7, HIPAA)
3. ✅ **Safety-critical testing** (clinical triage)
4. ✅ **Higher complexity than Grant App** (clinical logic + compliance)
5. ✅ **Matches Emma Lee's sophistication** (standards, multi-step workflows)
6. ✅ **Production-ready** ($4.5T market, immediate use cases)

---

## 🚀 Implementation Plan

### Phase 1: Core Tasks (Week 1-2)
- 8 patient intake tasks
- 10 appointment scheduling tasks
- Define FHIR resource schemas
- Build basic evaluators

### Phase 2: Complex Logic (Week 3-4)
- 8 insurance & authorization tasks
- 8 clinical triage tasks (safety-critical)
- Advanced FHIR validation
- HL7 message generation

### Phase 3: Orchestration (Week 5)
- 6 multi-channel workflow tasks
- End-to-end care coordination scenarios
- HIPAA compliance validation
- Performance tuning

### Phase 4: Hardening (Week 6)
- Test locally, target 40% pass rate
- Add hard edge cases if pass rate too high
- Documentation and production readiness

---

## 🎯 Success Criteria

**Merge-Ready When:**
1. ✅ 40 tasks implemented with clear expected outputs
2. ✅ All evaluators validate FHIR resource structure
3. ✅ Pass@1 between 35-55% (discriminative)
4. ✅ Safety-critical tasks (triage) have 0% false negatives on emergent cases
5. ✅ HIPAA compliance validated (no PHI leakage in logs/outputs)
6. ✅ Documentation complete (task descriptions, evaluation criteria)

**Production-Ready Benchmark:**
- Tests clinical reasoning + standards compliance + multi-channel orchestration
- Uses existing MCP infrastructure (no external APIs)
- Matches Emma Lee's complexity level
- Solves real $4.5T market problem

---

**Questions? Ready to build?**

Alpha, this is the healthcare-aligned iteration. Key differences from original AI Receptionist proposal:
1. **40 tasks** (vs 15) to match Emma Lee's scope
2. **FHIR, HL7, HIPAA** standards for complexity
3. **Safety-critical triage** for clinical reasoning
4. **No external APIs** (unlike Emma's Temporal/OPA) - uses existing MCP servers
5. **40% target pass rate** (discriminative, production-ready)

Ready to proceed with implementation? 🚀

