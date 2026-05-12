// Agent Flow Diagram - Visual flow showing how agents work together
// Based on LANDING_PAGE.md lines 202-249

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const AGENTS = [
  {
    id: 'receptionist',
    name: 'Receptionist Agent',
    icon: '👩‍💼',
    description: 'First Point of Contact',
    capabilities: ['Answers immediately', 'Assesses urgency', 'Routes to appropriate agent'],
    color: 'blue',
    position: 'top'
  },
  {
    id: 'scheduling',
    name: 'Scheduling Agent',
    icon: '📅',
    description: 'Appointment Booking',
    capabilities: ['Books in EHR', 'Checks availability', 'Sends reminders'],
    color: 'green',
    position: 'left'
  },
  {
    id: 'insurance',
    name: 'Insurance Agent',
    icon: '💳',
    description: 'Verification & Benefits',
    capabilities: ['Verifies coverage', 'Checks benefits', 'Handles prior auth'],
    color: 'purple',
    position: 'left'
  },
  {
    id: 'triage',
    name: 'Triage Agent',
    icon: '🚨',
    description: 'Urgency Assessment',
    capabilities: ['Routes to 911/ER', 'Schedules urgent', 'Never misses emergency'],
    color: 'red',
    position: 'right'
  },
  {
    id: 'telehealth',
    name: 'Telehealth Coordinator',
    icon: '📹',
    description: 'Video Consultations',
    capabilities: ['Hosts video', 'Records sessions', 'Transcribes (93.3%)'],
    color: 'indigo',
    position: 'right'
  },
  {
    id: 'ehr',
    name: 'EHR System',
    icon: '🏥',
    description: 'Epic, Cerner, athenahealth, etc.',
    capabilities: ['Real-time sync', 'Bidirectional', '80+ systems'],
    color: 'gray',
    position: 'bottom'
  }
]

export function AgentFlowDiagram() {
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [hoveredAgent, setHoveredAgent] = useState(null)

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-gray-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">🔄</span>
            Product Architecture
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            How The <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">AI Team Works Together</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            When a patient calls, the Receptionist Agent routes to the right specialist agent, who handles the task and syncs to your EHR.
          </p>
        </div>

        {/* Flow Diagram */}
        <Card className="mb-16 bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200">
          <div className="relative py-12">
            {/* Patient Contact */}
            <div className="text-center mb-8">
              <div className="inline-block">
                <div className="text-4xl mb-2">📞</div>
                <div className="font-bold text-lg text-gray-900">Patient Contact</div>
                <div className="text-sm text-gray-600">Call/Text/Web</div>
              </div>
            </div>

            {/* Arrow Down */}
            <div className="text-center mb-8">
              <div className="text-3xl text-blue-600">⬇️</div>
            </div>

            {/* Receptionist Agent (Top) */}
            <div className="text-center mb-12">
              <div
                className={`inline-block cursor-pointer transition-all transform hover:scale-110 ${
                  selectedAgent === 'receptionist' || hoveredAgent === 'receptionist'
                    ? 'ring-4 ring-blue-500 scale-110'
                    : ''
                }`}
                onClick={() => setSelectedAgent(selectedAgent === 'receptionist' ? null : 'receptionist')}
                onMouseEnter={() => setHoveredAgent('receptionist')}
                onMouseLeave={() => setHoveredAgent(null)}
              >
                <Card className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white border-0 min-w-[200px]">
                  <div className="text-4xl mb-2">{AGENTS[0].icon}</div>
                  <div className="font-bold text-lg mb-1">{AGENTS[0].name}</div>
                  <div className="text-sm opacity-90">{AGENTS[0].description}</div>
                </Card>
              </div>
            </div>

            {/* Arrows Down to Specialists */}
            <div className="text-center mb-8">
              <div className="text-3xl text-blue-600">⬇️</div>
            </div>

            {/* Specialist Agents Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
              {AGENTS.slice(1, 5).map((agent) => (
                <div
                  key={agent.id}
                  className={`cursor-pointer transition-all transform hover:scale-105 ${
                    selectedAgent === agent.id || hoveredAgent === agent.id
                      ? 'ring-4 ring-blue-500 scale-105'
                      : ''
                  }`}
                  onClick={() => setSelectedAgent(selectedAgent === agent.id ? null : agent.id)}
                  onMouseEnter={() => setHoveredAgent(agent.id)}
                  onMouseLeave={() => setHoveredAgent(null)}
                >
                  <Card className={`bg-gradient-to-br ${
                    agent.color === 'green' ? 'from-green-500 to-emerald-500' :
                    agent.color === 'purple' ? 'from-purple-500 to-pink-500' :
                    agent.color === 'red' ? 'from-red-500 to-orange-500' :
                    'from-indigo-500 to-purple-500'
                  } text-white border-0 text-center`}>
                    <div className="text-3xl mb-2">{agent.icon}</div>
                    <div className="font-bold text-sm mb-1">{agent.name}</div>
                    <div className="text-xs opacity-90">{agent.description}</div>
                  </Card>
                </div>
              ))}
            </div>

            {/* Arrow Down to EHR */}
            <div className="text-center mb-8">
              <div className="text-3xl text-gray-600">⬇️</div>
            </div>

            {/* EHR System (Bottom) */}
            <div className="text-center">
              <div
                className={`inline-block cursor-pointer transition-all transform hover:scale-110 ${
                  selectedAgent === 'ehr' || hoveredAgent === 'ehr'
                    ? 'ring-4 ring-gray-500 scale-110'
                    : ''
                }`}
                onClick={() => setSelectedAgent(selectedAgent === 'ehr' ? null : 'ehr')}
                onMouseEnter={() => setHoveredAgent('ehr')}
                onMouseLeave={() => setHoveredAgent(null)}
              >
                <Card className="bg-gradient-to-br from-gray-600 to-gray-800 text-white border-0 min-w-[250px]">
                  <div className="text-4xl mb-2">{AGENTS[5].icon}</div>
                  <div className="font-bold text-lg mb-1">{AGENTS[5].name}</div>
                  <div className="text-sm opacity-90">{AGENTS[5].description}</div>
                </Card>
              </div>
            </div>
          </div>
        </Card>

        {/* Selected Agent Details */}
        {selectedAgent && (
          <Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200 mb-16">
            {(() => {
              const agent = AGENTS.find(a => a.id === selectedAgent)
              if (!agent) return null

              return (
                <div>
                  <div className="text-center mb-6">
                    <div className="text-5xl mb-4">{agent.icon}</div>
                    <h3 className="text-3xl font-bold text-gray-900 mb-2">{agent.name}</h3>
                    <p className="text-lg text-gray-600">{agent.description}</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {agent.capabilities.map((capability, idx) => (
                      <div key={idx} className="bg-white rounded-lg p-4 border border-gray-200">
                        <div className="flex items-center gap-2">
                          <span className="text-green-500 text-xl">✅</span>
                          <span className="text-gray-700">{capability}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })()}
          </Card>
        )}

        {/* Bottom CTA */}
        <div className="text-center">
          <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              All Agents Work Together Seamlessly
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Each agent specializes in their domain, but they all sync to your EHR automatically.
            </p>
            <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              See Technical Architecture →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}

