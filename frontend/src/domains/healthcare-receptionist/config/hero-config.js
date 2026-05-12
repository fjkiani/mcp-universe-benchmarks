// Hero Section Configuration - Component-Driven, Visual-First
// Separates content from visual design for better creativity

export const heroConfig = {
  // Content (what to say)
  content: {
    headline: "Your AI-Powered Healthcare Receptionist Team: 10x Productivity, Same Great Staff",
    subheadline: "A complete team of AI receptionist agents that manage your entire healthcare office—from patient calls and scheduling to insurance verification and telehealth coordination. Enhances your existing staff and integrates seamlessly with your existing EHR and platforms.",
    primaryCTA: {
      text: "Start Free Trial",
      link: "/signup",
      note: "Deploy in 35-55 minutes • Works with 80+ EHRs • Enhance your team"
    },
    secondaryCTAs: [
      { text: "Watch Demo", link: "/demo" },
      { text: "View API Docs", link: "/docs" }
    ],
    badge: {
      icon: "🚀",
      text: "Powered by Model Context Protocol (MCP)"
    }
  },

  // Visual (how it looks)
  visual: {
    background: {
      type: "animated-blobs",
      colors: ["blue", "purple", "pink"],
      gradient: "bg-gradient-to-b from-white via-blue-50/50 to-white"
    },
    headline: {
      gradient: "bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent",
      animation: "animate-fade-in-up",
      size: "text-5xl md:text-7xl"
    },
    badge: {
      gradient: "bg-gradient-to-r from-blue-100 to-purple-100",
      border: "border border-blue-200",
      animation: "animate-pulse"
    },
    stats: [
      { 
        icon: "🏥", 
        value: "80+", 
        label: "EHR Systems",
        gradient: "from-blue-500 to-cyan-500",
        animation: "animate-count-up",
        delay: "delay-0"
      },
      { 
        icon: "⚡", 
        value: "24/7", 
        label: "Availability",
        gradient: "from-purple-500 to-pink-500",
        animation: "animate-count-up",
        delay: "delay-100"
      },
      { 
        icon: "🔒", 
        value: "100%", 
        label: "HIPAA Compliant",
        gradient: "from-green-500 to-emerald-500",
        animation: "animate-count-up",
        delay: "delay-200"
      },
      { 
        icon: "💰", 
        value: "$50B", 
        label: "Problem Solved",
        gradient: "from-orange-500 to-red-500",
        animation: "animate-count-up",
        delay: "delay-300"
      }
    ]
  },

  // Behavior (how it interacts)
  behavior: {
    ctaHover: "hover:scale-105 hover:shadow-xl",
    statsHover: "hover:scale-110 transition-transform",
    animation: {
      stagger: true,
      duration: 500
    }
  }
}

