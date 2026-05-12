// Showcase Page - Main showcase page combining all showcase components
// Displays real API status, test results, and progress from api-status.json

import { APIShowcase } from '../components/showcase/APIShowcase'
import { TestShowcase } from '../components/showcase/TestShowcase'
import { ProgressShowcase } from '../components/showcase/ProgressShowcase'

import { Navbar } from '../components/layout/Navbar'

export default function Showcase() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="pt-24 p-8">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            API Showcase
          </h1>
          <p className="text-gray-600">
            Real-time status of all APIs, tests, and integration progress
          </p>
        </div>

        {/* Progress Overview */}
        <ProgressShowcase />

        {/* API Status */}
        <APIShowcase />

        {/* Test Results */}
        <TestShowcase />
      </div>
      </div>
    </div>
  )
}

