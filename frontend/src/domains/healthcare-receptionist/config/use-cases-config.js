// Use Cases Configuration
export const useCasesConfig = [
  {
    title: "Primary Care Practice",
    before: {
      costs: [
        "3 receptionists @ $50K/year = $150K/year",
        "30% no-show rate = $75K/year lost revenue",
        "15 min per insurance verification = $30K/year lost time"
      ]
    },
    after: {
      costs: [
        "1 AI receptionist @ $5K/year = $5K/year",
        "50% reduction in no-shows = $37.5K/year saved",
        "2 sec insurance verification = $30K/year saved"
      ]
    },
    roi: "$207.5K/year saved (4,150% ROI)"
  },
  {
    title: "Multi-Location Health System",
    challenge: "10 locations, each with different EHR systems (Epic, Cerner, athenahealth)",
    solution: "Single AI receptionist works with all 10 EHRs via unified API",
    result: [
      "$500K/year saved (vs. 10 receptionists)",
      "Consistent patient experience across all locations",
      "Centralized management and reporting"
    ]
  },
  {
    title: "Urgent Care Clinic",
    challenge: "24/7 coverage, high triage accuracy required",
    solution: "AI receptionist with 100% emergent triage accuracy",
    result: [
      "Zero missed emergent cases",
      "$100K/year saved on overnight staffing",
      "Faster patient routing (3 sec vs. 5 min)"
    ]
  }
]

