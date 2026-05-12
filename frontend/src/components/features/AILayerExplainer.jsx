// AI Layer Explainer - Demystify AI for doctors
// Progressive disclosure with analogies
// Shows AI as helper, not replacement

import { useState } from 'react'
import { Card } from '../common/Card'

const EXPLANATION_STEPS = [
  {
    id: 'analogy',
    title: 'Think of it like a smart assistant for each desk',
    icon: '💡',
    description: 'You know how having an experienced assistant makes your day easier? They handle routine tasks so you can focus on complex cases. That\'s exactly what the AI layer does—but for every role in your office.',
    visual: {
      type: 'analogy',
      items: [
        { role: 'Receptionist', has: 'Smart assistant that answers routine calls', icon: '👩‍💼' },
        { role: 'Scheduler', has: 'Smart assistant that finds open slots instantly', icon: '📅' },
        { role: 'Insurance team', has: 'Smart assistant that checks coverage in seconds', icon: '💳' }
      ]
    }
  },
  {
    id: 'collaboration',
    title: 'Your staff and AI work together',
    icon: '🤝',
    description: 'The AI handles the repetitive, time-consuming tasks. Your staff handles the complex cases that need human judgment, empathy, and expertise. It\'s a partnership, not a replacement.',
    visual: {
      type: 'collaboration',
      scenarios: [
        {
          task: 'Routine appointment request',
          ai: 'Checks calendar, books appointment, sends confirmation',
          human: 'Reviews schedule, adjusts if needed',
          icon: '📅'
        },
        {
          task: 'Complex insurance case',
          ai: 'Gathers initial information, checks basic eligibility',
          human: 'Reviews details, calls insurance if needed, makes decision',
          icon: '💳'
        },
        {
          task: 'Patient with chest pain',
          ai: 'Detects emergency, routes to 911 immediately',
          human: 'Confirms, provides comfort, coordinates care',
          icon: '🚨'
        }
      ]
    }
  },
  {
    id: 'routine-tasks',
    title: 'AI handles the routine stuff',
    icon: '🤖',
    description: 'Most of your staff\'s day is spent on repetitive tasks that follow the same pattern every time. The AI learns these patterns and handles them automatically—freeing your staff to focus on patients.',
    visual: {
      type: 'task-split',
      routine: [
        'Answering "What are your hours?"',
        'Booking standard appointments',
        'Checking if insurance is active',
        'Sending appointment reminders',
        'Updating appointment times in system'
      ],
      complex: [
        'Handling upset patients',
        'Complex insurance issues',
        'Coordinating care between specialists',
        'Building patient relationships',
        'Making judgment calls'
      ]
    }
  },
  {
    id: 'result',
    title: 'The result: Your team achieves more',
    icon: '📈',
    description: 'Your staff doesn\'t work harder—they work smarter. One receptionist can handle the volume that used to require five, because the AI is handling routine calls while they focus on complex cases.',
    visual: {
      type: 'transformation',
      stats: [
        { label: 'Sarah, Receptionist', before: '20 calls/day', after: '100 calls/day', icon: '📞' },
        { label: 'Mike, Scheduler', before: '10 appts/day', after: '2,400 appts/day', icon: '📅' },
        { label: 'Lisa, Insurance', before: '30 checks/day', after: '13,500 checks/day', icon: '💳' }
      ]
    }
  }
]

export function AILayerExplainer() {
  const [currentStep, setCurrentStep] = useState(0)

  const step = EXPLANATION_STEPS[currentStep]

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">🤖</span>
            What Does "AI" Actually Do?
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            AI = Your <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Staff's Smart Assistant</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Don't worry about technical terms. Here's what "AI layer" really means for your practice.
          </p>
        </div>

        {/* Progress Indicators */}
        <div className="flex items-center justify-center gap-4 mb-12">
          {EXPLANATION_STEPS.map((s, idx) => (
            <button
              key={s.id}
              onClick={() => setCurrentStep(idx)}
              className={`flex flex-col items-center gap-2 p-4 rounded-lg transition-all ${
                idx === currentStep
                  ? 'bg-blue-100 ring-2 ring-blue-500'
                  : idx < currentStep
                  ? 'bg-green-50 hover:bg-green-100'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              <div className="text-3xl">{s.icon}</div>
              <div className={`text-xs font-semibold ${
                idx === currentStep ? 'text-blue-900' : 'text-gray-600'
              }`}>
                Step {idx + 1}
              </div>
              {idx < currentStep && (
                <div className="text-green-500 text-sm">✓</div>
              )}
            </button>
          ))}
        </div>

        {/* Step Content */}
        <Card className="bg-white border-2 border-blue-200 shadow-xl mb-8">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">{step.icon}</div>
            <h3 className="text-3xl font-bold text-gray-900 mb-4">{step.title}</h3>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              {step.description}
            </p>
          </div>

          {/* Visual */}
          <div className="mt-8">
            {step.visual.type === 'analogy' && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {step.visual.items.map((item, idx) => (
                  <div key={idx} className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-6 border-2 border-blue-200">
                    <div className="text-5xl mb-3 text-center">{item.icon}</div>
                    <div className="text-lg font-bold text-gray-900 text-center mb-2">{item.role}</div>
                    <div className="text-sm text-gray-700 text-center">{item.has}</div>
                  </div>
                ))}
              </div>
            )}

            {step.visual.type === 'collaboration' && (
              <div className="space-y-6">
                {step.visual.scenarios.map((scenario, idx) => (
                  <div key={idx} className="bg-gray-50 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-4">
                      <span className="text-3xl">{scenario.icon}</span>
                      <h4 className="text-xl font-bold text-gray-900">{scenario.task}</h4>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500">
                        <div className="text-sm font-semibold text-blue-900 mb-2">🤖 AI Assistant Does:</div>
                        <p className="text-gray-700">{scenario.ai}</p>
                      </div>
                      <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-500">
                        <div className="text-sm font-semibold text-green-900 mb-2">👤 Your Staff Does:</div>
                        <p className="text-gray-700">{scenario.human}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {step.visual.type === 'task-split' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-blue-50 rounded-lg p-6 border-2 border-blue-300">
                  <h4 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <span className="text-2xl">🤖</span>
                    AI Handles Routine Tasks
                  </h4>
                  <ul className="space-y-2">
                    {step.visual.routine.map((task, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-blue-500 mt-0.5">✓</span>
                        <span className="text-gray-700">{task}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="bg-green-50 rounded-lg p-6 border-2 border-green-300">
                  <h4 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <span className="text-2xl">👥</span>
                    Staff Focuses on Complex Work
                  </h4>
                  <ul className="space-y-2">
                    {step.visual.complex.map((task, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-green-500 mt-0.5">✓</span>
                        <span className="text-gray-700">{task}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {step.visual.type === 'transformation' && (
              <div className="space-y-4">
                {step.visual.stats.map((stat, idx) => (
                  <div key={idx} className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-6 border-2 border-green-200">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <span className="text-4xl">{stat.icon}</span>
                        <div>
                          <div className="text-lg font-bold text-gray-900">{stat.label}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-6">
                        <div className="text-center">
                          <div className="text-sm text-gray-600 mb-1">Before</div>
                          <div className="text-2xl font-bold text-red-600">{stat.before}</div>
                        </div>
                        <div className="text-3xl text-gray-400">→</div>
                        <div className="text-center">
                          <div className="text-sm text-gray-600 mb-1">With AI</div>
                          <div className="text-3xl font-bold text-green-600">{stat.after}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>

        {/* Navigation */}
        <div className="flex items-center justify-center gap-4">
          <button
            onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
            disabled={currentStep === 0}
            className="px-6 py-3 rounded-lg font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            ← Previous
          </button>
          
          <div className="text-sm text-gray-600">
            {currentStep + 1} of {EXPLANATION_STEPS.length}
          </div>

          <button
            onClick={() => setCurrentStep(Math.min(EXPLANATION_STEPS.length - 1, currentStep + 1))}
            disabled={currentStep === EXPLANATION_STEPS.length - 1}
            className="px-6 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-blue-500 to-purple-500 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            Next →
          </button>
        </div>

        {/* Summary */}
        {currentStep === EXPLANATION_STEPS.length - 1 && (
          <div className="mt-12">
            <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0 max-w-4xl mx-auto">
              <div className="text-center">
                <div className="text-4xl mb-4">✨</div>
                <h3 className="text-2xl font-bold mb-4">Bottom Line</h3>
                <p className="text-lg opacity-90 leading-relaxed">
                  You don't need to understand how AI works technically. What matters: your staff gets smart assistants that handle routine tasks, so they can focus on what they do best—taking care of patients.
                </p>
              </div>
            </Card>
          </div>
        )}
      </div>
    </section>
  )
}





