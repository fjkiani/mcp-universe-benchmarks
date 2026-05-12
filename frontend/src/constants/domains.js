// Domain Configuration Constants
// Each domain has its own landing page and configuration
// This enables reusable frontend architecture for multiple domains

export const DOMAIN_CONFIG = {
  'healthcare-receptionist': {
    id: 'healthcare-receptionist',
    name: 'Healthcare Receptionist AI',
    slug: 'healthcare-receptionist',
    landingPage: () => import('../domains/healthcare-receptionist/LandingPage'),
    apiBase: '/api/v1',
    theme: {
      primaryColor: '#2563eb', // Blue (healthcare)
    },
    features: ['scheduling', 'insurance', 'triage', 'ehr-integration']
  },
  // Future domains can be added here:
  // 'identity-service': { ... }
}

export const DEFAULT_DOMAIN = 'healthcare-receptionist'

// Get domain config by slug
export function getDomainConfig(slug) {
  return DOMAIN_CONFIG[slug] || DOMAIN_CONFIG[DEFAULT_DOMAIN]
}

// Get all domain slugs
export function getAllDomains() {
  return Object.keys(DOMAIN_CONFIG)
}

