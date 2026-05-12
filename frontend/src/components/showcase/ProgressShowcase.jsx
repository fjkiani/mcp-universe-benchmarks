// Progress Showcase Component - Displays overall progress from api-status.json

import { useQuery } from '@tanstack/react-query'
import { readApiStatus } from '../../utils/data-reader'
import { Card } from '../common/Card'
import { ProgressBar } from '../charts/ProgressBar'

export function ProgressShowcase() {
  const { data: apiStatus, isLoading } = useQuery({
    queryKey: ['api-status'],
    queryFn: readApiStatus,
    staleTime: 30000,
  })

  if (isLoading) {
    return <div className="text-center text-gray-600 py-8">Loading progress...</div>
  }

  if (!apiStatus || !apiStatus.summary) {
    return (
      <Card>
        <p className="text-gray-600">No progress data available.</p>
      </Card>
    )
  }

  const { summary } = apiStatus
  const coverage = summary.overall_coverage || 0
  const apiProgress = summary.total_apis > 0 
    ? ((summary.total_apis / 4) * 100) // Assuming 4 total APIs
    : 0

  return (
    <div className="space-y-6">
      <Card title="Overall Progress">
        <div className="space-y-6">
          {/* API Integration Progress */}
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">APIs Integrated</span>
              <span className="font-medium">{summary.total_apis} / 4</span>
            </div>
            <ProgressBar value={apiProgress} />
          </div>

          {/* Test Coverage */}
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Test Coverage</span>
              <span className="font-medium">{coverage}%</span>
            </div>
            <ProgressBar value={coverage} />
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
            <div>
              <p className="text-xs text-gray-500">Total APIs</p>
              <p className="text-lg font-bold text-gray-900">{summary.total_apis}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Endpoints</p>
              <p className="text-lg font-bold text-gray-900">{summary.total_endpoints}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Tests Passed</p>
              <p className="text-lg font-bold text-green-600">{summary.tests_passed}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Tests Pending</p>
              <p className="text-lg font-bold text-yellow-600">{summary.tests_pending || 0}</p>
            </div>
          </div>
        </div>
      </Card>

      {/* Frontend Integration Status */}
      {apiStatus.frontend_integration && (
        <Card title="Frontend Integration">
          <div className="space-y-2">
            <p className="text-sm text-gray-600">
              <span className="font-medium">{apiStatus.frontend_integration.integrated_apis}</span> APIs integrated
            </p>
            <p className="text-sm text-gray-600">
              <span className="font-medium">{apiStatus.frontend_integration.total_showcases}</span> showcase pages
            </p>
            {apiStatus.frontend_integration.last_synced && (
              <p className="text-xs text-gray-500">
                Last synced: {new Date(apiStatus.frontend_integration.last_synced).toLocaleString()}
              </p>
            )}
          </div>
        </Card>
      )}
    </div>
  )
}

