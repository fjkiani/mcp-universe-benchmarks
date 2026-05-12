# Frontend - Reusable Landing Page System

**Vite.js + React + TypeScript**

---

## 📚 Documentation

### **Core Architecture:**
- **`FRONTEND_ARCHITECTURE.md`** - Complete guide: structure, integration, data flow, development
- **`COMPONENT_ARCHITECTURE.md`** - Component design patterns, specialized components
- **`DESIGN_SYSTEM.md`** - Visual design system, components, design tokens

### **Landing Pages:**
- **`HOW_TO_CREATE_NEW_LANDING_PAGE.md`** - Step-by-step guide to create new landing pages
- **`REUSABLE_LANDING_PAGE_ARCHITECTURE.md`** - Reusable architecture details
- **`components/landing/COMPONENT_API.md`** - Component API documentation

### **Quick References:**
- **`REUSABLE_ARCHITECTURE_SUMMARY.md`** - Quick summary of reusable architecture

---

## 🚀 Quick Start

### **1. Install Dependencies:**
```bash
cd frontend
npm install
```

### **2. Start Development Server:**
```bash
npm run dev
# Opens on http://localhost:5173
```

### **3. Start Backend (Optional):**
```bash
cd backend
python3 main.py
# Backend runs on http://localhost:8000
```

---

## 📖 Key Concepts

### **Reusable Architecture:**
- **Domain-agnostic components** - Work for any product
- **Config-driven** - Content, visual, behavior separated
- **Visual constants** - Shared design system
- **< 1 hour** to create new landing page

### **Component Pattern:**
```jsx
<Component config={config} />
// Config contains: { content, visual, behavior }
```

### **Backend Integration:**
- ✅ Fully connected to FastAPI backend
- ✅ Automatic fallback to JSON if backend unavailable
- ✅ Real-time data from tasks, tests, sprint metrics

---

## 🎯 Pages

- `/` - Landing page (Healthcare Receptionist)
- `/dashboard` - Sprint metrics & progress
- `/showcase` - API status & tests
- `/servers` - Server status
- `/tasks` - Task progress

---

**Status:** ✅ Production-Ready  
**Architecture:** Reusable, DRY, Config-Driven  
**Design:** SaaS/YC-Style, Interactive, Visual
