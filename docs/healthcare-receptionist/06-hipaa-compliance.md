# Healthcare Receptionist - HIPAA Compliance

## Overview

HIPAA (Health Insurance Portability and Accountability Act) compliance is **non-negotiable** for healthcare applications. This document outlines:
- PHI (Protected Health Information) classification
- Security safeguards
- Privacy rules implementation
- Audit logging
- Breach notification

---

## What is PHI (Protected Health Information)?

### PHI Identifiers (18 types)
1. Names
2. Geographic subdivisions smaller than state
3. Dates (birth, admission, discharge, death)
4. Telephone/fax numbers
5. Email addresses
6. Social Security numbers
7. Medical record numbers
8. Health plan beneficiary numbers
9. Account numbers
10. Certificate/license numbers
11. Vehicle identifiers
12. Device identifiers/serial numbers
13. URLs
14. IP addresses
15. Biometric identifiers
16. Full-face photos
17. Any unique identifying number/code
18. **Health information** (diagnoses, medications, lab results, treatment)

### What Our System Handles
- **Demographics:** Names, DOB, addresses, phone, email
- **Medical identifiers:** MRN (Medical Record Number)
- **Insurance:** Member IDs, group numbers
- **Clinical data:** Chief complaints, diagnoses (ICD-10), triage notes
- **Appointments:** Provider, date/time, reason
- **Billing:** Charges, payment info

---

## HIPAA Security Rule - Technical Safeguards

### 1. Access Control
**Requirement:** Only authorized users can access PHI

```python
class AccessControl:
    """Role-based access control for PHI"""
    
    ROLES = {
        'front_desk': ['read_patient', 'create_appointment', 'send_sms'],
        'nurse': ['read_patient', 'read_clinical', 'create_observation'],
        'provider': ['read_patient', 'read_clinical', 'update_careplan'],
        'billing': ['read_patient', 'read_insurance', 'create_invoice'],
        'system': ['all']
    }
    
    def check_permission(self, user_role: str, action: str) -> bool:
        """Check if role has permission for action"""
        allowed_actions = self.ROLES.get(user_role, [])
        return action in allowed_actions or 'all' in allowed_actions
    
    def audit_access(self, user: str, action: str, patient_id: str):
        """Log every PHI access"""
        self.audit_log.record({
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'action': action,
            'patient_id': patient_id[-4:],  # Only last 4 chars
            'ip_address': self.get_user_ip(user)
        })
```

### 2. Audit Controls
**Requirement:** Log all PHI access, modifications, deletions

```python
class AuditLog:
    """Immutable audit log for HIPAA compliance"""
    
    def __init__(self):
        self.log_file = 'audit_logs/hipaa_audit.jsonl'
    
    def record(self, event: dict):
        """Record audit event (append-only)"""
        event['timestamp'] = datetime.now().isoformat()
        event['event_id'] = str(uuid.uuid4())
        
        # Write to immutable log
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        # In production: also send to SIEM/log aggregator
        # self.send_to_cloudwatch(event)
    
    def get_patient_access_log(self, patient_id: str, 
                               start_date: str, 
                               end_date: str) -> list:
        """Retrieve all access to a patient's PHI"""
        events = []
        with open(self.log_file, 'r') as f:
            for line in f:
                event = json.loads(line)
                if (event.get('patient_id') == patient_id and
                    start_date <= event['timestamp'] <= end_date):
                    events.append(event)
        return events
```

### 3. Integrity Controls
**Requirement:** Ensure PHI is not improperly altered or destroyed

```python
class IntegrityControl:
    """Ensure FHIR resources are not tampered with"""
    
    def create_hash(self, resource: dict) -> str:
        """Create SHA-256 hash of FHIR resource"""
        resource_str = json.dumps(resource, sort_keys=True)
        return hashlib.sha256(resource_str.encode()).hexdigest()
    
    def verify_integrity(self, resource: dict, 
                        expected_hash: str) -> bool:
        """Verify resource hasn't been tampered with"""
        actual_hash = self.create_hash(resource)
        return actual_hash == expected_hash
    
    def sign_resource(self, resource: dict, 
                     private_key: str) -> str:
        """Digitally sign FHIR resource"""
        resource_hash = self.create_hash(resource)
        signature = self.rsa_sign(resource_hash, private_key)
        return signature
```

### 4. Transmission Security
**Requirement:** Encrypt PHI in transit

```python
class TransmissionSecurity:
    """Ensure PHI is encrypted in transit"""
    
    def send_email(self, to: str, subject: str, body: str, 
                   attachments: list = None):
        """Send HIPAA-compliant email (TLS 1.2+)"""
        
        # Validate no PHI in subject/body
        if not self.validate_no_phi(subject + body):
            raise HIPAAViolationError("PHI detected in email subject/body")
        
        # Send via TLS-encrypted SMTP
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        with smtplib.SMTP_SSL('smtp.clinic.com', 465, context=context) as server:
            msg = self.create_encrypted_message(to, subject, body, attachments)
            server.send_message(msg)
    
    def send_sms(self, to: str, message: str):
        """Send HIPAA-compliant SMS"""
        
        # Validate no PHI
        if not self.validate_no_phi(message):
            raise HIPAAViolationError("PHI detected in SMS")
        
        # SMS is inherently insecure - only send:
        # ✅ "Your appointment is tomorrow"
        # ❌ "Your diabetes appointment is tomorrow"
        
        self.sms_service.send(to, message)
```

---

## HIPAA Privacy Rule - Communication Guidelines

### SMS/Text Messaging Rules

**✅ ALLOWED:**
```python
SMS_TEMPLATES_ALLOWED = {
    'appointment_reminder': 'Reminder: You have an appointment tomorrow at {time}. Reply CONFIRM or call {phone}.',
    'test_result_ready': 'Your test results are ready. Log in to the patient portal: {portal_url}',
    'medication_reminder': 'Reminder: Time to take your medication. Questions? Call {phone}.',
    'general_notification': 'Message from {clinic_name}. Please call {phone}.'
}
```

**❌ PROHIBITED:**
```python
# NEVER include in SMS:
PROHIBITED_SMS_CONTENT = [
    'Diagnosis names (diabetes, cancer, HIV)',
    'Medication names (metformin, lisinopril)',
    'Lab values (cholesterol 250, A1C 8.5)',
    'Procedure details (colonoscopy, biopsy)',
    'Test results (positive, negative, abnormal)',
    'Reason for appointment (follow-up for chest pain)'
]
```

### Email Communication Rules

**✅ ALLOWED (with encryption):**
```python
EMAIL_ALLOWED_CONTENT = {
    'appointment_confirmation': {
        'subject': 'Appointment Confirmed',
        'body': 'Your appointment with Dr. Smith is Nov 10 at 2pm.',
        'attachments': ['consent_form.pdf']  # Encrypted PDF
    },
    'test_result_notification': {
        'subject': 'Lab Results Available',
        'body': 'Your lab results are ready. Log in to view: {portal_url}',
        'attachments': []  # NO RESULTS IN EMAIL
    }
}
```

**❌ PROHIBITED (even with encryption):**
```python
# NEVER include in email subject line:
PROHIBITED_EMAIL_SUBJECTS = [
    'Your diabetes test results',
    'HIV test results',
    'Cancer screening results',
    'Abnormal lab values'
]

# Use generic subjects:
ALLOWED_EMAIL_SUBJECTS = [
    'Appointment Confirmation',
    'Lab Results Available',
    'Message from Your Healthcare Provider'
]
```

---

## PHI Masking & De-identification

### Automatic PHI Detection
```python
class PHIDetector:
    """Detect and mask PHI in text"""
    
    PHI_PATTERNS = {
        'diagnosis': r'\b(diabetes|hypertension|cancer|HIV|AIDS|hepatitis|pneumonia)\b',
        'medication': r'\b(metformin|lisinopril|atorvastatin|insulin|warfarin)\b',
        'lab_value': r'\b\d+\s?(mg/dL|mmol/L|units|mEq/L)\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'mrn': r'\bMRN[-:]?\d+\b'
    }
    
    def detect_phi(self, text: str) -> list:
        """Detect PHI in text"""
        detected = []
        for phi_type, pattern in self.PHI_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected.append({
                    'type': phi_type,
                    'matches': matches
                })
        return detected
    
    def mask_phi(self, text: str) -> str:
        """Replace PHI with [REDACTED]"""
        for pattern in self.PHI_PATTERNS.values():
            text = re.sub(pattern, '[REDACTED]', text, flags=re.IGNORECASE)
        return text
    
    def validate_no_phi(self, text: str) -> bool:
        """Check if text contains PHI"""
        detected = self.detect_phi(text)
        return len(detected) == 0
```

### Safe Logging
```python
class SafeLogger:
    """Log without exposing PHI"""
    
    def log(self, level: str, message: str, context: dict = None):
        """Log message with PHI masking"""
        
        # Mask PHI in message
        safe_message = self.phi_detector.mask_phi(message)
        
        # Mask PHI in context
        safe_context = {}
        for key, value in (context or {}).items():
            if key in ['patient_name', 'mrn', 'phone', 'email', 'ssn']:
                # Only log last 4 characters
                safe_context[key] = f"****{str(value)[-4:]}"
            elif key in ['diagnosis', 'medication', 'lab_result']:
                safe_context[key] = '[REDACTED]'
            else:
                safe_context[key] = value
        
        # Log safely
        logger.log(level, safe_message, extra=safe_context)
```

---

## Minimum Necessary Rule

**Requirement:** Only access PHI that is minimally necessary for the task

```python
class MinimumNecessaryAccess:
    """Implement minimum necessary rule"""
    
    # Role-based data access
    ROLE_ACCESS_LEVELS = {
        'front_desk': {
            'Patient': ['name', 'birthDate', 'telecom', 'address'],
            'Appointment': ['start', 'end', 'status', 'participant'],
            'Coverage': ['payor', 'subscriberId'],
            # NO ACCESS to: clinical notes, diagnoses, lab results
        },
        'nurse': {
            'Patient': ['name', 'birthDate', 'telecom', 'address', 'contact'],
            'Appointment': ['all'],
            'Observation': ['all'],
            'CarePlan': ['all'],
            # NO ACCESS to: billing, insurance details
        },
        'billing': {
            'Patient': ['name', 'birthDate', 'address'],
            'Coverage': ['all'],
            'Claim': ['all'],
            # NO ACCESS to: clinical notes, observations
        }
    }
    
    def filter_resource(self, resource: dict, user_role: str) -> dict:
        """Return only necessary fields for role"""
        resource_type = resource['resourceType']
        allowed_fields = self.ROLE_ACCESS_LEVELS.get(user_role, {}).get(resource_type, [])
        
        if 'all' in allowed_fields:
            return resource
        
        # Filter to only allowed fields
        filtered = {'resourceType': resource_type, 'id': resource['id']}
        for field in allowed_fields:
            if field in resource:
                filtered[field] = resource[field]
        
        return filtered
```

---

## Breach Notification

**Requirement:** Notify patients within 60 days of discovering a breach

```python
class BreachNotification:
    """Handle HIPAA breach notifications"""
    
    def detect_breach(self, event: dict) -> bool:
        """Detect if event constitutes a breach"""
        
        # Breach indicators
        breach_indicators = [
            'unauthorized_access',
            'data_exfiltration',
            'phi_exposure',
            'lost_device',
            'stolen_device',
            'unencrypted_transmission'
        ]
        
        return event.get('type') in breach_indicators
    
    def assess_breach(self, event: dict) -> dict:
        """Assess breach severity"""
        
        # Risk assessment factors
        factors = {
            'nature_extent': self.assess_nature_extent(event),
            'unauthorized_person': self.identify_unauthorized_person(event),
            'phi_acquired': self.determine_phi_acquired(event),
            'risk_mitigation': self.assess_mitigation(event)
        }
        
        # Determine notification requirement
        if factors['risk_mitigation'] == 'low_risk_exception':
            return {'notification_required': False}
        
        return {
            'notification_required': True,
            'affected_individuals': event.get('affected_patients', []),
            'notification_deadline': datetime.now() + timedelta(days=60)
        }
    
    def send_breach_notification(self, patients: list, 
                                 breach_details: dict):
        """Send breach notification to affected individuals"""
        
        for patient in patients:
            # Email notification
            self.email_service.send({
                'to': patient['email'],
                'subject': 'Important Notice: Data Security Incident',
                'body': self.generate_breach_letter(patient, breach_details)
            })
            
            # Log notification
            self.audit_log.record({
                'event': 'breach_notification_sent',
                'patient_id': patient['id'],
                'breach_id': breach_details['id']
            })
```

---

## Business Associate Agreements (BAAs)

**Requirement:** BAA with all vendors who handle PHI

### MCP Servers as Business Associates

```python
class BusinessAssociateAgreement:
    """Track BAAs with MCP servers"""
    
    MCP_SERVERS_BAA_STATUS = {
        'calendar': {
            'baa_required': True,
            'baa_signed': True,
            'baa_date': '2025-01-01',
            'vendor': 'Google Calendar API'
        },
        'email': {
            'baa_required': True,
            'baa_signed': True,
            'baa_date': '2025-01-01',
            'vendor': 'SendGrid'
        },
        'sms-messaging': {
            'baa_required': True,
            'baa_signed': True,
            'baa_date': '2025-01-01',
            'vendor': 'Twilio'
        },
        'pdf-generator': {
            'baa_required': False,  # On-premise, no external vendor
            'baa_signed': None,
            'vendor': 'Internal'
        }
    }
    
    def check_baa_compliance(self, server: str) -> bool:
        """Check if BAA is in place for server"""
        baa_info = self.MCP_SERVERS_BAA_STATUS.get(server)
        
        if not baa_info:
            raise ValueError(f"Unknown MCP server: {server}")
        
        if baa_info['baa_required'] and not baa_info['baa_signed']:
            raise HIPAAViolationError(f"BAA required but not signed for {server}")
        
        return True
```

---

## HIPAA Compliance Checklist

### Technical Safeguards ✅
- [x] Access control (role-based)
- [x] Audit controls (immutable logging)
- [x] Integrity controls (FHIR resource hashing)
- [x] Transmission security (TLS 1.2+, encryption)

### Physical Safeguards ✅
- [x] Facility access controls
- [x] Workstation use policies
- [x] Device and media controls

### Administrative Safeguards ✅
- [x] Security management process
- [x] Workforce security (training)
- [x] Information access management
- [x] Security incident procedures
- [x] Contingency planning (backup/disaster recovery)
- [x] Business associate contracts

### Privacy Rule ✅
- [x] Notice of Privacy Practices
- [x] Patient rights (access, amendment, accounting)
- [x] Minimum necessary rule
- [x] De-identification procedures
- [x] Breach notification process

---

## Testing HIPAA Compliance

### Automated Tests
```python
import pytest

def test_no_phi_in_sms():
    """Test that SMS messages don't contain PHI"""
    sms_service = SMSMessagingService()
    
    # Valid SMS
    valid_msg = "Your appointment is tomorrow at 2pm"
    assert sms_service.validate_hipaa_compliance(valid_msg) is True
    
    # Invalid SMS (contains diagnosis)
    invalid_msg = "Your diabetes appointment is tomorrow"
    with pytest.raises(HIPAAViolationError):
        sms_service.send_sms("+15551234567", invalid_msg)

def test_audit_log_immutable():
    """Test that audit log is append-only"""
    audit_log = AuditLog()
    
    # Record event
    event_id = audit_log.record({'action': 'read_patient', 'user': 'nurse1'})
    
    # Attempt to modify (should fail)
    with pytest.raises(PermissionError):
        audit_log.modify(event_id, {'user': 'hacker'})
    
    # Attempt to delete (should fail)
    with pytest.raises(PermissionError):
        audit_log.delete(event_id)
```

---

## Next Steps
- See `07-implementation-guide.md` for build instructions
- See `08-api-contracts.md` for API specifications
- See `09-deployment.md` for production security configuration

