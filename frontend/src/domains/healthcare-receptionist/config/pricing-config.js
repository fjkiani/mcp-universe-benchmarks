// Pricing Configuration
export const pricingConfig = {
  headline: "Simple, Transparent Pricing",
  tiers: [
    {
      name: "Starter Plan",
      price: "$499/month",
      features: [
        "Up to 500 appointments/month",
        "1 EHR integration",
        "Basic scheduling & reminders",
        "Email support"
      ]
    },
    {
      name: "Professional Plan",
      price: "$1,499/month",
      features: [
        "Up to 2,000 appointments/month",
        "Unlimited EHR integrations",
        "Insurance verification",
        "Triage capabilities",
        "Priority support"
      ],
      popular: true
    },
    {
      name: "Enterprise Plan",
      price: "Custom pricing",
      features: [
        "Unlimited appointments",
        "Custom integrations",
        "Dedicated support",
        "SLA guarantees",
        "Custom training"
      ]
    }
  ],
  includedInAll: [
    "HIPAA compliance",
    "24/7 coverage",
    "Real-time EHR sync",
    "No setup fees",
    "14-day free trial"
  ]
}

