// API Showcase Component - Displays real API status from api-status.json
// Reads from synced data (central/api-registry.yaml → frontend/src/data/api-status.json)

import { useQuery } from '@tanstack/react-query'
import { readApiStatus } from '../../utils/data-reader'
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'
import { ProgressBar } from '../charts/ProgressBar'

export function APIShowcase() {
  const { data: apiStatus, isLoading } = useQuery({
    queryKey: ['api-status'],
    queryFn: readApiStatus,
    staleTime: 30000, // Cache for 30 seconds
  })

  if (isLoading) {
    return (
      <div className="text-center text-gray-600 py-8">
        Loading API status...
      </div>
    )
  }

  if (!apiStatus || !apiStatus.apis || apiStatus.apis.length === 0) {
    return (
      <Card>
        <p className="text-gray-600">
          No API data available. Run: <code className="bg-gray-100 px-2 py-1 rounded">python central/frontend-sync.py</code>
        </p>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          API Status ({apiStatus.apis.length} APIs)
        </h2>
        <p className="text-sm text-gray-600 mb-6">
          Last synced: {new Date(apiStatus.timestamp).toLocaleString()}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {apiStatus.apis.map((api) => (
          <Card key={api.id} title={api.name} className="h-full">
            <div className="space-y-4">
              {/* Status Badge */}
              <div className="flex items-center justify-between">
                <Badge 
                  status={
                    api.status === 'active' ? 'success' :
                    api.status === 'pending' ? 'warning' : 'error'
                  }
                >
                  {api.status.toUpperCase()}
                </Badge>
                <span className="text-sm text-gray-500">
                  {api.category}
                </span>
              </div>

              {/* Test Metrics */}
              {api.tests && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Tests</span>
                    <span className="font-medium">
                      {api.tests.passed}/{api.tests.total} passed
                    </span>
                  </div>
                  <ProgressBar 
                    value={api.tests.coverage || 0}
                    label={`${api.tests.coverage}% coverage`}
                  />
                  {api.tests.pending > 0 && (
                    <p className="text-xs text-gray-500">
                      {api.tests.pending} pending
                    </p>
                  )}
                </div>
              )}

              {/* Endpoints */}
              {api.endpoints && api.endpoints.length > 0 && (
                <div>
                  <p className="text-sm text-gray-600 mb-2">
                    {api.endpoints.length} endpoints
                  </p>
                  <div className="space-y-1">
                    {api.endpoints.slice(0, 3).map((endpoint, idx) => (
                      <div key={idx} className="flex items-center justify-between text-xs">
                        <span className="text-gray-700">{endpoint.name}</span>
                        <Badge 
                          status={
                            endpoint.test_result === 'passed' ? 'success' :
                            endpoint.test_result === 'failed' ? 'error' : 'warning'
                          }
                          className="text-xs"
                        >
                          {endpoint.test_result || 'pending'}
                        </Badge>
                      </div>
                    ))}
                    {api.endpoints.length > 3 && (
                      <p className="text-xs text-gray-500">
                        +{api.endpoints.length - 3} more
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* Frontend Integration */}
              {api.frontend?.integrated && (
                <div className="pt-2 border-t border-gray-200">
                  <Badge status="info" className="text-xs">
                    Frontend Integrated
                  </Badge>
                </div>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}

