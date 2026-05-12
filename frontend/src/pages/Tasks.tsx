import { useQuery } from '@tanstack/react-query'
import { mcpClient } from '../api/mcp-client'
import { Navbar } from '../components/layout/Navbar'
import { Card } from '../components/common/Card'
import { Badge } from '../components/common/Badge'
import { ProgressBar } from '../components/charts/ProgressBar'

export default function Tasks() {
  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => mcpClient.getTasks(),
    refetchInterval: 30000 // Refresh every 30 seconds
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <div className="text-gray-600">Loading tasks...</div>
        </div>
      </div>
    )
  }

  // Group tasks by status
  const tasksByStatus = {
    completed: tasks?.filter(t => t.status === 'completed') || [],
    in_progress: tasks?.filter(t => t.status === 'in_progress') || [],
    pending: tasks?.filter(t => t.status === 'pending') || [],
    failed: tasks?.filter(t => t.status === 'failed') || []
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="pt-24 p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Tasks</h1>
            <p className="text-gray-600">
              Track all domain tasks, test results, and integration status
            </p>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <Card className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-1">
                {tasksByStatus.completed.length}
              </div>
              <div className="text-sm text-gray-600">Completed</div>
            </Card>
            <Card className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-1">
                {tasksByStatus.in_progress.length}
              </div>
              <div className="text-sm text-gray-600">In Progress</div>
            </Card>
            <Card className="text-center">
              <div className="text-3xl font-bold text-yellow-600 mb-1">
                {tasksByStatus.pending.length}
              </div>
              <div className="text-sm text-gray-600">Pending</div>
            </Card>
            <Card className="text-center">
              <div className="text-3xl font-bold text-red-600 mb-1">
                {tasksByStatus.failed.length}
              </div>
              <div className="text-sm text-gray-600">Failed</div>
            </Card>
          </div>

          {/* Tasks Grid */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">All Tasks</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {tasks?.map((task: any) => (
                <Card 
                  key={task.id} 
                  className="hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
                >
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <h3 className="text-lg font-bold text-gray-900">{task.name}</h3>
                      <Badge 
                        status={
                          task.status === 'completed' ? 'success' :
                          task.status === 'in_progress' ? 'info' :
                          task.status === 'failed' ? 'error' : 'warning'
                        }
                      >
                        {task.status.replace('_', ' ')}
                      </Badge>
                    </div>

                    {/* Pass Rate */}
                    {task.passRate !== undefined && task.passRate !== null && (
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-gray-500">Pass Rate</span>
                          <span className="text-sm font-semibold text-gray-900">
                            {task.passRate}%
                          </span>
                        </div>
                        <ProgressBar value={task.passRate} />
                      </div>
                    )}

                    {/* Category */}
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Category</p>
                      <p className="text-sm font-medium text-gray-700 capitalize">
                        {task.category.replace('_', ' ')}
                      </p>
                    </div>

                    {/* MCP Servers */}
                    <div>
                      <p className="text-xs text-gray-500 mb-2">MCP Servers</p>
                      <div className="flex flex-wrap gap-2">
                        {task.servers?.map((server: string, idx: number) => (
                          <Badge 
                            key={idx} 
                            status={server === 'nexhealth' ? 'success' : 'info'}
                            className="text-xs"
                          >
                            {server}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Last Tested */}
                    {task.lastTested && (
                      <div className="pt-3 border-t border-gray-100">
                        <p className="text-xs text-gray-500">
                          Last tested: {new Date(task.lastTested).toLocaleString()}
                        </p>
                      </div>
                    )}
                  </div>
                </Card>
              ))}
            </div>

            {(!tasks || tasks.length === 0) && (
              <Card className="text-center py-12">
                <p className="text-gray-500">No tasks found. Backend may be unavailable.</p>
                <p className="text-sm text-gray-400 mt-2">
                  Check backend connection or run tests to generate task data.
                </p>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}


