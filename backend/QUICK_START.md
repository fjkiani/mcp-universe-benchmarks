# Quick Start - Backend & Frontend

## 🚀 Start Both Servers

### **Terminal 1: Backend**
```bash
cd backend
python3 main.py
```
Server runs on: **http://localhost:8000**

### **Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```
Frontend runs on: **http://localhost:3000** or **http://localhost:5173**

---

## ✅ Test Endpoints

### **Backend Health**
```bash
curl http://localhost:8000/health
```

### **Sprint Metrics**
```bash
curl http://localhost:8000/api/v1/sprint/metrics
```

### **Tasks**
```bash
curl http://localhost:8000/api/v1/tasks
```

### **Servers**
```bash
curl http://localhost:8000/api/v1/servers
```

---

## 🌐 View in Browser

**Frontend Dashboard:**
- http://localhost:3000/dashboard
- http://localhost:5173/dashboard

**Backend API Docs:**
- http://localhost:8000/docs

---

## 📊 What You'll See

**Dashboard Shows:**
- Current Sprint: Sprint 3
- Tasks: 13/40 (32.5%)
- NexHealth: 8 tasks integrated
- Pass Rate: 100%
- Servers: 4/4 (100%)

**Tasks Page Shows:**
- 13 tasks with status
- NexHealth servers highlighted
- Pass rates from test results

