// Productivity Calculator - Interactive ROI calculator
// Based on LANDING_PAGE.md lines 447-496

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

export function ProductivityCalculator() {
  const [inputs, setInputs] = useState({
    receptionists: 3,
    schedulers: 2,
    insuranceStaff: 1,
    appointmentsPerDay: 20,
    verificationsPerDay: 10
  })

  const calculateResults = () => {
    // Receptionist: 1 → 5 workload capacity
    const receptionistMultiplier = 5
    const receptionistSavings = inputs.receptionists - Math.ceil(inputs.receptionists / receptionistMultiplier)
    
    // Scheduling: 240x faster (3 sec vs 12 min)
    const schedulingMultiplier = 240
    const newAppointmentCapacity = inputs.appointmentsPerDay * schedulingMultiplier
    
    // Insurance: 450x faster (2 sec vs 15 min)
    const insuranceMultiplier = 450
    const newVerificationCapacity = inputs.verificationsPerDay * insuranceMultiplier
    
    // Cost savings (assuming $50K/year per staff member)
    const staffCostPerYear = 50000
    const totalSavings = receptionistSavings * staffCostPerYear
    
    // Productivity increase
    const productivityIncrease = 10 // 10x overall
    
    return {
      receptionistSavings,
      newAppointmentCapacity,
      newVerificationCapacity,
      totalSavings,
      productivityIncrease
    }
  }

  const results = calculateResults()

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-green-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-green-100 text-green-800 text-sm font-medium">
            <span className="mr-2">💰</span>
            ROI Calculator
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Calculate Your <span className="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">Productivity ROI</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            See how AI tools can multiply your team's productivity and reduce costs.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {/* Input Panel */}
          <Card className="bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
              Current Team Setup
            </h3>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Receptionists
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={inputs.receptionists}
                  onChange={(e) => setInputs({ ...inputs, receptionists: parseInt(e.target.value) || 1 })}
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Scheduling Staff
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={inputs.schedulers}
                  onChange={(e) => setInputs({ ...inputs, schedulers: parseInt(e.target.value) || 1 })}
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Insurance Verification Staff
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={inputs.insuranceStaff}
                  onChange={(e) => setInputs({ ...inputs, insuranceStaff: parseInt(e.target.value) || 1 })}
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Appointments Per Day
                </label>
                <input
                  type="number"
                  min="1"
                  max="1000"
                  value={inputs.appointmentsPerDay}
                  onChange={(e) => setInputs({ ...inputs, appointmentsPerDay: parseInt(e.target.value) || 1 })}
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Insurance Verifications Per Day
                </label>
                <input
                  type="number"
                  min="1"
                  max="1000"
                  value={inputs.verificationsPerDay}
                  onChange={(e) => setInputs({ ...inputs, verificationsPerDay: parseInt(e.target.value) || 1 })}
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>
          </Card>

          {/* Results Panel */}
          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
              With AI Tools
            </h3>
            
            <div className="space-y-6">
              <div className="bg-white rounded-lg p-6 border-2 border-green-300">
                <div className="text-sm text-gray-600 mb-2">Receptionist Staff Needed</div>
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {Math.ceil(inputs.receptionists / 5)} → {inputs.receptionists}
                </div>
                <div className="text-sm text-gray-600">
                  {results.receptionistSavings > 0 
                    ? `Save ${results.receptionistSavings} receptionist${results.receptionistSavings > 1 ? 's' : ''} (5x capacity)`
                    : 'Same staff, 5x capacity'}
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 border-2 border-green-300">
                <div className="text-sm text-gray-600 mb-2">Appointment Capacity</div>
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {inputs.appointmentsPerDay} → {results.newAppointmentCapacity.toLocaleString()}/day
                </div>
                <div className="text-sm text-gray-600">
                  240x faster scheduling (3 sec vs 12 min)
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 border-2 border-green-300">
                <div className="text-sm text-gray-600 mb-2">Verification Capacity</div>
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {inputs.verificationsPerDay} → {results.newVerificationCapacity.toLocaleString()}/day
                </div>
                <div className="text-sm text-gray-600">
                  450x faster verification (2 sec vs 15 min)
                </div>
              </div>

              <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg p-6">
                <div className="text-sm opacity-90 mb-2">Annual Cost Savings</div>
                <div className="text-4xl font-bold mb-2">
                  ${results.totalSavings.toLocaleString()}/year
                </div>
                <div className="text-sm opacity-90">
                  {results.receptionistSavings > 0 
                    ? `From reduced staffing needs`
                    : 'From increased productivity'}
                </div>
              </div>

              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg p-6">
                <div className="text-sm opacity-90 mb-2">Productivity Multiplier</div>
                <div className="text-4xl font-bold mb-2">
                  {results.productivityIncrease}x
                </div>
                <div className="text-sm opacity-90">
                  Same great staff, dramatically more output
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Use Cases */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Real-World Use Cases
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-gradient-to-br from-blue-50 to-cyan-50">
              <h4 className="font-bold text-gray-900 mb-3">Primary Care Practice</h4>
              <p className="text-sm text-gray-600 mb-4">
                3 receptionists → 1 receptionist (5x capacity)
              </p>
              <Badge status="success" className="bg-green-100 text-green-800">
                10x Productivity
              </Badge>
            </Card>
            <Card className="bg-gradient-to-br from-purple-50 to-pink-50">
              <h4 className="font-bold text-gray-900 mb-3">Multi-Location System</h4>
              <p className="text-sm text-gray-600 mb-4">
                10 locations, all EHRs supported via unified API
              </p>
              <Badge status="success" className="bg-green-100 text-green-800">
                10x Productivity
              </Badge>
            </Card>
            <Card className="bg-gradient-to-br from-orange-50 to-red-50">
              <h4 className="font-bold text-gray-900 mb-3">Urgent Care Clinic</h4>
              <p className="text-sm text-gray-600 mb-4">
                24/7 coverage without overnight staff
              </p>
              <Badge status="success" className="bg-green-100 text-green-800">
                24/7 Coverage
              </Badge>
            </Card>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center">
          <Card className="bg-gradient-to-r from-green-600 to-blue-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Multiply Your Team's Productivity?
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Deploy AI tools in <strong>35-55 minutes</strong> and see results immediately.
            </p>
            <button className="px-8 py-3 bg-white text-green-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Start Free Trial →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}






