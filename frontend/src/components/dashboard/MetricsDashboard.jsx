// Metrics Dashboard - Comprehensive metrics visualization
import { Card } from '../common/Card'
import { MetricsChart } from './MetricsChart'
import { MetricCard } from '../landing/MetricCard'

export function MetricsDashboard({ metrics }) {
  // Generate time series data for trends
  const generateTrendData = (current, previous, days = 7) => {
    return Array.from({ length: days }, (_, i) => ({
      date: new Date(Date.now() - (days - i - 1) * 86400000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      value: previous + ((current - previous) / days) * (i + 1)
    }))
  }

  const taskTrend = generateTrendData(metrics?.tasksCompleted || 0, 0, 7)
  const serverTrend = generateTrendData(metrics?.serversTested || 0, 0, 7)

  return (
    <div className="space-y-6">
      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          metric={{
            icon: "📊",
            value: `${metrics?.passRate?.toFixed(1) || 0}%`,
            label: "Test Pass Rate",
            description: "Overall test success rate",
            change: metrics?.passRateChange || 0
          }}
        />
        <MetricCard
          metric={{
            icon: "✅",
            value: `${metrics?.tasksCompleted || 0}/${metrics?.tasksTotal || 0}`,
            label: "Tasks Completed",
            description: "Progress towards sprint goals",
            change: metrics?.tasksProgress || 0
          }}
        />
        <MetricCard
          metric={{
            icon: "🔌",
            value: `${metrics?.serversTested || 0}/${metrics?.serversTotal || 0}`,
            label: "Servers Tested",
            description: "MCP server test coverage",
            change: metrics?.serversProgress || 0
          }}
        />
        <MetricCard
          metric={{
            icon: "🏥",
            value: `${metrics?.nexhealthIntegrated || 0}`,
            label: "NexHealth Tasks",
            description: "Tasks with EHR integration",
          }}
        />
      </div>

      {/* Progress Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Task Progress Trend */}
        <Card title="Task Completion Trend">
          <MetricsChart
            type="line"
            data={taskTrend}
            config={{
              height: 250,
              xAxis: 'date',
              lines: [
                { dataKey: 'value', name: 'Tasks Completed', color: '#3b82f6' }
              ]
            }}
          />
        </Card>

        {/* Server Testing Trend */}
        <Card title="Server Testing Progress">
          <MetricsChart
            type="area"
            data={serverTrend}
            config={{
              height: 250,
              xAxis: 'date',
              areas: [
                { dataKey: 'value', name: 'Servers Tested', color: '#10b981' }
              ]
            }}
          />
        </Card>
      </div>

      {/* Sprint Metrics */}
      {metrics?.priorities && (
        <Card title="Sprint Priorities Progress">
          <div className="space-y-4">
            {metrics.priorities.map((priority, idx) => (
              <div key={priority.id || idx}>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-gray-900">{priority.name}</span>
                  <span className="text-sm text-gray-600">
                    {priority.completed}/{priority.tasks} ({((priority.completed / priority.tasks) * 100).toFixed(0)}%)
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all duration-500 ${
                      priority.status === 'completed' ? 'bg-green-500' :
                      priority.status === 'in_progress' ? 'bg-blue-500' :
                      'bg-yellow-500'
                    }`}
                    style={{ width: `${(priority.completed / priority.tasks) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  )
}

