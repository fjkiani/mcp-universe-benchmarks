// Data Reader Utility - Reads from api-status.json (synced from central workflow)
// Provides fallback when backend API is not available

/**
 * Read API status from synced JSON file
 * This is the primary data source until backend API is ready
 */
export async function readApiStatus() {
  try {
    // Try to import the JSON file (Vite handles this)
    const data = await import('../data/api-status.json')
    return data.default || data
  } catch (error) {
    console.warn('Could not load api-status.json, returning empty data:', error)
    return {
      timestamp: new Date().toISOString(),
      summary: {
        total_apis: 0,
        total_endpoints: 0,
        total_tests: 0,
        tests_passed: 0,
        tests_failed: 0,
        tests_pending: 0,
        overall_coverage: 0,
      },
      apis: [],
      frontend_integration: {
        total_showcases: 0,
        integrated_apis: 0,
        showcase_pages: [],
        last_synced: new Date().toISOString(),
      }
    }
  }
}

/**
 * Get API by ID
 */
export async function getApiById(apiId) {
  const data = await readApiStatus()
  return data.apis.find(api => api.id === apiId || api.name.toLowerCase().replace(/\s+/g, '_') === apiId)
}

/**
 * Get all APIs by category
 */
export async function getApisByCategory(category) {
  const data = await readApiStatus()
  return data.apis.filter(api => api.category === category)
}

/**
 * Get summary metrics
 */
export async function getSummary() {
  const data = await readApiStatus()
  return data.summary
}

/**
 * Get frontend integration status
 */
export async function getFrontendIntegration() {
  const data = await readApiStatus()
  return data.frontend_integration
}

