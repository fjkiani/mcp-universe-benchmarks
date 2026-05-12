# 🧪 Frontend Testing Guide

## Quick Start

### 1. Start Backend
```bash
cd backend
python main.py
```
✅ Backend runs on `http://localhost:8000`

### 2. Start Frontend
```bash
cd frontend
npm run dev
```
✅ Frontend runs on `http://localhost:5173`

### 3. Navigate to Demo
Open browser: **`http://localhost:5173/demo`**

Click **"Video Consultation"** tab (or go to `http://localhost:5173/demo#video`)

---

## Test Video Consultation Flow

### Step 1: Create Room
1. Fill in **Patient ID** (e.g., `MRN-12345`)
2. Fill in **Provider ID** (e.g., `dr_smith`)
3. Optionally add **Appointment ID**
4. Click **"Create Video Room"**
5. ✅ You should see: "Room Created Successfully!" with Room ID

### Step 2: Join as Patient
1. Click **"Join as Patient"** button
2. ✅ Video player should appear
3. Click **"Join Consultation"** button in player
4. ✅ You should see your video feed

### Step 3: Join as Provider
1. Scroll down to Provider View
2. Click **"Join as Provider"** button
3. ✅ Second video player appears
4. Click **"Join Consultation"** button
5. ✅ Provider video feed appears

### Step 4: Start Recording
1. In either player, click **"Start Recording"** button
2. ✅ Recording indicator should appear
3. ✅ Button changes to "Stop Recording"

### Step 5: Stop Recording & Auto-Transcribe
1. Click **"Stop Recording"** button
2. ✅ Recording stops
3. ✅ Transcription automatically starts (loading...)
4. ✅ Transcription results appear below:
   - Full transcription text
   - Medical entities (symptoms, medications, etc.)
   - Confidence score

---

## What to Expect

### Mock Mode (Default)
- ✅ Room creation works (mock room ID)
- ✅ Token generation works (mock token)
- ✅ Video player loads (but may show placeholder)
- ✅ Recording works (mock recording ID)
- ✅ Transcription works (mock transcription)

### Real Mode (With API Keys)
Set environment variables:
```bash
export DEMO_MOCK_MODE=false
export VIDEOSDK_API_KEY=your-videosdk-api-key
export VIDEOSDK_SECRET_KEY=your-videosdk-secret
export ASSEMBLYAI_API_KEY=your-assemblyai-api-key
```

Then:
- ✅ Real VideoSDK rooms created
- ✅ Real video streaming
- ✅ Real recordings on VideoSDK servers
- ✅ Real AssemblyAI transcription
- ✅ Everything stored in database

---

## Troubleshooting

### Backend not running?
```bash
cd backend
python main.py
```
Check: `http://localhost:8000/docs` should show API docs

### Frontend not running?
```bash
cd frontend
npm run dev
```
Check: `http://localhost:5173` should load

### VideoSDK not installed?
```bash
cd frontend
npm install @videosdk.live/react-sdk
```

### CORS errors?
Backend should have CORS enabled (already configured in `main.py`)

### API errors?
Check browser console (F12) for error messages
Check backend terminal for error logs

---

## Full Test Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Navigate to `/demo`
- [ ] Click "Video Consultation" tab
- [ ] Create room successfully
- [ ] Join as patient
- [ ] Join as provider
- [ ] Start recording
- [ ] Stop recording
- [ ] See transcription results
- [ ] Check database for stored consultation (if real mode)

---

## Database Check (Real Mode)

After a session, check stored consultation:
```bash
# In backend directory
python -c "
from database.session import SessionLocal
from database.models import VideoConsultation
db = SessionLocal()
consultations = db.query(VideoConsultation).all()
for c in consultations:
    print(f'Room: {c.room_id}, Transcript: {c.transcript_text[:50]}...')
"
```

Or use API:
```bash
curl http://localhost:8000/api/v1/video/consultations
```




