# 🎯 Demo Build Plan - Source of Truth

## 📋 **Source of Truth**
**Primary:** `.cursor/rules/healthcare-receptionist/PRODUCTION_APP_PLAN.md`

## 🎯 **7 Core Capabilities to Build**

1. ✅ **Patient Intake** - Collect demographics, insurance, create FHIR Patient resource
2. ✅ **Appointment Scheduling** - Book appointments with NexHealth EHR integration
3. ✅ **Insurance Verification** - Check eligibility, prior authorization
4. ✅ **Clinical Triage** - Safety-critical routing (chest pain → 911, mild → routine)
5. ✅ **HIPAA Communication** - SMS/Email with PHI detection and filtering
6. ✅ **Video Consultation** - VideoSDK room creation
7. ✅ **Medical Transcription** - AssemblyAI audio transcription with entity extraction

---

## ✅ **Current Status**

### **Backend:**
- ✅ Routes exist: `backend/api/routers/healthcare_demo.py`
- ✅ MCP client service: `backend/services/mcp_client_service.py`
- ⚠️ Currently in mock mode (needs real API keys)

### **Frontend:**
- ✅ All 7 forms exist: `frontend/src/pages/demo/`
- ✅ Demo page: `HealthcareDemoPage.jsx`
- ✅ Routes configured

### **API Keys:**
- ✅ Available in `GITHUB_SECRETS_VALUES.md`
- ⚠️ Need to configure in environment

---

## 🚀 **Implementation Plan**

### **Step 1: Configure Real API Keys**
- Update MCP client service to use real keys
- Set `DEMO_MOCK_MODE=false`
- Configure all 7 API keys from secrets file

### **Step 2: Verify Backend Routes**
- Ensure all 7 endpoints call real MCP servers
- Test each capability end-to-end
- Fix any integration issues

### **Step 3: Enhance Frontend**
- Ensure all forms connect to backend
- Add real-time feedback
- Show actual API responses

### **Step 4: End-to-End Testing**
- Test all 7 capabilities with real APIs
- Verify data flows correctly
- Ensure error handling works

---

## 📊 **Progress Tracking**

| Capability | Backend | Frontend | API Keys | Status |
|------------|---------|----------|----------|--------|
| Patient Intake | ✅ | ✅ | ✅ | 🟡 Needs real API |
| Appointment Scheduling | ✅ | ✅ | ✅ | 🟡 Needs real API |
| Insurance Verification | ✅ | ✅ | ✅ | 🟡 Needs real API |
| Clinical Triage | ✅ | ✅ | N/A | ✅ Complete |
| HIPAA SMS | ✅ | ✅ | ✅ | 🟡 Needs real API |
| Video Consultation | ✅ | ✅ | ✅ | 🟡 Needs real API |
| Medical Transcription | ✅ | ✅ | ✅ | 🟡 Needs real API |

**Legend:**
- ✅ Complete
- 🟡 Needs real API integration
- ⏳ In progress

---

## 🎯 **Goal**

**Build a complete, end-to-end demo where all 7 capabilities work with REAL APIs, not mocks.**

