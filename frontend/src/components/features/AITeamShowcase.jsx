// AI Team Showcase - Interactive component showing 6 specialized AI agents
// Based on LANDING_PAGE.md lines 85-128
// Shows productivity multipliers: 10x, 240x, 450x

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const AI_AGENTS = [
  {
    id: 'receptionist',
    name: 'Receptionist Agent',
    icon: '👩‍💼',
    color: 'blue',
    gradient: 'from-blue-500 to-cyan-500',
    capabilities: [
      'Handles routine calls, texts, and web inquiries 24/7',
      'Automates patient intake and registration',
      'Routes calls based on urgency (100% accuracy on emergencies)'
    ],
    enables: 'One receptionist to handle the workload of five',
    result: 'Your receptionist focuses on complex cases and patient relationships',
    multiplier: '5x',
    multiplierLabel: 'Workload Capacity'
  },
  {
    id: 'scheduling',
    name: 'Scheduling Agent',
    icon: '📅',
    color: 'green',
    gradient: 'from-green-500 to-emerald-500',
    capabilities: [
      'Books appointments directly in your EHR (80+ systems) in 3 seconds',
      'Checks real-time provider availability automatically',
      'Sends automated reminders and confirmations'
    ],
    enables: 'Scheduling staff to book 240x faster (3 sec vs 12 min)',
    result: 'Your scheduling team handles 240x more appointments',
    multiplier: '240x',
    multiplierLabel: 'Faster Booking'
  },
  {
    id: 'insurance',
    name: 'Insurance Agent',
    icon: '💳',
    color: 'purple',
    gradient: 'from-purple-500 to-pink-500',
    capabilities: [
      'Verifies insurance eligibility in 2 seconds (vs 15 minutes)',
      'Automatically checks benefits and coverage',
      'Handles prior authorizations'
    ],
    enables: 'Insurance staff to verify 450x faster (2 sec vs 15 min)',
    result: 'Your insurance team processes 450x more verifications',
    multiplier: '450x',
    multiplierLabel: 'Faster Verification'
  },
  {
    id: 'triage',
    name: 'Triage Agent',
    icon: '🚨',
    color: 'red',
    gradient: 'from-red-500 to-orange-500',
    capabilities: [
      'Assesses patient symptoms and urgency in real-time',
      'Routes life-threatening emergencies to 911/ER (never misses chest pain, stroke, severe allergic reactions)',
      'Schedules appropriate appointments for routine cases'
    ],
    enables: 'Triage nurses to focus on complex cases',
    result: 'Your triage team never misses a life-threatening emergency (0% miss rate vs 40% industry average)',
    multiplier: '0%',
    multiplierLabel: 'Miss Rate (vs 40% avg)'
  },
  {
    id: 'billing',
    name: 'Billing & Bookkeeping Agent',
    icon: '💰',
    color: 'amber',
    gradient: 'from-amber-500 to-yellow-500',
    capabilities: [
      'Automates claim submission and follow-up',
      'Tracks payments and outstanding balances',
      'Generates financial reports automatically'
    ],
    enables: 'Billing staff to process 10x more claims',
    result: 'Your billing team focuses on complex cases, not routine data entry',
    multiplier: '10x',
    multiplierLabel: 'Claim Processing'
  },
  {
    id: 'telehealth',
    name: 'Telehealth Coordinator',
    icon: '📹',
    color: 'indigo',
    gradient: 'from-indigo-500 to-purple-500',
    capabilities: [
      'Integrates with Zoom, Doxy.me, Teladoc (or provides built-in platform)',
      'Records and transcribes sessions (93.3% medical accuracy)',
      'Syncs directly to EHR automatically'
    ],
    enables: 'Telehealth staff to focus on patient care, not platform management',
    result: 'Your telehealth team handles more consultations with less admin work',
    multiplier: '93.3%',
    multiplierLabel: 'Transcription Accuracy'
  },
  {
    id: 'communication',
    name: 'Communication Agent',
    icon: '💬',
    color: 'teal',
    gradient: 'from-teal-500 to-cyan-500',
    capabilities: [
      'Sends HIPAA-compliant SMS and email automatically',
      'Automatically detects and blocks PHI',
      'Manages patient messaging'
    ],
    enables: 'Communication staff to handle 10x more messages',
    result: 'Your communication team focuses on complex cases, not routine messages',
    multiplier: '10x',
    multiplierLabel: 'Message Capacity'
  }
]

export function AITeamShowcase() {
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [hoveredAgent, setHoveredAgent] = useState(null)

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-gray-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">🤖</span>
            The AI Team
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Your <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Productivity Multipliers</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            A <strong>team of specialized AI agents</strong> that work alongside your existing staff—handling routine tasks so your team can focus on high-value patient care.
          </p>
        </div>

        {/* Productivity Multiplier Banner */}
        <Card className="mb-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
          <div className="text-center">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-2xl font-bold mb-4">The Productivity Multiplier</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mt-6">
              <div>
                <div className="text-2xl font-bold mb-2">1 → 5</div>
                <div className="text-xs opacity-90">Receptionist</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">240x</div>
                <div className="text-xs opacity-90">Scheduling</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">450x</div>
                <div className="text-xs opacity-90">Insurance</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">0%</div>
                <div className="text-xs opacity-90">Triage Miss</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">10x</div>
                <div className="text-xs opacity-90">Billing</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">93.3%</div>
                <div className="text-xs opacity-90">Transcription</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">10x</div>
                <div className="text-xs opacity-90">Messages</div>
              </div>
            </div>
            <p className="text-lg mt-6 opacity-90">
              <strong>Same great staff, 10x more output</strong>
            </p>
          </div>
        </Card>

        {/* AI Agents Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-16">
          {AI_AGENTS.map((agent) => (
            <Card
              key={agent.id}
              className={`relative cursor-pointer transition-all duration-300 transform border-2 ${
                selectedAgent === agent.id || hoveredAgent === agent.id
                  ? 'scale-105 shadow-2xl ring-4 ring-blue-300'
                  : 'hover:scale-102 hover:shadow-xl'
              } ${
                selectedAgent === agent.id
                  ? agent.color === 'blue' ? 'border-blue-500' :
                    agent.color === 'green' ? 'border-green-500' :
                    agent.color === 'purple' ? 'border-purple-500' :
                    agent.color === 'red' ? 'border-red-500' :
                    agent.color === 'indigo' ? 'border-indigo-500' :
                    agent.color === 'amber' ? 'border-amber-500' :
                    'border-teal-500'
                  : hoveredAgent === agent.id
                  ? agent.color === 'blue' ? 'border-blue-300' :
                    agent.color === 'green' ? 'border-green-300' :
                    agent.color === 'purple' ? 'border-purple-300' :
                    agent.color === 'red' ? 'border-red-300' :
                    agent.color === 'indigo' ? 'border-indigo-300' :
                    agent.color === 'amber' ? 'border-amber-300' :
                    'border-teal-300'
                  : 'border-gray-200'
              }`}
              onClick={() => setSelectedAgent(selectedAgent === agent.id ? null : agent.id)}
              onMouseEnter={() => setHoveredAgent(agent.id)}
              onMouseLeave={() => setHoveredAgent(null)}
            >
              {/* Header Gradient */}
              <div className={`absolute top-0 left-0 right-0 h-2 bg-gradient-to-r ${agent.gradient} rounded-t-lg`} />
              
              <div className="pt-4">
                {/* Agent Header */}
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-4xl">{agent.icon}</div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900">{agent.name}</h3>
                  </div>
                </div>

                {/* Multiplier Badge */}
                <div className={`mb-4 p-3 rounded-lg bg-gradient-to-r ${agent.gradient} text-white text-center`}>
                  <div className="text-2xl font-bold mb-1">{agent.multiplier}</div>
                  <div className="text-xs opacity-90">{agent.multiplierLabel}</div>
                </div>

                {/* Capabilities Preview */}
                <div className="space-y-2 mb-4">
                  {agent.capabilities.slice(0, 2).map((capability, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm text-gray-600">
                      <span className="text-green-500 mt-0.5">✓</span>
                      <span>{capability}</span>
                    </div>
                  ))}
                  {agent.capabilities.length > 2 && (
                    <div className="text-xs text-gray-500 italic">
                      +{agent.capabilities.length - 2} more capabilities
                    </div>
                  )}
                </div>

                {/* Quick Stats */}
                <div className="bg-gray-50 rounded-lg p-3 mb-4">
                  <div className="text-xs font-semibold text-gray-700 mb-1">Enables:</div>
                  <div className="text-sm text-gray-600">{agent.enables}</div>
                </div>

                {/* View Details Button */}
                <button
                  className={`w-full py-2 px-4 rounded-lg font-semibold text-sm transition-all ${
                    selectedAgent === agent.id
                      ? agent.color === 'blue' ? 'bg-blue-600 text-white hover:bg-blue-700' :
                        agent.color === 'green' ? 'bg-green-600 text-white hover:bg-green-700' :
                        agent.color === 'purple' ? 'bg-purple-600 text-white hover:bg-purple-700' :
                        agent.color === 'red' ? 'bg-red-600 text-white hover:bg-red-700' :
                        agent.color === 'indigo' ? 'bg-indigo-600 text-white hover:bg-indigo-700' :
                        agent.color === 'amber' ? 'bg-amber-600 text-white hover:bg-amber-700' :
                        'bg-teal-600 text-white hover:bg-teal-700'
                      : agent.color === 'blue' ? 'bg-blue-100 text-blue-700 hover:bg-blue-200' :
                        agent.color === 'green' ? 'bg-green-100 text-green-700 hover:bg-green-200' :
                        agent.color === 'purple' ? 'bg-purple-100 text-purple-700 hover:bg-purple-200' :
                        agent.color === 'red' ? 'bg-red-100 text-red-700 hover:bg-red-200' :
                        agent.color === 'indigo' ? 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200' :
                        agent.color === 'amber' ? 'bg-amber-100 text-amber-700 hover:bg-amber-200' :
                        'bg-teal-100 text-teal-700 hover:bg-teal-200'
                  }`}
                >
                  {selectedAgent === agent.id ? 'Selected ✓' : 'View Details'}
                </button>
              </div>
            </Card>
          ))}
        </div>

        {/* Selected Agent Details */}
        {selectedAgent && (
          <Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200">
            {(() => {
              const agent = AI_AGENTS.find(a => a.id === selectedAgent)
              if (!agent) return null

              return (
                <div>
                  <div className="text-center mb-6">
                    <div className="text-5xl mb-4">{agent.icon}</div>
                    <h3 className="text-3xl font-bold text-gray-900 mb-2">{agent.name}</h3>
                    <div className={`inline-block px-4 py-2 rounded-full bg-gradient-to-r ${agent.gradient} text-white font-bold text-lg`}>
                      {agent.multiplier} {agent.multiplierLabel}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Capabilities */}
                    <div>
                      <h4 className="font-bold text-lg mb-4 text-gray-900">Capabilities</h4>
                      <div className="space-y-3">
                        {agent.capabilities.map((capability, idx) => (
                          <div key={idx} className="flex items-start gap-3">
                            <span className="text-green-500 text-xl mt-0.5">✅</span>
                            <span className="text-gray-700">{capability}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Results */}
                    <div>
                      <h4 className="font-bold text-lg mb-4 text-gray-900">What It Enables</h4>
                      <div className="bg-white rounded-lg p-4 mb-4 border border-gray-200">
                        <div className="text-sm font-semibold text-blue-900 mb-2">Enables:</div>
                        <div className="text-gray-700">{agent.enables}</div>
                      </div>
                      <div className="bg-white rounded-lg p-4 border border-gray-200">
                        <div className="text-sm font-semibold text-green-900 mb-2">Result:</div>
                        <div className="text-gray-700">{agent.result}</div>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })()}
          </Card>
        )}

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Multiply Your Team's Productivity?
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Deploy all 6 AI agents in <strong>35-55 minutes</strong>. Same great staff, <strong>10x more output</strong>.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                Start Free Trial →
              </button>
              <button className="px-8 py-3 bg-transparent border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
                See How It Works →
              </button>
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}

