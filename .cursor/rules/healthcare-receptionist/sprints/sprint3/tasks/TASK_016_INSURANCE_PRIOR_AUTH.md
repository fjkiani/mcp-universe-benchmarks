# TASK 016: Insurance Prior Authorization Task

**Agent:** Task Designer  
**Status:** TODO  
**Priority:** P1  
**Estimated Time:** 2 hours

---

## 📋 Task Definition

Create a task JSON file for insurance prior authorization requests.

---

## 🎯 Inputs

**Reference Tasks:**
1. `domains/healthcare_receptionist/tasks/patient_intake_insurance_verification_003.json` - Insurance verification pattern
2. `domains/healthcare_receptionist/tasks/appointment_specialist_referral_010.json` - Referral workflow pattern

**Required Information:**
- Task ID: `insurance_prior_auth_016`
- MCP Servers: `nexhealth` (for insurance), `email` (for notifications)
- Complexity: Moderate
- Target Pass Rate: 30-40%

---

## 📤 Output (Deliverable)

Create `domains/healthcare_receptionist/tasks/insurance_prior_auth_016.json`:

```json
{
  "task_id": "insurance_prior_auth_016",
  "name": "Insurance Prior Authorization Request",
  "description": "Request prior authorization from insurance for a specialist procedure",
  "category": "insurance",
  "complexity": "moderate",
  "mcp_servers": [
    {"name": "nexhealth"},
    {"name": "email"}
  ],
  "question": "A patient needs a prior authorization for a specialist procedure. Patient: Sarah Johnson, DOB: 1985-03-15, Insurance: Blue Cross Blue Shield, Policy #: BCBS-123456789, Procedure: MRI of lumbar spine, Referring Provider: Dr. Smith (ID: 12345). Please submit a prior authorization request to the insurance company and send a confirmation email to the patient.",
  "expected_output": {
    "type": "json",
    "schema": {
      "prior_auth_requested": "boolean",
      "prior_auth_id": "string",
      "insurance_provider": "string",
      "procedure_code": "string",
      "status": "string",
      "estimated_approval_time": "string",
      "patient_notified": "boolean",
      "email_sent": "boolean"
    }
  },
  "output_format": {
    "prior_auth_requested": true,
    "prior_auth_id": "PA-2025-XXXXX",
    "insurance_provider": "Blue Cross Blue Shield",
    "procedure_code": "72148",
    "status": "submitted",
    "estimated_approval_time": "5-7 business days",
    "patient_notified": true,
    "email_sent": true
  },
  "evaluators": [
    {
      "name": "validate_insurance_prior_auth",
      "module": "healthcare_receptionist.evaluators.functions"
    }
  ]
}
```

---

## ✅ Acceptance Criteria

1. **File Created:**
   - [ ] `insurance_prior_auth_016.json` exists in `domains/healthcare_receptionist/tasks/`
   - [ ] Valid JSON syntax

2. **Task Structure:**
   - [ ] `task_id` matches filename
   - [ ] `mcp_servers` includes `nexhealth` and `email`
   - [ ] `question` field is clear and actionable
   - [ ] `expected_output` schema is complete
   - [ ] `output_format` shows example response
   - [ ] `evaluators` references correct function

3. **Content Quality:**
   - [ ] Question includes all necessary patient info
   - [ ] Question specifies insurance details
   - [ ] Question mentions procedure
   - [ ] Expected output matches real-world prior auth response

---

## 🧪 Testing

```bash
# Validate JSON syntax
python3 -m json.tool domains/healthcare_receptionist/tasks/insurance_prior_auth_016.json

# Validate structure (if local_tests available)
python3 local_tests/test_tasks.py --domain healthcare_receptionist --task insurance_prior_auth_016
```

**Expected Result:**
- ✅ JSON is valid
- ✅ All required fields present
- ✅ Structure matches reference tasks

---

## 🔍 Review Checklist (for Zo)

- [ ] File created in correct location
- [ ] JSON syntax valid
- [ ] All required fields present
- [ ] Question is clear and actionable
- [ ] MCP servers match requirements
- [ ] Evaluator reference is correct
- [ ] Follows pattern from reference tasks

---

## 📝 Output Format

**Submit via:**
1. Create `domains/healthcare_receptionist/tasks/insurance_prior_auth_016.json`
2. Copy this file to `.cursor/rules/healthcare-receptionist/sprints/sprint3/deliverables/TASK_016_COMPLETE.md`
3. Update status to `COMPLETE`

**Example Completion:**
```markdown
# TASK 016: COMPLETE

**Agent:** Task Designer  
**Time Taken:** 1.5 hours  
**Status:** ✅ COMPLETE

## Deliverables
- ✅ Created `insurance_prior_auth_016.json`
- ✅ Valid JSON syntax
- ✅ All required fields present

## Testing
- ✅ JSON validation passed
- ✅ Structure matches reference tasks

## Blockers
None

## Next Task
Ready for TASK_017 (Insurance Benefits Inquiry)
```

