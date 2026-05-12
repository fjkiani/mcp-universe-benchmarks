// API Metrics Component - Real-time API health and performance
import { Card } from '../common/Card'
import { MetricsChart } from './MetricsChart'
import { Badge } from '../common/Badge'

export function APIMetrics({ apiData }) {
  const servers = apiData?.servers || []
  
  // Generate performance data
  const performanceData = servers.map(server => ({
    name: server.name,
    requests: server.metrics?.requests || 0,
    errors: server.metrics?.errors || 0,
    avgLatency: server.metrics?.avgLatency || 0,
    uptime: server.metrics?.uptime || 0
  }))

  // Generate latency trend
  const latencyTrend = servers.flatMap(server => 
    (server.metrics?.latencyHistory || []).map((latency, idx) => ({
      time: `${idx * 5}m`,
      [server.name]: latency
    }))
  )

  return (
    <div className="space-y-6">
      {/* Server Health Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {servers.map((server, idx) => (
          <Card key={server.id || idx} className="hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-semibold text-gray-900">{server.name}</h4>
              <Badge status={server.status === 'active' ? 'success' : 'warning'}>
                {server.status}
              </Badge>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Uptime</span>
                <span className="font-semibold">{server.metrics?.uptime || 0}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full transition-all"
                  style={{ width: `${server.metrics?.uptime || 0}%` }}
                />
              </div>
              
              <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-gray-100">
                <div>
                  <div className="text-xs text-gray-500">Requests</div>
                  <div className="text-lg font-bold text-gray-900">{server.metrics?.requests || 0}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500">Avg Latency</div>
                  <div className="text-lg font-bold text-gray-900">{server.metrics?.avgLatency || 0}ms</div>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Performance Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Request vs Errors */}
        <Card title="API Request Volume">
          <MetricsChart
            type="bar"
            data={performanceData}
            config={{
              height: 300,
              xAxis: 'name',
              bars: [
                { dataKey: 'requests', name: 'Requests', color: '#3b82f6' },
                { dataKey: 'errors', name: 'Errors', color: '#ef4444' }
              ]
            }}
          />
        </Card>

        {/* Latency Trend */}
        <Card title="Average Latency">
          <MetricsChart
            type="line"
            data={latencyTrend.length > 0 ? latencyTrend : performanceData.map(s => ({ time: s.name, latency: s.avgLatency }))}
            config={{
              height: 300,
              xAxis: 'time',
              lines: [
                { dataKey: 'latency', name: 'Latency (ms)', color: '#8b5cf6' }
              ]
            }}
          />
        </Card>
      </div>

      {/* Real-time Metrics */}
      <Card title="Real-time API Metrics">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">
              {servers.reduce((sum, s) => sum + (s.metrics?.requests || 0), 0)}
            </div>
            <div className="text-sm text-gray-600 mt-1">Total Requests</div>
          </div>
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">
              {servers.reduce((sum, s) => sum + (s.metrics?.errors || 0), 0)}
            </div>
            <div className="text-sm text-gray-600 mt-1">Total Errors</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {servers.length > 0 
                ? (servers.reduce((sum, s) => sum + (s.metrics?.uptime || 0), 0) / servers.length).toFixed(1)
                : 0}%
            </div>
            <div className="text-sm text-gray-600 mt-1">Avg Uptime</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">
              {servers.length > 0
                ? (servers.reduce((sum, s) => sum + (s.metrics?.avgLatency || 0), 0) / servers.length).toFixed(0)
                : 0}ms
            </div>
            <div className="text-sm text-gray-600 mt-1">Avg Latency</div>
          </div>
        </div>
      </Card>
    </div>
  )
}

