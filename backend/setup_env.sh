#!/bin/bash
# Example: export demo API variables from your local .env (do not commit real values).
#
# Usage:
#   cp backend/.env.example backend/.env   # if you maintain one
#   set -a && source backend/.env && set +a
#   ./backend/setup_env.sh
#
# Or export the variables below manually before starting the backend.

echo "🔧 Example environment setup (set real values in shell or backend/.env)"

export SECRET_KEY="${SECRET_KEY:-change-me-in-production}"
export DATABASE_URL="${DATABASE_URL:-sqlite:///./healthcare_receptionist.db}"
export DEMO_MOCK_MODE="${DEMO_MOCK_MODE:-false}"

# Required for real demos — set in your environment; never commit literals.
: "${NEXHEALTH_API_KEY:?Set NEXHEALTH_API_KEY}"
: "${NEXHEALTH_API_URL:=https://api.nexhealth.com}"
: "${TWILIO_ACCOUNT_SID:?Set TWILIO_ACCOUNT_SID}"
: "${TWILIO_AUTH_TOKEN:?Set TWILIO_AUTH_TOKEN}"
: "${TWILIO_PHONE_NUMBER:?Set TWILIO_PHONE_NUMBER}"
: "${VIDEOSDK_API_KEY:?Set VIDEOSDK_API_KEY}"
: "${VIDEOSDK_SECRET_KEY:?Set VIDEOSDK_SECRET_KEY}"
: "${ASSEMBLYAI_API_KEY:?Set ASSEMBLYAI_API_KEY}"

echo "✅ Environment variables are present (values not printed)."
echo "Start backend:  cd backend && python main.py"
