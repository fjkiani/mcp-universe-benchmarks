// Enhanced Landing Page Configuration - Value-focused SaaS presentation
// This config powers the reusable landing page components

export const ENHANCED_LANDING = {
  // Hero Section with Stats
  hero: {
    badge: {
      icon: "🚀",
      text: "Powered by Model Context Protocol (MCP)"
    },
    headline: "Build Healthcare AI That Actually Integrates",
    subheadline: "Production-ready MCP servers connecting your AI agents to 80+ EHR systems, communication platforms, and healthcare APIs. Deploy in minutes, not months.",
    stats: [
      { icon: "🏥", value: "80+", label: "EHR Systems" },
      { icon: "⚡", value: "23", label: "API Tools" },
      { icon: "🔒", value: "100%", label: "HIPAA Compliant" },
      { icon: "🚀", value: "<1s", label: "Response Time" }
    ],
    primaryCTA: {
      text: "View Dashboard",
      link: "/dashboard"
    },
    secondaryCTAs: [
      { text: "API Showcase", link: "/showcase" },
      { text: "View Docs", link: "/docs" }
    ]
  },

  // Value Proposition - Business Benefits
  valueProps: {
    title: "Accelerate Your Healthcare AI Development",
    subtitle: "Stop building integrations from scratch. Use battle-tested MCP servers that handle the complexity for you.",
    values: [
      {
        icon: "⚡",
        title: "Ship Faster",
        description: "Pre-built integrations for NexHealth, Twilio, AssemblyAI, and VideoSDK. Go from idea to production in days, not months.",
        metrics: [
          { label: "Time to Production", value: "1 day" },
          { label: "vs. Building In-House", value: "3-6 months" }
        ],
        benefits: [
          "Ready-to-use API wrappers",
          "Production-tested reliability",
          "Automatic updates & maintenance"
        ]
      },
      {
        icon: "🔗",
        title: "Integrate Seamlessly",
        description: "MCP protocol ensures your AI agents can communicate with any system. Add new capabilities without rewriting code.",
        metrics: [
          { label: "Supported EHRs", value: "80+" },
          { label: "API Tools", value: "23" }
        ],
        benefits: [
          "Standard MCP interface",
          "Works with any LLM",
          "Modular architecture"
        ]
      },
      {
        icon: "🛡️",
        title: "Stay Compliant",
        description: "Built-in HIPAA compliance, PHI detection, and audit logging. Security and compliance handled from day one.",
        metrics: [
          { label: "Compliance", value: "SOC 2" },
          { label: "Uptime", value: "99.9%" }
        ],
        benefits: [
          "Automated PHI detection",
          "Complete audit trails",
          "BAA agreements included"
        ]
      }
    ]
  },

  // MCP Server Showcase
  mcpServers: {
    title: "Powered by Industry-Leading APIs",
    description: "Each MCP server wraps a best-in-class healthcare API, providing a unified interface for your AI agents.",
    servers: [
      {
        name: "NexHealth",
        icon: "🏥",
        category: "EHR Integration",
        description: "$1B unicorn connecting to 80+ EHR systems with 75K+ providers",
        toolsCount: 6,
        testCoverage: 100,
        capabilities: ["Appointments", "Insurance", "Patient Records"],
        integrations: "80",
        useCase: "Schedule appointments, verify insurance, and access patient records across Epic, Cerner, athenahealth, and 75+ other EHRs"
      },
      {
        name: "Twilio HIPAA",
        icon: "💬",
        category: "Communications",
        description: "HIPAA-compliant SMS and voice with PHI detection",
        toolsCount: 5,
        testCoverage: 20,
        capabilities: ["SMS", "Voice Calls", "PHI Detection"],
        integrations: "1",
        useCase: "Send secure patient communications, make automated calls, and ensure HIPAA compliance with built-in PHI filtering"
      },
      {
        name: "AssemblyAI",
        icon: "🎙️",
        category: "Medical Transcription",
        description: "93.3% accuracy on medical transcription with entity extraction",
        toolsCount: 5,
        testCoverage: 0,
        capabilities: ["Transcription", "Medical Entities", "Real-time"],
        integrations: "1",
        useCase: "Transcribe patient conversations, extract medical entities, and generate clinical documentation automatically"
      },
      {
        name: "VideoSDK",
        icon: "📹",
        category: "Telehealth",
        description: "Enterprise video platform for HIPAA-compliant consultations",
        toolsCount: 7,
        testCoverage: 0,
        capabilities: ["Video Rooms", "Recording", "Streaming"],
        integrations: "1",
        useCase: "Enable virtual consultations, record sessions for compliance, and provide seamless patient video experiences"
      }
    ]
  },

  // Integration Stack Visualization
  integrationStack: {
    title: "How It Fits Into Your Stack",
    description: "MCP servers act as the middleware layer between your AI agents and healthcare systems.",
    stack: [
      {
        name: "Your AI Agent",
        type: "Application Layer",
        icon: "🤖",
        description: "GPT-4, Claude, or any LLM-powered agent",
        examples: [
          "Healthcare Receptionist",
          "Clinical Documentation",
          "Patient Triage"
        ]
      },
      {
        name: "MCP Servers",
        type: "Integration Layer",
        icon: "🔌",
        description: "Unified API interface for healthcare systems",
        examples: [
          "NexHealth (EHR)",
          "Twilio (Comms)",
          "AssemblyAI (Transcription)"
        ]
      },
      {
        name: "Healthcare Systems",
        type: "Data Layer",
        icon: "🏥",
        description: "Your existing EHR, insurance, and communication platforms",
        examples: [
          "Epic / Cerner",
          "Insurance APIs",
          "Communication Platforms"
        ]
      }
    ]
  },

  // Feature Highlights
  features: {
    title: "Everything You Need to Build Healthcare AI",
    features: [
      {
        icon: "🔌",
        title: "Plug & Play Integration",
        description: "Connect to NexHealth, Twilio, AssemblyAI, and VideoSDK through a single MCP interface.",
        details: [
          "No complex API authentication",
          "Automatic rate limiting",
          "Built-in error handling"
        ],
        badge: "Production Ready"
      },
      {
        icon: "📊",
        title: "Real-Time Dashboard",
        description: "Monitor API health, test coverage, and integration status in one unified dashboard.",
        details: [
          "Live server status",
          "Test result tracking",
          "Performance metrics"
        ],
        badge: "Included"
      },
      {
        icon: "🧪",
        title: "Comprehensive Testing",
        description: "Automated test suites for every MCP server with detailed result tracking.",
        details: [
          "Structure validation",
          "API connectivity tests",
          "End-to-end workflows"
        ],
        badge: "23 Tests"
      },
      {
        icon: "📚",
        title: "Complete Documentation",
        description: "Detailed API docs, integration guides, and example implementations.",
        details: [
          "API reference",
          "Code examples",
          "Best practices"
        ],
        badge: "Always Updated"
      },
      {
        icon: "🔒",
        title: "Security First",
        description: "HIPAA-compliant by default with PHI detection and audit logging.",
        details: [
          "SOC 2 certified",
          "BAA agreements",
          "Encrypted data"
        ],
        badge: "HIPAA Compliant"
      },
      {
        icon: "🚀",
        title: "Continuous Updates",
        description: "We maintain all integrations and handle API changes automatically.",
        details: [
          "Zero-downtime updates",
          "Backward compatibility",
          "Version management"
        ],
        badge: "Managed"
      }
    ]
  },

  // Use Cases
  useCases: {
    title: "What You Can Build",
    cases: [
      {
        icon: "🤖",
        title: "AI Receptionists",
        description: "Automate appointment scheduling, insurance verification, and patient triage with NexHealth and Twilio integration.",
        results: ["24/7 availability", "Sub-second responses", "80+ EHR support"]
      },
      {
        icon: "📝",
        title: "Clinical Documentation",
        description: "Transcribe patient visits and generate clinical notes with AssemblyAI and EHR integration.",
        results: ["93% accuracy", "Real-time transcription", "Auto-populated EHR"]
      },
      {
        icon: "🩺",
        title: "Telehealth Platforms",
        description: "Build HIPAA-compliant video consultation platforms with VideoSDK and appointment management.",
        results: ["Enterprise video", "EHR integration", "Automated scheduling"]
      }
    ]
  },

  // Getting Started CTA
  cta: {
    title: "Start Building Today",
    subtitle: "All MCP servers are production-ready and include comprehensive documentation.",
    primaryCTA: {
      text: "View Dashboard",
      link: "/dashboard"
    },
    secondaryCTAs: [
      { text: "API Showcase", link: "/showcase" },
      { text: "View Servers", link: "/servers" }
    ],
    features: [
      "✓ 4 Production MCP Servers",
      "✓ 23 API Tools",
      "✓ Real-Time Dashboard",
      "✓ Complete Documentation"
    ]
  }
}

