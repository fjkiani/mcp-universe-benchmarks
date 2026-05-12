# Healthcare Receptionist - Implementation Guide

## Overview

Step-by-step guide to build and deploy the Healthcare Receptionist domain from scratch.

**Timeline:** 6 weeks (4 weeks development + 2 weeks testing/hardening)

---

## Phase 1: Project Setup (Week 1)

### 1.1 Clone Template Repository
```bash
# Clone the MCP Universe template
git clone https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template.git
cd lbx_mcp_universe_template

# Create healthcare-receptionist domain branch
git checkout -b domains/healthcare-receptionist/v1

# Update submodules
git submodule update --init --recursive
```

### 1.2 Create Domain Structure
```bash
# Create domain directory
mkdir -p domains/healthcare_receptionist/{tasks,evaluators,schemas}

# Create initial files
touch domains/healthcare_receptionist/config.yaml
touch domains/healthcare_receptionist/evaluators/__init__.py
touch domains/healthcare_receptionist/evaluators/functions.py
touch domains/healthcare_receptionist/README.md
```

### 1.3 Install Dependencies
```bash
# Install Python dependencies
cd lbx_mcp_universe_cli
uv sync

# Install additional healthcare-specific packages
uv pip install fhir.resources jsonschema python-dateutil
```

### 1.4 Configure LLMs and Agent
**File:** `domains/healthcare_receptionist/config.yaml`

```yaml
---
kind: llm
spec:
  name: llm-healthcare-agent
  type: litellm  # OpenAI-compatible / LiteLLM gateway
  config:
    model_name: openai/gpt-4o
    temperature: 0.1  # Low temp for clinical accuracy

---
kind: llm
spec:
  name: llm-healthcare-evaluator
  type: litellm  # OpenAI-compatible / LiteLLM gateway
  config:
    model_name: openai/gpt-4o-mini
    temperature: 0.0  # Deterministic evaluation

---
kind: agent
spec:
  name: healthcare-receptionist-agent
  type: react
  config:
    llm: llm-healthcare-agent
    max_iterations: 15  # Complex workflows need more steps
    system_prompt: |
      You are a healthcare receptionist AI assistant. You help with:
      - Patient intake and registration (FHIR Patient resources)
      - Appointment scheduling (FHIR Appointment resources)
      - Insurance verification (FHIR Coverage resources)
      - Clinical triage (FHIR Observation resources)
      - Care coordination (FHIR CarePlan, Task resources)
      
      CRITICAL SAFETY RULES:
      1. Chest pain, difficulty breathing, stroke symptoms = EMERGENT → 911/ER
      2. NEVER schedule routine appointments for emergent symptoms
      3. NEVER include PHI (diagnoses, medications, lab values) in SMS/email
      4. All patient data must be structured as FHIR R4 resources
      5. Generate MRNs in format: MRN-{5-digit-number}
      
      HIPAA COMPLIANCE:
      - SMS: Only "Your appointment is [date]" (NO diagnosis, procedure, or results)
      - Email subject: Generic ("Appointment Confirmation", NOT "Diabetes Appointment")
      - Email body: Use portal link for results (NO lab values in email)
      
      Available MCP servers:
      - calendar: Appointment scheduling, availability checks
      - email: HIPAA-compliant patient communication
      - sms-messaging: Appointment reminders (HIPAA-compliant)
      - task-management: Care coordination, follow-ups
      - google-search: Find pharmacies, clinics, insurance networks
      - pdf-generator: Consent forms, discharge summaries
      - date: Age calculation, appointment date logic

---
kind: benchmark
spec:
  name: healthcare-receptionist-benchmark
  description: |
    HARDENED healthcare receptionist benchmark (40 tasks).
    Tests patient intake, appointment scheduling, insurance authorization,
    clinical triage, and multi-channel orchestration.
    
    Target pass rate: 35-45% (discriminative)
    
  agent: healthcare-receptionist-agent
  llm: llm-healthcare-evaluator
  tasks:
    # Category 1: Patient Intake (8 tasks)
    - tasks/patient_intake_basic_001.json
    - tasks/patient_intake_hipaa_consent_002.json
    - tasks/patient_intake_insurance_verification_003.json
    - tasks/patient_intake_existing_lookup_004.json
    - tasks/patient_intake_multilanguage_005.json
    - tasks/patient_intake_emergency_contact_006.json
    - tasks/patient_intake_pharmacy_007.json
    - tasks/patient_intake_duplicate_detection_008.json
    
    # Category 2: Appointment Scheduling (10 tasks)
    - tasks/appointment_basic_009.json
    - tasks/appointment_specialist_referral_010.json
    - tasks/appointment_post_discharge_011.json
    - tasks/appointment_urgent_same_day_012.json
    - tasks/appointment_recurring_pt_013.json
    - tasks/appointment_reschedule_insurance_014.json
    - tasks/appointment_provider_matching_015.json
    - tasks/appointment_timezone_016.json
    - tasks/appointment_waitlist_017.json
    - tasks/appointment_reminder_018.json
    
    # Category 3: Insurance & Authorization (8 tasks)
    - tasks/insurance_prior_auth_detection_019.json
    - tasks/insurance_auth_status_lookup_020.json
    - tasks/insurance_out_of_network_021.json
    - tasks/insurance_copay_calculation_022.json
    - tasks/insurance_benefits_explanation_023.json
    - tasks/insurance_secondary_cob_024.json
    - tasks/insurance_uninsured_routing_025.json
    - tasks/insurance_high_cost_escalation_026.json
    
    # Category 4: Clinical Triage (8 tasks)
    - tasks/triage_chief_complaint_icd10_027.json
    - tasks/triage_urgency_chest_pain_028.json
    - tasks/triage_symptom_routing_029.json
    - tasks/triage_telehealth_eligibility_030.json
    - tasks/triage_nurse_handoff_031.json
    - tasks/triage_after_hours_032.json
    - tasks/triage_pharmacy_routing_033.json
    - tasks/triage_lab_result_inquiry_034.json
    
    # Category 5: Multi-Channel Orchestration (6 tasks)
    - tasks/orchestration_appointment_confirmation_035.json
    - tasks/orchestration_test_result_notification_036.json
    - tasks/orchestration_referral_coordination_037.json
    - tasks/orchestration_post_discharge_full_038.json
    - tasks/orchestration_prescription_refill_039.json
    - tasks/orchestration_billing_escalation_040.json
```

---

## Phase 2: FHIR Schema Setup (Week 1)

### 2.1 Install FHIR Libraries
```bash
uv pip install fhir.resources==7.1.0
```

### 2.2 Create FHIR Schema Validators
**File:** `domains/healthcare_receptionist/schemas/fhir_validator.py`

```python
from fhir.resources.patient import Patient
from fhir.resources.appointment import Appointment
from fhir.resources.coverage import Coverage
from fhir.resources.observation import Observation
from fhir.resources.careplan import CarePlan
from fhir.resources.task import Task
from pydantic import ValidationError
import json

class FHIRValidator:
    """Validates FHIR R4 resources"""
    
    RESOURCE_CLASSES = {
        'Patient': Patient,
        'Appointment': Appointment,
        'Coverage': Coverage,
        'Observation': Observation,
        'CarePlan': CarePlan,
        'Task': Task
    }
    
    def validate(self, resource: dict) -> tuple[bool, str]:
        """
        Validate FHIR resource
        
        Returns:
            (valid: bool, error_message: str)
        """
        resource_type = resource.get('resourceType')
        
        if resource_type not in self.RESOURCE_CLASSES:
            return False, f"Unknown resourceType: {resource_type}"
        
        try:
            # Parse with Pydantic FHIR model
            resource_class = self.RESOURCE_CLASSES[resource_type]
            resource_class(**resource)
            return True, ""
        except ValidationError as e:
            return False, str(e)
    
    def validate_patient(self, patient: dict) -> tuple[bool, str]:
        """Validate Patient resource with business rules"""
        # FHIR schema validation
        valid, error = self.validate(patient)
        if not valid:
            return False, f"FHIR validation failed: {error}"
        
        # Business rules
        if not patient.get('identifier'):
            return False, "Patient must have at least one identifier (MRN)"
        
        if not patient.get('telecom'):
            return False, "Patient must have at least one contact method"
        
        # Age check
        from datetime import datetime
        birth_date = patient.get('birthDate')
        if birth_date:
            age = (datetime.now().date() - datetime.fromisoformat(birth_date).date()).days // 365
            if age < 0 or age > 120:
                return False, f"Invalid age: {age}"
        
        return True, ""
```

---

## Phase 3: Task Creation (Week 2)

### 3.1 Task Template
**File:** `domains/healthcare_receptionist/tasks/patient_intake_basic_001.json`

```json
{
  "task_id": "patient_intake_basic_001",
  "category": "patient_intake",
  "difficulty": "easy",
  "description": "Basic new patient intake workflow",
  "prompt": "A new patient calls: 'Hi, I'd like to schedule my first appointment with Dr. Smith.' Complete the intake process: collect demographics, insurance, chief complaint, check provider availability, schedule appointment, send confirmation, and generate intake form. Return a FHIR Patient resource with appointment details.",
  "expected_output": {
    "patient": {
      "resourceType": "Patient",
      "identifier": [{"value": "MRN-12345"}],
      "name": [{"family": "Doe", "given": ["John"]}],
      "birthDate": "1985-03-15",
      "telecom": [{"system": "phone", "value": "555-1234"}]
    },
    "appointment": {
      "provider": "Dr. Smith",
      "date": "2025-11-10",
      "time": "14:00"
    },
    "intake_form_sent": true
  },
  "mcp_servers": [
    {"name": "calendar"},
    {"name": "email"},
    {"name": "pdf-generator"}
  ],
  "use_specified_server": true,
  "evaluators": {
    "func": "validate_patient_intake",
    "op": "healthcare.validate_patient_intake"
  }
}
```

### 3.2 Generate All 40 Tasks
```bash
# Use script to generate task files from templates
python scripts/generate_healthcare_tasks.py

# Verify all tasks created
ls -la domains/healthcare_receptionist/tasks/
# Should see 40 .json files
```

---

## Phase 4: Evaluator Implementation (Week 2-3)

### 4.1 Helper Functions
**File:** `domains/healthcare_receptionist/evaluators/functions.py`

```python
from lbx_cli.mcpuniverse.evaluator.functions import compare_func
from typing import Tuple, Any
import json
import re
from datetime import datetime

def unwrap_pydantic_and_parse_json(agent_response: Any) -> Tuple[bool, Any, str]:
    """Unwraps Pydantic FunctionResult and parses JSON"""
    try:
        # Handle Pydantic models
        if hasattr(agent_response, 'model_dump'):
            agent_response = agent_response.model_dump()
        elif hasattr(agent_response, 'dict'):
            agent_response = agent_response.dict()
        elif hasattr(agent_response, '__dict__'):
            agent_response = dict(agent_response.__dict__)
        
        # Unwrap nested 'result' keys
        while isinstance(agent_response, dict) and 'result' in agent_response and len(agent_response) == 1:
            agent_response = agent_response['result']
        
        # Parse JSON string
        if isinstance(agent_response, str):
            cleaned = agent_response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1]) if len(lines) > 2 else cleaned
            cleaned = cleaned.strip()
            data = json.loads(cleaned)
        elif isinstance(agent_response, dict):
            data = agent_response
        else:
            return False, None, f"Could not convert to dict. Type: {type(agent_response).__name__}"
        
        if not isinstance(data, dict):
            return False, None, f"Final data is not a dict! Type: {type(data).__name__}"
        
        return True, data, ""
        
    except json.JSONDecodeError as e:
        return False, None, f"JSON parse failed: {str(e)}"
    except Exception as e:
        return False, None, f"Unexpected error: {str(e)}"


def validate_hipaa_compliance(data: dict) -> Tuple[bool, str]:
    """Validates HIPAA compliance in communications"""
    PHI_PATTERNS = [
        r'\b(diabetes|hypertension|cancer|HIV|AIDS)\b',
        r'\b(metformin|lisinopril|insulin)\b',
        r'\b\d+\s?(mg/dL|mmol/L|units)\b'
    ]
    
    # Check SMS messages
    sms_messages = data.get('sms_messages', [])
    for msg in sms_messages:
        message_body = msg.get('body', '')
        for pattern in PHI_PATTERNS:
            if re.search(pattern, message_body, re.IGNORECASE):
                return False, f"HIPAA violation: PHI detected in SMS: {pattern}"
    
    # Check email subjects
    email_subjects = data.get('email_subjects', [])
    for subject in email_subjects:
        for pattern in PHI_PATTERNS:
            if re.search(pattern, subject, re.IGNORECASE):
                return False, f"HIPAA violation: PHI detected in email subject: {pattern}"
    
    return True, ""
```

### 4.2 Implement All 40 Evaluators
```python
@compare_func
async def validate_patient_intake(
    agent_response: Any,
    ground_truth: dict
) -> Tuple[bool, str]:
    """Validates basic patient intake workflow"""
    success, data, error = unwrap_pydantic_and_parse_json(agent_response)
    if not success:
        return False, f"Parse error: {error}"
    
    # Validate Patient resource
    patient = data.get('patient')
    if not patient or patient.get('resourceType') != 'Patient':
        return False, "Missing or invalid Patient resource"
    
    # Required fields
    required = ['identifier', 'name', 'birthDate', 'telecom']
    for field in required:
        if field not in patient:
            return False, f"Missing required field: {field}"
    
    # Appointment created
    if not data.get('appointment'):
        return False, "No appointment created"
    
    # Intake form sent
    if not data.get('intake_form_sent'):
        return False, "Intake form not sent"
    
    return True, "Patient intake validated successfully"

# ... Implement remaining 39 evaluators (see 05-evaluators.md)
```

---

## Phase 5: Local Testing (Week 3-4)

### 5.1 Validate Domain Structure
```bash
# Lint domain (checks config.yaml, tasks, evaluators)
cd /path/to/lbx_mcp_universe_template
uv run alignerr_mcp lint-domain --domain healthcare_receptionist

# Should see:
# ✅ Domain structure is valid!
# Summary: LLMs: 2, Agents: 1, Benchmarks: 1, Tasks: 40
```

### 5.2 Test Individual Tasks
```bash
# Test single task
uv run alignerr_mcp validate \
  --domain healthcare_receptionist \
  --tasks patient_intake_basic_001

# Test category
uv run alignerr_mcp validate \
  --domain healthcare_receptionist \
  --tasks patient_intake_*

# Test all tasks (long-running)
uv run alignerr_mcp validate \
  --domain healthcare_receptionist
```

### 5.3 Analyze Results
```bash
# View results summary
cat evaluation_results/healthcare_receptionist_summary.json

# Expected output:
# {
#   "total_tasks": 40,
#   "passed": 16,
#   "failed": 24,
#   "pass_rate": 0.40,
#   "by_category": {
#     "patient_intake": {"passed": 5, "failed": 3},
#     "appointment_scheduling": {"passed": 5, "failed": 5},
#     "insurance_authorization": {"passed": 2, "failed": 6},
#     "clinical_triage": {"passed": 2, "failed": 6},
#     "multi_channel_orchestration": {"passed": 2, "failed": 4}
#   }
# }
```

---

## Phase 6: Hardening (Week 4-5)

### 6.1 If Pass Rate Too High (>55%)
```bash
# Add harder tasks or make existing tasks stricter
# Example: Add edge cases to Task 028 (chest pain triage)
```

**File:** `domains/healthcare_receptionist/tasks/triage_urgency_chest_pain_028_hard.json`
```json
{
  "task_id": "triage_urgency_chest_pain_028_hard",
  "description": "Chest pain triage with ambiguous symptoms",
  "prompt": "Patient: 'I have chest discomfort, maybe indigestion?' (Patient downplaying symptoms). Ask triage questions to determine if emergent.",
  "expected_output": {
    "triage_category": "EMERGENT",
    "recommended_action": "call_911"
  }
}
```

### 6.2 If Pass Rate Too Low (<30%)
```bash
# Simplify some tasks or improve agent prompt
# Example: Add more guidance to config.yaml system_prompt
```

### 6.3 Target: 35-45% Pass Rate
- Too easy (>70%) = not discriminative
- Too hard (<20%) = agents can't learn
- **Sweet spot: 35-45%** = production-ready discriminative benchmark

---

## Phase 7: CI/CD Integration (Week 5)

### 7.1 Push to GitHub
```bash
# Commit changes
git add domains/healthcare_receptionist/
git commit -m "feat: Add Healthcare Receptionist domain (40 tasks, FHIR R4, HIPAA-compliant)"

# Push to branch
git push origin domains/healthcare-receptionist/v1
```

### 7.2 Create Pull Request
```bash
# Create PR via GitHub CLI
gh pr create \
  --title "Healthcare Receptionist Domain (40 tasks, 40% target)" \
  --body "
## Summary
Healthcare-specific receptionist domain with 40 tasks across 5 categories.

## Key Features
- FHIR R4 resources (Patient, Appointment, Coverage, Observation, CarePlan, Task)
- HIPAA compliance validation
- Safety-critical triage logic (chest pain = 911/ER)
- Multi-channel orchestration (calendar, email, SMS, tasks, PDF)

## Expected Results
- **Target Pass@1:** 35-45% (discriminative)
- **Task Count:** 40 (8 intake, 10 scheduling, 8 insurance, 8 triage, 6 orchestration)
- **Difficulty:** Very High

## Test Results
Local testing shows 40% pass rate (ideal discriminative benchmark).

Ready for merge!
"
```

### 7.3 Wait for CI/CD
```bash
# CI/CD will automatically:
# 1. Lint domain structure
# 2. Run all 40 tasks
# 3. Post evaluation report as PR comment

# Check PR for results:
# https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template/pull/XXX
```

---

## Phase 8: Production Deployment (Week 6)

### 8.1 Merge to Main
```bash
# After PR approval, merge
gh pr merge --squash
```

### 8.2 Deploy to Production
```bash
# Deploy via CI/CD pipeline
# (Handled by GitHub Actions)
```

---

## Troubleshooting

### Issue 1: "No such command 'lint-domain'"
**Solution:** Update CLI submodule
```bash
git submodule update --remote lbx_mcp_universe_cli
uv sync
```

### Issue 2: "FHIR validation failed"
**Solution:** Check resource structure
```python
from domains.healthcare_receptionist.schemas.fhir_validator import FHIRValidator

validator = FHIRValidator()
valid, error = validator.validate_patient(patient_resource)
print(f"Valid: {valid}, Error: {error}")
```

### Issue 3: "HIPAA violation detected"
**Solution:** Check PHI in communications
```python
from domains.healthcare_receptionist.evaluators.functions import validate_hipaa_compliance

valid, error = validate_hipaa_compliance({
    'sms_messages': [{'body': 'Your diabetes appointment is tomorrow'}]
})
print(f"Valid: {valid}, Error: {error}")
# Output: Valid: False, Error: HIPAA violation: PHI detected in SMS: diabetes
```

### Issue 4: Pass rate too high/low
**Solution:** Adjust task difficulty
- Too high: Add edge cases, stricter evaluators
- Too low: Simplify tasks, improve agent prompt

---

## Best Practices

### 1. FHIR Resource Generation
```python
# ✅ GOOD: Use structured FHIR resources
patient = {
    "resourceType": "Patient",
    "identifier": [{"value": "MRN-12345"}],
    "name": [{"family": "Doe", "given": ["John"]}]
}

# ❌ BAD: Unstructured data
patient = {
    "name": "John Doe",
    "mrn": "12345"
}
```

### 2. HIPAA Compliance
```python
# ✅ GOOD: Generic SMS
"Your appointment is tomorrow at 2pm"

# ❌ BAD: PHI in SMS
"Your diabetes appointment is tomorrow"
```

### 3. Safety-Critical Triage
```python
# ✅ GOOD: Immediate escalation for chest pain
if 'chest pain' in chief_complaint:
    return {'triage_category': 'EMERGENT', 'action': 'call_911'}

# ❌ BAD: Scheduled appointment for chest pain
if 'chest pain' in chief_complaint:
    return {'triage_category': 'URGENT', 'action': 'schedule_same_day'}
```

---

## Next Steps
- See `08-api-contracts.md` for API specifications
- See `09-deployment.md` for production deployment

