// Twenty Four Seven Coverage - 24/7 availability visualization
// Based on LANDING_PAGE.md lines 357-367

import { useState, useEffect } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const HOURS = Array.from({ length: 24 }, (_, i) => i)
const COST_PER_MISSED_CALL = 150 // Average revenue per appointment
const ANNUAL_MISSED_CALLS = 333 // $50K / $150 per call

export function TwentyFourSevenCoverage() {
  const [currentHour, setCurrentHour] = useState(new Date().getHours())
  const [selectedHour, setSelectedHour] = useState(null)
  const [missedCalls, setMissedCalls] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentHour(new Date().getHours())
    }, 60000) // Update every minute

    return () => clearInterval(interval)
  }, [])

  const getHourLabel = (hour) => {
    if (hour === 0) return '12 AM'
    if (hour < 12) return `${hour} AM`
    if (hour === 12) return '12 PM'
    return `${hour - 12} PM`
  }

  const getAvailabilityStatus = (hour) => {
    // Business hours: 8 AM - 6 PM (8-18)
    if (hour >= 8 && hour < 18) {
      return { status: 'staff', label: 'Staff Available', color: 'green' }
    }
    return { status: 'ai', label: 'AI Coverage', color: 'blue' }
  }

  const calculateSavings = () => {
    return missedCalls * COST_PER_MISSED_CALL
  }

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-gray-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">⏰</span>
            24/7 Coverage
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">Never Miss a Call</span> - Even at 2 AM
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Practices lose <strong>$50K/year</strong> in missed after-hours calls. Our AI answers <strong>100% of calls</strong>, 24/7.
          </p>
        </div>

        {/* Problem Statement */}
        <Card className="mb-16 bg-gradient-to-r from-red-600 to-orange-600 text-white border-0">
          <div className="text-center">
            <div className="text-3xl mb-4">💸</div>
            <h3 className="text-2xl font-bold mb-4">The Problem</h3>
            <p className="text-lg opacity-90 max-w-2xl mx-auto">
              Practices lose <strong>$50K/year</strong> in missed after-hours calls. Staff can't work 24/7, but patients need care around the clock.
            </p>
          </div>
        </Card>

        {/* 24-Hour Timeline */}
        <Card className="mb-16">
          <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">
            24-Hour Coverage Timeline
          </h3>
          
          <div className="grid grid-cols-12 gap-2 mb-8">
            {HOURS.map((hour) => {
              const availability = getAvailabilityStatus(hour)
              const isCurrent = hour === currentHour
              const isSelected = hour === selectedHour
              
              return (
                <div
                  key={hour}
                  className={`text-center p-2 rounded-lg cursor-pointer transition-all transform hover:scale-110 ${
                    isCurrent
                      ? 'ring-4 ring-blue-500 scale-110'
                      : isSelected
                      ? 'ring-2 ring-blue-300'
                      : ''
                  } ${
                    availability.status === 'staff'
                      ? 'bg-green-100 border-2 border-green-300'
                      : 'bg-blue-100 border-2 border-blue-300'
                  }`}
                  onClick={() => setSelectedHour(hour === selectedHour ? null : hour)}
                >
                  <div className="text-xs font-bold text-gray-900 mb-1">
                    {getHourLabel(hour)}
                  </div>
                  <div className={`text-xs ${
                    availability.status === 'staff' ? 'text-green-700' : 'text-blue-700'
                  }`}>
                    {availability.label}
                  </div>
                  {isCurrent && (
                    <div className="text-xs text-blue-600 font-bold mt-1">NOW</div>
                  )}
                </div>
              )
            })}
          </div>

          {/* Legend */}
          <div className="flex justify-center gap-6 mb-6">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-300 rounded"></div>
              <span className="text-sm text-gray-700">Staff Hours (8 AM - 6 PM)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-blue-300 rounded"></div>
              <span className="text-sm text-gray-700">AI Coverage (24/7)</span>
            </div>
          </div>

          {/* Selected Hour Details */}
          {selectedHour !== null && (
            <Card className="bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200">
              <div className="text-center">
                <h4 className="text-xl font-bold text-gray-900 mb-4">
                  Coverage at {getHourLabel(selectedHour)}
                </h4>
                {(() => {
                  const availability = getAvailabilityStatus(selectedHour)
                  return (
                    <div>
                      <Badge 
                        status={availability.status === 'staff' ? 'success' : 'info'}
                        className="mb-4"
                      >
                        {availability.label}
                      </Badge>
                      <p className="text-gray-700">
                        {availability.status === 'staff'
                          ? 'Your staff handles calls during business hours with AI assistance for routine tasks.'
                          : 'AI handles all calls automatically, ensuring no patient call goes unanswered.'}
                      </p>
                    </div>
                  )
                })()}
              </div>
            </Card>
          )}
        </Card>

        {/* Benefits Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <Card className="text-center bg-gradient-to-br from-blue-500 to-cyan-500 text-white">
            <div className="text-4xl mb-3">🌙</div>
            <div className="text-2xl font-bold mb-2">Never Sleeps</div>
            <div className="text-sm opacity-90">Answers calls 24/7</div>
          </Card>
          <Card className="text-center bg-gradient-to-br from-green-500 to-emerald-500 text-white">
            <div className="text-4xl mb-3">💰</div>
            <div className="text-2xl font-bold mb-2">No Overtime</div>
            <div className="text-sm opacity-90">No additional staffing costs</div>
          </Card>
          <Card className="text-center bg-gradient-to-br from-purple-500 to-pink-500 text-white">
            <div className="text-4xl mb-3">⚡</div>
            <div className="text-2xl font-bold mb-2">Instant Response</div>
            <div className="text-sm opacity-90">No hold time</div>
          </Card>
          <Card className="text-center bg-gradient-to-br from-orange-500 to-red-500 text-white">
            <div className="text-4xl mb-3">✅</div>
            <div className="text-2xl font-bold mb-2">Consistent Quality</div>
            <div className="text-sm opacity-90">Same service every time</div>
          </Card>
        </div>

        {/* Cost Savings Calculator */}
        <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200">
          <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">
            💰 Cost Savings Calculator
          </h3>
          
          <div className="max-w-md mx-auto">
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Missed Calls Per Year (Industry Average: 333)
              </label>
              <input
                type="number"
                min="0"
                max="1000"
                value={missedCalls}
                onChange={(e) => setMissedCalls(parseInt(e.target.value) || 0)}
                className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-green-500 focus:outline-none"
              />
            </div>
            
            <Card className="bg-white text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">
                ${calculateSavings().toLocaleString()}/year
              </div>
              <div className="text-sm text-gray-600">Revenue Lost to Missed Calls</div>
              <div className="mt-4 text-lg font-semibold text-gray-900">
                With AI: <span className="text-green-600">$0 lost</span> (100% call capture)
              </div>
            </Card>
          </div>
        </Card>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <Card className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Capture 100% of Patient Calls, 24/7
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Never lose another patient call—even at 2 AM. AI handles after-hours calls automatically.
            </p>
            <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              See How It Works →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}






