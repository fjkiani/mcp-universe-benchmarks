// Product Page - "What Is Receptionist OS?"
// Deep understanding of the product: SaaS + AI Layer + Deployment Options

import { Navbar } from '../components/layout/Navbar'
import { SaaSExplainer } from '../components/features/SaaSExplainer'
import { AILayerExplainer } from '../components/features/AILayerExplainer'
import { ProductOptionsSelector } from '../components/landing/ProductOptionsSelector'
import { CTA } from '../components/landing/CTA'

export default function ProductPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      {/* Page Hero */}
      <section className="pt-32 pb-12 px-4 bg-gradient-to-br from-indigo-50 via-white to-purple-50">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-indigo-100 text-indigo-800 text-sm font-medium">
            <span className="mr-2">💼</span>
            Product Overview
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            What Is <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Receptionist OS</span>?
          </h1>
          
          <p className="text-xl text-gray-600 leading-relaxed mb-8">
            A complete software platform that runs your front office—from patient calls to appointments to insurance—with smart features that make your staff 10x more productive.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <SaaSExplainer />
      <AILayerExplainer />
      <ProductOptionsSelector />

      {/* Next Steps CTA */}
      <section className="py-20 px-4 bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Ready to See Real Results?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            See how this transforms your team&apos;s day-to-day work
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="/how-it-works"
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold text-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              See Real Transformations →
            </a>
            <a
              href="/capabilities"
              className="px-8 py-4 bg-white text-gray-900 rounded-lg font-semibold text-lg border-2 border-gray-300 hover:border-blue-500 transition-all"
            >
              Explore Capabilities
            </a>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <CTA />
    </div>
  )
}




