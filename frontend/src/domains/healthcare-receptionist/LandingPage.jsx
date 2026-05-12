// Healthcare Receptionist Landing Page
// Uses reusable landing components + domain-specific constants (DRY)

import { Navbar } from '../../components/layout/Navbar'
import { Hero } from '../../components/landing/Hero'
import { ProductOptionsSelector } from '../../components/landing/ProductOptionsSelector'
import { ProblemStatement } from '../../components/landing/ProblemStatement'
import { Solution } from '../../components/landing/Solution'
import { HowItWorks } from '../../components/landing/HowItWorks'
import { DeploymentOptionsComparison } from '../../components/landing/DeploymentOptionsComparison'
import { FeaturesShowcase } from '../../components/features/FeaturesShowcase'
import { ProductivityCalculator } from '../../components/landing/ProductivityCalculator'
import { TechnicalArchitecture } from '../../components/landing/TechnicalArchitecture'
import { Differentiation } from '../../components/landing/Differentiation'
import { SocialProof } from '../../components/landing/SocialProof'
import { UseCases } from '../../components/landing/UseCases'
import { TechnicalSpecs } from '../../components/landing/TechnicalSpecs'
import { Pricing } from '../../components/landing/Pricing'
import { FAQ } from '../../components/landing/FAQ'
import { CTA } from '../../components/landing/CTA'
import { LANDING_SECTIONS } from './config/index'

export default function HealthcareReceptionistLanding() {
  const { 
    hero, 
    problem, 
    solution, 
    howItWorks, 
    features,
    architecture,
    differentiation,
    socialProof,
    useCases,
    technicalSpecs,
    gettingStarted,
    pricing, 
    faq, 
    cta 
  } = LANDING_SECTIONS

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <Navbar />
      
      {/* Hero Section - Now uses component-driven config */}
      <Hero config={hero} />

      {/* What Is This Product? - Product Options Selector */}
      <ProductOptionsSelector />

      {/* Problem Statement */}
      <ProblemStatement
        headline={problem.headline}
        description={problem.description}
        problems={problem.problems}
        result={problem.result}
      />

      {/* Solution */}
      <Solution
        headline={solution.headline}
        description={solution.description}
        whatItDoes={solution.whatItDoes}
        whatItReplaces={solution.whatItReplaces}
      />

      {/* How It Works */}
      <HowItWorks
        headline={howItWorks.headline}
        subheadline={howItWorks.subheadline}
        steps={howItWorks.steps}
      />

      {/* Deployment Options Comparison */}
      <DeploymentOptionsComparison />

      {/* Features - Now using specialized interactive components */}
      <FeaturesShowcase />

      {/* Production Demo CTA */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            See It In Action - Live Production Demo
          </h2>
          <p className="text-xl opacity-90 mb-8 leading-relaxed">
            Try all 7 capabilities with real end-to-end workflows. No mocks—actual operations using MCP servers.
          </p>
          <a
            href="/demo"
            className="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:shadow-2xl transition-all transform hover:scale-105"
          >
            Launch Production Demo →
          </a>
        </div>
      </section>

      {/* Technical Architecture */}
      <TechnicalArchitecture
        headline={architecture.headline}
        subheadline={architecture.subheadline}
        description={architecture.description}
        whyMCP={architecture.whyMCP}
        stack={architecture.stack}
      />

      {/* Differentiation */}
      <Differentiation
        headline={differentiation.headline}
        comparison={differentiation.comparison}
      />

      {/* Social Proof */}
      <SocialProof
        headline={socialProof.headline}
        poweredBy={socialProof.poweredBy}
        builtOn={socialProof.builtOn}
      />

      {/* Use Cases */}
      <UseCases useCases={useCases} />

      {/* Productivity Calculator */}
      <ProductivityCalculator />

      {/* Technical Specifications */}
      <TechnicalSpecs
        headline={technicalSpecs.headline}
        api={technicalSpecs.api}
        ehrs={technicalSpecs.ehrs}
        integrations={technicalSpecs.integrations}
        compliance={technicalSpecs.compliance}
      />

      {/* Getting Started */}
      <HowItWorks
        headline={gettingStarted.headline}
        subheadline={gettingStarted.subheadline}
        steps={gettingStarted.steps}
      />

      {/* Pricing */}
      <Pricing
        headline={pricing.headline}
        tiers={pricing.tiers}
        includedInAll={pricing.includedInAll}
      />

      {/* FAQ */}
      <FAQ faqs={faq} />

      {/* CTA */}
      <CTA
        headline={cta.headline}
        subheadline={cta.subheadline}
        primaryCTA={cta.primaryCTA}
        note={cta.note}
        secondaryCTAs={cta.secondaryCTAs}
      />

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-lg mb-4">Healthcare Receptionist AI</h3>
              <p className="text-gray-400 text-sm">
                Powered by Model Context Protocol (MCP)
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Documentation</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="/docs" className="hover:text-white">Documentation</a></li>
                <li><a href="/api" className="hover:text-white">API Reference</a></li>
                <li><a href="/status" className="hover:text-white">Status</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="/security" className="hover:text-white">Security</a></li>
                <li><a href="/privacy" className="hover:text-white">Privacy Policy</a></li>
                <li><a href="/terms" className="hover:text-white">Terms of Service</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>Email: hello@healthcare-receptionist.ai</li>
                <li>Phone: 1-800-HEALTH-AI</li>
                <li>Support: support@healthcare-receptionist.ai</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
            © 2025 Healthcare Receptionist AI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}

