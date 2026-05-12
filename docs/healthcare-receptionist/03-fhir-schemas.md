# Healthcare Receptionist - FHIR R4 Schemas

## Overview

All patient data structured as **FHIR R4 resources**. This ensures:
- Interoperability with EMR systems (Epic, Cerner, Athena)
- Standards compliance
- Structured validation
- Future-proof data model

## FHIR Resources Used

```
Patient          → Demographics, insurance, contacts
Appointment      → Scheduled visits, provider info
Coverage         → Insurance eligibility, benefits
Observation      → Clinical notes (triage, vitals)
CarePlan         → Treatment plans, discharge instructions
Task             → Follow-ups, authorizations, coordination
DocumentReference → PDFs (intake forms, discharge summaries)
```

---

## 1. Patient Resource

**Purpose:** Core demographics, insurance, contacts

### Schema
```json
{
  "resourceType": "Patient",
  "id": "pt-12345",
  "identifier": [
    {
      "system": "http://clinic.com/mrn",
      "value": "MRN-12345"
    }
  ],
  "active": true,
  "name": [
    {
      "use": "official",
      "family": "Doe",
      "given": ["John", "Robert"]
    }
  ],
  "telecom": [
    {
      "system": "phone",
      "value": "555-1234",
      "use": "mobile"
    },
    {
      "system": "email",
      "value": "john.doe@email.com"
    }
  ],
  "gender": "male",
  "birthDate": "1985-03-15",
  "address": [
    {
      "use": "home",
      "line": ["123 Main St", "Apt 4B"],
      "city": "Boston",
      "state": "MA",
      "postalCode": "02101"
    }
  ],
  "contact": [
    {
      "relationship": [{
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
          "code": "C",
          "display": "Emergency Contact"
        }]
      }],
      "name": {
        "family": "Doe",
        "given": ["Jane"]
      },
      "telecom": [{
        "system": "phone",
        "value": "555-5678"
      }]
    }
  ]
}
```

### Python Model
```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class HumanName(BaseModel):
    use: str = "official"
    family: str
    given: List[str]

class ContactPoint(BaseModel):
    system: str  # "phone" | "email" | "fax"
    value: str
    use: Optional[str] = None  # "home" | "work" | "mobile"

class Address(BaseModel):
    use: str = "home"
    line: List[str]
    city: str
    state: str
    postalCode: str

class PatientContact(BaseModel):
    relationship: List[dict]
    name: HumanName
    telecom: List[ContactPoint]

class Patient(BaseModel):
    resourceType: str = Field(default="Patient", const=True)
    id: Optional[str] = None
    identifier: List[dict]
    active: bool = True
    name: List[HumanName]
    telecom: List[ContactPoint]
    gender: str  # "male" | "female" | "other" | "unknown"
    birthDate: date
    address: List[Address]
    contact: Optional[List[PatientContact]] = None
```

### Validation
```python
def validate_patient(data: dict) -> bool:
    # Required fields
    required = ['resourceType', 'identifier', 'name', 'birthDate']
    if not all(k in data for k in required):
        return False
    
    # Must have at least one contact method
    if not data.get('telecom'):
        return False
    
    # Age must be realistic (0-120 years)
    age = calculate_age(data['birthDate'])
    if age < 0 or age > 120:
        return False
    
    return True
```

---

## 2. Appointment Resource

**Purpose:** Scheduled visits, provider info, status tracking

### Schema
```json
{
  "resourceType": "Appointment",
  "id": "appt-67890",
  "status": "booked",
  "serviceCategory": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/service-category",
      "code": "17",
      "display": "General Practice"
    }]
  }],
  "serviceType": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/service-type",
      "code": "57",
      "display": "Cardiology"
    }]
  }],
  "appointmentType": {
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/v2-0276",
      "code": "FOLLOWUP",
      "display": "Follow-up"
    }]
  },
  "reasonReference": [{
    "reference": "Observation/obs-123",
    "display": "CHF Management"
  }],
  "start": "2025-11-10T14:00:00-05:00",
  "end": "2025-11-10T14:30:00-05:00",
  "minutesDuration": 30,
  "participant": [
    {
      "actor": {
        "reference": "Patient/pt-12345",
        "display": "John Doe"
      },
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "Practitioner/dr-smith",
        "display": "Dr. John Smith, MD"
      },
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "Location/cardiology-clinic-302",
        "display": "Cardiology Clinic, Room 302"
      },
      "status": "accepted"
    }
  ]
}
```

### Python Model
```python
from datetime import datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    PROPOSED = "proposed"
    PENDING = "pending"
    BOOKED = "booked"
    ARRIVED = "arrived"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    NOSHOW = "noshow"

class Appointment(BaseModel):
    resourceType: str = Field(default="Appointment", const=True)
    id: Optional[str] = None
    status: AppointmentStatus
    serviceType: List[dict]
    start: datetime
    end: datetime
    minutesDuration: int
    participant: List[dict]
    reasonReference: Optional[List[dict]] = None
```

---

## 3. Coverage Resource

**Purpose:** Insurance eligibility, benefits, authorization

### Schema
```json
{
  "resourceType": "Coverage",
  "id": "cov-12345",
  "status": "active",
  "subscriber": {
    "reference": "Patient/pt-12345"
  },
  "subscriberId": "ABC123456",
  "beneficiary": {
    "reference": "Patient/pt-12345"
  },
  "relationship": {
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship",
      "code": "self"
    }]
  },
  "period": {
    "start": "2025-01-01",
    "end": "2025-12-31"
  },
  "payor": [{
    "display": "Blue Cross Blue Shield"
  }],
  "class": [
    {
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/coverage-class",
          "code": "group"
        }]
      },
      "value": "GRP999",
      "name": "Corporate Plan"
    }
  ],
  "costToBeneficiary": [
    {
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/coverage-copay-type",
          "code": "copay"
        }]
      },
      "valueMoney": {
        "value": 50,
        "currency": "USD"
      }
    }
  ]
}
```

### Python Model
```python
class Coverage(BaseModel):
    resourceType: str = Field(default="Coverage", const=True)
    id: Optional[str] = None
    status: str  # "active" | "cancelled" | "draft" | "entered-in-error"
    subscriber: dict
    subscriberId: str  # Member ID
    beneficiary: dict  # Patient reference
    relationship: dict  # self | spouse | child | parent
    period: dict  # start/end dates
    payor: List[dict]  # Insurance company
    class_: List[dict] = Field(alias="class")  # Group, plan info
    costToBeneficiary: Optional[List[dict]] = None  # Copay, deductible
```

### Business Logic
```python
class CoverageService:
    def check_eligibility(self, coverage: Coverage, 
                         service_date: date) -> dict:
        """Check if coverage is active on service date"""
        period = coverage.period
        start = datetime.fromisoformat(period['start']).date()
        end = datetime.fromisoformat(period['end']).date()
        
        if not (start <= service_date <= end):
            return {
                'eligible': False,
                'reason': 'Coverage not active on service date'
            }
        
        return {
            'eligible': True,
            'payor': coverage.payor[0]['display'],
            'copay': self.extract_copay(coverage)
        }
    
    def extract_copay(self, coverage: Coverage) -> float:
        """Extract copay amount from coverage"""
        for cost in coverage.costToBeneficiary or []:
            if cost['type']['coding'][0]['code'] == 'copay':
                return cost['valueMoney']['value']
        return 0.0
```

---

## 4. Observation Resource

**Purpose:** Clinical notes, triage, chief complaint

### Schema
```json
{
  "resourceType": "Observation",
  "id": "obs-triage-123",
  "status": "final",
  "category": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/observation-category",
      "code": "exam",
      "display": "Exam"
    }]
  }],
  "code": {
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "29308-4",
      "display": "Chief Complaint"
    }]
  },
  "subject": {
    "reference": "Patient/pt-12345"
  },
  "effectiveDateTime": "2025-11-03T10:30:00-05:00",
  "valueString": "Chest pain x 2 hours, worsening",
  "interpretation": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
      "code": "H",
      "display": "High (emergent)"
    }]
  }],
  "note": [{
    "text": "Patient reports radiating pain to left arm, shortness of breath. IMMEDIATE ESCALATION to ER."
  }]
}
```

### Python Model
```python
class Observation(BaseModel):
    resourceType: str = Field(default="Observation", const=True)
    id: Optional[str] = None
    status: str  # "registered" | "preliminary" | "final"
    category: List[dict]
    code: dict  # LOINC/SNOMED code
    subject: dict  # Patient reference
    effectiveDateTime: datetime
    valueString: Optional[str] = None
    interpretation: Optional[List[dict]] = None  # Normal/High/Low
    note: Optional[List[dict]] = None
```

---

## 5. CarePlan Resource

**Purpose:** Treatment plans, discharge instructions

### Schema
```json
{
  "resourceType": "CarePlan",
  "id": "cp-discharge-123",
  "status": "active",
  "intent": "plan",
  "title": "CHF Post-Discharge Care Plan",
  "description": "Follow-up care after CHF exacerbation hospitalization",
  "subject": {
    "reference": "Patient/pt-12345"
  },
  "period": {
    "start": "2025-11-03",
    "end": "2025-12-03"
  },
  "activity": [
    {
      "detail": {
        "kind": "Appointment",
        "code": {
          "text": "Cardiology follow-up"
        },
        "status": "scheduled",
        "scheduledTiming": {
          "event": ["2025-11-10"]
        },
        "performer": [{
          "reference": "Practitioner/dr-smith"
        }]
      }
    },
    {
      "detail": {
        "kind": "MedicationRequest",
        "code": {
          "text": "Take Furosemide 40mg daily"
        },
        "status": "in-progress"
      }
    },
    {
      "detail": {
        "kind": "Task",
        "code": {
          "text": "Daily weight monitoring"
        },
        "status": "in-progress",
        "description": "Weigh yourself daily. Call if weight increases >3lbs in 24h."
      }
    }
  ]
}
```

---

## 6. Task Resource

**Purpose:** Care coordination, follow-ups, authorizations

### Schema
```python
{
  "resourceType": "Task",
  "id": "task-auth-123",
  "status": "requested",
  "intent": "order",
  "priority": "urgent",
  "code": {
    "coding": [{
      "system": "http://hl7.org/fhir/CodeSystem/task-code",
      "code": "approve",
      "display": "Activate/approve the focal resource"
    }]
  },
  "description": "Prior authorization for MRI brain (CPT 70553)",
  "for": {
    "reference": "Patient/pt-12345"
  },
  "authoredOn": "2025-11-03T14:00:00-05:00",
  "requester": {
    "reference": "Practitioner/dr-smith"
  },
  "owner": {
    "display": "Authorization Team"
  },
  "restriction": {
    "period": {
      "end": "2025-11-06"
    }
  }
}
```

---

## 7. DocumentReference Resource

**Purpose:** Link PDFs (intake, discharge summaries)

### Schema
```json
{
  "resourceType": "DocumentReference",
  "id": "doc-discharge-123",
  "status": "current",
  "type": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "18842-5",
      "display": "Discharge Summary"
    }]
  },
  "subject": {
    "reference": "Patient/pt-12345"
  },
  "date": "2025-11-03T16:00:00-05:00",
  "author": [{
    "reference": "Practitioner/dr-smith"
  }],
  "content": [{
    "attachment": {
      "contentType": "application/pdf",
      "url": "https://storage.clinic.com/discharge/pt-12345-20251103.pdf",
      "title": "Discharge Summary - CHF Exacerbation"
    }
  }]
}
```

---

## FHIR Validation

### JSON Schema Validation
```python
import jsonschema

class FHIRValidator:
    def __init__(self):
        self.schemas = {
            'Patient': self.load_schema('Patient.schema.json'),
            'Appointment': self.load_schema('Appointment.schema.json'),
            'Coverage': self.load_schema('Coverage.schema.json'),
            # ... more schemas
        }
    
    def validate(self, resource: dict) -> bool:
        resource_type = resource.get('resourceType')
        if resource_type not in self.schemas:
            raise ValueError(f"Unknown resource type: {resource_type}")
        
        schema = self.schemas[resource_type]
        jsonschema.validate(resource, schema)
        return True
```

### Business Rules Validation
```python
class BusinessRuleValidator:
    def validate_appointment(self, appt: Appointment) -> List[str]:
        errors = []
        
        # Start must be before end
        if appt.start >= appt.end:
            errors.append("Start time must be before end time")
        
        # Duration must match start/end
        actual_duration = (appt.end - appt.start).total_seconds() / 60
        if abs(actual_duration - appt.minutesDuration) > 1:
            errors.append("Duration doesn't match start/end times")
        
        # Must have at least patient + provider
        if len(appt.participant) < 2:
            errors.append("Must have patient and provider")
        
        return errors
```

## Next Steps
- See `04-task-categories.md` for 40 task definitions
- See `05-evaluators.md` for FHIR validation in evaluators
- See `07-implementation-guide.md` for code examples

