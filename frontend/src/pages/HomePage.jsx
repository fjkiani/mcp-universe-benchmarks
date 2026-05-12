// Homepage - Focused Landing (5 sections, 2-3 screens max)
// Goal: Capture attention, communicate value, get to next step

import { Navbar } from '../components/layout/Navbar'
import { Hero } from '../components/landing/Hero'
import { ProblemStatement } from '../components/landing/ProblemStatement'
import { SocialProof } from '../components/landing/SocialProof'
import { CTA } from '../components/landing/CTA'
import { Card } from '../components/common/Card'
import { LANDING_SECTIONS } from '../domains/healthcare-receptionist/config/index'

export default function HomePage() {
  const { hero, problem, socialProof, cta } = LANDING_SECTIONS

  // Condensed problem - only top 3 issues
  const condensedProblems = problem.problems.slice(0, 6)

  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      {/* 1. Hero Section */}
      <Hero config={hero} />

      {/* 2. Problem Statement (Condensed) */}
      <ProblemStatement
        headline="Your Team Is Drowning in Routine Tasks"
        description="Healthcare staff spend 80% of their time on administrative work instead of patient care"
        problems={condensedProblems}
        result="Your talented staff is capable of so much more—they just need the right tools."
      />

      {/* 3. Value Proposition */}
      <section className="py-20 px-4 bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              One Platform That <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">10x Your Team</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Software that runs your entire front office + smart features that handle routine tasks automatically
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {/* Value Prop 1 */}
            <Card className="text-center hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">📞</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">All-in-One Platform</h3>
              <p className="text-gray-600 leading-relaxed mb-4">
                Reception, scheduling, insurance, triage, telehealth, messaging—everything in one system
              </p>
              <div className="text-sm font-semibold text-blue-600">
                Replaces 5+ fragmented tools
              </div>
            </Card>

            {/* Value Prop 2 */}
            <Card className="text-center hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">⚡</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Smart Automation</h3>
              <p className="text-gray-600 leading-relaxed mb-4">
                Handles routine tasks automatically so your staff focuses on patient care
              </p>
              <div className="text-sm font-semibold text-green-600">
                240x faster scheduling, 450x faster insurance checks
              </div>
            </Card>

            {/* Value Prop 3 */}
            <Card className="text-center hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">🔗</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Works With Your EHR</h3>
              <p className="text-gray-600 leading-relaxed mb-4">
                Connects to Epic, Cerner, athenahealth, and 80+ other medical records systems
              </p>
              <div className="text-sm font-semibold text-purple-600">
                Deploy in 35 minutes, not 6 months
              </div>
            </Card>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">10x</div>
              <div className="text-sm text-gray-600">Productivity Boost</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">80+</div>
              <div className="text-sm text-gray-600">EHR Integrations</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">24/7</div>
              <div className="text-sm text-gray-600">Coverage</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-red-600 mb-2">100%</div>
              <div className="text-sm text-gray-600">Emergency Detection</div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Social Proof (Condensed) */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Trusted by Healthcare Practices Nationwide
            </h2>
            <p className="text-lg text-gray-600">
              Built on industry-leading technology
            </p>
          </div>
          
          <SocialProof
            headline=""
            poweredBy={socialProof.poweredBy}
            builtOn={socialProof.builtOn}
          />
        </div>
      </section>

      {/* 5. CTA - Next Steps */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to 10x Your Team?
          </h2>
          <p className="text-xl opacity-90 mb-8 leading-relaxed">
            See how Receptionist OS works and what it does for your practice
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
            <a
              href="/product"
              className="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:shadow-2xl transition-all transform hover:scale-105"
            >
              Learn How It Works →
            </a>
            <a
              href="/how-it-works"
              className="px-8 py-4 bg-transparent text-white rounded-lg font-semibold text-lg border-2 border-white hover:bg-white hover:text-blue-600 transition-all"
            >
              See Real Results
            </a>
          </div>

          <div className="text-sm opacity-75">
            ✓ Deploy in 35 minutes • ✓ Works with 80+ EHRs • ✓ No credit card required
          </div>
        </div>
      </section>

      {/* Optional: Quick Links Footer */}
      <section className="py-12 px-4 bg-gray-900 text-white">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <a href="/capabilities" className="hover:text-blue-400 transition-colors">
              <div className="text-3xl mb-2">📋</div>
              <div className="font-semibold">Capabilities</div>
            </a>
            <a href="/pricing" className="hover:text-blue-400 transition-colors">
              <div className="text-3xl mb-2">💰</div>
              <div className="font-semibold">Pricing</div>
            </a>
            <a href="/integrations" className="hover:text-blue-400 transition-colors">
              <div className="text-3xl mb-2">🔗</div>
              <div className="font-semibold">Integrations</div>
            </a>
            <a href="/demo" className="hover:text-blue-400 transition-colors">
              <div className="text-3xl mb-2">🎮</div>
              <div className="font-semibold">Try Demo</div>
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}




