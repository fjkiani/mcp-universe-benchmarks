// Central export for all modular configs
// This makes it easy to import and maintain

import { heroConfig } from './hero-config'
import { problemConfig } from './problem-config'
import { solutionConfig } from './solution-config'
import { howItWorksConfig } from './how-it-works-config'
import { featuresConfig } from './features-config'
import { architectureConfig } from './architecture-config'
import { differentiationConfig } from './differentiation-config'
import { socialProofConfig } from './social-proof-config'
import { useCasesConfig } from './use-cases-config'
import { technicalSpecsConfig } from './technical-specs-config'
import { gettingStartedConfig } from './getting-started-config'
import { pricingConfig } from './pricing-config'
import { faqConfig } from './faq-config'
import { ctaConfig } from './cta-config'
import { mcpServersConfig } from './mcp-servers-config'
import { valuePropsConfig } from './value-props-config'
import { integrationStackConfig } from './integration-stack-config'

// Re-export individual configs
export { heroConfig }
export { problemConfig }
export { solutionConfig }
export { howItWorksConfig }
export { featuresConfig }
export { architectureConfig }
export { differentiationConfig }
export { socialProofConfig }
export { useCasesConfig }
export { technicalSpecsConfig }
export { gettingStartedConfig }
export { pricingConfig }
export { faqConfig }
export { ctaConfig }
export { mcpServersConfig }
export { valuePropsConfig }
export { integrationStackConfig }

// Aggregate all configs for convenience (matches old LANDING_SECTIONS structure)
export const LANDING_SECTIONS = {
  hero: heroConfig,
  problem: problemConfig,
  solution: solutionConfig,
  howItWorks: howItWorksConfig,
  features: featuresConfig,
  architecture: architectureConfig,
  differentiation: differentiationConfig,
  socialProof: socialProofConfig,
  useCases: useCasesConfig,
  technicalSpecs: technicalSpecsConfig,
  gettingStarted: gettingStartedConfig,
  pricing: pricingConfig,
  faq: faqConfig,
  cta: ctaConfig
}

