# Healthcare Receptionist Domain

Benchmark for testing AI agents on healthcare receptionist workflows with HIPAA compliance and FHIR standards.

## Domain Structure

```
domains/healthcare_receptionist/
├── config.yaml              # Domain configuration
├── README.md                # Domain documentation
├── tasks/                   # 40 task JSON files
│   ├── Patient Intake (8 tasks)
│   ├── Appointment Scheduling (10 tasks)
│   ├── Insurance & Authorization (8 tasks)
│   ├── Clinical Triage (8 tasks)
│   └── Multi-Channel Orchestration (6 tasks)
└── evaluators/              # Evaluator functions
    ├── __init__.py
    ├── error_types.py       # [parse_error] and [validation_error]
    └── functions.py          # Validation functions
```

## Tasks Breakdown

**Patient Intake (8 tasks):**
- Basic intake, HIPAA consent, insurance verification
- New patient onboarding, existing patient lookup
- Multi-language intake, emergency contacts, pharmacy preference

**Appointment Scheduling (10 tasks):**
- Basic scheduling, specialist referrals, follow-ups
- Urgent same-day, recurring appointments
- Rescheduling with insurance, provider matching
- Timezone handling, wait-list management, reminders

**Insurance & Authorization (8 tasks):**
- Eligibility verification, prior authorization checks
- Out-of-network detection, copay calculation
- Benefits explanation, secondary insurance, uninsured routing

**Clinical Triage (8 tasks):**
- Chief complaint classification, urgency assessment
- Symptom-based routing, telehealth eligibility
- Nurse triage handoff, after-hours protocol
- Pharmacy routing, lab result inquiry

**Multi-Channel Orchestration (6 tasks):**
- Appointment confirmation workflows
- Test result notifications
- Referral coordination
- Post-discharge follow-up
- Prescription refills
- Billing inquiry escalation

## MCP Servers Required

Uses 4 custom servers (via submodule):
- `twilio_hipaa` - HIPAA-compliant SMS/Voice (5 tools)
- `assemblyai` - Medical transcription (5 tools)
- `videosdk` - Video consultations (7 tools)
- `nexhealth` - EHR integration (6 tools)

**Server Status:** PR pending in mothership repo

## Configuration

- **LLM Models:** Claude Sonnet 4.5, GPT-4o, GPT-4o-mini
- **Evaluators:** Error classification with `[parse_error]` and `[validation_error]`
- **Target Pass Rate:** 40% (discriminative benchmark)
- **Standards:** FHIR R4, HL7 v2.x, HIPAA compliance

## Expected Results

- **Target Pass Rate:** 40% (16/40 tasks)
- **Safety-Critical:** Clinical triage tasks require 100% accuracy on emergent cases
- **Complexity:** Very High (clinical logic + compliance + multi-step workflows)

## Next Steps

After server PR merges:
1. Update submodule to point to merged servers
2. Run LLM agent tests
3. Measure performance and iterate




