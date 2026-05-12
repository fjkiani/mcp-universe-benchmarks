# Healthcare Receptionist - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Agent Layer                             │
│  (ReAct agent — GPT-4 class model via LiteLLM / provider)               │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              Orchestration Layer                             │
│  - Workflow Engine (task sequencing)                        │
│  - HIPAA Compliance Filter (PHI masking)                    │
│  - FHIR Resource Manager (validation, transformation)       │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              Business Logic Layer                            │
│  ┌──────────────┬──────────────┬────────────┬─────────────┐│
│  │  Patient     │  Appointment │  Insurance │  Clinical   ││
│  │  Intake      │  Scheduling  │  Auth      │  Triage     ││
│  │  Service     │  Service     │  Service   │  Service    ││
│  └──────────────┴──────────────┴────────────┴─────────────┘│
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              MCP Server Integration Layer                    │
│  ┌──────────┬──────────┬────────────┬───────────┬─────────┐│
│  │ calendar │  email   │ sms-msg   │  task-mgmt│ pdf-gen ││
│  └──────────┴──────────┴────────────┴───────────┴─────────┘│
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              Data Layer                                      │
│  - FHIR Resource Store (Patient, Appointment, Coverage)     │
│  - Task Queue (authorization requests, follow-ups)          │
│  - Audit Log (HIPAA compliance tracking)                    │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Agent Layer
**Technology:** ReAct agent powered by a GPT-4 class model (via your configured LLM provider / LiteLLM gateway)

**Responsibilities:**
- Parse natural language patient requests
- Plan multi-step workflows
- Execute MCP server tool calls
- Generate FHIR-compliant responses

**Configuration:**
```yaml
kind: agent
spec:
  name: healthcare-receptionist-agent
  type: react
  config:
    llm: llm-healthcare
    max_iterations: 10
    tools:
      - calendar.create_event
      - calendar.check_availability
      - email.send_message
      - sms_messaging.send_sms
      - task_management.create_task
      - pdf_generator.create_pdf
      - google_search.search
```

### 2. Orchestration Layer
**Purpose:** Workflow sequencing, HIPAA compliance, FHIR validation

**Components:**

**A. Workflow Engine**
```python
class WorkflowEngine:
    """Orchestrates multi-step healthcare workflows"""
    
    def execute_intake_workflow(self, patient_data: dict) -> FHIRPatient:
        # 1. Validate patient data
        validated = self.validate_patient_data(patient_data)
        
        # 2. Check for duplicates (by name, DOB, SSN)
        existing = self.check_duplicate_patient(validated)
        
        # 3. Create FHIR Patient resource
        fhir_patient = self.create_fhir_patient(validated)
        
        # 4. Store in FHIR resource store
        self.fhir_store.save(fhir_patient)
        
        # 5. Create welcome task
        self.task_service.create_welcome_task(fhir_patient.id)
        
        return fhir_patient
```

**B. HIPAA Compliance Filter**
```python
class HIPAAFilter:
    """Filters PHI from communications"""
    
    PHI_PATTERNS = {
        'diagnosis': r'\b(diabetes|hypertension|cancer|HIV)\b',
        'medication': r'\b(metformin|lisinopril|tamoxifen)\b',
        'lab_values': r'\b\d+\s?(mg/dL|mmol/L|units)\b'
    }
    
    def mask_phi_in_sms(self, message: str) -> str:
        """Ensure SMS messages don't contain PHI"""
        # ✅ "Your appointment is Nov 10" 
        # ❌ "Your diabetes appointment is Nov 10"
        for pattern in self.PHI_PATTERNS.values():
            if re.search(pattern, message, re.IGNORECASE):
                raise HIPAAViolationError(f"PHI detected in message")
        return message
```

**C. FHIR Resource Manager**
```python
class FHIRResourceManager:
    """Validates and transforms FHIR R4 resources"""
    
    def validate_patient(self, data: dict) -> bool:
        # Check required fields
        required = ['resourceType', 'identifier', 'name', 'birthDate']
        if not all(k in data for k in required):
            return False
        
        # Validate structure
        schema = self.load_schema('Patient')
        jsonschema.validate(data, schema)
        
        return True
    
    def create_appointment(self, patient_id: str, provider: str, 
                          datetime: str) -> FHIRAppointment:
        return {
            "resourceType": "Appointment",
            "status": "booked",
            "participant": [
                {"actor": {"reference": f"Patient/{patient_id}"}},
                {"actor": {"reference": f"Practitioner/{provider}"}}
            ],
            "start": datetime,
            "end": self.calculate_end_time(datetime, duration=30)
        }
```

### 3. Business Logic Layer
**Purpose:** Domain-specific logic for each category

**A. Patient Intake Service**
```python
class PatientIntakeService:
    def __init__(self, fhir_manager, calendar, email, pdf_gen):
        self.fhir = fhir_manager
        self.calendar = calendar
        self.email = email
        self.pdf = pdf_gen
    
    async def onboard_new_patient(self, patient_data: dict, 
                                   provider: str) -> dict:
        # 1. Create FHIR Patient
        patient = self.fhir.create_patient(patient_data)
        
        # 2. Check provider availability
        slots = await self.calendar.get_availability(
            provider=provider,
            days_ahead=14
        )
        
        # 3. Book first appointment
        appointment = await self.calendar.create_event(
            title=f"New Patient Visit - {patient['name'][0]['given'][0]}",
            start=slots[0]['start'],
            duration=60,
            attendees=[provider]
        )
        
        # 4. Generate intake forms
        intake_pdf = await self.pdf.generate({
            'template': 'patient_intake',
            'data': patient_data
        })
        
        # 5. Send confirmation email
        await self.email.send({
            'to': patient_data['email'],
            'subject': 'Welcome to [Clinic Name]',
            'body': f"Your appointment is {appointment['start']}",
            'attachments': [intake_pdf]
        })
        
        return {
            'patient': patient,
            'appointment': appointment,
            'intake_form_sent': True
        }
```

**B. Appointment Scheduling Service**
```python
class AppointmentSchedulingService:
    def __init__(self, fhir_manager, calendar, task_mgmt):
        self.fhir = fhir_manager
        self.calendar = calendar
        self.tasks = task_mgmt
    
    async def schedule_with_authorization_check(
        self, patient_id: str, procedure_code: str, 
        provider: str) -> dict:
        
        # 1. Get patient insurance
        coverage = self.fhir.get_coverage(patient_id)
        
        # 2. Check if procedure requires prior auth
        requires_auth = self.check_prior_authorization(
            procedure_code, coverage['payor']
        )
        
        if requires_auth:
            # Create task for authorization team
            task = await self.tasks.create({
                'title': f'Prior Auth: {procedure_code}',
                'assigned_to': 'authorization_team',
                'priority': 'high',
                'due_date': self.get_business_days_ahead(3)
            })
            
            return {
                'appointment': None,
                'requires_authorization': True,
                'task_id': task['id'],
                'message': 'Authorization required, we will call you'
            }
        
        # 3. Schedule appointment
        appointment = await self.calendar.create_event(...)
        return {'appointment': appointment}
```

**C. Insurance Authorization Service**
```python
class InsuranceAuthorizationService:
    # CPT codes requiring prior authorization
    HIGH_COST_IMAGING = ['70553', '71275', '72148']  # MRI, CT angio, etc
    HIGH_COST_PROCEDURES = ['27447', '43644']  # Joint replacement, etc
    
    def check_prior_authorization(self, cpt_code: str, 
                                   payor: str) -> bool:
        """Check if procedure requires prior auth"""
        # Check general rules
        if cpt_code in self.HIGH_COST_IMAGING:
            return True
        if cpt_code in self.HIGH_COST_PROCEDURES:
            return True
        
        # Check payor-specific rules
        if payor == 'Medicare' and cpt_code in self.MEDICARE_PA_LIST:
            return True
        
        return False
    
    def calculate_patient_responsibility(self, coverage: dict, 
                                        procedure_cost: float) -> dict:
        """Calculate copay/coinsurance/deductible"""
        deductible_met = coverage.get('deductible_met', 0)
        deductible_total = coverage.get('deductible_total', 0)
        coinsurance_rate = coverage.get('coinsurance', 0.2)  # 20%
        copay = coverage.get('copay', 0)
        
        remaining_deductible = max(0, deductible_total - deductible_met)
        
        if copay > 0:
            return {'patient_owes': copay, 'breakdown': 'Copay'}
        
        if remaining_deductible > 0:
            deductible_portion = min(procedure_cost, remaining_deductible)
            coinsurance_portion = (procedure_cost - deductible_portion) * coinsurance_rate
            total = deductible_portion + coinsurance_portion
            return {
                'patient_owes': total,
                'breakdown': f'${deductible_portion} deductible + ${coinsurance_portion} coinsurance'
            }
        
        return {
            'patient_owes': procedure_cost * coinsurance_rate,
            'breakdown': f'{coinsurance_rate*100}% coinsurance'
        }
```

**D. Clinical Triage Service**
```python
class ClinicalTriageService:
    # Safety-critical: emergent symptoms
    EMERGENT_SYMPTOMS = [
        'chest pain', 'difficulty breathing', 'stroke symptoms',
        'severe bleeding', 'loss of consciousness', 'seizure'
    ]
    
    # ICD-10 mapping for common chief complaints
    ICD10_MAP = {
        'chest pain': 'R07.9',
        'cough': 'R05',
        'headache': 'R51',
        'fever': 'R50.9'
    }
    
    def triage_patient(self, chief_complaint: str, 
                      symptoms: list[str]) -> dict:
        """Safety-critical triage logic"""
        
        # Check for emergent symptoms
        for symptom in symptoms:
            if any(emergent in symptom.lower() 
                   for emergent in self.EMERGENT_SYMPTOMS):
                return {
                    'triage_category': 'EMERGENT',
                    'recommended_action': 'call_911',
                    'escalated_to': 'emergency_services',
                    'message': 'Call 911 immediately'
                }
        
        # Assess urgency
        urgency = self.assess_urgency(chief_complaint, symptoms)
        
        if urgency == 'urgent':
            return {
                'triage_category': 'URGENT',
                'recommended_action': 'same_day_appointment',
                'message': 'We need to see you today'
            }
        
        return {
            'triage_category': 'ROUTINE',
            'recommended_action': 'schedule_appointment',
            'icd10_code': self.ICD10_MAP.get(chief_complaint.lower(), 'Z00.00')
        }
```

### 4. MCP Server Integration Layer
**Purpose:** Abstract MCP server tool calls

```python
class MCPServerAdapter:
    """Unified interface for all MCP servers"""
    
    def __init__(self):
        self.calendar = CalendarServer()
        self.email = EmailServer()
        self.sms = SMSMessagingServer()
        self.tasks = TaskManagementServer()
        self.pdf = PDFGeneratorServer()
        self.search = GoogleSearchServer()
        self.date = DateServer()
    
    async def send_hipaa_compliant_sms(self, phone: str, 
                                       message: str) -> dict:
        """Send SMS with HIPAA validation"""
        # 1. Mask PHI
        safe_message = self.hipaa_filter.mask_phi_in_sms(message)
        
        # 2. Send via MCP server
        result = await self.sms.send_message({
            'to': phone,
            'body': safe_message
        })
        
        # 3. Log for audit
        self.audit_log.record('sms_sent', {
            'phone': phone[-4:],  # Only last 4 digits
            'timestamp': datetime.now().isoformat()
        })
        
        return result
```

### 5. Data Layer
**Purpose:** Persistent storage for FHIR resources and tasks

**A. FHIR Resource Store**
```python
class FHIRResourceStore:
    """In-memory FHIR resource storage (use DB in production)"""
    
    def __init__(self):
        self.patients = {}
        self.appointments = {}
        self.coverage = {}
        self.observations = {}
    
    def save_patient(self, patient: dict) -> str:
        patient_id = str(uuid.uuid4())
        patient['id'] = patient_id
        self.patients[patient_id] = patient
        return patient_id
    
    def search_patient(self, name: str = None, dob: str = None, 
                      mrn: str = None) -> list[dict]:
        """Fuzzy search for existing patients"""
        results = []
        for patient in self.patients.values():
            if mrn and any(id['value'] == mrn for id in patient['identifier']):
                results.append(patient)
            elif name and dob:
                patient_name = patient['name'][0]['family']
                if fuzz.ratio(name, patient_name) > 80 and patient['birthDate'] == dob:
                    results.append(patient)
        return results
```

**B. Audit Log (HIPAA Compliance)**
```python
class AuditLog:
    """Track all PHI access for HIPAA compliance"""
    
    def record(self, action: str, details: dict):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user': details.get('user', 'system'),
            'patient_id': details.get('patient_id', 'N/A'),
            'details': details
        }
        self.log.append(entry)
        
        # In production: write to immutable log store
        # self.s3_client.put_object(
        #     Bucket='hipaa-audit-logs',
        #     Key=f'{entry["timestamp"]}.json',
        #     Body=json.dumps(entry)
        # )
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Agent | GPT-4 class (provider-configured) | Natural language understanding, planning |
| Orchestration | Python 3.12+ | Workflow engine, FHIR validation |
| Business Logic | Python services | Domain-specific logic |
| MCP Servers | Existing servers | calendar, email, sms, tasks, pdf, search, date |
| Data Store | JSON files (dev) / PostgreSQL (prod) | FHIR resources, tasks, audit logs |
| Validation | jsonschema, pydantic | FHIR R4 schema validation |
| HIPAA | regex filters, encryption | PHI masking, audit logging |

## API Contracts
See `08-api-contracts.md` for detailed API specifications.

## Deployment
See `09-deployment.md` for production deployment guide.

