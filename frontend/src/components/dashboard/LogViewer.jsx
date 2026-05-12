// Log Viewer Component - Display logs and metrics in real-time
import { useState } from 'react'
import { Card } from '../common/Card'

export function LogViewer({ logs, title = "System Logs", maxLines = 50 }) {
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const filteredLogs = logs
    ?.filter(log => {
      if (filter !== 'all' && log.level !== filter) return false
      if (searchTerm && !log.message.toLowerCase().includes(searchTerm.toLowerCase())) return false
      return true
    })
    .slice(0, maxLines) || []

  const getLevelColor = (level) => {
    switch (level) {
      case 'error': return 'text-red-600 bg-red-50 border-red-200'
      case 'warning': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'success': return 'text-green-600 bg-green-50 border-green-200'
      case 'info': return 'text-blue-600 bg-blue-50 border-blue-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  return (
    <Card className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Search logs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All</option>
            <option value="error">Errors</option>
            <option value="warning">Warnings</option>
            <option value="success">Success</option>
            <option value="info">Info</option>
          </select>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto bg-gray-900 rounded-lg p-4 font-mono text-sm">
        {filteredLogs.length === 0 ? (
          <div className="text-gray-400 text-center py-8">No logs found</div>
        ) : (
          <div className="space-y-1">
            {filteredLogs.map((log, idx) => (
              <div
                key={idx}
                className={`flex items-start gap-3 p-2 rounded border-l-4 ${getLevelColor(log.level)}`}
              >
                <span className="text-gray-400 text-xs flex-shrink-0 w-20">
                  {log.timestamp || new Date().toLocaleTimeString()}
                </span>
                <span className="text-xs font-semibold uppercase flex-shrink-0 w-16">
                  [{log.level}]
                </span>
                <span className="text-gray-300 flex-1">
                  {log.message}
                </span>
                {log.source && (
                  <span className="text-xs text-gray-500 flex-shrink-0">
                    {log.source}
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
        <span>Showing {filteredLogs.length} of {logs?.length || 0} logs</span>
        <span>Auto-refresh: ON</span>
      </div>
    </Card>
  )
}

