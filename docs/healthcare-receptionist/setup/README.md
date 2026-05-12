# Setup Documentation

**API keys and configuration setup guides**

---

## Files

| File | Purpose |
|------|---------|
| **[API_KEYS_SETUP.md](API_KEYS_SETUP.md)** | Complete guide for setting up API keys - environment variables, mock mode, security |
| **[API_KEYS_CONFIRMATION.md](API_KEYS_CONFIRMATION.md)** | Confirmation of required API keys for CI/CD pipeline (7 secrets) |
| **[CI_CD_API_KEYS_NEEDED.md](CI_CD_API_KEYS_NEEDED.md)** | API keys needed for GitHub Actions CI/CD pipeline |

---

## Quick Start

**For local development:**
1. **[API_KEYS_SETUP.md](API_KEYS_SETUP.md)** - Complete setup guide with all options

**For CI/CD:**
1. **[API_KEYS_CONFIRMATION.md](API_KEYS_CONFIRMATION.md)** - List of required secrets
2. **[CI_CD_API_KEYS_NEEDED.md](CI_CD_API_KEYS_NEEDED.md)** - CI/CD specific requirements

---

## Required API Keys

### For Local Development:
- `SECRET_KEY` (required) - JWT token signing
- `NEXHEALTH_API_KEY` (optional) - EHR integration
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` (optional) - SMS
- `VIDEOSDK_API_KEY`, `VIDEOSDK_SECRET_KEY` (optional) - Video consultations
- `ASSEMBLYAI_API_KEY` (optional) - Transcription

### For CI/CD Pipeline:
- All 7 secrets listed in [API_KEYS_CONFIRMATION.md](API_KEYS_CONFIRMATION.md)

**Note:** Mock mode works without API keys for development and demos.

---

**Last Updated:** 2025-01-XX






