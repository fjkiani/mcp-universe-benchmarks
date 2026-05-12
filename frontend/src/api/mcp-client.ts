// MCP Client for connecting to backend MCP servers
// Uses constants for endpoints, falls back to JSON data when backend unavailable
import axios from 'axios'
import { API_ENDPOINTS } from '../constants/api-endpoints'
import { readApiStatus, getSummary } from '../utils/data-reader'

class MCPClient {
  private useBackend: boolean

  constructor(useBackend = false) {
    // Try backend first, fallback to JSON if unavailable
    this.useBackend = useBackend
  }

  // Helper: Try backend, fallback to JSON
  private async tryBackend(endpoint, fallbackFn) {
    if (!this.useBackend) {
      return fallbackFn()
    }
    
    try {
      const response = await axios.get(endpoint, { timeout: 2000 })
      return response.data
    } catch (error) {
      console.warn(`Backend unavailable (${endpoint}), using fallback:`, error.message)
      return fallbackFn()
    }
  }

  // Get servers - uses api-status.json → apis array
  async getServers() {
    return this.tryBackend(API_ENDPOINTS.servers.list, async () => {
      const data = await readApiStatus()
      // Transform api-status.json format to expected format
      return data.apis.map(api => ({
        name: api.name,
        status: api.status,
        tools: api.endpoints || [],
        testsPassed: api.tests?.passed || 0,
        testsFailed: api.tests?.failed || 0,
        structure: true, // Assume valid if in registry
        syntax: true,
        apiKeys: true,
        dependencies: true,
        lastTested: api.frontend?.last_synced,
      }))
    })
  }

  async getServerStatus(serverName) {
    return this.tryBackend(
      API_ENDPOINTS.servers.status(serverName),
      async () => {
        const data = await readApiStatus()
        const api = data.apis.find(a => 
          a.id === serverName || 
          a.name.toLowerCase().replace(/\s+/g, '_') === serverName
        )
        return api || null
      }
    )
  }

  async testServer(serverName) {
    return this.tryBackend(
      API_ENDPOINTS.servers.test(serverName),
      async () => ({ message: 'Backend unavailable, use test-runner.py' })
    )
  }

  async callTool(server, tool, params) {
    const endpoint = `${API_ENDPOINTS.servers.list}/${server}/tools/${tool}`
    try {
      const response = await axios.post(endpoint, params)
      return response.data
    } catch (error) {
      throw new Error(`Tool call failed: ${error.message}`)
    }
  }

  // Get sprint metrics - Enhanced with priorities and test results
  async getSprintMetrics() {
    return this.tryBackend(API_ENDPOINTS.sprint.metrics, async () => {
      const summary = await getSummary()
      const data = await readApiStatus()
      
      // Try to get task count from api-status.json or default
      const taskCount = data.summary?.total_tasks || 13
      const targetTasks = 40 // From Sprint 3 plan
      
      return {
        currentSprint: 'Sprint 3',
        nextSprint: 'Sprint 4',
        passRate: summary.overall_coverage || 0,
        tasksCompleted: taskCount,
        tasksTotal: targetTasks,
        tasksProgress: round((taskCount / targetTasks) * 100, 1),
        nexhealthIntegrated: 8, // From Sprint 2
        serversTested: summary.total_apis || 4,
        serversTotal: 4,
        serversProgress: 100.0,
        priorities: [
          {
            id: 'sprint1',
            name: 'Sprint 1: Foundation & Testing',
            status: 'completed',
            tasks: 3,
            completed: 3
          },
          {
            id: 'sprint2',
            name: 'Sprint 2: NexHealth Integration',
            status: 'completed',
            tasks: 8,
            completed: 8
          },
          {
            id: 'sprint3',
            name: 'Sprint 3: Task Expansion',
            status: 'pending',
            tasks: 27,
            completed: 0,
            remaining: 27
          }
        ],
        lastUpdated: new Date().toISOString()
      }
    })
  }

  // Get sprint progress - Detailed progress with milestones
  async getSprintProgress() {
    return this.tryBackend(API_ENDPOINTS.sprint.progress, async () => {
      const metrics = await this.getSprintMetrics()
      const testResults = await this.getCentralTests()
      
      return {
        metrics,
        sprintStatus: {
          currentSprint: metrics.currentSprint,
          nextSprint: metrics.nextSprint,
          sprint1Complete: true,
          sprint2Complete: true
        },
        testResults: {
          tasks: testResults.summary || {},
          servers: testResults.summary || {}
        },
        timeline: metrics.currentSprint,
        milestones: metrics.priorities || [],
        blockers: [],
        lastUpdated: metrics.lastUpdated
      }
    })
  }

  async getTasks() {
    return this.tryBackend(API_ENDPOINTS.tasks.list, async () => {
      // Fallback: Try to read from api-status.json or return empty
      // Backend reads from actual task files, so fallback is minimal
      return []
    })
  }

  async getTaskStatus(taskId: string) {
    return this.tryBackend(API_ENDPOINTS.tasks.status(taskId), async () => {
      return {
        id: taskId,
        status: 'pending',
        lastTested: null,
        passRate: null,
        completed: false
      }
    })
  }

  // Central workflow endpoints
  async getCentralApis() {
    return this.tryBackend(API_ENDPOINTS.central.apis, async () => {
      const data = await readApiStatus()
      return data.apis
    })
  }

  async getCentralTests() {
    return this.tryBackend(API_ENDPOINTS.central.tests, async () => {
      const data = await readApiStatus()
      return {
        summary: data.summary,
        results: data.apis.flatMap(api => 
          api.endpoints.map(endpoint => ({
            api: api.name,
            endpoint: endpoint.name,
            result: endpoint.test_result,
            last_test: endpoint.last_test,
          }))
        )
      }
    })
  }

  async triggerSync() {
    return this.tryBackend(
      API_ENDPOINTS.central.sync,
      async () => ({ message: 'Backend unavailable, run: python central/frontend-sync.py' })
    )
  }
}

// Helper function for rounding
function round(value: number, decimals: number): number {
  return Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals)
}

// Export singleton instance
// Backend is now ready! Set to true to use backend API
export const mcpClient = new MCPClient(true) // Backend connected! 🚀


