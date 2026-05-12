# ClearMyMind Sandbox Datasets

No hardware. No HIPAA liability. Real EDI payloads. Real clinical text. 200 synthetic claims with built-in denial patterns. Let's prove it end-to-end.

---

## 📁 Directory Structure

```
datasets/
├── edi_samples/
│   ├── 270_eligibility_request.edi   ← X12 270 — Fire at any payer sandbox (Availity, CHC)
│   ├── 271_eligibility_response.edi  ← X12 271 — Parsed to extract copay/deductible
│   └── 837_professional_claim.edi    ← X12 837P — Intentional modifier-25 error for scrubber demo
├── soap_notes/
│   └── medical_transcriptions.json   ← 50 real de-identified transcriptions (HuggingFace)
└── claims/
    ├── synthetic_claims_200.json     ← 200 synthetic claims with denial flags
    └── synthetic_claims_200.csv      ← Same data in CSV for data science workflows
```

---

## 📦 Data Sources

| File | Source | License |
|------|--------|---------|
| `medical_transcriptions.json` | [rungalileo/medical_transcription_40](https://huggingface.co/datasets/rungalileo/medical_transcription_40) | Public HuggingFace |
| `270/271/837 EDI samples` | Synthetic, based on X12 5010 transaction specs | ASME X12 public spec |
| `synthetic_claims_200.*` | Generated locally — ICD-10, CPT, payer rules | Synthetic |

---

## 🔬 Agent Proof Targets

### Agent 1: Front-Desk Receptionist
- Input: `270_eligibility_request.edi`
- Output: `271_eligibility_response.edi` → parse copay → fire Twilio mock
- Sandbox: [Availity Sandbox](https://availity.com) | [Change Healthcare Dev Portal](https://developers.changehealthcare.com)

### Agent 2: Post-Visit Analyzer
- Input: any record from `medical_transcriptions.json` (field: `text`)
- Pipeline: AssemblyAI transcription → ICD-10 mapping → SOAP note generation → FHIR R4 bundle
- API key needed: AssemblyAI (free tier covers this)

### Agent 3: Claims Intelligence
- Input: `synthetic_claims_200.csv`
- Target: flag `denial_predicted: true` records before submission
- 70% of records have embedded denial rules — prove the scrubber catches them

---

## 🚀 Next Move

Pick one agent and go end-to-end. Record it. That's the proof.
