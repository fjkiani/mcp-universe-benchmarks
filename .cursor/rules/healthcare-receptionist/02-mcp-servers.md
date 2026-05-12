# Healthcare Receptionist - MCP Server Integrations

## Overview

All 7 MCP servers used are **existing** - no new servers required. Complexity comes from healthcare-specific usage patterns.

```
healthcare-receptionist/
├── calendar          → Appointment scheduling, provider availability
├── email             → HIPAA-compliant confirmations, summaries
├── sms-messaging     → Appointment reminders, test alerts
├── task-management   → Care coordination, follow-ups
├── google-search     → Pharmacy/clinic/insurance lookup
├── pdf-generator     → Consent forms, discharge summaries
└── date              → Age calculation, appointment logic
```

## Server Integrations

### 1. Calendar Server
**Purpose:** Appointment scheduling, provider availability checks

**Healthcare-Specific Usage:**
- Provider availability with specialties
- Block scheduling (e.g., surgery blocks)
- Recurring appointments (PT series, dialysis)
- Wait-list management
- Multi-location clinic support

**Tool Calls:**
```python
# Check provider availability
await calendar.get_availability({
    'provider': 'Dr. Smith',
    'specialty': 'cardiology',
    'start_date': '2025-11-10',
    'end_date': '2025-11-24',
    'duration': 30  # minutes
})

# Create appointment
await calendar.create_event({
    'title': 'Follow-up: CHF Management',
    'start': '2025-11-10T14:00:00',
    'end': '2025-11-10T14:30:00',
    'attendees': ['Dr. Smith', 'patient@email.com'],
    'location': 'Cardiology Clinic, Room 302',
    'description': 'Post-discharge follow-up for CHF exacerbation'
})

# Reschedule with conflict check
await calendar.update_event({
    'event_id': 'evt_123',
    'new_start': '2025-11-12T10:00:00',
    'check_conflicts': True
})
```

**FHIR Mapping:**
```python
def calendar_event_to_fhir_appointment(event: dict) -> dict:
    return {
        "resourceType": "Appointment",
        "status": "booked",
        "serviceType": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/service-type",
                "code": "57",
                "display": "Cardiology"
            }]
        }],
        "start": event['start'],
        "end": event['end'],
        "participant": [
            {"actor": {"reference": f"Practitioner/{event['provider_id']}"}},
            {"actor": {"reference": f"Patient/{event['patient_id']}"}}
        ]
    }
```

---

### 2. Email Server
**Purpose:** HIPAA-compliant patient communication

**Healthcare-Specific Usage:**
- Appointment confirmations
- Discharge summaries
- Lab result notifications (with portal link, not actual results)
- Consent forms
- Billing statements

**Tool Calls:**
```python
# Send appointment confirmation
await email.send_message({
    'to': 'patient@email.com',
    'subject': 'Appointment Confirmed - [Clinic Name]',
    'body': '''
        Your appointment is confirmed:
        
        Date: November 10, 2025
        Time: 2:00 PM
        Provider: Dr. Smith
        Location: Cardiology Clinic, Room 302
        
        Please arrive 15 minutes early to complete check-in.
        
        [HIPAA-compliant footer]
    ''',
    'attachments': ['intake_form.pdf']
})

# HIPAA-compliant lab notification
await email.send_message({
    'to': 'patient@email.com',
    'subject': 'Lab Results Available',
    'body': '''
        Your lab results are now available in the patient portal.
        
        Please log in to view your results:
        https://portal.clinic.com/login
        
        [NO PHI IN EMAIL - results only in portal]
    '''
})
```

**HIPAA Validation:**
```python
class HIPAAEmailValidator:
    DISALLOWED_TERMS = [
        'diagnosis', 'HIV', 'positive', 'negative', 'cancer',
        'mg/dL', 'abnormal', 'high', 'low', 'medication'
    ]
    
    def validate(self, subject: str, body: str) -> bool:
        """Ensure no PHI in email subject/body"""
        combined = (subject + ' ' + body).lower()
        for term in self.DISALLOWED_TERMS:
            if term in combined:
                raise HIPAAViolationError(
                    f"PHI detected: '{term}' found in email"
                )
        return True
```

---

### 3. SMS Messaging Server
**Purpose:** Appointment reminders, urgent alerts

**Healthcare-Specific Usage:**
- 24-hour appointment reminders
- Test result ready notifications
- Medication reminders
- Urgent clinic closures/delays

**Tool Calls:**
```python
# Send appointment reminder
await sms_messaging.send_sms({
    'to': '+15551234567',
    'message': 'Reminder: You have an appointment tomorrow at 2:00 PM with Dr. Smith. Reply CONFIRM or call 555-0100.'
})

# Send test result notification
await sms_messaging.send_sms({
    'to': '+15551234567',
    'message': 'Your lab results are ready. Log in to the patient portal to view: https://portal.clinic.com'
})
```

**HIPAA-Compliant SMS Templates:**
```python
SMS_TEMPLATES = {
    'appointment_reminder': 'Reminder: You have an appointment {date} at {time}. Reply CONFIRM or call {clinic_phone}.',
    
    'test_result_ready': 'Your test results are ready. Log in to the patient portal to view: {portal_url}',
    
    'medication_reminder': 'Reminder: Time to take your medication. Questions? Call {clinic_phone}.',
    
    # ✅ GOOD - no PHI
    # ❌ BAD: 'Your cholesterol is 250' - contains lab value
    # ❌ BAD: 'Diabetes appointment tomorrow' - contains diagnosis
}
```

---

### 4. Task Management Server
**Purpose:** Care coordination, follow-ups

**Healthcare-Specific Usage:**
- Prior authorization requests
- Nurse follow-up calls
- Referral coordination
- Lab result reviews
- Discharge planning

**Tool Calls:**
```python
# Create prior authorization task
await task_management.create_task({
    'title': 'Prior Auth: MRI Brain (CPT 70553)',
    'description': 'Patient: John Doe (MRN-12345)\nInsurance: Blue Cross\nProcedure: MRI brain with contrast\nDue: 3 business days',
    'assigned_to': 'authorization_team',
    'priority': 'high',
    'due_date': '2025-11-06',
    'tags': ['prior_auth', 'imaging', 'urgent']
})

# Create post-discharge follow-up
await task_management.create_task({
    'title': 'Check-in Call: CHF Patient',
    'description': 'Patient: John Doe (MRN-12345)\nDischarge: 11/3/25\nCall on day 3 to check weight, SOB, med compliance',
    'assigned_to': 'nurse_coordinator',
    'due_date': '2025-11-06',
    'tags': ['post_discharge', 'cardiology', 'high_risk']
})
```

**FHIR Mapping:**
```python
def task_to_fhir_task(task: dict) -> dict:
    return {
        "resourceType": "Task",
        "status": "requested",
        "intent": "order",
        "priority": "urgent" if task['priority'] == 'high' else "routine",
        "description": task['description'],
        "for": {"reference": f"Patient/{task['patient_id']}"},
        "authoredOn": datetime.now().isoformat(),
        "restriction": {
            "period": {"end": task['due_date']}
        }
    }
```

---

### 5. Google Search Server
**Purpose:** Look up external resources

**Healthcare-Specific Usage:**
- Find pharmacies near patient address
- Look up clinic hours/phone numbers
- Find insurance provider networks
- Verify provider credentials

**Tool Calls:**
```python
# Find nearby pharmacies
await google_search.search({
    'query': 'CVS pharmacy near 123 Main St, Boston MA',
    'num_results': 5
})

# Look up insurance network
await google_search.search({
    'query': 'Blue Cross providers in network cardiology Boston',
    'num_results': 10
})

# Verify provider credentials
await google_search.search({
    'query': 'Dr. John Smith cardiology Massachusetts medical license',
    'num_results': 3
})
```

---

### 6. PDF Generator Server
**Purpose:** Generate healthcare documents

**Healthcare-Specific Usage:**
- Patient intake forms
- Consent forms (HIPAA, treatment)
- Discharge summaries
- Care instructions
- Billing statements

**Tool Calls:**
```python
# Generate patient intake form
await pdf_generator.create_pdf({
    'template': 'patient_intake_form',
    'data': {
        'patient_name': 'John Doe',
        'dob': '1985-03-15',
        'insurance': 'Blue Cross',
        'emergency_contact': 'Jane Doe - 555-0200'
    },
    'output_filename': 'intake_form_john_doe.pdf'
})

# Generate discharge summary
await pdf_generator.create_pdf({
    'template': 'discharge_summary',
    'data': {
        'patient_name': 'John Doe',
        'discharge_date': '2025-11-03',
        'diagnosis': 'CHF exacerbation',
        'medications': [
            'Furosemide 40mg daily',
            'Metoprolol 25mg BID'
        ],
        'follow_up': 'Cardiology in 7 days',
        'warning_signs': 'Weight gain >3lbs, increased SOB'
    },
    'output_filename': 'discharge_summary.pdf'
})
```

**FHIR Mapping:**
```python
def pdf_to_fhir_document_reference(pdf: dict) -> dict:
    return {
        "resourceType": "DocumentReference",
        "status": "current",
        "type": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "18842-5",
                "display": "Discharge Summary"
            }]
        },
        "subject": {"reference": f"Patient/{pdf['patient_id']}"},
        "date": datetime.now().isoformat(),
        "content": [{
            "attachment": {
                "contentType": "application/pdf",
                "url": pdf['output_filename']
            }
        }]
    }
```

---

### 7. Date Server
**Purpose:** Date/time calculations

**Healthcare-Specific Usage:**
- Calculate patient age from DOB
- Check if appointment is within authorization window
- Calculate follow-up dates (e.g., 7 days post-discharge)
- Validate date ranges for recurring appointments

**Tool Calls:**
```python
# Calculate age
await date.calculate_age({
    'birth_date': '1985-03-15',
    'as_of_date': '2025-11-03'
})
# Returns: 40 years

# Add business days (for authorization deadlines)
await date.add_business_days({
    'start_date': '2025-11-03',
    'days': 3
})
# Returns: '2025-11-06' (skips weekend)

# Check if within window
await date.is_within_range({
    'date': '2025-11-10',
    'start': '2025-11-03',
    'end': '2025-11-10'
})
# Returns: True (within 7-day follow-up window)
```

---

## Integration Patterns

### Pattern 1: Multi-Server Workflows
**Example:** New patient intake

```python
async def new_patient_intake(patient_data: dict) -> dict:
    # 1. Calculate age (date server)
    age = await date.calculate_age({
        'birth_date': patient_data['dob']
    })
    
    # 2. Check provider availability (calendar)
    slots = await calendar.get_availability({
        'provider': patient_data['requested_provider'],
        'days_ahead': 14
    })
    
    # 3. Create appointment (calendar)
    appointment = await calendar.create_event({
        'title': f'New Patient Visit - {patient_data["name"]}',
        'start': slots[0]['start']
    })
    
    # 4. Generate intake form (pdf-generator)
    pdf = await pdf_generator.create_pdf({
        'template': 'patient_intake',
        'data': patient_data
    })
    
    # 5. Send confirmation (email)
    await email.send_message({
        'to': patient_data['email'],
        'subject': 'Appointment Confirmed',
        'attachments': [pdf['filename']]
    })
    
    # 6. Create welcome task (task-management)
    await task_management.create_task({
        'title': f'Welcome call: {patient_data["name"]}',
        'assigned_to': 'front_desk'
    })
    
    return {
        'patient_id': patient_data['mrn'],
        'appointment': appointment,
        'intake_form_sent': True
    }
```

### Pattern 2: HIPAA-Compliant Notifications
**Example:** Lab result notification

```python
async def notify_lab_results_ready(patient: dict) -> dict:
    # ✅ CORRECT: No PHI in notification
    
    # 1. Email with portal link (no results in email)
    await email.send_message({
        'to': patient['email'],
        'subject': 'Lab Results Available',
        'body': 'Your lab results are ready. Log in to view: https://portal.clinic.com'
    })
    
    # 2. SMS alert (no results in SMS)
    await sms_messaging.send_sms({
        'to': patient['phone'],
        'message': 'Your lab results are ready in the patient portal'
    })
    
    # 3. Task for provider review
    await task_management.create_task({
        'title': f'Review labs: {patient["name"]}',
        'assigned_to': patient['primary_provider'],
        'priority': 'normal'
    })
    
    # ❌ WRONG: Would violate HIPAA
    # await sms_messaging.send_sms({
    #     'message': 'Your cholesterol is 250 mg/dL'  # PHI!
    # })
```

### Pattern 3: Authorization Workflows
**Example:** Prior authorization check

```python
async def check_prior_authorization(patient_id: str, 
                                    procedure_code: str) -> dict:
    # 1. Get patient insurance (FHIR store)
    coverage = fhir_store.get_coverage(patient_id)
    
    # 2. Check if requires auth
    requires_auth = insurance_service.check_prior_auth(
        procedure_code, coverage['payor']
    )
    
    if requires_auth:
        # 3. Create auth task (task-management)
        task = await task_management.create_task({
            'title': f'Prior Auth: {procedure_code}',
            'assigned_to': 'authorization_team',
            'due_date': await date.add_business_days({
                'start_date': 'today',
                'days': 3
            })
        })
        
        # 4. Notify patient (email)
        await email.send_message({
            'to': patient['email'],
            'subject': 'Authorization Required',
            'body': 'Your insurance requires authorization. We will submit and call you within 3 business days.'
        })
        
        return {
            'requires_authorization': True,
            'task_id': task['id'],
            'estimated_turnaround': '3 business days'
        }
    
    return {'requires_authorization': False}
```

## Testing MCP Integrations

### Unit Tests
```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_new_patient_intake():
    # Mock MCP servers
    calendar = AsyncMock()
    calendar.get_availability.return_value = [{
        'start': '2025-11-10T14:00:00',
        'end': '2025-11-10T15:00:00'
    }]
    
    email = AsyncMock()
    pdf = AsyncMock()
    pdf.create_pdf.return_value = {'filename': 'intake.pdf'}
    
    # Test workflow
    service = PatientIntakeService(calendar, email, pdf)
    result = await service.new_patient_intake({
        'name': 'John Doe',
        'dob': '1985-03-15',
        'email': 'john@email.com'
    })
    
    # Assertions
    assert result['intake_form_sent'] is True
    calendar.create_event.assert_called_once()
    email.send_message.assert_called_once()
```

## Error Handling

### MCP Server Failures
```python
class MCPServerErrorHandler:
    async def call_with_retry(self, server_call, max_retries=3):
        for attempt in range(max_retries):
            try:
                return await server_call()
            except MCPServerTimeout:
                if attempt == max_retries - 1:
                    # Fallback: create manual task
                    await self.create_fallback_task(server_call)
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Next Steps
- See `03-fhir-schemas.md` for FHIR resource definitions
- See `05-evaluators.md` for evaluation logic
- See `07-implementation-guide.md` for build instructions

