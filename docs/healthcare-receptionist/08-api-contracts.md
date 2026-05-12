# Healthcare Receptionist - API Contracts

## Overview

API specifications for all Healthcare Receptionist domain operations. Includes:
- Request/response formats
- Error handling
- FHIR resource schemas
- MCP server contracts
- Rate limiting

---

## Core API Endpoints

### 1. Patient Intake API

#### POST /api/v1/patient/intake
**Description:** Create new patient and schedule first appointment

**Request:**
```json
{
  "patient_data": {
    "name": {
      "family": "Doe",
      "given": ["John", "Robert"]
    },
    "birthDate": "1985-03-15",
    "gender": "male",
    "telecom": [
      {"system": "phone", "value": "555-1234", "use": "mobile"},
      {"system": "email", "value": "john.doe@email.com"}
    ],
    "address": {
      "line": ["123 Main St", "Apt 4B"],
      "city": "Boston",
      "state": "MA",
      "postalCode": "02101"
    }
  },
  "insurance": {
    "carrier": "Blue Cross Blue Shield",
    "member_id": "ABC123456",
    "group": "GRP999"
  },
  "chief_complaint": "Annual physical",
  "requested_provider": "Dr. Smith",
  "preferred_date": "2025-11-10"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "patient": {
    "resourceType": "Patient",
    "id": "pt-12345",
    "identifier": [
      {"system": "http://clinic.com/mrn", "value": "MRN-12345"}
    ],
    "name": [{"family": "Doe", "given": ["John", "Robert"]}],
    "birthDate": "1985-03-15",
    "gender": "male",
    "telecom": [
      {"system": "phone", "value": "555-1234", "use": "mobile"}
    ]
  },
  "appointment": {
    "resourceType": "Appointment",
    "id": "appt-67890",
    "status": "booked",
    "start": "2025-11-10T14:00:00-05:00",
    "end": "2025-11-10T14:30:00-05:00",
    "participant": [
      {"actor": {"reference": "Patient/pt-12345"}},
      {"actor": {"reference": "Practitioner/dr-smith"}}
    ]
  },
  "intake_form": {
    "url": "https://storage.clinic.com/intake/pt-12345.pdf",
    "sent_via_email": true
  }
}
```

**Error Responses:**
```json
// 400 Bad Request - Missing required fields
{
  "status": "error",
  "code": "MISSING_REQUIRED_FIELD",
  "message": "Missing required field: birthDate",
  "details": {
    "field": "birthDate",
    "required_fields": ["name", "birthDate", "telecom"]
  }
}

// 409 Conflict - Duplicate patient detected
{
  "status": "error",
  "code": "DUPLICATE_PATIENT",
  "message": "Patient with same name and DOB already exists",
  "details": {
    "existing_patient_id": "pt-99999",
    "match_confidence": 0.95
  }
}

// 422 Unprocessable Entity - FHIR validation failed
{
  "status": "error",
  "code": "FHIR_VALIDATION_ERROR",
  "message": "Invalid FHIR Patient resource",
  "details": {
    "errors": [
      "birthDate must be in YYYY-MM-DD format",
      "telecom[0].system must be 'phone', 'email', or 'fax'"
    ]
  }
}
```

---

### 2. Appointment Scheduling API

#### POST /api/v1/appointment/schedule
**Description:** Schedule appointment with provider

**Request:**
```json
{
  "patient_id": "pt-12345",
  "provider": "Dr. Smith",
  "appointment_type": "follow-up",
  "preferred_date": "2025-11-10",
  "preferred_time": "14:00",
  "duration_minutes": 30,
  "reason": "Cardiology follow-up",
  "insurance_check": true
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "appointment": {
    "resourceType": "Appointment",
    "id": "appt-67890",
    "status": "booked",
    "serviceType": [
      {"coding": [{"code": "57", "display": "Cardiology"}]}
    ],
    "start": "2025-11-10T14:00:00-05:00",
    "end": "2025-11-10T14:30:00-05:00",
    "participant": [
      {"actor": {"reference": "Patient/pt-12345"}},
      {"actor": {"reference": "Practitioner/dr-smith"}},
      {"actor": {"reference": "Location/cardiology-clinic-302"}}
    ]
  },
  "confirmation": {
    "email_sent": true,
    "sms_sent": true,
    "reminder_scheduled": "2025-11-09T14:00:00-05:00"
  },
  "insurance_status": {
    "authorization_required": false,
    "estimated_copay": 50.00
  }
}
```

**Error Responses:**
```json
// 404 Not Found - Provider not available
{
  "status": "error",
  "code": "PROVIDER_UNAVAILABLE",
  "message": "Dr. Smith has no availability on 2025-11-10",
  "details": {
    "next_available_slots": [
      "2025-11-12T09:00:00-05:00",
      "2025-11-12T14:00:00-05:00"
    ]
  }
}

// 402 Payment Required - Prior authorization needed
{
  "status": "pending_authorization",
  "code": "PRIOR_AUTH_REQUIRED",
  "message": "Procedure requires prior authorization",
  "details": {
    "procedure_code": "CPT-70553",
    "authorization_task_id": "task-auth-123",
    "estimated_turnaround": "3 business days"
  }
}
```

---

### 3. Insurance Verification API

#### POST /api/v1/insurance/verify
**Description:** Verify insurance eligibility and benefits

**Request:**
```json
{
  "patient_id": "pt-12345",
  "insurance": {
    "carrier": "Blue Cross Blue Shield",
    "member_id": "ABC123456",
    "group": "GRP999"
  },
  "service_date": "2025-11-10",
  "procedure_code": "CPT-99214"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "coverage": {
    "resourceType": "Coverage",
    "id": "cov-12345",
    "status": "active",
    "subscriber": {"reference": "Patient/pt-12345"},
    "payor": [{"display": "Blue Cross Blue Shield"}],
    "period": {
      "start": "2025-01-01",
      "end": "2025-12-31"
    }
  },
  "eligibility": {
    "eligible": true,
    "coverage_active": true,
    "in_network": true
  },
  "benefits": {
    "deductible": {
      "total": 2000.00,
      "met": 500.00,
      "remaining": 1500.00
    },
    "out_of_pocket_max": {
      "total": 6000.00,
      "met": 1200.00,
      "remaining": 4800.00
    },
    "copay": {
      "office_visit": 50.00,
      "specialist": 75.00,
      "emergency_room": 250.00
    },
    "coinsurance": 0.20
  },
  "prior_authorization": {
    "required": false,
    "procedure_code": "CPT-99214"
  }
}
```

**Error Responses:**
```json
// 403 Forbidden - Coverage inactive
{
  "status": "error",
  "code": "COVERAGE_INACTIVE",
  "message": "Insurance coverage is not active on service date",
  "details": {
    "coverage_end_date": "2024-12-31",
    "service_date": "2025-11-10"
  }
}
```

---

### 4. Clinical Triage API

#### POST /api/v1/triage/assess
**Description:** Assess urgency and route patient (SAFETY-CRITICAL)

**Request:**
```json
{
  "patient_id": "pt-12345",
  "chief_complaint": "Chest pain",
  "symptoms": [
    "radiating to left arm",
    "shortness of breath",
    "diaphoresis"
  ],
  "onset": "2 hours ago",
  "severity": 8,
  "medical_history": ["hypertension", "smoker"]
}
```

**Response (200 OK - EMERGENT):**
```json
{
  "status": "success",
  "triage": {
    "resourceType": "Observation",
    "id": "obs-triage-123",
    "status": "final",
    "code": {
      "coding": [{"code": "29308-4", "display": "Chief Complaint"}]
    },
    "valueString": "Chest pain x 2 hours, worsening",
    "interpretation": [
      {"coding": [{"code": "H", "display": "High (emergent)"}]}
    ]
  },
  "assessment": {
    "triage_category": "EMERGENT",
    "urgency_level": "CRITICAL",
    "recommended_action": "call_911",
    "icd10_code": "R07.9"
  },
  "instructions": {
    "patient_message": "Call 911 immediately for chest pain evaluation. Do not drive yourself to the hospital.",
    "clinical_task_created": true,
    "task_id": "task-urgent-456"
  }
}
```

**Response (200 OK - ROUTINE):**
```json
{
  "status": "success",
  "triage": {
    "resourceType": "Observation",
    "id": "obs-triage-789",
    "valueString": "Cough x 3 days, no fever"
  },
  "assessment": {
    "triage_category": "ROUTINE",
    "urgency_level": "LOW",
    "recommended_action": "schedule_appointment",
    "icd10_code": "R05"
  },
  "instructions": {
    "patient_message": "Schedule a routine appointment with your provider",
    "telehealth_eligible": true
  }
}
```

**Error Responses:**
```json
// 500 Internal Server Error - Safety-critical failure
{
  "status": "error",
  "code": "TRIAGE_SAFETY_FAILURE",
  "message": "CRITICAL: Chest pain not identified as emergent",
  "details": {
    "actual_triage": "ROUTINE",
    "expected_triage": "EMERGENT",
    "action_taken": "Escalated to human triage nurse"
  }
}
```

---

### 5. Multi-Channel Orchestration API

#### POST /api/v1/orchestration/post-discharge
**Description:** Complete post-discharge workflow

**Request:**
```json
{
  "patient_id": "pt-12345",
  "discharge_date": "2025-11-03",
  "discharge_diagnosis": "CHF exacerbation",
  "follow_up_specialty": "cardiology",
  "follow_up_in_days": 7,
  "medications": [
    "Furosemide 40mg daily",
    "Metoprolol 25mg BID"
  ],
  "warning_signs": "Call if weight increases >3lbs in 24h or SOB worsens",
  "care_plan_activities": [
    "Cardiology follow-up",
    "Daily weight monitoring",
    "Medication adherence"
  ]
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "workflow_steps": {
    "step_1_appointment": {
      "completed": true,
      "appointment": {
        "resourceType": "Appointment",
        "id": "appt-follow-up-123",
        "start": "2025-11-10T09:00:00-05:00",
        "participant": [
          {"actor": {"reference": "Patient/pt-12345"}},
          {"actor": {"reference": "Practitioner/dr-jones-cardiology"}}
        ]
      }
    },
    "step_2_discharge_summary": {
      "completed": true,
      "document": {
        "resourceType": "DocumentReference",
        "id": "doc-discharge-123",
        "content": [{
          "attachment": {
            "url": "https://storage.clinic.com/discharge/pt-12345-20251103.pdf"
          }
        }]
      }
    },
    "step_3_email_sent": {
      "completed": true,
      "hipaa_compliant": true,
      "encrypted": true
    },
    "step_4_medication_reminders": {
      "completed": true,
      "reminders_scheduled": [
        {"medication": "Furosemide", "time": "2025-11-04T08:00:00-05:00"},
        {"medication": "Metoprolol", "time": "2025-11-04T08:00:00-05:00"}
      ]
    },
    "step_5_nurse_task": {
      "completed": true,
      "task": {
        "resourceType": "Task",
        "id": "task-check-in-456",
        "status": "requested",
        "description": "Post-discharge check-in call",
        "for": {"reference": "Patient/pt-12345"},
        "owner": {"display": "Nurse Coordinator"},
        "restriction": {"period": {"end": "2025-11-06"}}
      }
    },
    "step_6_care_plan": {
      "completed": true,
      "care_plan": {
        "resourceType": "CarePlan",
        "id": "cp-discharge-123",
        "status": "active",
        "title": "CHF Post-Discharge Care Plan",
        "subject": {"reference": "Patient/pt-12345"},
        "period": {
          "start": "2025-11-03",
          "end": "2025-12-03"
        },
        "activity": [
          {"detail": {"code": {"text": "Cardiology follow-up"}}},
          {"detail": {"code": {"text": "Daily weight monitoring"}}},
          {"detail": {"code": {"text": "Medication adherence"}}}
        ]
      }
    }
  },
  "workflow_complete": true,
  "all_steps_passed": true
}
```

**Error Responses:**
```json
// 206 Partial Content - Workflow partially completed
{
  "status": "partial_success",
  "code": "WORKFLOW_INCOMPLETE",
  "message": "Some workflow steps failed",
  "workflow_steps": {
    "step_1_appointment": {"completed": true},
    "step_2_discharge_summary": {"completed": true},
    "step_3_email_sent": {"completed": false, "error": "SMTP timeout"},
    "step_4_medication_reminders": {"completed": true},
    "step_5_nurse_task": {"completed": true},
    "step_6_care_plan": {"completed": true}
  },
  "failed_steps": ["step_3_email_sent"],
  "retry_recommended": true
}
```

---

## Error Code Reference

### Client Errors (4xx)

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `MISSING_REQUIRED_FIELD` | 400 | Required field missing in request |
| `INVALID_FORMAT` | 400 | Field format invalid (e.g., date, phone) |
| `UNAUTHORIZED` | 401 | Missing or invalid API key |
| `FORBIDDEN` | 403 | User lacks permission for operation |
| `PATIENT_NOT_FOUND` | 404 | Patient ID not found |
| `PROVIDER_NOT_FOUND` | 404 | Provider not found |
| `PROVIDER_UNAVAILABLE` | 404 | Provider has no availability |
| `DUPLICATE_PATIENT` | 409 | Patient already exists |
| `FHIR_VALIDATION_ERROR` | 422 | FHIR resource schema validation failed |
| `HIPAA_VIOLATION` | 422 | PHI detected in SMS/email |

### Server Errors (5xx)

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `MCP_SERVER_TIMEOUT` | 503 | MCP server timed out |
| `TRIAGE_SAFETY_FAILURE` | 500 | Safety-critical triage error |

---

## Rate Limiting

**Rate Limits:**
- **Patient Intake:** 10 requests/minute per IP
- **Appointment Scheduling:** 20 requests/minute per IP
- **Insurance Verification:** 30 requests/minute per IP
- **Clinical Triage:** 50 requests/minute per IP (safety-critical, higher limit)

**Rate Limit Headers:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1730736000
```

**Rate Limit Exceeded (429):**
```json
{
  "status": "error",
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests",
  "details": {
    "limit": 10,
    "reset_at": "2025-11-03T14:05:00Z"
  }
}
```

---

## Authentication

**API Key Authentication:**
```bash
curl -X POST https://api.clinic.com/v1/patient/intake \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @request.json
```

**OAuth 2.0 (for production):**
```bash
# Get access token
curl -X POST https://api.clinic.com/oauth/token \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"

# Use access token
curl -X POST https://api.clinic.com/v1/patient/intake \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d @request.json
```

---

## Webhook Events

**POST /api/v1/webhooks**

**Events:**
- `patient.created`
- `appointment.scheduled`
- `appointment.cancelled`
- `authorization.approved`
- `authorization.denied`
- `triage.emergent`

**Example Webhook Payload:**
```json
{
  "event": "triage.emergent",
  "timestamp": "2025-11-03T14:30:00Z",
  "data": {
    "patient_id": "pt-12345",
    "triage_category": "EMERGENT",
    "chief_complaint": "Chest pain",
    "action_taken": "911_advised"
  }
}
```

---

## Next Steps
- See `09-deployment.md` for production deployment
- See `06-hipaa-compliance.md` for security details


