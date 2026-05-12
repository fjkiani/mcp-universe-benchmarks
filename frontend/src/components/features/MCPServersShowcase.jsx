// MCP Servers Showcase - 4 custom MCP servers and 23 tools
// Based on LANDING_PAGE.md lines 373-422

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const MCP_SERVERS = [
  {
    id: 'nexhealth',
    name: 'NexHealth',
    icon: '🏥',
    toolCount: 6,
    description: '80+ EHR systems, real-time scheduling',
    color: 'blue',
    gradient: 'from-blue-500 to-cyan-500',
    tools: [
      'get_patient_info',
      'schedule_appointment',
      'check_availability',
      'update_appointment',
      'cancel_appointment',
      'get_appointment_history'
    ],
    apiStatus: 'connected',
    ehrCount: '80+'
  },
  {
    id: 'twilio_hipaa',
    name: 'Twilio HIPAA',
    icon: '📞',
    toolCount: 5,
    description: 'HIPAA-compliant SMS/Voice with PHI detection',
    color: 'green',
    gradient: 'from-green-500 to-emerald-500',
    tools: [
      'send_sms',
      'make_voice_call',
      'detect_phi',
      'block_phi_message',
      'get_message_history'
    ],
    apiStatus: 'connected',
    features: ['PHI Detection', 'BAA Available']
  },
  {
    id: 'assemblyai',
    name: 'AssemblyAI',
    icon: '🎤',
    toolCount: 5,
    description: '93.3% medical transcription accuracy',
    color: 'purple',
    gradient: 'from-purple-500 to-pink-500',
    tools: [
      'transcribe_audio',
      'transcribe_medical_audio',
      'get_transcription',
      'summarize_transcription',
      'extract_medical_entities'
    ],
    apiStatus: 'connected',
    accuracy: '93.3%'
  },
  {
    id: 'videosdk',
    name: 'VideoSDK',
    icon: '📹',
    toolCount: 7,
    description: 'Telehealth consultations, recording',
    color: 'indigo',
    gradient: 'from-indigo-500 to-purple-500',
    tools: [
      'create_room',
      'join_room',
      'start_recording',
      'stop_recording',
      'get_recording',
      'transcribe_recording',
      'sync_to_ehr'
    ],
    apiStatus: 'connected',
    features: ['HD Video', 'Recording', 'EHR Sync']
  }
]

export function MCPServersShowcase() {
  const [selectedServer, setSelectedServer] = useState(null)
  const [showTools, setShowTools] = useState(false)

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-gray-50 via-white to-indigo-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-indigo-100 text-indigo-800 text-sm font-medium">
            <span className="mr-2">🔧</span>
            Technical Architecture
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Built on <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Model Context Protocol</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            <strong>4 Custom MCP Servers</strong> with <strong>23 production-ready tools</strong>. Real API integrations with live connections.
          </p>
        </div>

        {/* Stats Banner */}
        <Card className="mb-16 bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-0">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">4</div>
              <div className="text-sm opacity-90">MCP Servers</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">23</div>
              <div className="text-sm opacity-90">Production Tools</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">80+</div>
              <div className="text-sm opacity-90">EHR Systems</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">100%</div>
              <div className="text-sm opacity-90">API Connected</div>
            </div>
          </div>
        </Card>

        {/* MCP Servers Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
          {MCP_SERVERS.map((server) => (
            <Card
              key={server.id}
              className={`relative cursor-pointer transition-all duration-300 transform hover:scale-105 border-2 ${
                selectedServer === server.id
                  ? server.color === 'blue' ? 'border-blue-500 ring-4 ring-blue-300' :
                    server.color === 'green' ? 'border-green-500 ring-4 ring-green-300' :
                    server.color === 'purple' ? 'border-purple-500 ring-4 ring-purple-300' :
                    'border-indigo-500 ring-4 ring-indigo-300'
                  : 'border-gray-200'
              }`}
              onClick={() => setSelectedServer(selectedServer === server.id ? null : server.id)}
            >
              <div className={`absolute top-0 left-0 right-0 h-2 bg-gradient-to-r ${server.gradient} rounded-t-lg`} />
              
              <div className="pt-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="text-4xl">{server.icon}</div>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">{server.name}</h3>
                      <p className="text-sm text-gray-600">{server.description}</p>
                    </div>
                  </div>
                  <Badge status="success" className="bg-green-100 text-green-800">
                    {server.toolCount} tools
                  </Badge>
                </div>

                <div className="flex items-center gap-4 mb-4">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm text-gray-600">{server.apiStatus}</span>
                  </div>
                  {server.ehrCount && (
                    <Badge status="info" className="bg-blue-100 text-blue-800">
                      {server.ehrCount} EHRs
                    </Badge>
                  )}
                  {server.accuracy && (
                    <Badge status="info" className="bg-purple-100 text-purple-800">
                      {server.accuracy}
                    </Badge>
                  )}
                </div>

                {server.features && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {server.features.map((feature, idx) => (
                      <Badge key={idx} status="info" className="text-xs">
                        {feature}
                      </Badge>
                    ))}
                  </div>
                )}

                <button
                  className={`w-full py-2 px-4 rounded-lg font-semibold text-sm transition-all ${
                    selectedServer === server.id
                      ? server.color === 'blue' ? 'bg-blue-600 text-white hover:bg-blue-700' :
                        server.color === 'green' ? 'bg-green-600 text-white hover:bg-green-700' :
                        server.color === 'purple' ? 'bg-purple-600 text-white hover:bg-purple-700' :
                        'bg-indigo-600 text-white hover:bg-indigo-700'
                      : server.color === 'blue' ? 'bg-blue-100 text-blue-700 hover:bg-blue-200' :
                        server.color === 'green' ? 'bg-green-100 text-green-700 hover:bg-green-200' :
                        server.color === 'purple' ? 'bg-purple-100 text-purple-700 hover:bg-purple-200' :
                        'bg-indigo-100 text-indigo-700 hover:bg-indigo-200'
                  }`}
                  onClick={(e) => {
                    e.stopPropagation()
                    setShowTools(!showTools)
                  }}
                >
                  {showTools ? 'Hide' : 'Show'} Tools
                </button>
              </div>
            </Card>
          ))}
        </div>

        {/* Tools Explorer */}
        {showTools && selectedServer && (
          <Card className="mb-16 bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-indigo-200">
            {(() => {
              const server = MCP_SERVERS.find(s => s.id === selectedServer)
              if (!server) return null

              return (
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                    {server.name} Tools ({server.toolCount})
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {server.tools.map((tool, idx) => (
                      <div key={idx} className="bg-white rounded-lg p-4 border border-gray-200">
                        <div className="flex items-center gap-2">
                          <span className="text-green-500">✓</span>
                          <code className="text-sm font-mono text-gray-700">{tool}</code>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })()}
          </Card>
        )}

        {/* Architecture Diagram */}
        <Card className="mb-16 bg-gradient-to-br from-gray-50 to-blue-50 border-2 border-blue-200">
          <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Architecture Flow
          </h3>
          <div className="space-y-6">
            <div className="text-center">
              <div className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-bold">
                AI Agent Team (GPT-4 / Claude)
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl text-gray-600">⬇️</div>
              <div className="text-sm text-gray-600">MCP Protocol (Standard)</div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {MCP_SERVERS.map((server) => (
                <div key={server.id} className="bg-white rounded-lg p-4 border-2 border-gray-200 text-center">
                  <div className="text-2xl mb-2">{server.icon}</div>
                  <div className="font-semibold text-sm text-gray-900">{server.name}</div>
                  <div className="text-xs text-gray-600">{server.toolCount} tools</div>
                </div>
              ))}
            </div>
            <div className="text-center">
              <div className="text-2xl text-gray-600">⬇️</div>
              <div className="text-sm text-gray-600">Real API Calls</div>
            </div>
            <div className="text-center">
              <div className="inline-block bg-green-600 text-white px-6 py-3 rounded-lg font-bold">
                Production APIs (Live)
              </div>
            </div>
          </div>
        </Card>

        {/* Bottom CTA */}
        <div className="text-center">
          <Card className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Production-Ready MCP Servers
            </h3>
            <p className="text-lg mb-6 opacity-90">
              All 4 servers are built, tested, and connected to real APIs. Ready to deploy in 35-55 minutes.
            </p>
            <button className="px-8 py-3 bg-white text-indigo-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              View API Documentation →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}

