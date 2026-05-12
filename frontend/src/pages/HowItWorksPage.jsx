// How It Works Page - "Real Staff Transformations"
// Shows tangible impact through before/after stories and ROI calculator

import { Navbar } from '../components/layout/Navbar'
import { BeforeAfterComparison } from '../components/features/BeforeAfterComparison'
import { AITeamShowcase } from '../components/features/AITeamShowcase'
import { ProductivityCalculator } from '../components/landing/ProductivityCalculator'
import { CTA } from '../components/landing/CTA'

export default function HowItWorksPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      {/* Page Hero */}
      <section className="pt-32 pb-12 px-4 bg-gradient-to-br from-blue-50 via-white to-green-50">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">📈</span>
            Real Results
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            How It <span className="bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">Transforms</span> Your Team
          </h1>
          
          <p className="text-xl text-gray-600 leading-relaxed mb-8">
            Your staff doesn&apos;t work harder—they work smarter. See real transformations from actual practices using Receptionist OS.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <BeforeAfterComparison />
      <AITeamShowcase />
      <ProductivityCalculator />

      {/* Next Steps CTA */}
      <section className="py-20 px-4 bg-gradient-to-br from-green-50 to-blue-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Want to See Specific Capabilities?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Explore how each module works and what it does for your practice
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="/capabilities"
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-green-600 text-white rounded-lg font-semibold text-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              Explore All Capabilities →
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




