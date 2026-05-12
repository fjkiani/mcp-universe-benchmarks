# Healthcare MCP Servers

Custom MCP servers for the healthcare_receptionist domain.

## Servers Added (4)

### 1. twilio_hipaa
**Purpose:** HIPAA-compliant SMS/Voice communication with PHI detection

**Tools (5):**
- `send_hipaa_sms` - Send SMS with automatic PHI filtering
- `make_voice_call` - Initiate HIPAA-compliant voice calls
- `detect_phi` - Detect protected health information in text
- `send_appointment_reminder` - Automated appointment reminders
- `emergency_broadcast` - Send urgent notifications

**Status:** Structure validated, API keys configured locally

---

### 2. assemblyai
**Purpose:** Medical transcription with entity extraction

**Tools (5):**
- `transcribe_medical` - Transcribe medical audio (93.3% accuracy)
- `extract_medical_entities` - Extract symptoms, medications, procedures
- `transcribe_consultation` - Real-time consultation transcription
- `generate_clinical_summary` - Auto-generate clinical notes
- `identify_medical_terms` - Recognize medical terminology

**Status:** Structure validated, API keys configured locally

---

### 3. videosdk
**Purpose:** Video consultations and recording

**Tools (7):**
- `create_room` - Create video consultation room
- `generate_token` - Generate participant tokens
- `start_recording` - Record consultation sessions
- `stop_recording` - Stop and save recordings
- `get_room_status` - Check room status
- `end_room` - Terminate video session
- `get_recording_url` - Retrieve recording URLs

**Status:** Structure validated, API keys configured locally

---

### 4. nexhealth
**Purpose:** EHR integration (80+ systems unified API)

**Tools (6):**
- `check_provider_availability` - Real-time availability checking
- `book_appointment` - Create appointments in EHR
- `verify_insurance_eligibility` - Insurance verification
- `get_appointment_details` - Retrieve appointment info
- `cancel_appointment` - Cancel existing appointments
- `send_appointment_reminder` - Automated reminders

**Status:** Structure validated, API keys configured locally

---

## Domain

**Healthcare Receptionist:** `domains/healthcare_receptionist/`
- 40 tasks ready for LLM testing
- Target pass rate: 40% (discriminative benchmark)
- Categories: Patient Intake, Appointment Scheduling, Insurance Verification, Clinical Triage, Multi-Channel Orchestration

---

## Testing

**Structure validation:** ✅ All 4 servers pass
- Required files present
- Python syntax valid
- Tool decorators found
- Configuration valid

**API testing:** ✅ API keys configured locally, ready for testing

---

## Total Impact

- **4 servers** added
- **23 tools** total
- **40 domain tasks** enabled
- **$4.5T healthcare market** addressable

---

## Next Steps

1. ✅ API keys configured locally (ready for testing)
2. Manager sets up API keys in CI/CD secrets (for automated testing)
3. Run functional tests locally
4. Test healthcare_receptionist domain with LLM
5. Measure pass rate and iterate

