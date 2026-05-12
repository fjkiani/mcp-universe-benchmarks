// Technical Architecture Configuration
export const architectureConfig = {
  headline: "Technical Architecture",
  subheadline: "Built on Model Context Protocol (MCP)",
  description: "Model Context Protocol is the standard for connecting AI agents to external systems. Think of it as \"USB for AI\"—a universal connector that works with any system.",
  whyMCP: [
    "Standard protocol - Works with any LLM (GPT-4, Claude, etc.)",
    "Modular architecture - Add new capabilities easily",
    "Secure by design - Built-in security and compliance",
    "Future-proof - Compatible with new AI models"
  ],
  stack: {
    description: "We wrap industry-leading APIs (NexHealth, Twilio, AssemblyAI, VideoSDK) in a unified MCP interface, so your AI agent can interact with all of them seamlessly.",
    components: [
      { name: "AI Agent", description: "GPT-4 / Claude - Healthcare Receptionist Intelligence" },
      { name: "MCP Protocol", description: "Standard connector" },
      { name: "MCP Servers", description: "NexHealth (EHR), Twilio (SMS), AssemblyAI (Transcribe), VideoSDK (Video)" },
      { name: "Your Systems", description: "Your EHR System (Epic/Cerner), Your Insurance (Availity), Your Communication (Twilio)" }
    ]
  }
}

