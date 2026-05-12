// Test Showcase Component - Displays test results from api-status.json

import { useQuery } from '@tanstack/react-query'
import { readApiStatus } from '../../utils/data-reader'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

export function TestShowcase() {
  const { data: apiStatus, isLoading } = useQuery({
    queryKey: ['api-status'],
    queryFn: readApiStatus,
    staleTime: 30000,
  })

  if (isLoading) {
    return <div className="text-center text-gray-600 py-8">Loading test results...</div>
  }

  if (!apiStatus || !apiStatus.summary) {
    return (
      <Card>
        <p className="text-gray-600">No test data available.</p>
      </Card>
    )
  }

  const { summary } = apiStatus
  const passRate = summary.total_tests > 0 
    ? ((summary.tests_passed / summary.total_tests) * 100).toFixed(1)
    : 0

  // Collect all endpoints with test results
  const allEndpoints = apiStatus.apis.flatMap(api =>
    api.endpoints.map(endpoint => ({
      api: api.name,
      endpoint: endpoint.name,
      result: endpoint.test_result,
      lastTest: endpoint.last_test,
      tested: endpoint.tested,
    }))
  )

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <p className="text-sm text-gray-600 mb-1">Total Tests</p>
          <p className="text-2xl font-bold text-gray-900">{summary.total_tests}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600 mb-1">Passed</p>
          <p className="text-2xl font-bold text-green-600">{summary.tests_passed}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600 mb-1">Failed</p>
          <p className="text-2xl font-bold text-red-600">{summary.tests_failed}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600 mb-1">Pass Rate</p>
          <p className="text-2xl font-bold text-gray-900">{passRate}%</p>
        </Card>
      </div>

      {/* Test Results Table */}
      <Card title="Test Results">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  API
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Endpoint
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Result
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Last Test
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {allEndpoints.map((test, idx) => (
                <tr key={idx}>
                  <td className="px-4 py-3 text-sm text-gray-900">{test.api}</td>
                  <td className="px-4 py-3 text-sm text-gray-700 font-mono">{test.endpoint}</td>
                  <td className="px-4 py-3">
                    <Badge
                      status={
                        test.result === 'passed' ? 'success' :
                        test.result === 'failed' ? 'error' : 'warning'
                      }
                    >
                      {test.result || 'pending'}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {test.lastTest 
                      ? new Date(test.lastTest).toLocaleString()
                      : 'Never'
                    }
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

