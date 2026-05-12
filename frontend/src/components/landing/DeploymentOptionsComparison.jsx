// Deployment Options Comparison - Detailed Option 1 vs Option 2
// Based on LANDING_PAGE.md lines 142-199

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const OPTION_1 = {
  id: 'saas',
  title: 'Complete SaaS Platform',
  subtitle: 'Unified Experience',
  icon: '🚀',
  deploymentTime: '35 minutes',
  features: [
    'Complete telehealth platform',
    'Integrates with or replaces Zoom, Doxy.me, Teladoc',
    'Built-in scheduling',
    'Works with your existing scheduling team',
    'EHR integration - Works with 80+ EHR systems',
    'AI agent team - All productivity multipliers included',
    'Unified patient experience - One platform, one login'
  ],
  howItEnhances: [
    'Your receptionists use AI to handle routine calls, focus on complex cases',
    'Your scheduling staff uses AI to book 240x faster, handle more appointments',
    'Your insurance team uses AI to verify 450x faster, process more patients',
    'Your triage nurses use AI to never miss emergencies, handle routine instantly'
  ],
  deploymentSteps: [
    { step: 1, title: 'Connect your EHR', time: '5 minutes' },
    { step: 2, title: 'Configure your practice', time: '10 minutes' },
    { step: 3, title: 'Train your team on new tools', time: '15 minutes' },
    { step: 4, title: 'Go live', time: '5 minutes' }
  ],
  bestFor: [
    'Practices wanting unified experience',
    'New practices starting from scratch',
    'Practices ready to enhance team productivity'
  ],
  color: 'blue',
  gradient: 'from-blue-500 to-cyan-500'
}

const OPTION_2 = {
  id: 'mcp',
  title: 'MCP Agent Integration',
  subtitle: 'Enhance Existing Workflows',
  icon: '🔌',
  deploymentTime: '55 minutes',
  features: [
    'MCP agent that integrates into your existing EHR',
    'AI capabilities added to your current workflow',
    'Works with existing platforms - Enhances Zoom, Doxy.me, etc.',
    'No platform switch - Keep using what you have',
    'Gradual adoption - Add capabilities as your team is ready'
  ],
  howItEnhances: [
    'Your existing staff gets AI tools integrated into their current workflows',
    'No retraining needed—AI works with tools they already know',
    'Gradual adoption—add AI capabilities as your team is ready',
    'Same great staff, same workflows, 10x more productivity'
  ],
  deploymentSteps: [
    { step: 1, title: 'Install MCP agent in your EHR', time: '10 minutes' },
    { step: 2, title: 'Configure AI agents', time: '15 minutes' },
    { step: 3, title: 'Train your team on new capabilities', time: '20 minutes' },
    { step: 4, title: 'Test with sample workflows', time: '10 minutes' }
  ],
  bestFor: [
    'Practices happy with current platforms',
    'Large health systems with existing infrastructure',
    'Practices wanting to enhance team gradually'
  ],
  color: 'purple',
  gradient: 'from-purple-500 to-pink-500'
}

export function DeploymentOptionsComparison() {
  const [selectedOption, setSelectedOption] = useState(null)
  const [viewMode, setViewMode] = useState('comparison') // 'comparison' or 'detailed'

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">⚙️</span>
            Deployment Options
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Choose Your <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Deployment Path</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Two ways to deploy—complete platform or seamless integration. Both enhance your team's productivity.
          </p>

          {/* View Toggle */}
          <div className="flex justify-center gap-4 mb-8">
            <button
              onClick={() => setViewMode('comparison')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                viewMode === 'comparison'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Side-by-Side Comparison
            </button>
            <button
              onClick={() => setViewMode('detailed')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                viewMode === 'detailed'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Detailed View
            </button>
          </div>
        </div>

        {viewMode === 'comparison' ? (
          /* Side-by-Side Comparison */
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
            {[OPTION_1, OPTION_2].map((option) => (
              <Card
                key={option.id}
                className={`relative cursor-pointer transition-all duration-300 transform hover:scale-102 border-2 ${
                  selectedOption === option.id
                    ? option.color === 'blue' ? 'border-blue-500 ring-4 ring-blue-300' : 'border-purple-500 ring-4 ring-purple-300'
                    : 'border-gray-200'
                }`}
                onClick={() => setSelectedOption(selectedOption === option.id ? null : option.id)}
              >
                <div className={`absolute top-0 left-0 right-0 h-2 bg-gradient-to-r ${option.gradient} rounded-t-lg`} />
                
                <div className="pt-4">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="text-4xl">{option.icon}</div>
                      <div>
                        <h3 className="text-2xl font-bold text-gray-900">{option.title}</h3>
                        <p className="text-sm text-gray-600">{option.subtitle}</p>
                      </div>
                    </div>
                    <Badge status="info" className={option.color === 'blue' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'}>
                      {option.deploymentTime}
                    </Badge>
                  </div>

                  <div className="space-y-3 mb-6">
                    {option.features.slice(0, 4).map((feature, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <span className="text-green-500 text-xl mt-0.5">✅</span>
                        <span className="text-gray-700 text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    <div className="text-sm font-semibold text-gray-900 mb-2">Best For:</div>
                    <ul className="space-y-1">
                      {option.bestFor.map((item, idx) => (
                        <li key={idx} className="text-xs text-gray-600 flex items-center gap-2">
                          <span>•</span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          /* Detailed View */
          <div className="space-y-12">
            {[OPTION_1, OPTION_2].map((option) => (
              <Card key={option.id} className="border-2 border-gray-200">
                <div className={`absolute top-0 left-0 right-0 h-2 bg-gradient-to-r ${option.gradient} rounded-t-lg`} />
                
                <div className="pt-6">
                  <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-4">
                      <div className="text-5xl">{option.icon}</div>
                      <div>
                        <h3 className="text-3xl font-bold text-gray-900">{option.title}</h3>
                        <p className="text-lg text-gray-600">{option.subtitle}</p>
                      </div>
                    </div>
                    <Badge status="info" className={option.color === 'blue' ? 'bg-blue-100 text-blue-800 text-lg px-4 py-2' : 'bg-purple-100 text-purple-800 text-lg px-4 py-2'}>
                      {option.deploymentTime} to Deploy
                    </Badge>
                  </div>

                  {/* Features */}
                  <div className="mb-8">
                    <h4 className="text-xl font-bold text-gray-900 mb-4">What You Get:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {option.features.map((feature, idx) => (
                        <div key={idx} className="flex items-start gap-3">
                          <span className="text-green-500 text-xl mt-0.5">✅</span>
                          <span className="text-gray-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* How It Enhances */}
                  <div className="mb-8">
                    <h4 className="text-xl font-bold text-gray-900 mb-4">How It Enhances Your Team:</h4>
                    <div className="space-y-3">
                      {option.howItEnhances.map((item, idx) => (
                        <div key={idx} className="bg-blue-50 rounded-lg p-4">
                          <p className="text-gray-700">{item}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Deployment Steps */}
                  <div className="mb-8">
                    <h4 className="text-xl font-bold text-gray-900 mb-4">Deployment Steps:</h4>
                    <div className="space-y-4">
                      {option.deploymentSteps.map((step) => (
                        <div key={step.step} className="flex items-center gap-4 bg-gray-50 rounded-lg p-4">
                          <div className={`w-10 h-10 rounded-full bg-gradient-to-r ${option.gradient} text-white flex items-center justify-center font-bold`}>
                            {step.step}
                          </div>
                          <div className="flex-1">
                            <div className="font-semibold text-gray-900">{step.title}</div>
                            <div className="text-sm text-gray-600">{step.time}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Best For */}
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h4 className="text-xl font-bold text-gray-900 mb-4">Best For:</h4>
                    <ul className="space-y-2">
                      {option.bestFor.map((item, idx) => (
                        <li key={idx} className="flex items-center gap-3">
                          <span className="text-blue-600 text-xl">•</span>
                          <span className="text-gray-700">{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Deploy?
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Choose your deployment option and get started in <strong>35-55 minutes</strong>.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                Start Free Trial →
              </button>
              <button className="px-8 py-3 bg-transparent border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
                Schedule Demo →
              </button>
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}






