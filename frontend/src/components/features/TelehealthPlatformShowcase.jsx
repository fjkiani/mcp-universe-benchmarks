// Telehealth Platform Showcase - Platform capabilities
// Based on LANDING_PAGE.md lines 312-327

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const PLATFORMS = [
  { name: 'Zoom', icon: '📹', status: 'integrated', color: 'blue' },
  { name: 'Doxy.me', icon: '💻', status: 'integrated', color: 'green' },
  { name: 'Teladoc', icon: '🏥', status: 'integrated', color: 'purple' },
  { name: 'Built-in Platform', icon: '🚀', status: 'available', color: 'indigo' }
]

const INTEGRATION_FEATURES = [
  {
    platform: 'Zoom',
    features: ['AI scheduling integration', 'EHR sync', 'Automated reminders']
  },
  {
    platform: 'Doxy.me',
    features: ['AI intake forms', 'EHR sync', 'Automated reminders']
  },
  {
    platform: 'Teladoc',
    features: ['AI triage integration', 'EHR documentation', 'Automated follow-up']
  }
]

export function TelehealthPlatformShowcase() {
  const [selectedPlatform, setSelectedPlatform] = useState(null)
  const [viewMode, setViewMode] = useState('replace') // 'replace' or 'integrate'

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-indigo-100 text-indigo-800 text-sm font-medium">
            <span className="mr-2">📹</span>
            Telehealth Coordination
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Telehealth Coordination: <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">One Capability of Your Receptionist Team</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Your AI receptionist team coordinates telehealth—managing scheduling, intake, and EHR sync. Telehealth is one part of complete office management, not the whole product.
          </p>

          {/* View Toggle */}
          <div className="flex justify-center gap-4 mb-8">
            <button
              onClick={() => setViewMode('replace')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                viewMode === 'replace'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Replace Everything
            </button>
            <button
              onClick={() => setViewMode('integrate')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                viewMode === 'integrate'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Integrate With Existing
            </button>
          </div>
        </div>

        {viewMode === 'replace' ? (
          /* Option A: Replace Everything */
          <div className="mb-16">
            <Card className="bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-indigo-200">
              <div className="text-center mb-8">
                <div className="text-5xl mb-4">🚀</div>
                <h3 className="text-3xl font-bold text-gray-900 mb-4">Built-in Platform</h3>
                <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                  Complete telehealth platform that replaces Zoom, Doxy.me, Teladoc, and your existing tools.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <Card className="text-center bg-white">
                  <div className="text-3xl mb-3">📹</div>
                  <h4 className="font-bold text-gray-900 mb-2">Built-in Video</h4>
                  <p className="text-sm text-gray-600">Replaces Zoom, Doxy.me, Teladoc</p>
                </Card>
                <Card className="text-center bg-white">
                  <div className="text-3xl mb-3">📅</div>
                  <h4 className="font-bold text-gray-900 mb-2">Built-in Scheduling</h4>
                  <p className="text-sm text-gray-600">No separate system needed</p>
                </Card>
                <Card className="text-center bg-white">
                  <div className="text-3xl mb-3">🔄</div>
                  <h4 className="font-bold text-gray-900 mb-2">EHR Integration</h4>
                  <p className="text-sm text-gray-600">Everything syncs automatically</p>
                </Card>
                <Card className="text-center bg-white">
                  <div className="text-3xl mb-3">🔑</div>
                  <h4 className="font-bold text-gray-900 mb-2">Unified Experience</h4>
                  <p className="text-sm text-gray-600">One platform, one login</p>
                </Card>
              </div>

              <div className="bg-white rounded-lg p-6">
                <h4 className="font-bold text-gray-900 mb-4 text-center">Key Features:</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">93.3% Medical Transcription Accuracy</div>
                      <div className="text-sm text-gray-600">Records and transcribes sessions automatically</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">Direct EHR Sync</div>
                      <div className="text-sm text-gray-600">All consultations sync to EHR instantly</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">HIPAA-Compliant</div>
                      <div className="text-sm text-gray-600">Built-in compliance from day one</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">No Platform Switch</div>
                      <div className="text-sm text-gray-600">Everything in one place</div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        ) : (
          /* Option B: Integrate With Everything */
          <div className="mb-16">
            <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200">
              <div className="text-center mb-8">
                <div className="text-5xl mb-4">🔌</div>
                <h3 className="text-3xl font-bold text-gray-900 mb-4">Integrate With Existing</h3>
                <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                  Works with your existing platforms—adds AI capabilities without replacing what you have.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {INTEGRATION_FEATURES.map((integration, idx) => (
                  <Card
                    key={idx}
                    className={`cursor-pointer transition-all transform hover:scale-105 ${
                      selectedPlatform === integration.platform
                        ? 'ring-4 ring-purple-300 scale-105'
                        : ''
                    }`}
                    onClick={() => setSelectedPlatform(selectedPlatform === integration.platform ? null : integration.platform)}
                  >
                    <div className="text-center mb-4">
                      <div className="text-4xl mb-2">
                        {PLATFORMS.find(p => p.name === integration.platform)?.icon || '📹'}
                      </div>
                      <h4 className="text-xl font-bold text-gray-900">{integration.platform}</h4>
                      <Badge status="success" className="mt-2">Integrated</Badge>
                    </div>
                    <div className="space-y-2">
                      {integration.features.map((feature, fidx) => (
                        <div key={fidx} className="flex items-start gap-2 text-sm">
                          <span className="text-green-500">✓</span>
                          <span className="text-gray-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </Card>
                ))}
              </div>

              <div className="bg-white rounded-lg p-6">
                <h4 className="font-bold text-gray-900 mb-4 text-center">Integration Benefits:</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">Keep Using What You Know</div>
                      <div className="text-sm text-gray-600">No retraining needed—AI works with existing tools</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">Add AI Capabilities</div>
                      <div className="text-sm text-gray-600">Scheduling, EHR sync, reminders automatically</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">Gradual Adoption</div>
                      <div className="text-sm text-gray-600">Add capabilities as your team is ready</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="text-green-500 text-xl">✅</span>
                    <div>
                      <div className="font-semibold text-gray-900">No Platform Switch</div>
                      <div className="text-sm text-gray-600">Enhance what you have, don't replace it</div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Transcription Accuracy */}
        <Card className="mb-16 bg-gradient-to-r from-green-600 to-emerald-600 text-white text-center">
          <div className="text-5xl mb-4">🎯</div>
          <h3 className="text-3xl font-bold mb-4">93.3% Medical Transcription Accuracy</h3>
          <p className="text-lg opacity-90 max-w-2xl mx-auto">
            All consultations are automatically recorded and transcribed with medical-grade accuracy, then synced directly to your EHR.
          </p>
        </Card>

        {/* Bottom CTA */}
        <div className="text-center">
          <Card className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Choose Your Telehealth Solution
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Replace everything or integrate with existing—both options enhance your team's productivity.
            </p>
            <button className="px-8 py-3 bg-white text-indigo-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              See Platform Demo →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}


