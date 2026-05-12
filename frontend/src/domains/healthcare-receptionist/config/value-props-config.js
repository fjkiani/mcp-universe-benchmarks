// Value Propositions Configuration - Business-focused benefits
export const valuePropsConfig = {
  title: "Accelerate Your Healthcare AI Development",
  subtitle: "Stop building integrations from scratch. Use battle-tested MCP servers that handle the complexity for you.",
  layout: "3-column", // 2-column, 3-column, 4-column
  values: [
    {
      id: "ship-faster",
      icon: "⚡",
      iconGradient: ["from-yellow-400", "to-orange-500"],
      title: "Ship Faster",
      description: "Pre-built integrations for NexHealth, Twilio, AssemblyAI, and VideoSDK. Go from idea to production in days, not months.",
      metrics: [
        { 
          label: "Time to Production", 
          value: "1 day",
          color: "green",
          comparison: "vs 3-6 months"
        },
        { 
          label: "Setup Time", 
          value: "20 min",
          color: "blue",
          comparison: "vs weeks"
        }
      ],
      benefits: [
        { text: "Ready-to-use API wrappers", icon: "✅" },
        { text: "Production-tested reliability", icon: "✅" },
        { text: "Automatic updates & maintenance", icon: "✅" }
      ],
      cta: {
        text: "View Servers",
        link: "/servers"
      },
      animation: "pulse"
    },
    {
      id: "integrate-seamlessly",
      icon: "🔗",
      iconGradient: ["from-blue-500", "to-purple-500"],
      title: "Integrate Seamlessly",
      description: "MCP protocol ensures your AI agents can communicate with any system. Add new capabilities without rewriting code.",
      metrics: [
        { 
          label: "Supported EHRs", 
          value: "80+",
          color: "purple",
          comparison: "vs 1-5 competitors"
        },
        { 
          label: "API Tools", 
          value: "23",
          color: "blue",
          comparison: "and growing"
        }
      ],
      benefits: [
        { text: "Standard MCP interface", icon: "🔌" },
        { text: "Works with any LLM", icon: "🤖" },
        { text: "Modular architecture", icon: "🧩" }
      ],
      cta: {
        text: "See Integration",
        link: "/showcase"
      },
      animation: "bounce"
    },
    {
      id: "stay-compliant",
      icon: "🛡️",
      iconGradient: ["from-green-500", "to-emerald-500"],
      title: "Stay Compliant",
      description: "Built-in HIPAA compliance, PHI detection, and audit logging. Security and compliance handled from day one.",
      metrics: [
        { 
          label: "Compliance", 
          value: "SOC 2",
          color: "green",
          comparison: "Type II certified"
        },
        { 
          label: "Uptime", 
          value: "99.9%",
          color: "blue",
          comparison: "SLA guaranteed"
        }
      ],
      benefits: [
        { text: "Automated PHI detection", icon: "🔍" },
        { text: "Complete audit trails", icon: "📋" },
        { text: "BAA agreements included", icon: "📄" }
      ],
      cta: {
        text: "Security Docs",
        link: "/security"
      },
      animation: "glow"
    }
  ]
}

