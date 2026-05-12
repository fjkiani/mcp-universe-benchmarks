// Integration Stack Configuration - How it fits in user's architecture
export const integrationStackConfig = {
  title: "How It Fits Into Your Stack",
  subtitle: "MCP servers act as the middleware layer between your AI agents and healthcare systems.",
  theme: "dark", // dark, light, gradient
  layers: [
    {
      id: "application",
      name: "Your AI Agent",
      type: "Application Layer",
      icon: "🤖",
      iconBg: "bg-gradient-to-br from-blue-500 to-purple-600",
      description: "GPT-4, Claude, or any LLM-powered agent",
      examples: [
        { name: "Healthcare Receptionist", icon: "👨‍⚕️" },
        { name: "Clinical Documentation", icon: "📝" },
        { name: "Patient Triage", icon: "🩺" }
      ],
      color: "blue",
      connector: "down"
    },
    {
      id: "integration",
      name: "MCP Servers",
      type: "Integration Layer",
      icon: "🔌",
      iconBg: "bg-gradient-to-br from-purple-500 to-pink-600",
      description: "Unified API interface for healthcare systems",
      examples: [
        { name: "NexHealth (EHR)", icon: "🏥" },
        { name: "Twilio (Comms)", icon: "💬" },
        { name: "AssemblyAI (Transcription)", icon: "🎙️" }
      ],
      color: "purple",
      connector: "down",
      highlight: true // Highlight this layer
    },
    {
      id: "data",
      name: "Healthcare Systems",
      type: "Data Layer",
      icon: "🏥",
      iconBg: "bg-gradient-to-br from-green-500 to-emerald-600",
      description: "Your existing EHR, insurance, and communication platforms",
      examples: [
        { name: "Epic / Cerner", icon: "💻" },
        { name: "Insurance APIs", icon: "💳" },
        { name: "Communication Platforms", icon: "📱" }
      ],
      color: "green",
      connector: "none"
    }
  ],
  flow: {
    direction: "vertical", // vertical, horizontal
    animation: "pulse", // pulse, flow, none
    showArrows: true
  }
}

