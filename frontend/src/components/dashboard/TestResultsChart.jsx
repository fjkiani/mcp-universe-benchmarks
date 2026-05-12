// Test Results Chart - Visualize test coverage and results
import { Card } from '../common/Card'
import { MetricsChart } from './MetricsChart'

export function TestResultsChart({ testData }) {
  // Transform test data for charts
  const coverageData = testData?.servers?.map(server => ({
    name: server.name,
    passed: server.tests?.passed || 0,
    failed: server.tests?.failed || 0,
    pending: server.tests?.pending || 0,
    coverage: server.tests?.coverage || 0
  })) || []

  const pieData = testData?.summary ? [
    { name: 'Passed', value: testData.summary.tests_passed || 0 },
    { name: 'Failed', value: testData.summary.tests_failed || 0 },
    { name: 'Pending', value: testData.summary.tests_pending || 0 }
  ] : []

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Test Coverage Bar Chart */}
      <Card title="Test Coverage by Server">
        <MetricsChart
          type="bar"
          data={coverageData}
          config={{
            height: 300,
            xAxis: 'name',
            bars: [
              { dataKey: 'passed', name: 'Passed', color: '#10b981' },
              { dataKey: 'failed', name: 'Failed', color: '#ef4444' },
              { dataKey: 'pending', name: 'Pending', color: '#f59e0b' }
            ]
          }}
        />
      </Card>

      {/* Test Status Pie Chart */}
      <Card title="Overall Test Status">
        <MetricsChart
          type="pie"
          data={pieData}
          config={{
            height: 300,
            dataKey: 'value'
          }}
        />
      </Card>

      {/* Coverage Trend */}
      {testData?.trend && (
        <Card title="Coverage Trend" className="lg:col-span-2">
          <MetricsChart
            type="area"
            data={testData.trend}
            config={{
              height: 300,
              xAxis: 'date',
              areas: [
                { dataKey: 'coverage', name: 'Coverage %', color: '#3b82f6' }
              ]
            }}
          />
        </Card>
      )}
    </div>
  )
}

