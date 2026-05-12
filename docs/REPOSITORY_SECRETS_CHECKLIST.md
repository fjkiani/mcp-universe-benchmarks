# Repository secrets checklist (names only)

Use your platform’s secret store (e.g. GitHub Actions → Secrets). **Do not commit real values.**

For healthcare demo / MCP CI, typical names:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `ASSEMBLYAI_API_KEY`
- `VIDEOSDK_API_KEY`
- `VIDEOSDK_SECRET_KEY`
- `NEXHEALTH_API_KEY`
- `NEXHEALTH_API_URL` (optional; often `https://api.nexhealth.com`)

Copy values from each vendor console into `.env` locally; never paste them into tracked files.
