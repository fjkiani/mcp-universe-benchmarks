import { Card } from '../common/Card'
import { Badge } from '../common/Badge'
import { ProgressBar } from '../charts/ProgressBar'
import { ServerStatus as ServerStatusType } from '../../api/types'

interface ServerStatusProps {
  server: ServerStatusType
}

export function ServerStatus({ server }: ServerStatusProps) {
  const totalTests = server.testsPassed + server.testsFailed
  const passRate = totalTests > 0 ? (server.testsPassed / totalTests) * 100 : 0
  
  const statusBadge = {
    ready: 'success' as const,
    testing: 'info' as const,
    failed: 'error' as const,
    pending: 'warning' as const
  }
  
  return (
    <Card title={server.name} className="h-full">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Badge status={statusBadge[server.status]}>
            {server.status.toUpperCase()}
          </Badge>
          <span className="text-sm text-gray-500">
            {server.tools.length} tools
          </span>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-600 mb-1">Structure</p>
            <Badge status={server.structure ? 'success' : 'error'}>
              {server.structure ? '✅ Valid' : '❌ Invalid'}
            </Badge>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Syntax</p>
            <Badge status={server.syntax ? 'success' : 'error'}>
              {server.syntax ? '✅ Valid' : '❌ Invalid'}
            </Badge>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">API Keys</p>
            <Badge status={server.apiKeys ? 'success' : 'error'}>
              {server.apiKeys ? '✅ Set' : '❌ Missing'}
            </Badge>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Dependencies</p>
            <Badge status={server.dependencies ? 'success' : 'warning'}>
              {server.dependencies ? '✅ Ready' : '⚠️ Needs Setup'}
            </Badge>
          </div>
        </div>
        
        {totalTests > 0 && (
          <ProgressBar
            value={passRate}
            label={`${server.testsPassed}/${totalTests} tests passed`}
          />
        )}
        
        {server.lastTested && (
          <p className="text-xs text-gray-500">
            Last tested: {new Date(server.lastTested).toLocaleString()}
          </p>
        )}
      </div>
    </Card>
  )
}







