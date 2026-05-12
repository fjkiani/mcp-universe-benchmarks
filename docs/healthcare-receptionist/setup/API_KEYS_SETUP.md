# 🔑 API Keys Setup Guide

## ⚠️ **Important: I Don't Have Access to Your API Keys**

API keys are **NOT stored in the codebase** - they must be configured via environment variables for security.

---

## 🔐 **Required API Keys**

### **1. Authentication (Required)**
```bash
export SECRET_KEY="your-jwt-secret-key-here"
```
**Purpose:** JWT token signing for authentication  
**Generate:** Use a secure random string (32+ characters)

---

### **2. NexHealth (Optional - for EHR integration)**
```bash
export NEXHEALTH_API_KEY="your-nexhealth-api-key"
```
**Purpose:** Patient registration, appointment booking, insurance verification  
**Get from:** Contact NexHealth for API access  
**Note:** Works in mock mode without this key

---

### **3. Twilio HIPAA (Optional - for SMS)**
```bash
export TWILIO_ACCOUNT_SID="your-account-sid"
export TWILIO_AUTH_TOKEN="your-auth-token"
```
**Purpose:** HIPAA-compliant SMS messaging  
**Get from:** https://console.twilio.com/  
**Note:** Works in mock mode without these keys

---

### **4. VideoSDK (Optional - for video consultations)**
```bash
export VIDEOSDK_API_KEY="your-videosdk-api-key"
export VIDEOSDK_SECRET_KEY="your-videosdk-secret-key"
```
**Purpose:** Video consultation rooms, recording  
**Get from:** https://app.videosdk.live/api-keys  
**Free tier:** 10,000 minutes/month  
**Note:** Works in mock mode without these keys

---

### **5. AssemblyAI (Optional - for transcription)**
```bash
export ASSEMBLYAI_API_KEY="your-assemblyai-api-key"
```
**Purpose:** Medical transcription (93.3% accuracy)  
**Get from:** https://www.assemblyai.com/app/account  
**Free tier:** Available  
**Note:** Works in mock mode without this key

---

## 🚀 **Setup Instructions**

### **Option 1: Environment Variables (Recommended)**

Create a `.env` file in the `backend/` directory:

```bash
# .env file
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./healthcare_receptionist.db

# Optional API keys (for real integrations)
NEXHEALTH_API_KEY=your-key-here
TWILIO_ACCOUNT_SID=your-sid-here
TWILIO_AUTH_TOKEN=your-token-here
VIDEOSDK_API_KEY=your-key-here
VIDEOSDK_SECRET_KEY=your-secret-here
ASSEMBLYAI_API_KEY=your-key-here

# Mock mode (default: true - works without API keys)
DEMO_MOCK_MODE=true
```

Then load in your code:
```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file
```

### **Option 2: Export in Shell**

```bash
export SECRET_KEY="your-secret-key"
export NEXHEALTH_API_KEY="your-key"
export TWILIO_ACCOUNT_SID="your-sid"
export TWILIO_AUTH_TOKEN="your-token"
export VIDEOSDK_API_KEY="your-key"
export VIDEOSDK_SECRET_KEY="your-secret"
export ASSEMBLYAI_API_KEY="your-key"
```

---

## 🎭 **Mock Mode (Default)**

**The system works WITHOUT API keys in mock mode!**

```bash
export DEMO_MOCK_MODE=true  # Default
```

**What mock mode does:**
- ✅ Returns realistic mock responses
- ✅ Perfect for development and demos
- ✅ No external API calls
- ✅ No costs
- ✅ Works immediately

**To use real APIs:**
```bash
export DEMO_MOCK_MODE=false
# Then provide the required API keys
```

---

## 🔒 **Security Best Practices**

### **✅ DO:**
- Store API keys in environment variables
- Use `.env` file (add to `.gitignore`)
- Rotate keys regularly
- Use different keys for dev/staging/production
- Restrict API key permissions when possible

### **❌ DON'T:**
- Commit API keys to git
- Hardcode keys in source code
- Share keys in chat/email
- Use production keys in development

---

## 📋 **Current Status**

### **What Works Without Keys:**
- ✅ Authentication (needs SECRET_KEY only)
- ✅ Patient management
- ✅ Appointment management
- ✅ Dashboard
- ✅ All features in mock mode

### **What Needs Keys (Optional):**
- ⏳ Real NexHealth EHR integration
- ⏳ Real Twilio SMS sending
- ⏳ Real VideoSDK video calls
- ⏳ Real AssemblyAI transcription

---

## 🎯 **Quick Start**

### **Minimum Setup (Works Immediately):**
```bash
export SECRET_KEY="change-this-to-random-string"
export DEMO_MOCK_MODE=true
```

### **Full Setup (Real APIs):**
1. Get API keys from each service
2. Add to `.env` file
3. Set `DEMO_MOCK_MODE=false`
4. Restart backend

---

## 📝 **Example .env File**

```bash
# Required
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-min-32-chars

# Database (SQLite for dev, PostgreSQL for production)
DATABASE_URL=sqlite:///./healthcare_receptionist.db

# Mock mode (works without API keys)
DEMO_MOCK_MODE=true

# Optional: Real API keys (uncomment and add when ready)
# NEXHEALTH_API_KEY=
# TWILIO_ACCOUNT_SID=
# TWILIO_AUTH_TOKEN=
# VIDEOSDK_API_KEY=
# VIDEOSDK_SECRET_KEY=
# ASSEMBLYAI_API_KEY=
```

---

## ✅ **Summary**

- **I don't have access to your API keys** - they're stored in your environment
- **Mock mode works without keys** - perfect for development
- **Real APIs need keys** - get them from each service
- **Store keys securely** - use environment variables, never commit to git

**The product works immediately in mock mode - no API keys needed to get started!** 🚀




