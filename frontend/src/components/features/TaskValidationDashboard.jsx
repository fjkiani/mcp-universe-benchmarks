// Task Validation Dashboard - 40 validated tasks
// Based on LANDING_PAGE.md line 381

import { useState } from 'react'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

const TASK_CATEGORIES = [
  {
    id: 'intake',
    name: 'Patient Intake',
    icon: '📋',
    taskCount: 10,
    passRate: 35,
    color: 'blue',
    tasks: [
      'Register new patient',
      'Update patient information',
      'Verify patient identity',
      'Collect insurance information',
      'Complete intake forms',
      'Schedule initial appointment',
      'Send welcome message',
      'Set up patient portal',
      'Collect medical history',
      'Verify contact information'
    ]
  },
  {
    id: 'scheduling',
    name: 'Appointment Scheduling',
    icon: '📅',
    taskCount: 8,
    passRate: 38,
    color: 'green',
    tasks: [
      'Book appointment in EHR',
      'Check provider availability',
      'Send appointment reminder',
      'Reschedule appointment',
      'Cancel appointment',
      'Add to waitlist',
      'Confirm appointment',
      'Handle no-show follow-up'
    ]
  },
  {
    id: 'triage',
    name: 'Triage & Urgency',
    icon: '🚨',
    taskCount: 7,
    passRate: 40,
    color: 'red',
    tasks: [
      'Assess symptom urgency',
      'Route emergency to 911',
      'Schedule urgent appointment',
      'Route routine to scheduling',
      'Document triage decision',
      'Notify provider of emergency',
      'Follow up on urgent case'
    ]
  },
  {
    id: 'insurance',
    name: 'Insurance Verification',
    icon: '💳',
    taskCount: 8,
    passRate: 32,
    color: 'purple',
    tasks: [
      'Verify insurance eligibility',
      'Check benefits coverage',
      'Verify copay amount',
      'Check deductible status',
      'Handle prior authorization',
      'Update insurance in EHR',
      'Verify secondary insurance',
      'Handle insurance changes'
    ]
  },
  {
    id: 'communication',
    name: 'Patient Communication',
    icon: '💬',
    taskCount: 7,
    passRate: 36,
    color: 'teal',
    tasks: [
      'Send appointment reminder',
      'Send test results',
      'Send medication reminder',
      'Handle patient questions',
      'Send follow-up message',
      'Block PHI in messages',
      'Schedule callback'
    ]
  }
]

export function TaskValidationDashboard() {
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [viewMode, setViewMode] = useState('overview') // 'overview' or 'detailed'

  const totalTasks = TASK_CATEGORIES.reduce((sum, cat) => sum + cat.taskCount, 0)
  const avgPassRate = Math.round(
    TASK_CATEGORIES.reduce((sum, cat) => sum + cat.passRate, 0) / TASK_CATEGORIES.length
  )

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-gray-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">✅</span>
            Task Validation
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">40 Validated Tasks</span> Across All Categories
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Tested across patient intake, scheduling, triage, insurance, and communication. <strong>30-40% pass rate</strong> ensures production-quality performance.
          </p>
        </div>

        {/* Stats Banner */}
        <Card className="mb-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">{totalTasks}</div>
              <div className="text-sm opacity-90">Validated Tasks</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">{TASK_CATEGORIES.length}</div>
              <div className="text-sm opacity-90">Categories</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">{avgPassRate}%</div>
              <div className="text-sm opacity-90">Average Pass Rate</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">100%</div>
              <div className="text-sm opacity-90">Production Ready</div>
            </div>
          </div>
        </Card>

        {/* Category Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {TASK_CATEGORIES.map((category) => (
            <Card
              key={category.id}
              className={`cursor-pointer transition-all duration-300 transform hover:scale-105 border-2 ${
                selectedCategory === category.id
                  ? category.color === 'blue' ? 'border-blue-500 ring-4 ring-blue-300' :
                    category.color === 'green' ? 'border-green-500 ring-4 ring-green-300' :
                    category.color === 'red' ? 'border-red-500 ring-4 ring-red-300' :
                    category.color === 'purple' ? 'border-purple-500 ring-4 ring-purple-300' :
                    'border-teal-500 ring-4 ring-teal-300'
                  : 'border-gray-200'
              }`}
              onClick={() => setSelectedCategory(selectedCategory === category.id ? null : category.id)}
            >
              <div className="text-center">
                <div className="text-4xl mb-3">{category.icon}</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{category.name}</h3>
                <div className="flex items-center justify-center gap-4 mb-4">
                  <Badge status="info" className="bg-blue-100 text-blue-800">
                    {category.taskCount} tasks
                  </Badge>
                  <Badge status="success" className="bg-green-100 text-green-800">
                    {category.passRate}% pass
                  </Badge>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="text-sm text-gray-600 mb-1">Pass Rate</div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        category.color === 'blue' ? 'bg-blue-500' :
                        category.color === 'green' ? 'bg-green-500' :
                        category.color === 'red' ? 'bg-red-500' :
                        category.color === 'purple' ? 'bg-purple-500' :
                        'bg-teal-500'
                      }`}
                      style={{ width: `${category.passRate}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Selected Category Details */}
        {selectedCategory && (
          <Card className="mb-16 bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200">
            {(() => {
              const category = TASK_CATEGORIES.find(c => c.id === selectedCategory)
              if (!category) return null

              return (
                <div>
                  <div className="text-center mb-6">
                    <div className="text-5xl mb-4">{category.icon}</div>
                    <h3 className="text-3xl font-bold text-gray-900 mb-2">{category.name}</h3>
                    <div className="flex items-center justify-center gap-4">
                      <Badge status="info" className="bg-blue-100 text-blue-800 text-lg">
                        {category.taskCount} Tasks
                      </Badge>
                      <Badge status="success" className="bg-green-100 text-green-800 text-lg">
                        {category.passRate}% Pass Rate
                      </Badge>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {category.tasks.map((task, idx) => (
                      <div key={idx} className="bg-white rounded-lg p-4 border border-gray-200">
                        <div className="flex items-center gap-2">
                          <span className="text-green-500">✓</span>
                          <span className="text-sm text-gray-700">{task}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })()}
          </Card>
        )}

        {/* Benchmark Info */}
        <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 mb-16">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Benchmark-Validated Performance
            </h3>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto mb-6">
              Our <strong>30-40% pass rate</strong> ensures production-quality performance. Each task is tested against real-world scenarios with actual API integrations.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg p-4">
                <div className="text-3xl font-bold text-green-600 mb-2">30-40%</div>
                <div className="text-sm text-gray-600">Pass Rate Range</div>
              </div>
              <div className="bg-white rounded-lg p-4">
                <div className="text-3xl font-bold text-blue-600 mb-2">100%</div>
                <div className="text-sm text-gray-600">Real API Tests</div>
              </div>
              <div className="bg-white rounded-lg p-4">
                <div className="text-3xl font-bold text-purple-600 mb-2">40</div>
                <div className="text-sm text-gray-600">Validated Tasks</div>
              </div>
            </div>
          </div>
        </Card>

        {/* Bottom CTA */}
        <div className="text-center">
          <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
            <h3 className="text-2xl font-bold mb-4">
              Production-Ready Task Validation
            </h3>
            <p className="text-lg mb-6 opacity-90">
              All 40 tasks are validated with real API integrations. Ready for production deployment.
            </p>
            <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              View Test Results →
            </button>
          </Card>
        </div>
      </div>
    </section>
  )
}






