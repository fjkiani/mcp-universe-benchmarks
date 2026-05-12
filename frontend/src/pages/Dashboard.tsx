import { useQuery, useQueryClient } from '@tanstack/react-query'
import { mcpClient } from '../api/mcp-client'
import { ENDPOINTS, API_BASE } from '../api/config'
import { Navbar } from '../components/layout/Navbar'
import { ServerStatus } from '../components/dashboard/ServerStatus'
import { MetricsDashboard } from '../components/dashboard/MetricsDashboard'
import { TestResultsChart } from '../components/dashboard/TestResultsChart'
import { APIMetrics } from '../components/dashboard/APIMetrics'
import { LogViewer } from '../components/dashboard/LogViewer'
import { Card } from '../components/common/Card'
import { Badge } from '../components/common/Badge'
import { useState } from 'react'

export default function Dashboard() {
  const { data: servers, isLoading: serversLoading } = useQuery({
    queryKey: ['servers'],
    queryFn: () => mcpClient.getServers(),
    refetchInterval: 30000 // Refresh every 30 seconds
  })

  const { data: metrics, isLoading: metricsLoading } = useQuery({
    queryKey: ['sprint-metrics'],
    queryFn: () => mcpClient.getSprintMetrics(),
    refetchInterval: 60000 // Refresh every minute
  })

  const { data: sprintProgress } = useQuery({
    queryKey: ['sprint-progress'],
    queryFn: () => mcpClient.getSprintProgress(),
    refetchInterval: 60000,
    enabled: false // Disable for now, can enable when needed
  })

  const { data: testResults } = useQuery({
    queryKey: ['test-results'],
    queryFn: async () => {
      const data = await import('../data/api-status.json')
      return data.default || data
    }
  })

  const queryClient = useQueryClient()
  const [testRunning, setTestRunning] = useState(false)
  const [lastRefresh, setLastRefresh] = useState(new Date())

  // Live agent health polling — builds log feed from real API state
  const { data: agentHealth } = useQuery({
    queryKey: ['agent-health'],
    queryFn: async () => {
      const res = await fetch(ENDPOINTS.agentHealth)
      if (!res.ok) throw new Error('Health check failed')
      return res.json()
    },
    refetchInterval: 15000,
  })

  // Derive live log entries from real API state
  const now = new Date()
  const fmt = (d: Date) => d.toLocaleTimeString()
  const logs = agentHealth ? [
    { timestamp: fmt(now), level: 'success', message: `Agent health: ${agentHealth.status?.toUpperCase()} — mock_mode: ${agentHealth.mock_mode}`, source: 'agent-health' },
    { timestamp: fmt(new Date(now.getTime() - 5000)), level: agentHealth.openai_configured ? 'success' : 'warning', message: `OpenAI GPT-4o: ${agentHealth.openai_configured ? 'CONFIGURED ✓' : 'NOT CONFIGURED ✗'}`, source: 'api-check' },
    { timestamp: fmt(new Date(now.getTime() - 10000)), level: agentHealth.nexhealth_configured ? 'success' : 'warning', message: `NexHealth EHR: ${agentHealth.nexhealth_configured ? 'CONFIGURED ✓' : 'NOT CONFIGURED ✗'}`, source: 'api-check' },
    { timestamp: fmt(new Date(now.getTime() - 15000)), level: agentHealth.twilio_configured ? 'success' : 'warning', message: `Twilio HIPAA SMS: ${agentHealth.twilio_configured ? 'CONFIGURED ✓' : 'NOT CONFIGURED ✗'}`, source: 'api-check' },
    { timestamp: fmt(new Date(now.getTime() - 20000)), level: agentHealth.assemblyai_configured ? 'success' : 'warning', message: `AssemblyAI: ${agentHealth.assemblyai_configured ? 'CONFIGURED ✓' : 'NOT CONFIGURED ✗'}`, source: 'api-check' },
    { timestamp: fmt(new Date(now.getTime() - 25000)), level: agentHealth.videosdk_configured ? 'success' : 'warning', message: `VideoSDK: ${agentHealth.videosdk_configured ? 'CONFIGURED ✓' : 'NOT CONFIGURED ✗'}`, source: 'api-check' },
  ] : [
    { timestamp: fmt(now), level: 'warning', message: 'Connecting to backend...', source: 'health-monitor' },
  ]

  const handleRunTests = async () => {
    setTestRunning(true)
    try {
      await fetch(`${API_BASE}/api/v1/sprint/run`, { method: 'POST' })
      await queryClient.invalidateQueries({ queryKey: ['test-results'] })
    } catch (e) {
      console.warn('Test runner endpoint not available:', e)
    } finally {
      setTestRunning(false)
    }
  }

  const handleRefresh = () => {
    queryClient.invalidateQueries()
    setLastRefresh(new Date())
  }

  if (serversLoading || metricsLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <div className="text-gray-600">Loading dashboard metrics...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="pt-24 p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-4xl font-bold text-gray-900 mb-2">
                  Dashboard
                </h1>
                <p className="text-gray-600">
                  Real-time metrics, test results, and system health monitoring
                </p>
              </div>
              <div className="flex items-center gap-3">
                <Badge status="success">
                  Live
                </Badge>
                <span className="text-sm text-gray-500">
                  Last updated: {lastRefresh.toLocaleTimeString()}
                </span>
              </div>
            </div>
          </div>

          {/* Metrics Dashboard */}
          {metrics && (
            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Sprint Metrics</h2>
              <MetricsDashboard metrics={metrics} />
            </section>
          )}

          {/* Test Results */}
          {testResults && (
            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Test Results & Coverage</h2>
              <TestResultsChart testData={testResults} />
            </section>
          )}

          {/* API Metrics */}
          {servers && (
            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">API Health & Performance</h2>
              <APIMetrics apiData={{ servers }} />
            </section>
          )}

          {/* Server Status Grid */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Server Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {servers?.map((server: any) => (
                <ServerStatus key={server.name} server={server} />
              ))}
            </div>
          </section>

          {/* System Logs */}
          <section>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <LogViewer
                logs={logs}
                title="System Logs"
                maxLines={20}
              />
              <Card title="Quick Actions">
                <div className="space-y-3">
                  <button
                    onClick={handleRunTests}
                    disabled={testRunning}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                  >
                    {testRunning ? 'Running Tests...' : 'Run All Tests'}
                  </button>
                  <button
                    onClick={handleRefresh}
                    className="w-full px-4 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    Refresh Metrics
                  </button>
                  <a
                    href={`${API_BASE}/api/v1/sprint/metrics`}
                    target="_blank"
                    rel="noreferrer"
                    className="block w-full px-4 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 transition-colors text-center"
                  >
                    Export Report ↗
                  </a>
                </div>
              </Card>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

