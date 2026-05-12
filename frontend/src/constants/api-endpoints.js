// API Endpoints Constants - Single source of truth for all backend endpoints
// Backend-first approach: All endpoints defined here, used by API client

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const API_ENDPOINTS = {
  // Central workflow endpoints (from CENTRAL_WORKFLOW.md)
  central: {
    apis: `${API_BASE}/central/apis`,
    tests: `${API_BASE}/central/tests`,
    sync: `${API_BASE}/central/sync`,
  },
  
  // Server endpoints
  servers: {
    list: `${API_BASE}/servers`,
    status: (name) => `${API_BASE}/servers/${name}`,
    test: (name) => `${API_BASE}/servers/${name}/test`,
  },
  
  // Sprint endpoints
  sprint: {
    metrics: `${API_BASE}/sprint/metrics`,
    progress: `${API_BASE}/sprint/progress`,
  },
  
  // Task endpoints
  tasks: {
    list: `${API_BASE}/tasks`,
    status: (id) => `${API_BASE}/tasks/${id}/status`,
  },
}

// Fallback data file (synced from central workflow)
export const DATA_FILE = '/src/data/api-status.json'

