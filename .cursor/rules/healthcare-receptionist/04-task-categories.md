# Healthcare Receptionist - Task Categories (40 Tasks)

## Overview

40 tasks across 5 categories, targeting 35-45% overall pass rate.

| Category | Tasks | Pass@1 | Difficulty |
|----------|-------|--------|------------|
| Patient Intake | 8 | 65% | Moderate-High |
| Appointment Scheduling | 10 | 50% | High |
| Insurance & Authorization | 8 | 30% | Very High |
| Clinical Triage | 8 | 25% | Extreme |
| Multi-Channel Orchestration | 6 | 20% | Extreme |

---

## Category 1: Patient Intake & Registration (8 tasks)

### Task 001: Basic New Patient Intake
**Difficulty:** Easy  
**Expected Pass@1:** 80%

**Input:**
```
Patient: "Hi, I'd like to schedule my first appointment with Dr. Smith"
```

**Expected workflow:**
1. Collect demographics (name, DOB, address, phone)
2. Collect insurance (carrier, member ID, group number)
3. Ask chief complaint
4. Check Dr. Smith availability via `calendar`
5. Create appointment
6. Send confirmation via `email`
7. Generate intake form via `pdf-generator`
8. Return FHIR Patient resource

**Evaluator:** `validate_patient_intake`
- FHIR Patient resource valid
- Appointment created
- Consent documented
- At least one contact method

---

### Task 002: HIPAA Consent & Identity Verification
**Difficulty:** Medium  
**Expected Pass@1:** 70%

**Input:**
```json
{
  "patient_name": "John Doe",
  "dob": "1985-03-15",
  "last_4_ssn": "1234"
}
```

**Expected workflow:**
1. Verify identity (name + DOB + SSN match)
2. Obtain HIPAA consent
3. Document consent in FHIR Consent resource
4. Log in audit trail
5. Return consent confirmation

**Evaluator:** `validate_hipaa_consent`
- Consent resource created
- Identity verified
- Audit log entry created
- Consent timestamp present

---

### Task 003: Insurance Eligibility Verification
**Difficulty:** Hard  
**Expected Pass@1:** 50%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "insurance": {
    "carrier": "Blue Cross",
    "member_id": "ABC123456",
    "group": "GRP999"
  }
}
```

**Expected workflow:**
1. Create FHIR Coverage resource
2. Check eligibility (active coverage)
3. Extract benefits (copay, deductible)
4. Check payor network
5. Return coverage summary

**Evaluator:** `validate_insurance_verification`
- Coverage resource valid
- Eligibility status correct
- Copay extracted
- Network status checked

---

### Task 004: Existing Patient Lookup (Fuzzy Match)
**Difficulty:** Hard  
**Expected Pass@1:** 50%

**Input:**
```
"Jon Do, born March 15, 1985"
```

**Expected workflow:**
1. Parse name and DOB
2. Fuzzy search FHIR Patient store (name ~80% match, DOB exact)
3. Return matching patients
4. If multiple, ask for disambiguation (SSN, address)
5. Return Patient resource

**Evaluator:** `validate_patient_search`
- Fuzzy matching used
- Correct patient found
- Disambiguation if multiple matches

---

### Task 005: Multi-Language Intake (Spanish)
**Difficulty:** Medium  
**Expected Pass@1:** 60%

**Input:**
```
"Hola, necesito una cita con el Dr. Smith"
```

**Expected workflow:**
1. Detect language (Spanish)
2. Route to Spanish-speaking staff OR use translation
3. Complete intake in Spanish
4. Document preferred language in FHIR Patient
5. Return patient resource with `communication.language = 'es'`

**Evaluator:** `validate_multilanguage_intake`
- Language detected
- Preferred language documented
- Intake completed

---

### Task 006: Emergency Contact Registration
**Difficulty:** Easy  
**Expected Pass@1:** 80%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "emergency_contact": {
    "name": "Jane Doe",
    "relationship": "spouse",
    "phone": "555-5678"
  }
}
```

**Expected workflow:**
1. Update FHIR Patient resource
2. Add `contact` array with emergency contact
3. Validate phone number format
4. Return updated Patient resource

**Evaluator:** `validate_emergency_contact`
- Contact added to Patient resource
- Relationship coded correctly
- Phone validated

---

### Task 007: Pharmacy Preference Capture
**Difficulty:** Medium  
**Expected Pass@1:** 65%

**Input:**
```
"I use CVS pharmacy at 123 Main St, Boston MA"
```

**Expected workflow:**
1. Use `google-search` to find pharmacy
2. Create FHIR Location resource for pharmacy
3. Link to Patient resource
4. Return pharmacy details

**Evaluator:** `validate_pharmacy_preference`
- Location resource created
- Linked to patient
- Address correct

---

### Task 008: Duplicate Patient Detection
**Difficulty:** Hard  
**Expected Pass@1:** 45%

**Input:**
```json
{
  "name": "John Doe",
  "dob": "1985-03-15",
  "phone": "555-1234"
}
```

**Expected workflow:**
1. Search for existing patients (name + DOB)
2. If found, warn "Possible duplicate"
3. Compare phone, address, SSN
4. If high confidence match, return existing patient
5. If uncertain, ask for disambiguation

**Evaluator:** `validate_duplicate_detection`
- Duplicate detected
- Comparison logic correct
- Appropriate disambiguation requested

---

## Category 2: Clinical Appointment Scheduling (10 tasks)

### Task 009: Basic Appointment Scheduling
**Difficulty:** Easy  
**Expected Pass@1:** 75%

**Input:**
```
"Book me for Tuesday at 2pm with Dr. Smith"
```

**Expected workflow:**
1. Parse date/time
2. Check Dr. Smith availability via `calendar`
3. Create appointment
4. Send confirmation via `email`
5. Return FHIR Appointment resource

**Evaluator:** `validate_basic_scheduling`
- Appointment created
- Time correct
- Confirmation sent

---

### Task 010: Specialist Referral with Authorization
**Difficulty:** Very Hard  
**Expected Pass@1:** 30%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "referral": {
    "from": "PCP",
    "to": "cardiology",
    "reason": "chest pain evaluation"
  }
}
```

**Expected workflow:**
1. Check if insurance requires referral authorization
2. If yes, create Task for authorization team
3. Find cardiology providers in network via `google-search`
4. Check availability via `calendar`
5. Tentatively schedule (pending auth)
6. Create FHIR Appointment with `status=pending`

**Evaluator:** `validate_specialist_referral`
- Authorization check performed
- Task created if needed
- Network providers searched
- Appointment status correct

---

### Task 011: Post-Discharge Follow-Up Scheduling
**Difficulty:** Hard  
**Expected Pass@1:** 45%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "discharge_date": "2025-11-03",
  "follow_up_specialty": "cardiology",
  "follow_up_in_days": 7
}
```

**Expected workflow:**
1. Use `date` to calculate target date (7 days from discharge)
2. Search for cardiology appointments within window
3. Create appointment
4. Link to CarePlan resource
5. Return appointment details

**Evaluator:** `validate_post_discharge_scheduling`
- Date calculation correct
- Within 7-day window
- Linked to CarePlan

---

### Task 012: Urgent Same-Day Appointment
**Difficulty:** Hard  
**Expected Pass@1:** 40%

**Input:**
```
"I need to see a doctor today, I have severe abdominal pain"
```

**Expected workflow:**
1. Triage urgency (severe pain = urgent)
2. Check same-day availability via `calendar`
3. If no slots, find urgent care/walk-in
4. Create appointment or provide urgent care info
5. Return appointment or alternative options

**Evaluator:** `validate_urgent_scheduling`
- Urgency correctly assessed
- Same-day slot found OR alternative provided

---

### Task 013: Recurring Appointments (PT Series)
**Difficulty:** Medium  
**Expected Pass@1:** 60%

**Input:**
```
"Schedule 6 weeks of physical therapy, twice a week"
```

**Expected workflow:**
1. Calculate 12 appointments over 6 weeks
2. Check PT availability via `calendar`
3. Create 12 appointments (Monday/Wednesday pattern)
4. Send confirmation with all dates via `email`
5. Return array of FHIR Appointment resources

**Evaluator:** `validate_recurring_appointments`
- 12 appointments created
- Pattern correct (2x/week)
- All within 6-week window

---

### Task 014: Rescheduling with Insurance Re-Check
**Difficulty:** Very Hard  
**Expected Pass@1:** 35%

**Input:**
```json
{
  "appointment_id": "appt-123",
  "new_date": "2025-12-01",
  "patient_mrn": "MRN-12345"
}
```

**Expected workflow:**
1. Get existing appointment
2. Check if patient has insurance authorization
3. If authorization expires before new date, warn + create auth task
4. Check provider availability on new date
5. Update appointment
6. Send updated confirmation via `email`

**Evaluator:** `validate_reschedule_with_insurance`
- Authorization window checked
- Task created if needed
- Appointment updated
- Confirmation sent

---

### Task 015: Provider Preference Matching
**Difficulty:** Medium  
**Expected Pass@1:** 55%

**Input:**
```
"I want a female cardiologist who speaks Spanish"
```

**Expected workflow:**
1. Search providers by specialty (cardiology)
2. Filter by gender (female)
3. Filter by language (Spanish)
4. Return list via `google-search` or internal directory
5. Allow patient to choose
6. Schedule with chosen provider

**Evaluator:** `validate_provider_matching`
- Filters applied correctly
- List presented
- Patient choice honored

---

### Task 016: Timezone Handling (Multi-Location)
**Difficulty:** Hard  
**Expected Pass@1:** 45%

**Input:**
```json
{
  "patient_timezone": "America/Los_Angeles",
  "clinic_timezone": "America/New_York",
  "requested_time": "2pm Pacific"
}
```

**Expected workflow:**
1. Convert 2pm Pacific to 5pm Eastern
2. Check clinic availability in Eastern time
3. Create appointment with correct timezone
4. Send confirmation in patient's timezone
5. Return appointment with both timezones

**Evaluator:** `validate_timezone_handling`
- Conversion correct
- Confirmation shows patient timezone
- FHIR resource has correct UTC time

---

### Task 017: Wait-List Management
**Difficulty:** Medium  
**Expected Pass@1:** 50%

**Input:**
```
"Dr. Smith is booked, add me to the cancellation list"
```

**Expected workflow:**
1. Create Task for wait-list
2. Monitor calendar for cancellations
3. When slot opens, notify patient via `sms-messaging`
4. Give 2-hour window to confirm
5. Return wait-list confirmation

**Evaluator:** `validate_waitlist_management`
- Task created
- SMS notification triggered
- Time window enforced

---

### Task 018: Appointment Reminders (24h Before)
**Difficulty:** Easy  
**Expected Pass@1:** 75%

**Input:**
```json
{
  "appointment_id": "appt-123",
  "patient_phone": "555-1234",
  "appointment_time": "2025-11-10T14:00:00"
}
```

**Expected workflow:**
1. Use `date` to calculate 24h before
2. Schedule SMS reminder via `sms-messaging`
3. Message: "Reminder: appointment tomorrow at 2pm. Reply CONFIRM or call"
4. Return confirmation

**Evaluator:** `validate_appointment_reminder`
- Timing correct (24h before)
- HIPAA-compliant message (no diagnosis)

---

## Category 3: Insurance & Authorization (8 tasks)

### Task 019: Prior Authorization Detection
**Difficulty:** Very Hard  
**Expected Pass@1:** 30%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "procedure_code": "CPT-70553",  // MRI brain
  "insurance": "Blue Cross"
}
```

**Expected workflow:**
1. Check if CPT-70553 requires prior auth (it does)
2. Create Task for authorization team
3. Notify patient via `email`
4. Generate FHIR CoverageEligibilityRequest
5. Return auth status

**Evaluator:** `validate_prior_auth_detection`
- CPT code correctly identified as requiring auth
- Task created with 3-day deadline
- Patient notified

---

### Task 020: Authorization Status Lookup
**Difficulty:** Medium  
**Expected Pass@1:** 55%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "procedure_code": "CPT-70553"
}
```

**Expected workflow:**
1. Search for existing authorization Task
2. Check status (pending/approved/denied)
3. Return auth details
4. If approved, provide approval number + valid dates

**Evaluator:** `validate_auth_status_lookup`
- Correct authorization found
- Status accurate
- Dates checked

---

### Task 021: Out-of-Network Detection
**Difficulty:** Hard  
**Expected Pass@1:** 40%

**Input:**
```json
{
  "patient_insurance": "Blue Cross",
  "provider": "Dr. Jones"
}
```

**Expected workflow:**
1. Check if Dr. Jones in Blue Cross network
2. If out-of-network, warn patient
3. Estimate patient cost (full charge vs. in-network copay)
4. Offer alternative in-network providers
5. Return network status

**Evaluator:** `validate_out_of_network_detection`
- Network status correct
- Cost estimate provided
- Alternatives offered

---

### Task 022: Copay Calculation
**Difficulty:** Hard  
**Expected Pass@1:** 45%

**Input:**
```json
{
  "coverage": {
    "payor": "Medicare",
    "plan_type": "Medicare Advantage",
    "copay_specialist": 50
  },
  "appointment_type": "specialist"
}
```

**Expected workflow:**
1. Extract copay from Coverage resource
2. Match appointment type (specialist = $50)
3. Return patient responsibility
4. Send estimate via `email`

**Evaluator:** `validate_copay_calculation`
- Copay correctly extracted
- Appointment type matched
- Estimate sent

---

### Task 023: Benefits Explanation (Deductible)
**Difficulty:** Very Hard  
**Expected Pass@1:** 25%

**Input:**
```json
{
  "coverage": {
    "deductible_total": 2000,
    "deductible_met": 500,
    "coinsurance": 0.2
  },
  "procedure_cost": 1000
}
```

**Expected workflow:**
1. Calculate remaining deductible ($1500)
2. Patient pays $1000 toward deductible
3. After deductible met, coinsurance applies
4. Explain to patient: "You'll pay $1000 toward your deductible"
5. Return breakdown

**Evaluator:** `validate_benefits_explanation`
- Deductible calculation correct
- Coinsurance logic correct
- Explanation clear

---

### Task 024: Secondary Insurance (Coordination of Benefits)
**Difficulty:** Extreme  
**Expected Pass@1:** 20%

**Input:**
```json
{
  "primary_insurance": "Blue Cross",
  "secondary_insurance": "Aetna",
  "procedure_cost": 1000
}
```

**Expected workflow:**
1. Bill primary insurance first
2. Calculate primary payment (e.g., 80% = $800)
3. Bill secondary for remaining ($200)
4. Calculate secondary payment (e.g., 50% = $100)
5. Patient owes $100
6. Return breakdown

**Evaluator:** `validate_coordination_of_benefits`
- Primary billed first
- Secondary calculation correct
- Patient responsibility accurate

---

### Task 025: Uninsured Patient Routing
**Difficulty:** Medium  
**Expected Pass@1:** 60%

**Input:**
```
"I don't have insurance"
```

**Expected workflow:**
1. Offer financial assistance programs
2. Provide self-pay discount information
3. Use `google-search` to find local resources (Medicaid, free clinics)
4. Create Task for financial counselor
5. Return resource list

**Evaluator:** `validate_uninsured_routing`
- Financial assistance offered
- Resources provided
- Task created

---

### Task 026: High-Cost Procedure Escalation
**Difficulty:** Hard  
**Expected Pass@1:** 40%

**Input:**
```json
{
  "procedure_code": "CPT-27447",  // Total knee replacement
  "estimated_cost": 35000
}
```

**Expected workflow:**
1. Identify as high-cost procedure
2. Require pre-authorization
3. Create Task for case manager
4. Schedule pre-surgery counseling
5. Return escalation confirmation

**Evaluator:** `validate_high_cost_escalation`
- High-cost identified
- Authorization required
- Case manager involved

---

## Category 4: Clinical Triage & Routing (8 tasks)

### Task 027: Chief Complaint Classification (ICD-10)
**Difficulty:** Medium  
**Expected Pass@1:** 55%

**Input:**
```
"I have a bad cough for 3 days"
```

**Expected workflow:**
1. Classify as respiratory symptom
2. Map to ICD-10: R05 (Cough)
3. Assess urgency (routine)
4. Create FHIR Observation
5. Return classification

**Evaluator:** `validate_chief_complaint_classification`
- ICD-10 code correct
- Urgency appropriate

---

### Task 028: Urgency Assessment
**Difficulty:** Hard  
**Expected Pass@1:** 45%

**Input:**
```
"I have chest pain, it's been getting worse"
```

**Expected workflow:**
1. Identify EMERGENT symptom (chest pain)
2. Ask triage questions (radiating, SOB, history)
3. Route to ER/911 based on answers
4. Create urgent Task
5. Document in FHIR Observation

**Evaluator:** `validate_urgency_assessment`
- Chest pain identified as emergent
- Triage questions asked
- Appropriate routing (ER/911)

---

### Task 029: Symptom-Based Routing
**Difficulty:** Medium  
**Expected Pass@1:** 60%

**Input:**
```
"My knee hurts after a fall"
```

**Expected workflow:**
1. Identify musculoskeletal injury
2. Route to orthopedics
3. Check if urgent (fracture suspected) → X-ray first
4. Schedule appointment
5. Return routing decision

**Evaluator:** `validate_symptom_routing`
- Correct specialty (orthopedics)
- Urgency assessed
- X-ray ordered if needed

---

### Task 030: Telehealth Eligibility
**Difficulty:** Hard  
**Expected Pass@1:** 40%

**Input:**
```
"Can I do a video visit for my skin rash?"
```

**Expected workflow:**
1. Assess if telehealth-appropriate (yes, dermatology often is)
2. Check if insurance covers telehealth
3. Offer virtual appointment
4. Send video link via `email`
5. Return telehealth confirmation

**Evaluator:** `validate_telehealth_eligibility`
- Appropriateness assessed
- Insurance coverage checked
- Video link sent

---

### Task 031: Nurse Triage Handoff
**Difficulty:** Hard  
**Expected Pass@1:** 40%

**Input:**
```
"I'm not sure if I should come in for my fever"
```

**Expected workflow:**
1. Recognize need for clinical judgment
2. Escalate to nurse triage line
3. Create Task for nurse callback
4. Provide callback timeline (30 min)
5. Return handoff confirmation

**Evaluator:** `validate_nurse_handoff`
- Escalation appropriate
- Task created
- Timeline communicated

---

### Task 032: After-Hours Protocol
**Difficulty:** Hard  
**Expected Pass@1:** 35%

**Input:**
```
"It's 10pm, I need to see a doctor"
```

**Expected workflow:**
1. Recognize after-hours
2. Assess urgency (emergent → ER, urgent → on-call, routine → next day)
3. Provide on-call number OR ER directions
4. Return after-hours guidance

**Evaluator:** `validate_after_hours_protocol`
- Time recognized
- Appropriate routing
- Contact info provided

---

### Task 033: Pharmacy Routing (Refill vs New Rx)
**Difficulty:** Medium  
**Expected Pass@1:** 55%

**Input:**
```
"I need a refill of my blood pressure medication"
```

**Expected workflow:**
1. Check if refills remaining
2. If yes, route to pharmacy
3. If no, route to provider for new Rx
4. Return routing decision

**Evaluator:** `validate_pharmacy_routing`
- Refill status checked
- Correct routing (pharmacy vs provider)

---

### Task 034: Lab Result Inquiry
**Difficulty:** Hard  
**Expected Pass@1:** 40%

**Input:**
```
"Are my lab results ready?"
```

**Expected workflow:**
1. Check if results available
2. If yes, notify results in portal (HIPAA-compliant, no values over phone)
3. If critical, escalate to provider immediately
4. Return status

**Evaluator:** `validate_lab_result_inquiry`
- Results checked
- HIPAA compliance (no values given)
- Critical results escalated

---

## Category 5: HIPAA-Compliant Multi-Channel Orchestration (6 tasks)

### Task 035: Appointment Confirmation Workflow
**Difficulty:** Hard  
**Expected Pass@1:** 40%

**Input:**
```json
{
  "appointment_id": "appt-123",
  "patient": {...}
}
```

**Expected workflow:**
1. Create appointment via `calendar`
2. Send encrypted confirmation via `email`
3. Add to patient portal
4. Schedule SMS reminder (24h before)
5. Return workflow confirmation

**Evaluator:** `validate_appointment_workflow`
- All 4 steps completed
- HIPAA compliance validated

---

### Task 036: Test Result Notification
**Difficulty:** Very Hard  
**Expected Pass@1:** 25%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "test_type": "Complete Blood Count",
  "critical_result": false
}
```

**Expected workflow:**
1. Send portal notification (results available)
2. Send SMS alert via `sms-messaging`: "Results ready in portal"
3. If critical, call patient + escalate to provider
4. Return notification confirmation

**Evaluator:** `validate_test_result_notification`
- Portal notification sent
- SMS HIPAA-compliant (no values)
- Critical results escalated

---

### Task 037: Referral Coordination
**Difficulty:** Extreme  
**Expected Pass@1:** 20%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "referral_from": "PCP",
  "referral_to": "cardiology",
  "medical_records_needed": true
}
```

**Expected workflow:**
1. Schedule specialist appointment via `calendar`
2. Generate medical records summary via `pdf-generator`
3. Send records to specialist via `email` (encrypted)
4. Create Task for follow-up coordination
5. Notify patient via `email`
6. Generate FHIR DocumentReference

**Evaluator:** `validate_referral_coordination`
- All 6 steps completed
- Records sent securely
- DocumentReference created

---

### Task 038: Post-Discharge Follow-Up (Full Workflow)
**Difficulty:** Extreme  
**Expected Pass@1:** 15%

**Input:**
```json
{
  "patient_mrn": "MRN-12345",
  "discharge_date": "2025-11-03",
  "diagnosis": "CHF exacerbation",
  "follow_up_in_days": 7
}
```

**Expected workflow:**
1. Schedule cardiology follow-up via `calendar` (within 7 days)
2. Generate discharge summary via `pdf-generator`
3. Send summary via `email` (HIPAA-compliant)
4. Schedule medication reminders via `sms-messaging`
5. Create check-in task for nurse via `task-management`
6. Generate FHIR Appointment + CarePlan + Task

**Evaluator:** `validate_post_discharge_workflow`
- All 6 steps completed
- FHIR resources created
- Timing correct (within 7 days)

---

### Task 039: Prescription Refill Workflow
**Difficulty:** Hard  
**Expected Pass@1:** 35%

**Input:**
```
"I need a refill of my lisinopril"
```

**Expected workflow:**
1. Check last fill date via `date` (must be >30 days ago)
2. Check refills remaining
3. If yes, route to pharmacy
4. If no, create Task for provider
5. Notify patient of timeline
6. Return refill status

**Evaluator:** `validate_refill_workflow`
- Date check performed
- Correct routing
- Patient notified

---

### Task 040: Billing Inquiry Escalation
**Difficulty:** Medium  
**Expected Pass@1:** 50%

**Input:**
```
"I have a question about my bill"
```

**Expected workflow:**
1. Create Task for billing department via `task-management`
2. Send summary via `email` to billing
3. Provide patient with billing contact info
4. Set callback expectation (24-48h)
5. Return escalation confirmation

**Evaluator:** `validate_billing_escalation`
- Task created
- Summary sent to billing
- Timeline communicated

---

## Summary Statistics

**Total Tasks:** 40

**By Difficulty:**
- Easy: 5 tasks (avg 78% pass)
- Medium: 12 tasks (avg 58% pass)
- Hard: 15 tasks (avg 42% pass)
- Very Hard: 5 tasks (avg 28% pass)
- Extreme: 3 tasks (avg 18% pass)

**Overall Expected Pass@1:** 40% (discriminative)

## Next Steps
- See `05-evaluators.md` for evaluation logic for each task
- See `07-implementation-guide.md` for code templates

