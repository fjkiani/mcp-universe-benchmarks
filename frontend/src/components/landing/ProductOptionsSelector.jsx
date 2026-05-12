// Product Options Selector - Interactive component for "What Is This Product?" section
// Shows two deployment options: Complete SaaS Platform vs MCP Agent Integration
// Based on LANDING_PAGE.md lines 27-50

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const OPTION_1 = {
  id: 'saas',
  title: 'All-in-One Office Software',
  subtitle: 'Everything in one place',
  icon: '🚀',
  description: 'Complete software that runs your entire front office—from phones to appointments to insurance',
  features: [
    'All front-office operations in one system (calls, scheduling, insurance, messages)',
    'Works with Zoom, Doxy.me, or use built-in video visits',
    'Connects directly to your medical records (Epic, Cerner, athenahealth, etc.)',
    'Ready to use in 35 minutes - no building required'
  ],
  deploymentTime: '35 minutes',
  bestFor: [
    'Practices wanting everything in one place',
    'New practices just getting started',
    'Practices ready to simplify their workflow'
  ],
  color: 'blue',
  gradient: 'from-blue-500 to-cyan-500'
}

const OPTION_2 = {
  id: 'mcp',
  title: 'Add-On for Your Current System',
  subtitle: 'Keep what you have, add smart features',
  icon: '🔌',
  description: 'Adds smart automation to your existing systems without changing anything',
  features: [
    'Adds automation to your current medical records system',
    'Works with Epic, Cerner, athenahealth, and 80+ other systems',
    'Keeps your existing workflow—just makes it faster',
    'No need to learn new software or switch systems'
  ],
  deploymentTime: '55 minutes',
  bestFor: [
    'Practices happy with their current setup',
    'Large health systems with existing systems',
    'Practices wanting to add features gradually'
  ],
  color: 'purple',
  gradient: 'from-purple-500 to-pink-500'
}

export function ProductOptionsSelector() {
  const [selectedOption, setSelectedOption] = useState(null)
  const [hoveredOption, setHoveredOption] = useState(null)

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">🎯</span>
            What Is This Product?
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Software That <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Makes Your Staff More Productive</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-4">
            Receptionist OS is software that runs your front office operations. It has smart features that handle routine tasks automatically, so your staff can focus on patients.
          </p>

          <p className="text-lg text-gray-700 max-w-2xl mx-auto font-medium">
            Your team stays the same—they just get <strong className="text-blue-600">10x more done</strong> each day.
          </p>
        </div>

        {/* Philosophy Banner */}
        <Card className="mb-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
          <div className="text-center">
            <div className="text-3xl mb-4">💡</div>
            <h3 className="text-2xl font-bold mb-4">How It Works</h3>
            <p className="text-lg opacity-90 max-w-3xl mx-auto">
              One receptionist can handle the calls that used to require five people. Your scheduling team books appointments in <strong>3 seconds</strong> instead of 12 minutes. Insurance verification happens in <strong>2 seconds</strong> instead of 15 minutes. <strong>Same staff, dramatically more output.</strong>
            </p>
          </div>
        </Card>

        {/* Two Options */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {/* Option 1: Complete SaaS Platform */}
          <Card
            className={`relative cursor-pointer transition-all duration-300 transform ${
              selectedOption === OPTION_1.id || hoveredOption === OPTION_1.id
                ? 'scale-105 shadow-2xl ring-4 ring-blue-300'
                : 'hover:scale-102 hover:shadow-xl'
            } border-2 ${
              selectedOption === OPTION_1.id
                ? 'border-blue-500'
                : hoveredOption === OPTION_1.id
                ? 'border-blue-300'
                : 'border-gray-200'
            }`}
            onClick={() => setSelectedOption(selectedOption === OPTION_1.id ? null : OPTION_1.id)}
            onMouseEnter={() => setHoveredOption(OPTION_1.id)}
            onMouseLeave={() => setHoveredOption(null)}
          >
            {/* Header */}
            <div className={`absolute top-0 left-0 right-0 h-2 bg-gradient-to-r ${OPTION_1.gradient} rounded-t-lg`} />
            
            <div className="pt-4">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{OPTION_1.icon}</div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{OPTION_1.title}</h3>
                    <p className="text-sm text-gray-600">{OPTION_1.subtitle}</p>
                  </div>
                </div>
                <Badge status="info" className="bg-blue-100 text-blue-800">
                  {OPTION_1.deploymentTime}
                </Badge>
              </div>

              <p className="text-gray-700 mb-6 font-medium">{OPTION_1.description}</p>

              {/* Features */}
              <div className="space-y-3 mb-6">
                {OPTION_1.features.map((feature, idx) => (
                  <div key={idx} className="flex items-start gap-3">
                    <span className="text-green-500 text-xl mt-0.5">✅</span>
                    <span className="text-gray-700 flex-1">{feature}</span>
                  </div>
                ))}
              </div>

              {/* Best For */}
              <div className="bg-blue-50 rounded-lg p-4 mb-4">
                <div className="text-sm font-semibold text-blue-900 mb-2">Best For:</div>
                <ul className="space-y-1">
                  {OPTION_1.bestFor.map((item, idx) => (
                    <li key={idx} className="text-sm text-blue-800 flex items-center gap-2">
                      <span className="text-blue-500">•</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* CTA */}
              <button
                className={`w-full py-3 px-6 rounded-lg font-semibold transition-all ${
                  selectedOption === OPTION_1.id
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                }`}
              >
                {selectedOption === OPTION_1.id ? 'Selected ✓' : 'Choose This Option'}
              </button>
            </div>
          </Card>

          {/* Option 2: MCP Agent Integration */}
          <Card
            className={`relative cursor-pointer transition-all duration-300 transform ${
              selectedOption === OPTION_2.id || hoveredOption === OPTION_2.id
                ? 'scale-105 shadow-2xl ring-4 ring-purple-300'
                : 'hover:scale-102 hover:shadow-xl'
            } border-2 ${
              selectedOption === OPTION_2.id
                ? 'border-purple-500'
                : hoveredOption === OPTION_2.id
                ? 'border-purple-300'
                : 'border-gray-200'
            }`}
            onClick={() => setSelectedOption(selectedOption === OPTION_2.id ? null : OPTION_2.id)}
            onMouseEnter={() => setHoveredOption(OPTION_2.id)}
            onMouseLeave={() => setHoveredOption(null)}
          >
            {/* Header */}
            <div className={`absolute top-0 left-0 right-0 h-2 bg-gradient-to-r ${OPTION_2.gradient} rounded-t-lg`} />
            
            <div className="pt-4">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{OPTION_2.icon}</div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{OPTION_2.title}</h3>
                    <p className="text-sm text-gray-600">{OPTION_2.subtitle}</p>
                  </div>
                </div>
                <Badge status="info" className="bg-purple-100 text-purple-800">
                  {OPTION_2.deploymentTime}
                </Badge>
              </div>

              <p className="text-gray-700 mb-6 font-medium">{OPTION_2.description}</p>

              {/* Features */}
              <div className="space-y-3 mb-6">
                {OPTION_2.features.map((feature, idx) => (
                  <div key={idx} className="flex items-start gap-3">
                    <span className="text-green-500 text-xl mt-0.5">✅</span>
                    <span className="text-gray-700 flex-1">{feature}</span>
                  </div>
                ))}
              </div>

              {/* Best For */}
              <div className="bg-purple-50 rounded-lg p-4 mb-4">
                <div className="text-sm font-semibold text-purple-900 mb-2">Best For:</div>
                <ul className="space-y-1">
                  {OPTION_2.bestFor.map((item, idx) => (
                    <li key={idx} className="text-sm text-purple-800 flex items-center gap-2">
                      <span className="text-purple-500">•</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* CTA */}
              <button
                className={`w-full py-3 px-6 rounded-lg font-semibold transition-all ${
                  selectedOption === OPTION_2.id
                    ? 'bg-purple-600 text-white hover:bg-purple-700'
                    : 'bg-purple-100 text-purple-700 hover:bg-purple-200'
                }`}
              >
                {selectedOption === OPTION_2.id ? 'Selected ✓' : 'Choose This Option'}
              </button>
            </div>
          </Card>
        </div>

        {/* Comparison Table */}
        {selectedOption && (
          <Card className="bg-gradient-to-br from-gray-50 to-blue-50 border-2 border-blue-200">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {selectedOption === OPTION_1.id ? OPTION_1.title : OPTION_2.title}
              </h3>
              <p className="text-gray-600">
                {selectedOption === OPTION_1.id ? OPTION_1.description : OPTION_2.description}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {selectedOption === OPTION_1.id ? '35 min' : '55 min'}
                </div>
                <div className="text-sm text-gray-600">Deployment Time</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">10x</div>
                <div className="text-sm text-gray-600">Productivity Multiplier</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">80+</div>
                <div className="text-sm text-gray-600">EHR Systems Supported</div>
              </div>
            </div>
          </Card>
        )}

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Enhance Your Team's Productivity?
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


