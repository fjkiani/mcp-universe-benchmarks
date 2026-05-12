// Appointment Scheduling Demo - Interactive comparison showing 12min → 3sec
// Visual, animated component replacing text dump

import { useState, useEffect } from 'react'
import { Card } from '../common/Card'

const TRADITIONAL_STEPS = [
  { step: 1, text: "Receptionist checks EHR calendar", time: 2, icon: "👩‍💼" },
  { step: 2, text: "Calls patient back", time: 5, icon: "📞" },
  { step: 3, text: "Manually enters appointment", time: 3, icon: "⌨️" },
  { step: 4, text: "Sends confirmation", time: 2, icon: "📧" }
]

const AI_STEPS = [
  { step: 1, text: "AI checks EHR availability", time: 0.3, icon: "🤖" },
  { step: 2, text: "Books appointment directly in EHR", time: 0.5, icon: "⚡" },
  { step: 3, text: "Sends confirmation automatically", time: 0.2, icon: "✅" }
]

export function AppointmentSchedulingDemo() {
  const [isRunning, setIsRunning] = useState(false)
  const [currentStep, setCurrentStep] = useState({ traditional: 0, ai: 0 })
  const [timeElapsed, setTimeElapsed] = useState({ traditional: 0, ai: 0 })

  const startDemo = () => {
    setIsRunning(true)
    setCurrentStep({ traditional: 0, ai: 0 })
    setTimeElapsed({ traditional: 0, ai: 0 })
  }

  useEffect(() => {
    if (!isRunning) return

    const interval = setInterval(() => {
      setTimeElapsed(prev => ({
        traditional: prev.traditional + 0.1,
        ai: prev.ai + 0.1
      }))
    }, 100)

    return () => clearInterval(interval)
  }, [isRunning])

  // Auto-advance steps based on time
  useEffect(() => {
    if (!isRunning) return

    // Traditional steps
    let traditionalTime = 0
    for (let i = 0; i < TRADITIONAL_STEPS.length; i++) {
      traditionalTime += TRADITIONAL_STEPS[i].time * 60 // Convert to seconds
      if (timeElapsed.traditional >= traditionalTime && currentStep.traditional === i) {
        setCurrentStep(prev => ({ ...prev, traditional: i + 1 }))
      }
    }

    // AI steps
    let aiTime = 0
    for (let i = 0; i < AI_STEPS.length; i++) {
      aiTime += AI_STEPS[i].time
      if (timeElapsed.ai >= aiTime && currentStep.ai === i) {
        setCurrentStep(prev => ({ ...prev, ai: i + 1 }))
      }
    }

    // Stop when both are complete
    if (currentStep.traditional >= TRADITIONAL_STEPS.length && currentStep.ai >= AI_STEPS.length) {
      setTimeout(() => setIsRunning(false), 1000)
    }
  }, [timeElapsed, currentStep, isRunning])

  const formatTime = (seconds) => {
    if (seconds < 60) return `${seconds.toFixed(1)}s`
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}m ${remainingSeconds.toFixed(0)}s`
  }

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-orange-50 via-white to-red-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-orange-100 text-orange-800 text-sm font-medium">
            <span className="mr-2">⚡</span>
            Real-Time Appointment Scheduling
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            <span className="bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">240x Faster</span> Appointment Scheduling
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Traditional appointment booking takes <strong>12 minutes</strong>. Our AI does it in <strong>3 seconds</strong>.
          </p>

          <button
            onClick={startDemo}
            disabled={isRunning}
            className={`px-8 py-4 rounded-lg font-semibold text-lg transition-all transform ${
              isRunning 
                ? 'bg-gray-400 text-gray-600 cursor-not-allowed' 
                : 'bg-orange-600 text-white hover:bg-orange-700 hover:scale-105'
            }`}
          >
            {isRunning ? 'Demo Running...' : 'Start Live Demo'} ⚡
          </button>
        </div>

        {/* Side-by-Side Comparison */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {/* Traditional Way */}
          <Card className="bg-gradient-to-br from-red-50 to-orange-50 border-2 border-red-200">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-red-700 mb-2">Traditional Way</h3>
              <div className="text-4xl font-bold text-red-600">
                {formatTime(timeElapsed.traditional)}
              </div>
              <div className="text-sm text-red-600">Target: 12 minutes</div>
            </div>

            <div className="space-y-4">
              {TRADITIONAL_STEPS.map((step, idx) => (
                <div
                  key={idx}
                  className={`flex items-center gap-4 p-4 rounded-lg transition-all ${
                    currentStep.traditional > idx 
                      ? 'bg-red-100 border-2 border-red-300' 
                      : currentStep.traditional === idx && isRunning
                      ? 'bg-yellow-100 border-2 border-yellow-300 animate-pulse'
                      : 'bg-white border border-gray-200'
                  }`}
                >
                  <div className="text-2xl">{step.icon}</div>
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{step.text}</div>
                    <div className="text-sm text-gray-600">{step.time} minutes</div>
                  </div>
                  {currentStep.traditional > idx && (
                    <div className="text-red-600">✅</div>
                  )}
                </div>
              ))}
            </div>
          </Card>

          {/* AI Way */}
          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-green-700 mb-2">Our AI Way</h3>
              <div className="text-4xl font-bold text-green-600">
                {formatTime(timeElapsed.ai)}
              </div>
              <div className="text-sm text-green-600">Target: 3 seconds</div>
            </div>

            <div className="space-y-4">
              {AI_STEPS.map((step, idx) => (
                <div
                  key={idx}
                  className={`flex items-center gap-4 p-4 rounded-lg transition-all ${
                    currentStep.ai > idx 
                      ? 'bg-green-100 border-2 border-green-300' 
                      : currentStep.ai === idx && isRunning
                      ? 'bg-yellow-100 border-2 border-yellow-300 animate-pulse'
                      : 'bg-white border border-gray-200'
                  }`}
                >
                  <div className="text-2xl">{step.icon}</div>
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{step.text}</div>
                    <div className="text-sm text-gray-600">{step.time} seconds</div>
                  </div>
                  {currentStep.ai > idx && (
                    <div className="text-green-600">✅</div>
                  )}
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Results Summary */}
        <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-center">
          <h3 className="text-3xl font-bold mb-4">
            The Result: 240x Faster Scheduling
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="text-4xl font-bold mb-2">12 min → 3 sec</div>
              <div className="text-lg opacity-90">Time Reduction</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">4 → 1</div>
              <div className="text-lg opacity-90">Steps Eliminated</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">0%</div>
              <div className="text-lg opacity-90">Human Error Rate</div>
            </div>
          </div>
        </Card>
      </div>
    </section>
  )
}
