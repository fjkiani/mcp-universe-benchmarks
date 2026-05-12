// Capability Grid - 8 clickable cards for each core module
// Links to individual capability deep-dive pages

import { Card } from '../../common/Card'

const CAPABILITIES = [
  {
    id: 'reception',
    icon: '📞',
    name: 'Reception Desk',
    summary: 'Handles all patient calls, texts, and messages 24/7',
    benefit: 'No more missed calls or patients on hold',
    gradient: 'from-blue-500 to-cyan-500',
    stats: { label: 'Response Time', value: '< 1 sec' }
  },
  {
    id: 'scheduling',
    icon: '📅',
    name: 'Smart Scheduling',
    summary: 'Books appointments directly in your system in 3 seconds',
    benefit: 'Staff handles 240x more bookings',
    gradient: 'from-green-500 to-emerald-500',
    stats: { label: 'Booking Speed', value: '3 seconds' }
  },
  {
    id: 'insurance',
    icon: '💳',
    name: 'Insurance Verification',
    summary: 'Verifies coverage instantly instead of 15-minute phone calls',
    benefit: 'Process 450x more verifications',
    gradient: 'from-purple-500 to-pink-500',
    stats: { label: 'Verification Time', value: '2 seconds' }
  },
  {
    id: 'triage',
    icon: '🚨',
    name: 'Patient Triage',
    summary: 'Assesses urgency and routes emergencies immediately',
    benefit: 'Zero missed life-threatening cases',
    gradient: 'from-red-500 to-orange-500',
    stats: { label: 'Emergency Detection', value: '100%' }
  },
  {
    id: 'telehealth',
    icon: '📹',
    name: 'Telehealth Coordination',
    summary: 'Manages video visits, recordings, and documentation',
    benefit: 'Works with Zoom, Doxy.me, or built-in platform',
    gradient: 'from-indigo-500 to-purple-500',
    stats: { label: 'Transcription Accuracy', value: '93.3%' }
  },
  {
    id: 'messaging',
    icon: '💬',
    name: 'Patient Messaging',
    summary: 'HIPAA-compliant text and email with automatic PHI protection',
    benefit: 'Handle 10x more patient messages',
    gradient: 'from-teal-500 to-cyan-500',
    stats: { label: 'Message Capacity', value: '10x' }
  },
  {
    id: 'ehr-sync',
    icon: '🔄',
    name: 'EHR Connection',
    summary: 'Connects to 80+ medical records systems automatically',
    benefit: 'Never update two systems again',
    gradient: 'from-amber-500 to-yellow-500',
    stats: { label: 'Supported EHRs', value: '80+' }
  },
  {
    id: 'compliance',
    icon: '🔒',
    name: 'Admin & Security',
    summary: 'HIPAA compliance, encryption, and audit trails built-in',
    benefit: 'Stay compliant automatically',
    gradient: 'from-gray-600 to-slate-600',
    stats: { label: 'Compliance', value: 'Built-in' }
  }
]

export function CapabilityGrid() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Explore Each <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Capability</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Click any module to learn how it works and see it in action
          </p>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {CAPABILITIES.map((capability) => (
            <a
              key={capability.id}
              href={`/capabilities/${capability.id}`}
              className="block group"
            >
              <Card className="h-full hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 cursor-pointer border-2 border-transparent hover:border-blue-300">
                {/* Icon */}
                <div className={`w-16 h-16 mx-auto mb-4 rounded-xl bg-gradient-to-br ${capability.gradient} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform`}>
                  <span className="text-4xl">{capability.icon}</span>
                </div>

                {/* Name */}
                <h3 className="text-xl font-bold text-gray-900 mb-3 text-center group-hover:text-blue-600 transition-colors">
                  {capability.name}
                </h3>

                {/* Summary */}
                <p className="text-sm text-gray-600 mb-3 leading-relaxed">
                  {capability.summary}
                </p>

                {/* Benefit */}
                <div className="bg-green-50 rounded-lg p-3 mb-4">
                  <p className="text-xs font-semibold text-green-800">
                    ✨ {capability.benefit}
                  </p>
                </div>

                {/* Stat */}
                <div className={`bg-gradient-to-r ${capability.gradient} bg-opacity-10 rounded-lg p-3 mb-4`}>
                  <div className="text-xs text-gray-600 mb-1">{capability.stats.label}</div>
                  <div className={`text-2xl font-bold bg-gradient-to-r ${capability.gradient} bg-clip-text text-transparent`}>
                    {capability.stats.value}
                  </div>
                </div>

                {/* Learn More Link */}
                <div className="text-center">
                  <span className="text-blue-600 font-semibold text-sm group-hover:underline inline-flex items-center gap-1">
                    Learn more
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </span>
                </div>
              </Card>
            </a>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 text-center">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-8 max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              All Capabilities Work Together
            </h3>
            <p className="text-gray-700 mb-6 leading-relaxed">
              These 8 modules form a complete front-office platform. Each one enhances the others, and they all connect seamlessly to your medical records system.
            </p>
            <a
              href="/product"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
            >
              See How They Connect →
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}




