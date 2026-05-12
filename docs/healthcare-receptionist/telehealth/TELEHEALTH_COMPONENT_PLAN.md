# 🎯 Telehealth Component Plan - Modular Approach

## 📋 **Source of Truth**
**Implementation Guide:** `ENHANCED_TELEHEALTH_IMPLEMENTATION.md`

## 🎯 **Goal**
Build a complete telehealth session with embedded video player and auto-transcription using a **modular, component-based approach**.

---

## 🧩 **Component Architecture**

### **Backend Components:**
1. `VideoTokenService` - Token generation logic
2. `RecordingService` - Recording management
3. `TranscriptionService` - Transcription pipeline

### **Frontend Components:**
1. `VideoSDKPlayer` - Core video player component
2. `VideoControls` - Control buttons (mic, camera, record)
3. `VideoParticipant` - Individual participant view
4. `VideoRoom` - Room container/wrapper
5. `TranscriptionDisplay` - Show transcription results
6. `TokenGenerator` - Handle token generation UI

---

## 📦 **Component Breakdown**

### **1. Backend: Token Generation**
- **File:** `backend/api/routers/video.py` (new router)
- **Endpoint:** `POST /api/v1/video/generate-token`
- **Purpose:** Generate VideoSDK tokens for participants

### **2. Backend: Recording Management**
- **File:** `backend/api/routers/video.py`
- **Endpoints:**
  - `POST /api/v1/video/recordings/start`
  - `POST /api/v1/video/recordings/stop`
  - `GET /api/v1/video/recordings/{id}/status`

### **3. Backend: Transcription Pipeline**
- **File:** `backend/api/routers/video.py`
- **Endpoint:** `POST /api/v1/video/transcribe-recording`
- **Purpose:** Auto-transcribe after recording stops

### **4. Frontend: VideoSDK Player (Core)**
- **File:** `frontend/src/components/video/VideoSDKPlayer.jsx`
- **Purpose:** Main video player component
- **Props:** `roomId`, `token`, `onJoin`, `onLeave`

### **5. Frontend: Video Controls**
- **File:** `frontend/src/components/video/VideoControls.jsx`
- **Purpose:** Mic, camera, record controls
- **Props:** `onToggleMic`, `onToggleCamera`, `onStartRecording`, `onStopRecording`

### **6. Frontend: Participant View**
- **File:** `frontend/src/components/video/VideoParticipant.jsx`
- **Purpose:** Display single participant video
- **Props:** `participantId`, `name`, `stream`

### **7. Frontend: Video Room Container**
- **File:** `frontend/src/components/video/VideoRoom.jsx`
- **Purpose:** Wraps MeetingProvider and manages room state
- **Props:** `roomId`, `token`, `participants`

### **8. Frontend: Transcription Display**
- **File:** `frontend/src/components/video/TranscriptionDisplay.jsx`
- **Purpose:** Show transcription and medical entities
- **Props:** `transcription`, `entities`, `loading`

### **9. Frontend: Token Generator**
- **File:** `frontend/src/components/video/TokenGenerator.jsx`
- **Purpose:** Handle token generation UI
- **Props:** `roomId`, `participantName`, `role`, `onTokenGenerated`

---

## 🚀 **Implementation Order**

1. ✅ Backend token generation endpoint
2. ✅ Backend recording endpoints
3. ✅ Backend transcription endpoint
4. ✅ Frontend: VideoSDKPlayer (core)
5. ✅ Frontend: VideoControls
6. ✅ Frontend: VideoParticipant
7. ✅ Frontend: VideoRoom (wrapper)
8. ✅ Frontend: TranscriptionDisplay
9. ✅ Frontend: TokenGenerator
10. ✅ Integrate into VideoConsultation page

---

## 📁 **File Structure**

```
backend/
├── api/routers/
│   └── video.py                    # New: Video endpoints

frontend/
├── src/
│   ├── components/
│   │   └── video/
│   │       ├── VideoSDKPlayer.jsx      # Core player
│   │       ├── VideoControls.jsx       # Controls
│   │       ├── VideoParticipant.jsx    # Participant view
│   │       ├── VideoRoom.jsx           # Room wrapper
│   │       ├── TranscriptionDisplay.jsx # Transcription UI
│   │       └── TokenGenerator.jsx      # Token UI
│   └── pages/demo/
│       └── VideoConsultation.jsx       # Updated to use components
```

---

## ✅ **Principles**

1. **Single Responsibility** - Each component does one thing
2. **Reusability** - Components can be used independently
3. **Composability** - Components compose together
4. **Testability** - Easy to test in isolation
5. **Maintainability** - Clear, focused code

---

**Let's build this step by step, one component at a time!** 🚀




