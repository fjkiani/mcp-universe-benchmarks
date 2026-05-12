// Capabilities Page - Overview of all 8 core modules
// Grid navigation to capability deep-dive pages

import { Navbar } from '../components/layout/Navbar'
import { CapabilityGrid } from '../components/pages/capability/CapabilityGrid'
import { CTA } from '../components/landing/CTA'

export default function CapabilitiesPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      {/* Page Hero */}
      <section className="pt-32 pb-12 px-4 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-purple-100 text-purple-800 text-sm font-medium">
            <span className="mr-2">⚡</span>
            Core Capabilities
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            8 Modules That Run <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Your Entire Office</span>
          </h1>
          
          <p className="text-xl text-gray-600 leading-relaxed mb-8">
            From patient calls to insurance verification to telehealth—everything your front office needs in one unified platform.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-3 mb-8">
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">📞 Reception</span>
            </div>
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">📅 Scheduling</span>
            </div>
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">💳 Insurance</span>
            </div>
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">🚨 Triage</span>
            </div>
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">📹 Telehealth</span>
            </div>
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">💬 Messaging</span>
            </div>
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">🔄 EHR Sync</span>
            </div>
            <div className="px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
              <span className="text-sm font-semibold text-gray-700">🔒 Compliance</span>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content - Capability Grid */}
      <CapabilityGrid />

      {/* See It In Action Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-green-50 to-blue-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            See Real Staff Transformations
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Learn how these capabilities transform your team&apos;s day-to-day work
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="/how-it-works"
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-green-600 text-white rounded-lg font-semibold text-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              See Before/After Stories →
            </a>
            <a
              href="/pricing"
              className="px-8 py-4 bg-white text-gray-900 rounded-lg font-semibold text-lg border-2 border-gray-300 hover:border-blue-500 transition-all"
            >
              View Pricing
            </a>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <CTA />
    </div>
  )
}




