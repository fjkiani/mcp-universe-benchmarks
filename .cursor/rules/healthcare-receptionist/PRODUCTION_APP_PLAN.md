# Healthcare Receptionist - Production Application Plan

**Goal:** Build a full end-to-end production demo using existing infrastructure from STATUS.md

**Current State:** We have tests, servers, and basic status cards  
**Target State:** Working production app with real healthcare workflows

---

## 🎯 Core Capabilities to Showcase

### From HEALTHCARE_RECEPTIONIST_V2.md:

1. **Patient Intake** - Collect demographics, insurance, create FHIR Patient resource
2. **Appointment Scheduling** - Book appointments with NexHealth EHR integration
3. **Insurance Verification** - Check eligibility, prior authorization
4. **Clinical Triage** - Safety-critical routing (chest pain → 911, mild → routine)
5. **HIPAA Communication** - SMS/Email with PHI detection and filtering
6. **Video Consultation** - VideoSDK room creation
7. **Medical Transcription** - AssemblyAI audio transcription with entity extraction

---

## 📋 PRODUCTION APP ARCHITECTURE

### Frontend Pages (User-Facing)

```
/                              → Landing page (what we have now)
/demo                          → NEW: Full production demo
  ├── /demo/patient-intake     → Patient registration form
  ├── /demo/appointment        → Appointment booking
  ├── /demo/insurance          → Insurance verification
  ├── /demo/triage             → Clinical triage assessment
  ├── /demo/sms                → Send HIPAA SMS
  ├── /demo/video              → Video consultation
  └── /demo/transcribe         → Medical transcription

/capabilities                  → Existing capabilities page (keep)
/showcase                      → Existing showcase (backend testing)
```

---

## 🏗️ IMPLEMENTATION PLAN

### Phase 1: Backend Routes (Jr can build this)

**File:** `backend/routes/healthcare_demo.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/demo/healthcare", tags=["Healthcare Demo"])

# 1. Patient Intake
@router.post("/patient-intake")
async def create_patient(patient_data: PatientIntakeRequest):
    """
    Create FHIR Patient resource and register in NexHealth
    
    Input:
    {
      "firstName": "John",
      "lastName": "Doe",
      "dob": "1985-03-15",
      "phone": "555-1234",
      "insurance": {
        "carrier": "Blue Cross",
        "memberId": "ABC123",
        "groupNumber": "GRP999"
      }
    }
    
    Output:
    {
      "success": true,
      "mrn": "MRN-12345",
      "fhir_resource": { ... },
      "nexhealth_patient_id": "pat_xxx"
    }
    """
    # Call nexhealth.create_patient()
    # Generate FHIR Patient resource
    # Return patient info
    pass

# 2. Appointment Booking
@router.post("/book-appointment")
async def book_appointment(appointment: AppointmentRequest):
    """
    Book appointment in NexHealth EHR
    
    Input:
    {
      "patientId": "MRN-12345",
      "providerId": "dr_smith",
      "date": "2025-11-15",
      "time": "14:00",
      "reason": "Annual physical"
    }
    
    Output:
    {
      "success": true,
      "appointment_id": "appt_xxx",
      "confirmation_sent": true,
      "fhir_appointment": { ... }
    }
    """
    # Call nexhealth.book_appointment()
    # Send confirmation via email
    # Return confirmation
    pass

# 3. Insurance Verification
@router.post("/verify-insurance")
async def verify_insurance(insurance: InsuranceRequest):
    """
    Check insurance eligibility and prior auth requirements
    
    Input:
    {
      "patientId": "MRN-12345",
      "procedureCode": "CPT-70553",  // MRI
      "insurance": {
        "carrier": "Blue Cross",
        "memberId": "ABC123"
      }
    }
    
    Output:
    {
      "coverage_active": true,
      "requires_prior_auth": true,
      "estimated_cost": "$50 copay",
      "deductible_met": false
    }
    """
    # Call nexhealth.verify_insurance_eligibility()
    # Check prior auth requirements
    # Return coverage info
    pass

# 4. Clinical Triage
@router.post("/triage")
async def triage_patient(triage: TriageRequest):
    """
    Assess patient urgency and route appropriately
    
    Input:
    {
      "chiefComplaint": "chest pain",
      "duration": "2 hours",
      "severity": "8/10",
      "symptoms": ["shortness of breath", "left arm pain"]
    }
    
    Output:
    {
      "urgency": "EMERGENT",
      "recommended_action": "call_911",
      "advice": "Call 911 immediately for chest pain evaluation",
      "safety_protocol": "chest_pain_emergent"
    }
    """
    # Clinical decision logic
    # Safety-critical routing
    # Return triage result
    pass

# 5. HIPAA SMS
@router.post("/send-sms")
async def send_hipaa_sms(sms: SMSRequest):
    """
    Send HIPAA-compliant SMS with PHI detection
    
    Input:
    {
      "phone": "+15551234567",
      "message": "Your appointment with Dr. Smith for diabetes is Nov 15 at 2pm"
    }
    
    Output:
    {
      "success": true,
      "phi_detected": ["diabetes", "Dr. Smith"],
      "message_sent": "Your appointment is Nov 15 at 2pm",
      "phi_filtered": true
    }
    """
    # Call twilio_hipaa.send_hipaa_sms()
    # PHI detection and filtering
    # Return result
    pass

# 6. Video Consultation
@router.post("/create-video-room")
async def create_video_room(video: VideoRequest):
    """
    Create VideoSDK room for consultation
    
    Input:
    {
      "patientId": "MRN-12345",
      "providerId": "dr_smith",
      "appointmentId": "appt_xxx"
    }
    
    Output:
    {
      "success": true,
      "room_id": "room_xxx",
      "patient_link": "https://video.example.com/room_xxx?token=xxx",
      "provider_link": "https://video.example.com/room_xxx?token=yyy"
    }
    """
    # Call videosdk.create_room()
    # Generate participant tokens
    # Return room links
    pass

# 7. Medical Transcription
@router.post("/transcribe-audio")
async def transcribe_audio(audio: AudioRequest):
    """
    Transcribe medical audio with entity extraction
    
    Input:
    {
      "audio_url": "https://example.com/audio.mp3",
      "patient_id": "MRN-12345"
    }
    
    Output:
    {
      "success": true,
      "transcription": "Patient reports chest pain for 2 hours...",
      "medical_entities": {
        "symptoms": ["chest pain"],
        "duration": ["2 hours"],
        "medications": []
      }
    }
    """
    # Call assemblyai.transcribe_medical()
    # Extract medical entities
    # Return transcription
    pass
```

---

### Phase 2: Frontend Demo Pages (Jr can build this)

**File:** `frontend/src/pages/demo/HealthcareDemoPage.tsx`

```tsx
import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import PatientIntakeForm from './PatientIntakeForm';
import AppointmentBooking from './AppointmentBooking';
import InsuranceVerification from './InsuranceVerification';
import ClinicalTriage from './ClinicalTriage';
import HipaaSMS from './HipaaSMS';
import VideoConsultation from './VideoConsultation';
import MedicalTranscription from './MedicalTranscription';

export default function HealthcareDemoPage() {
  return (
    <div className="healthcare-demo">
      <h1>Healthcare Receptionist - Live Demo</h1>
      
      {/* Navigation */}
      <nav className="demo-nav">
        <Link to="/demo/patient-intake">Patient Intake</Link>
        <Link to="/demo/appointment">Appointment Booking</Link>
        <Link to="/demo/insurance">Insurance Verification</Link>
        <Link to="/demo/triage">Clinical Triage</Link>
        <Link to="/demo/sms">HIPAA SMS</Link>
        <Link to="/demo/video">Video Consultation</Link>
        <Link to="/demo/transcribe">Medical Transcription</Link>
      </nav>

      {/* Routes */}
      <Routes>
        <Route path="/patient-intake" element={<PatientIntakeForm />} />
        <Route path="/appointment" element={<AppointmentBooking />} />
        <Route path="/insurance" element={<InsuranceVerification />} />
        <Route path="/triage" element={<ClinicalTriage />} />
        <Route path="/sms" element={<HipaaSMS />} />
        <Route path="/video" element={<VideoConsultation />} />
        <Route path="/transcribe" element={<MedicalTranscription />} />
      </Routes>
    </div>
  );
}
```

---

### Phase 3: Individual Feature Components

#### **File:** `frontend/src/pages/demo/PatientIntakeForm.tsx`

```tsx
import React, { useState } from 'react';
import { apiClient } from '../../api/mcp-client';

export default function PatientIntakeForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    dob: '',
    phone: '',
    insurance: {
      carrier: '',
      memberId: '',
      groupNumber: ''
    }
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await apiClient.post(
        '/api/v1/demo/healthcare/patient-intake',
        formData
      );
      setResult(response.data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="patient-intake-form">
      <h2>Patient Intake & Registration</h2>
      <p>Create a new patient record in FHIR format and register in NexHealth EHR</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>First Name</label>
          <input
            type="text"
            value={formData.firstName}
            onChange={(e) => setFormData({...formData, firstName: e.target.value})}
            required
          />
        </div>

        <div className="form-group">
          <label>Last Name</label>
          <input
            type="text"
            value={formData.lastName}
            onChange={(e) => setFormData({...formData, lastName: e.target.value})}
            required
          />
        </div>

        <div className="form-group">
          <label>Date of Birth</label>
          <input
            type="date"
            value={formData.dob}
            onChange={(e) => setFormData({...formData, dob: e.target.value})}
            required
          />
        </div>

        <div className="form-group">
          <label>Phone</label>
          <input
            type="tel"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            required
          />
        </div>

        <h3>Insurance Information</h3>
        
        <div className="form-group">
          <label>Insurance Carrier</label>
          <select
            value={formData.insurance.carrier}
            onChange={(e) => setFormData({
              ...formData,
              insurance: {...formData.insurance, carrier: e.target.value}
            })}
            required
          >
            <option value="">Select Carrier</option>
            <option value="Blue Cross Blue Shield">Blue Cross Blue Shield</option>
            <option value="Aetna">Aetna</option>
            <option value="UnitedHealthcare">UnitedHealthcare</option>
            <option value="Medicare">Medicare</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Creating Patient...' : 'Create Patient Record'}
        </button>
      </form>

      {/* Results Display */}
      {result && (
        <div className="result-panel">
          <h3>Result:</h3>
          {result.success ? (
            <div className="success">
              <p>✅ Patient Created Successfully!</p>
              <p><strong>MRN:</strong> {result.mrn}</p>
              <p><strong>NexHealth ID:</strong> {result.nexhealth_patient_id}</p>
              
              <details>
                <summary>View FHIR Resource</summary>
                <pre>{JSON.stringify(result.fhir_resource, null, 2)}</pre>
              </details>
            </div>
          ) : (
            <div className="error">
              <p>❌ Error: {result.error}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## 📊 USING STATUS.MD INFRASTRUCTURE

### Leverage Existing Central Workflow:

```
STATUS.md → Already defines:
  ├── MCP Servers (twilio_hipaa, assemblyai, videosdk, nexhealth) ✅
  ├── API Registry (central/api-registry.yaml) ✅
  ├── Frontend Sync (central/frontend-sync.py) ✅
  └── Backend API Pattern (backend/routes/) ✅

New Production Demo:
  ├── Uses same servers ✅
  ├── Uses same backend infrastructure ✅
  ├── Adds user-facing forms (NEW)
  └── Shows real-world workflows (NEW)
```

---

## 🎯 DELIVERABLES

### For Manager Demo:

1. **Live Demo URL:** `http://localhost:5173/demo`
2. **7 Working Features:**
   - Patient Intake → Creates real FHIR Patient
   - Appointment Booking → Books in NexHealth
   - Insurance Verification → Checks eligibility
   - Clinical Triage → Safety-critical routing
   - HIPAA SMS → Sends filtered SMS
   - Video Consultation → Creates VideoSDK room
   - Medical Transcription → Transcribes audio

### Instead of showing:
```
✅ Structure Valid
✅ Syntax Valid
✅ 7 tools
```

### Show this:
```
[Patient Intake Form]
Name: John Doe
DOB: 1985-03-15
[Submit] → ✅ Patient MRN-12345 created in NexHealth

[Book Appointment]
Provider: Dr. Smith
Date: Nov 15, 2:00 PM
[Book] → ✅ Appointment confirmed, SMS sent

[Clinical Triage]
Complaint: Chest pain
[Assess] → 🚨 EMERGENT: Call 911 immediately
```

---

## 🚀 IMPLEMENTATION TIMELINE

### Week 1: Backend (Jr)
- [ ] Day 1-2: Create `backend/routes/healthcare_demo.py`
- [ ] Day 3: Implement 7 endpoint handlers
- [ ] Day 4-5: Connect to MCP servers (nexhealth, twilio, videosdk, assemblyai)

### Week 2: Frontend (Jr)
- [ ] Day 1: Create demo navigation and routing
- [ ] Day 2-3: Build 7 form components
- [ ] Day 4: Style and polish UI
- [ ] Day 5: End-to-end testing

### Week 3: Polish & Deploy
- [ ] Integration testing
- [ ] Error handling
- [ ] Production deployment
- [ ] Manager demo

---

## 📋 JR'S TASK LIST

### Priority 1: Backend Routes
1. Create `backend/routes/healthcare_demo.py`
2. Implement 7 POST endpoints:
   - `/api/v1/demo/healthcare/patient-intake`
   - `/api/v1/demo/healthcare/book-appointment`
   - `/api/v1/demo/healthcare/verify-insurance`
   - `/api/v1/demo/healthcare/triage`
   - `/api/v1/demo/healthcare/send-sms`
   - `/api/v1/demo/healthcare/create-video-room`
   - `/api/v1/demo/healthcare/transcribe-audio`
3. Connect each endpoint to corresponding MCP server tool
4. Return structured JSON responses

### Priority 2: Frontend Demo Pages
1. Create `frontend/src/pages/demo/` directory
2. Build `HealthcareDemoPage.tsx` (navigation)
3. Build 7 feature components:
   - `PatientIntakeForm.tsx`
   - `AppointmentBooking.tsx`
   - `InsuranceVerification.tsx`
   - `ClinicalTriage.tsx`
   - `HipaaSMS.tsx`
   - `VideoConsultation.tsx`
   - `MedicalTranscription.tsx`
4. Add route to `App.tsx`: `<Route path="/demo/*" element={<HealthcareDemoPage />} />`

### Priority 3: Integration
1. Test each feature end-to-end
2. Add error handling
3. Polish UI/UX
4. Write user guide

---

## 🎨 UI/UX DESIGN

### Demo Page Layout:

```
┌────────────────────────────────────────┐
│  Healthcare Receptionist - Live Demo   │
├────────────────────────────────────────┤
│  [Patient Intake] [Appointment] [...]  │  ← Tab Navigation
├────────────────────────────────────────┤
│                                        │
│  ┌──────────────────────────────────┐ │
│  │  Current Feature Form            │ │
│  │  ├── Input fields                │ │
│  │  ├── Submit button               │ │
│  │  └── Loading state               │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │  Live Result Display             │ │
│  │  ├── Success message             │ │
│  │  ├── Returned data               │ │
│  │  └── FHIR resource (expandable)  │ │
│  └──────────────────────────────────┘ │
│                                        │
└────────────────────────────────────────┘
```

---

## ✅ SUCCESS CRITERIA

### For Manager:
- ✅ Can visit `/demo` and see 7 working features
- ✅ Each feature performs real action (not mock)
- ✅ Results display immediately
- ✅ Professional UI/UX
- ✅ Production-ready demo

### For Team:
- ✅ Reuses existing infrastructure from STATUS.md
- ✅ No new servers needed
- ✅ Clear separation: tests (showcase) vs demo (production)
- ✅ Extensible for future features

---

## 📝 NEXT STEPS

1. **Zo:** Review and approve this plan
2. **Jr:** Start with Priority 1 (Backend Routes)
3. **Jr:** Move to Priority 2 (Frontend Pages)
4. **Team:** Test and polish
5. **Manager:** Demo meeting

---

**This plan leverages everything from STATUS.md while adding user-facing production features that showcase real capabilities, not just test results.**

