// HIPAA Compliance Center - Interactive compliance features showcase
// Based on LANDING_PAGE.md lines 344-353

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const COMPLIANCE_FEATURES = [
  {
    id: 'phi-detection',
    title: 'PHI Detection',
    icon: '🛡️',
    description: 'Automatically detects and blocks PHI in SMS/email',
    status: 'active',
    demo: 'Try sending a message with PHI to see it blocked in real-time',
    color: 'blue'
  },
  {
    id: 'audit-logging',
    title: 'Audit Logging',
    icon: '📋',
    description: 'Every action is logged with timestamp and user',
    status: 'active',
    demo: 'View complete audit trail for all patient interactions',
    color: 'green'
  },
  {
    id: 'baa',
    title: 'BAA Available',
    icon: '📄',
    description: 'Business Associate Agreement for all APIs',
    status: 'available',
    demo: 'Download BAA templates for all integrated services',
    color: 'purple'
  },
  {
    id: 'encryption',
    title: 'End-to-End Encryption',
    icon: '🔐',
    description: 'All data encrypted in transit and at rest',
    status: 'active',
    demo: 'See encryption status for all data flows',
    color: 'indigo'
  },
  {
    id: 'access-controls',
    title: 'Access Controls',
    icon: '👥',
    description: 'Role-based access management',
    status: 'active',
    demo: 'Configure role-based permissions',
    color: 'teal'
  }
]

export function HIPAAComplianceCenter() {
  const [selectedFeature, setSelectedFeature] = useState(null)
  const [phiDemo, setPhiDemo] = useState({ message: '', blocked: false })

  const testPHIDetection = (message) => {
    // Simple PHI detection demo
    const phiPatterns = [
      /\b\d{3}-\d{2}-\d{4}\b/, // SSN
      /\b\d{3}\.\d{3}\.\d{4}\b/, // Phone
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, // Email (could contain PHI)
      /\b\d{1,2}\/\d{1,2}\/\d{4}\b/, // Date of birth
    ]
    
    const hasPHI = phiPatterns.some(pattern => pattern.test(message))
    setPhiDemo({ message, blocked: hasPHI })
  }

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-indigo-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-indigo-100 text-indigo-800 text-sm font-medium">
            <span className="mr-2">🔒</span>
            HIPAA Compliance
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            <span className="bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent">Built-in Compliance</span> from Day One
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Most AI tools require manual HIPAA compliance. Ours is <strong>built-in from day one</strong>—no configuration needed.
          </p>
        </div>

        {/* Compliance Badge */}
        <Card className="mb-16 bg-gradient-to-r from-indigo-600 to-blue-600 text-white border-0 text-center">
          <div className="text-5xl mb-4">✅</div>
          <h3 className="text-3xl font-bold mb-4">HIPAA-Compliant by Design</h3>
          <p className="text-lg opacity-90 max-w-2xl mx-auto">
            All features are HIPAA-compliant out of the box. No additional setup required.
          </p>
        </Card>

        {/* Compliance Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {COMPLIANCE_FEATURES.map((feature) => (
            <Card
              key={feature.id}
              className={`cursor-pointer transition-all duration-300 transform hover:scale-105 hover:shadow-xl border-2 ${
                selectedFeature === feature.id
                  ? feature.color === 'blue' ? 'border-blue-500' :
                    feature.color === 'green' ? 'border-green-500' :
                    feature.color === 'purple' ? 'border-purple-500' :
                    feature.color === 'indigo' ? 'border-indigo-500' :
                    'border-teal-500'
                  : 'border-gray-200'
              }`}
              onClick={() => setSelectedFeature(selectedFeature === feature.id ? null : feature.id)}
            >
              <div className="text-center">
                <div className="text-4xl mb-3">{feature.icon}</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-600 mb-4">{feature.description}</p>
                <Badge 
                  status={feature.status === 'active' ? 'success' : 'info'}
                  className="mb-3"
                >
                  {feature.status === 'active' ? 'Active' : 'Available'}
                </Badge>
              </div>
            </Card>
          ))}
        </div>

        {/* PHI Detection Demo */}
        <Card className="mb-16 bg-gradient-to-br from-red-50 to-orange-50 border-2 border-red-200">
          <div className="text-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              🛡️ PHI Detection Demo
            </h3>
            <p className="text-gray-600 mb-6">
              Try sending a message with PHI to see it blocked automatically
            </p>
            
            <div className="max-w-md mx-auto">
              <input
                type="text"
                placeholder="Type a message (try including SSN: 123-45-6789)"
                className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none mb-4"
                onChange={(e) => testPHIDetection(e.target.value)}
              />
              
              {phiDemo.message && (
                <div className={`p-4 rounded-lg ${
                  phiDemo.blocked 
                    ? 'bg-red-100 border-2 border-red-300' 
                    : 'bg-green-100 border-2 border-green-300'
                }`}>
                  <div className="flex items-center gap-2 mb-2">
                    {phiDemo.blocked ? (
                      <>
                        <span className="text-red-600 text-xl">🚫</span>
                        <span className="font-bold text-red-800">PHI Detected - Message Blocked</span>
                      </>
                    ) : (
                      <>
                        <span className="text-green-600 text-xl">✅</span>
                        <span className="font-bold text-green-800">No PHI Detected - Message Safe</span>
                      </>
                    )}
                  </div>
                  <p className="text-sm text-gray-700">
                    {phiDemo.blocked 
                      ? 'This message contains protected health information and cannot be sent via unsecured channels.'
                      : 'This message is safe to send.'}
                  </p>
                </div>
              )}
            </div>
          </div>
        </Card>

        {/* Compliance Checklist */}
        <Card className="bg-gradient-to-br from-gray-50 to-blue-50 border-2 border-blue-200">
          <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Complete Compliance Checklist
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {COMPLIANCE_FEATURES.map((feature) => (
              <div key={feature.id} className="flex items-start gap-3">
                <span className="text-green-600 text-xl mt-0.5">✅</span>
                <div>
                  <div className="font-semibold text-gray-900">{feature.title}</div>
                  <div className="text-sm text-gray-600">{feature.description}</div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <Card className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Compliance Built-In, Not Bolted On
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Every feature is HIPAA-compliant from day one. No additional configuration needed.
            </p>
            <button className="px-8 py-3 bg-white text-indigo-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              View Compliance Documentation →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}






