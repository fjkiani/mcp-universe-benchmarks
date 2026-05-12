// SaaS Explainer - Interactive module explorer
// Shows what Receptionist OS is (the SaaS product) before introducing AI
// Doctor-friendly language, benefit-first

import { useState } from 'react'
import { Card } from '../common/Card'

const CORE_MODULES = [
  {
    id: 'reception',
    name: 'Reception Desk',
    icon: '📞',
    color: 'blue',
    gradient: 'from-blue-500 to-cyan-500',
    simple: 'Handles all patient calls, texts, and messages',
    detailed: 'Every time a patient calls, texts, or fills out a form on your website, this module manages it. It answers immediately, collects information, and routes them to the right person or department.',
    benefit: 'No more missed calls or patients on hold. Every patient gets an immediate response, 24/7.',
    examples: [
      'Patient calls to schedule appointment',
      'Patient texts about prescription refill',
      'New patient fills out intake form'
    ]
  },
  {
    id: 'scheduling',
    name: 'Smart Scheduling',
    icon: '📅',
    color: 'green',
    gradient: 'from-green-500 to-emerald-500',
    simple: 'Books appointments directly in your system',
    detailed: 'Automatically checks your calendar, finds available slots, books the appointment, and sends confirmations—all in your existing scheduling system (Epic, Cerner, or whichever you use).',
    benefit: 'Your staff never manually enters appointments again. No double-bookings, no scheduling errors.',
    examples: [
      'Books appointment while patient is on phone',
      'Sends automatic reminders (text/email)',
      'Manages cancellations and rescheduling'
    ]
  },
  {
    id: 'insurance',
    name: 'Insurance Verification',
    icon: '💳',
    color: 'purple',
    gradient: 'from-purple-500 to-pink-500',
    simple: 'Checks insurance coverage automatically',
    detailed: 'Instantly verifies patient insurance eligibility, checks benefits, and handles prior authorization tracking—all before the appointment.',
    benefit: 'No more spending 15 minutes per patient on hold with insurance companies. Done in 2 seconds.',
    examples: [
      'Checks if insurance is active',
      'Verifies coverage for specific procedures',
      'Tracks prior authorization status'
    ]
  },
  {
    id: 'triage',
    name: 'Patient Triage',
    icon: '🚨',
    color: 'red',
    gradient: 'from-red-500 to-orange-500',
    simple: 'Assesses urgency and routes appropriately',
    detailed: 'Asks patients about their symptoms, determines urgency level, and immediately routes emergencies (chest pain, stroke symptoms) to 911 or ER while scheduling routine cases for appointments.',
    benefit: 'Never miss a life-threatening emergency. Routine cases get scheduled automatically.',
    examples: [
      'Routes chest pain to 911 immediately',
      'Schedules cold/flu for next available slot',
      'Escalates complex cases to nurse'
    ]
  },
  {
    id: 'telehealth',
    name: 'Telehealth Coordination',
    icon: '📹',
    color: 'indigo',
    gradient: 'from-indigo-500 to-purple-500',
    simple: 'Manages video visits (works with Zoom, Doxy.me, etc.)',
    detailed: 'Schedules video visits, sends links to patients, records sessions, and syncs everything to your records. Works with your existing video platform or provides a built-in one.',
    benefit: 'Telehealth visits run smoothly without your staff managing links, reminders, and follow-up.',
    examples: [
      'Sends video link to patient',
      'Records and transcribes consultation',
      'Updates medical record automatically'
    ]
  },
  {
    id: 'messaging',
    name: 'Patient Messaging',
    icon: '💬',
    color: 'teal',
    gradient: 'from-teal-500 to-cyan-500',
    simple: 'Sends text messages and emails (HIPAA-compliant)',
    detailed: 'Handles all patient communication via text and email while automatically protecting health information (PHI). Every message is logged and compliant.',
    benefit: 'Communicate freely with patients while staying HIPAA-compliant—no more worrying about security.',
    examples: [
      'Appointment reminders via text',
      'Test result notifications',
      'Follow-up care instructions'
    ]
  },
  {
    id: 'ehr-sync',
    name: 'EHR Connection',
    icon: '🔄',
    color: 'amber',
    gradient: 'from-amber-500 to-yellow-500',
    simple: 'Connects everything to your medical records system',
    detailed: 'Every appointment, call, message, and update goes directly into your EHR (Epic, Cerner, athenahealth, or any of 80+ systems). No manual data entry.',
    benefit: 'You never update two systems again. Everything stays in sync automatically.',
    examples: [
      'Appointment shows in your EHR instantly',
      'Call notes update patient chart',
      'Insurance verification saves to record'
    ]
  },
  {
    id: 'admin',
    name: 'Admin & Security',
    icon: '🔒',
    color: 'gray',
    gradient: 'from-gray-500 to-slate-500',
    simple: 'Keeps everything secure and compliant',
    detailed: 'Manages user permissions, logs every action for compliance, encrypts all data, and handles all HIPAA requirements automatically.',
    benefit: 'Stay compliant without thinking about it. All security and audit trails handled automatically.',
    examples: [
      'Role-based access (receptionist vs doctor)',
      'Complete audit trail for compliance',
      'Automatic HIPAA compliance'
    ]
  }
]

export function SaaSExplainer() {
  const [selectedModule, setSelectedModule] = useState(null)
  const [hoveredModule, setHoveredModule] = useState(null)

  const module = selectedModule || hoveredModule

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-indigo-100 text-indigo-800 text-sm font-medium">
            <span className="mr-2">💼</span>
            What Is Receptionist OS?
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            One <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Complete System</span> for Your Front Office
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-4">
            Receptionist OS is software that runs your entire front office—from the phone ringing to the appointment being in your calendar. Everything in one place, connected to your medical records.
          </p>

          <p className="text-lg text-gray-700 max-w-2xl mx-auto font-medium">
            <strong>Click any module below</strong> to see what it does in plain English.
          </p>
        </div>

        {/* Module Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          {CORE_MODULES.map((mod) => (
            <button
              key={mod.id}
              onClick={() => setSelectedModule(selectedModule?.id === mod.id ? null : mod)}
              onMouseEnter={() => setHoveredModule(mod)}
              onMouseLeave={() => setHoveredModule(null)}
              className={`relative p-6 rounded-xl border-2 transition-all duration-300 transform ${
                selectedModule?.id === mod.id
                  ? `bg-gradient-to-br ${mod.gradient} text-white border-transparent scale-105 shadow-2xl`
                  : hoveredModule?.id === mod.id
                  ? 'bg-white border-indigo-300 scale-105 shadow-lg'
                  : 'bg-white border-gray-200 hover:border-indigo-200 hover:shadow-md'
              }`}
            >
              <div className="text-center">
                <div className="text-4xl mb-2">{mod.icon}</div>
                <div className={`text-sm font-semibold ${
                  selectedModule?.id === mod.id ? 'text-white' : 'text-gray-900'
                }`}>
                  {mod.name}
                </div>
              </div>

              {selectedModule?.id === mod.id && (
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-white rounded-full flex items-center justify-center shadow-lg">
                  <span className="text-green-500 text-sm">✓</span>
                </div>
              )}
            </button>
          ))}
        </div>

        {/* Module Details */}
        {module && (
          <Card className="bg-white border-2 border-indigo-200 shadow-xl animate-fade-in-up">
            <div className="flex items-start gap-6">
              {/* Icon */}
              <div className={`flex-shrink-0 w-20 h-20 rounded-2xl bg-gradient-to-br ${module.gradient} flex items-center justify-center shadow-lg`}>
                <span className="text-5xl">{module.icon}</span>
              </div>

              <div className="flex-1">
                {/* Title */}
                <h3 className="text-3xl font-bold text-gray-900 mb-2">{module.name}</h3>
                <p className="text-lg text-gray-600 mb-4">{module.simple}</p>

                {/* Detailed Explanation */}
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <div className="text-sm font-semibold text-gray-700 mb-2">How it works:</div>
                  <p className="text-gray-700 leading-relaxed">{module.detailed}</p>
                </div>

                {/* Benefit */}
                <div className={`bg-gradient-to-r ${module.gradient} bg-opacity-10 rounded-lg p-4 mb-4`}>
                  <div className="text-sm font-semibold text-gray-900 mb-2">✨ What this means for you:</div>
                  <p className="text-gray-900 font-medium leading-relaxed">{module.benefit}</p>
                </div>

                {/* Examples */}
                <div>
                  <div className="text-sm font-semibold text-gray-700 mb-2">Real examples:</div>
                  <ul className="space-y-2">
                    {module.examples.map((example, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-green-500 mt-0.5">✓</span>
                        <span className="text-gray-700">{example}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Summary */}
        <div className="mt-12 text-center">
          <Card className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-0 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-2xl font-bold mb-4">The Result: Your Front Office in One Place</h3>
              <p className="text-lg opacity-90 leading-relaxed">
                Instead of juggling multiple systems, phone lines, and manual processes—everything runs through one unified platform that connects directly to your medical records. Your staff focuses on patients, not paperwork.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}





