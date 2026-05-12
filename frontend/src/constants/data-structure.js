// Data Structure Constants - Documents api-status.json structure
// This helps developers understand the data format from central workflow

/**
 * API Status JSON Structure (from frontend-sync.py)
 * 
 * File: frontend/src/data/api-status.json
 * Source: central/api-registry.yaml → frontend-sync.py → api-status.json
 */
export const API_STATUS_STRUCTURE = {
  // Top-level structure
  timestamp: 'ISO timestamp',
  summary: {
    total_apis: 'number',
    total_endpoints: 'number',
    total_tests: 'number',
    tests_passed: 'number',
    tests_failed: 'number',
    tests_pending: 'number',
    overall_coverage: 'number (percentage)',
  },
  apis: [
    {
      id: 'string (api identifier)',
      name: 'string (display name)',
      category: 'string (communication, transcription, video, ehr)',
      status: 'string (active, pending, failed)',
      mcp_server: 'string (server name)',
      endpoints: [
        {
          name: 'string',
          tested: 'boolean',
          test_result: 'string (passed, failed, pending)',
          last_test: 'ISO timestamp',
          showcase: 'boolean',
        }
      ],
      tests: {
        total: 'number',
        passed: 'number',
        failed: 'number',
        pending: 'number',
        coverage: 'number (percentage)',
      },
      frontend: {
        integrated: 'boolean',
        showcase_page: 'string (route path)',
        last_synced: 'ISO timestamp',
      }
    }
  ],
  frontend_integration: {
    total_showcases: 'number',
    integrated_apis: 'number',
    showcase_pages: ['array of routes'],
    last_synced: 'ISO timestamp',
  }
}

// Helper to validate data structure
export function validateApiStatus(data) {
  return data && 
         data.summary && 
         Array.isArray(data.apis) &&
         typeof data.timestamp === 'string'
}

