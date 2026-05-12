// Features Configuration - Component-ready feature cards
export const featuresConfig = [
  {
    title: "Universal EHR Integration",
    highlight: "⭐",
    description: "The Problem: Most healthcare AI tools support 1-2 EHR systems. You need one that works with yours.",
    solution: "80+ EHR systems supported (Epic, Cerner, athenahealth, drchrono, Dentrix, Eaglesoft, etc.)",
    benefits: [
      "Single API - Works with all of them",
      "Real-time sync - No batch processing delays",
      "Bidirectional - Reads and writes to EHR"
    ],
    impact: "Most practices can't use AI receptionists because they don't support their EHR. We support **80x more EHRs** than competitors."
  },
  {
    title: "Real-Time Appointment Scheduling",
    highlight: "⚡",
    description: "Traditional Way: 12 minutes per appointment",
    traditional: [
      "Receptionist checks EHR calendar (2 min)",
      "Calls patient back (5 min)",
      "Manually enters appointment (3 min)",
      "Sends confirmation (2 min)"
    ],
    ourWay: [
      "AI checks EHR availability (<1 sec)",
      "Books appointment directly in EHR (<1 sec)",
      "Sends confirmation automatically (<1 sec)"
    ],
    result: "**240x faster** appointment scheduling (3 seconds vs 12 minutes)"
  },
  {
    title: "Instant Insurance Verification",
    highlight: "⚡",
    description: "Traditional Way: 15 minutes per patient",
    traditional: [
      "Phone call to insurance (5 min wait)",
      "Manual data entry (5 min)",
      "Verification call (5 min)"
    ],
    ourWay: [
      "Real-time API call to insurance (2 sec)",
      "Automatic eligibility check",
      "Benefits extracted automatically"
    ],
    result: "**450x faster** insurance verification (2 seconds vs 15 minutes)"
  },
  {
    title: "Safety-Critical Triage",
    highlight: "🛡️",
    description: "The Problem: 40% of emergent cases (chest pain, stroke) are misrouted, leading to delayed care.",
    solution: "100% accuracy on emergent triage (safety-critical)",
    benefits: [
      "Immediate routing to 911/ER (not routine appointments)",
      "FHIR-compliant documentation",
      "Audit trail for compliance"
    ],
    impact: "One misrouted chest pain call can be fatal. Our AI has **100% accuracy** on emergent cases."
  },
  {
    title: "HIPAA-Compliant by Design",
    highlight: "🔒",
    description: "Built-in Compliance:",
    benefits: [
      "PHI detection - Automatically blocks PHI in SMS/email",
      "Audit logging - Every action is logged",
      "BAA available - Business Associate Agreement for all APIs",
      "Encryption - End-to-end encryption for all data",
      "Access controls - Role-based access management"
    ],
    impact: "Most AI tools require manual HIPAA compliance. Ours is **built-in from day one**."
  },
  {
    title: "24/7 Coverage",
    highlight: "🌙",
    description: "The Problem: Practices lose $50K/year in missed after-hours calls.",
    solution: "Never sleeps - Answers calls 24/7",
    benefits: [
      "No overtime - No additional staffing costs",
      "Instant response - No hold time",
      "Consistent quality - Same service every time"
    ],
    impact: "Capture **100% of patient calls**, even at 2 AM."
  }
]

