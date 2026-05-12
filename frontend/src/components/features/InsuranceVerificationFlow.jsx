// Insurance Verification Flow - Interactive comparison showing 15min → 2sec
// Visual, animated component similar to AppointmentSchedulingDemo
// Based on LANDING_PAGE.md lines 101-106

import { useState, useEffect } from 'react'
import { Card } from '../common/Card'

const TRADITIONAL_STEPS = [
  { step: 1, text: "Staff calls insurance company", time: 5, icon: "📞" },
  { step: 2, text: "Waits on hold for representative", time: 4, icon: "⏳" },
  { step: 3, text: "Provides patient information verbally", time: 3, icon: "🗣️" },
  { step: 4, text: "Manually enters coverage details", time: 2, icon: "⌨️" },
  { step: 5, text: "Files verification in patient record", time: 1, icon: "📁" }
]

const AI_STEPS = [
  { step: 1, text: "AI queries insurance API automatically", time: 0.5, icon: "🤖" },
  { step: 2, text: "Retrieves eligibility and benefits", time: 0.8, icon: "⚡" },
  { step: 3, text: "Syncs to EHR automatically", time: 0.7, icon: "✅" }
]

export function InsuranceVerificationFlow() {
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
    <section className="py-20 px-4 bg-gradient-to-br from-purple-50 via-white to-pink-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-purple-100 text-purple-800 text-sm font-medium">
            <span className="mr-2">💳</span>
            Insurance Verification
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">450x Faster</span> Insurance Verification
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Traditional insurance verification takes <strong>15 minutes</strong>. Our AI does it in <strong>2 seconds</strong>.
          </p>

          <button
            onClick={startDemo}
            disabled={isRunning}
            className={`px-8 py-4 rounded-lg font-semibold text-lg transition-all transform ${
              isRunning 
                ? 'bg-gray-400 text-gray-600 cursor-not-allowed' 
                : 'bg-purple-600 text-white hover:bg-purple-700 hover:scale-105'
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
              <div className="text-sm text-red-600">Target: 15 minutes</div>
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
              <div className="text-sm text-green-600">Target: 2 seconds</div>
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
        <Card className="bg-gradient-to-r from-purple-600 to-pink-600 text-white text-center">
          <h3 className="text-3xl font-bold mb-4">
            The Result: 450x Faster Verification
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="text-4xl font-bold mb-2">15 min → 2 sec</div>
              <div className="text-lg opacity-90">Time Reduction</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">5 → 3</div>
              <div className="text-lg opacity-90">Steps Simplified</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">450x</div>
              <div className="text-lg opacity-90">Faster Processing</div>
            </div>
          </div>
        </Card>

        {/* Additional Benefits */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <Card className="text-center bg-gradient-to-br from-blue-50 to-cyan-50">
            <div className="text-3xl mb-3">✅</div>
            <h4 className="font-bold text-gray-900 mb-2">Automatic Benefits Check</h4>
            <p className="text-sm text-gray-600">Checks coverage, deductibles, and copays automatically</p>
          </Card>
          <Card className="text-center bg-gradient-to-br from-green-50 to-emerald-50">
            <div className="text-3xl mb-3">📋</div>
            <h4 className="font-bold text-gray-900 mb-2">Prior Authorization</h4>
            <p className="text-sm text-gray-600">Handles prior authorizations without manual paperwork</p>
          </Card>
          <Card className="text-center bg-gradient-to-br from-purple-50 to-pink-50">
            <div className="text-3xl mb-3">🔄</div>
            <h4 className="font-bold text-gray-900 mb-2">Real-time Sync</h4>
            <p className="text-sm text-gray-600">Updates EHR instantly with verification results</p>
          </Card>
        </div>
      </div>
    </section>
  )
}






