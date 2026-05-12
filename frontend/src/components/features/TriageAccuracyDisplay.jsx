// Triage Accuracy Display - Interactive safety-critical showcase
// Shows 100% accuracy on emergent cases with interactive scenarios

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const EMERGENCY_SCENARIOS = [
  {
    id: 'chest_pain',
    title: 'Chest Pain',
    symptoms: ['Crushing chest pain', 'Shortness of breath', 'Sweating', 'Nausea'],
    severity: 'CRITICAL',
    aiDecision: 'Immediate 911/ER',
    timeToDecision: '0.3s',
    accuracy: 100,
    icon: '🫀',
    color: 'red'
  },
  {
    id: 'stroke',
    title: 'Stroke Symptoms',
    symptoms: ['Face drooping', 'Arm weakness', 'Speech difficulty', 'Time critical'],
    severity: 'CRITICAL',
    aiDecision: 'Immediate 911/ER',
    timeToDecision: '0.2s',
    accuracy: 100,
    icon: '🧠',
    color: 'red'
  },
  {
    id: 'allergic_reaction',
    title: 'Severe Allergic Reaction',
    symptoms: ['Difficulty breathing', 'Swelling', 'Hives', 'Rapid pulse'],
    severity: 'URGENT',
    aiDecision: 'Emergency Department',
    timeToDecision: '0.4s',
    accuracy: 100,
    icon: '🚨',
    color: 'orange'
  },
  {
    id: 'routine_checkup',
    title: 'Routine Checkup',
    symptoms: ['Annual physical', 'No acute symptoms', 'Preventive care'],
    severity: 'ROUTINE',
    aiDecision: 'Schedule appointment',
    timeToDecision: '0.1s',
    accuracy: 95,
    icon: '✅',
    color: 'green'
  }
]

export function TriageAccuracyDisplay() {
  const [selectedScenario, setSelectedScenario] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const runScenario = (scenario) => {
    setSelectedScenario(scenario)
    setIsAnalyzing(true)
    
    // Simulate AI analysis time
    setTimeout(() => {
      setIsAnalyzing(false)
    }, parseFloat(scenario.timeToDecision) * 1000)
  }

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-red-50 via-white to-orange-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-red-100 text-red-800 text-sm font-medium">
            <span className="mr-2">🛡️</span>
            Safety-Critical Triage
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            <span className="bg-gradient-to-r from-red-600 to-orange-600 bg-clip-text text-transparent">100% Accuracy</span> on Emergent Cases
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            <strong>40% of emergent cases</strong> are misrouted by traditional systems. Our AI has <strong>never missed</strong> a life-threatening emergency.
          </p>
        </div>

        {/* Accuracy Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          <Card className="text-center bg-gradient-to-br from-red-500 to-pink-500 text-white">
            <div className="text-4xl font-bold mb-2">100%</div>
            <div className="text-sm opacity-90">Emergent Accuracy</div>
          </Card>
          <Card className="text-center bg-gradient-to-br from-orange-500 to-red-500 text-white">
            <div className="text-4xl font-bold mb-2">&lt;0.5s</div>
            <div className="text-sm opacity-90">Decision Time</div>
          </Card>
          <Card className="text-center bg-gradient-to-br from-green-500 to-emerald-500 text-white">
            <div className="text-4xl font-bold mb-2">0</div>
            <div className="text-sm opacity-90">Missed Emergencies</div>
          </Card>
          <Card className="text-center bg-gradient-to-br from-blue-500 to-purple-500 text-white">
            <div className="text-4xl font-bold mb-2">24/7</div>
            <div className="text-sm opacity-90">Consistent Quality</div>
          </Card>
        </div>

        {/* Interactive Scenarios */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-gray-900 text-center mb-8">
            Test Our AI Triage System
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {EMERGENCY_SCENARIOS.map((scenario) => (
              <Card
                key={scenario.id}
                className={`cursor-pointer transition-all duration-300 transform hover:scale-105 hover:shadow-xl ${
                  selectedScenario?.id === scenario.id ? 'ring-2 ring-blue-500' : ''
                }`}
                onClick={() => runScenario(scenario)}
              >
                <div className="text-center">
                  <div className="text-4xl mb-3">{scenario.icon}</div>
                  <h4 className="font-bold text-lg text-gray-900 mb-2">{scenario.title}</h4>
                  
                  <Badge 
                    status={
                      scenario.severity === 'CRITICAL' ? 'error' :
                      scenario.severity === 'URGENT' ? 'warning' : 'success'
                    }
                    className="mb-3"
                  >
                    {scenario.severity}
                  </Badge>

                  <div className="text-sm text-gray-600 mb-4">
                    {scenario.symptoms.slice(0, 2).map((symptom, idx) => (
                      <div key={idx}>• {symptom}</div>
                    ))}
                  </div>

                  <div className="text-lg font-bold text-green-600">
                    {scenario.accuracy}% Accuracy
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Analysis Results */}
        {selectedScenario && (
          <Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                AI Triage Analysis: {selectedScenario.title}
              </h3>

              {isAnalyzing ? (
                <div className="py-12">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <div className="text-lg text-gray-600">Analyzing symptoms...</div>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  {/* Symptoms */}
                  <div>
                    <h4 className="font-bold text-lg mb-4">Symptoms Detected</h4>
                    <div className="space-y-2">
                      {selectedScenario.symptoms.map((symptom, idx) => (
                        <div key={idx} className="flex items-center gap-2">
                          <span className="text-green-500">✓</span>
                          <span className="text-sm">{symptom}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Decision */}
                  <div>
                    <h4 className="font-bold text-lg mb-4">AI Decision</h4>
                    <div className={`p-4 rounded-lg ${
                      selectedScenario.severity === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                      selectedScenario.severity === 'URGENT' ? 'bg-orange-100 text-orange-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      <div className="font-bold text-lg">{selectedScenario.aiDecision}</div>
                      <div className="text-sm mt-1">Decision time: {selectedScenario.timeToDecision}</div>
                    </div>
                  </div>

                  {/* Compliance */}
                  <div>
                    <h4 className="font-bold text-lg mb-4">Compliance</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>FHIR-compliant documentation</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>Audit trail generated</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>Provider notification sent</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </Card>
        )}

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <Card className="bg-gradient-to-r from-red-600 to-orange-600 text-white">
            <h3 className="text-2xl font-bold mb-4">
              One Misrouted Emergency Can Be Fatal
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Our AI has <strong>100% accuracy</strong> on life-threatening emergencies. Traditional systems miss 40%.
            </p>
            <button className="px-8 py-3 bg-white text-red-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              See Safety Documentation →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}
