// MCP Servers Configuration - Visual, component-ready data
export const mcpServersConfig = {
  title: "Powered by Industry-Leading APIs",
  subtitle: "Each MCP server wraps a best-in-class healthcare API, providing a unified interface for your AI agents.",
  layout: "grid-4", // grid-2, grid-3, grid-4
  servers: [
    {
      id: "nexhealth",
      name: "NexHealth",
      icon: "🏥",
      category: "EHR Integration",
      description: "$1B unicorn connecting to 80+ EHR systems with 75K+ providers",
      toolsCount: 6,
      testCoverage: 100,
      status: "active",
      gradient: ["from-blue-500", "to-cyan-500"],
      capabilities: [
        { name: "Appointments", icon: "📅" },
        { name: "Insurance", icon: "💳" },
        { name: "Patient Records", icon: "📋" }
      ],
      integrations: 80,
      useCase: "Schedule appointments, verify insurance, and access patient records across Epic, Cerner, athenahealth, and 75+ other EHRs",
      metrics: [
        { label: "Providers", value: "75K+" },
        { label: "Patients", value: "30M+" }
      ],
      badge: "Most Popular"
    },
    {
      id: "twilio_hipaa",
      name: "Twilio HIPAA",
      icon: "💬",
      category: "Communications",
      description: "HIPAA-compliant SMS and voice with PHI detection",
      toolsCount: 5,
      testCoverage: 20,
      status: "active",
      gradient: ["from-red-500", "to-orange-500"],
      capabilities: [
        { name: "SMS", icon: "📱" },
        { name: "Voice Calls", icon: "📞" },
        { name: "PHI Detection", icon: "🔍" }
      ],
      integrations: 1,
      useCase: "Send secure patient communications, make automated calls, and ensure HIPAA compliance with built-in PHI filtering",
      metrics: [
        { label: "Uptime", value: "99.9%" },
        { label: "Compliance", value: "SOC 2" }
      ]
    },
    {
      id: "assemblyai",
      name: "AssemblyAI",
      icon: "🎙️",
      category: "Medical Transcription",
      description: "93.3% accuracy on medical transcription with entity extraction",
      toolsCount: 5,
      testCoverage: 0,
      status: "active",
      gradient: ["from-purple-500", "to-pink-500"],
      capabilities: [
        { name: "Transcription", icon: "📝" },
        { name: "Medical Entities", icon: "🏷️" },
        { name: "Real-time", icon: "⚡" }
      ],
      integrations: 1,
      useCase: "Transcribe patient conversations, extract medical entities, and generate clinical documentation automatically",
      metrics: [
        { label: "Accuracy", value: "93.3%" },
        { label: "Languages", value: "100+" }
      ]
    },
    {
      id: "videosdk",
      name: "VideoSDK",
      icon: "📹",
      category: "Telehealth",
      description: "Enterprise video platform for HIPAA-compliant consultations",
      toolsCount: 7,
      testCoverage: 0,
      status: "active",
      gradient: ["from-green-500", "to-emerald-500"],
      capabilities: [
        { name: "Video Rooms", icon: "🎥" },
        { name: "Recording", icon: "💾" },
        { name: "Streaming", icon: "📡" }
      ],
      integrations: 1,
      useCase: "Enable virtual consultations, record sessions for compliance, and provide seamless patient video experiences",
      metrics: [
        { label: "Concurrent Users", value: "10K+" },
        { label: "HD Quality", value: "1080p" }
      ]
    }
  ]
}

