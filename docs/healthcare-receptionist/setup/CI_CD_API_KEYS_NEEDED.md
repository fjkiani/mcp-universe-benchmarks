# CI/CD API Keys Needed for Healthcare Servers

**For:** GitHub Actions pipeline (automated testing)

## Required Secrets

### 1. Twilio HIPAA Server
- `TWILIO_ACCOUNT_SID` - Twilio account identifier
- `TWILIO_AUTH_TOKEN` - Twilio authentication token
- `TWILIO_PHONE_NUMBER` - Twilio phone number (format: +1234567890)

### 2. AssemblyAI Server
- `ASSEMBLYAI_API_KEY` - AssemblyAI API key

### 3. VideoSDK Server
- `VIDEOSDK_API_KEY` - VideoSDK API key
- `VIDEOSDK_SECRET_KEY` - VideoSDK secret key (JWT token)

### 4. NexHealth Server
- `NEXHEALTH_API_KEY` - NexHealth API key
- `NEXHEALTH_API_URL` - NexHealth API URL (optional, defaults to https://api.nexhealth.com)

---

## Total: 7 Secrets

**Required (6):**
1. `TWILIO_ACCOUNT_SID`
2. `TWILIO_AUTH_TOKEN`
3. `TWILIO_PHONE_NUMBER`
4. `ASSEMBLYAI_API_KEY`
5. `VIDEOSDK_API_KEY`
6. `VIDEOSDK_SECRET_KEY`
7. `NEXHEALTH_API_KEY`

**Optional (1):**
- `NEXHEALTH_API_URL` (has default value)

---

## Where to Add

**GitHub Repository:** `lbx_mcp_universe_mcp_servers_mothership`

**Path:** Settings → Secrets and variables → Actions → New repository secret

---

## Note

These keys are already configured locally for development. Adding them to GitHub Actions secrets will enable:
- Automated API testing in CI/CD
- Functional test validation
- Real API integration tests

---

**Status:** Ready to add to GitHub Actions secrets

