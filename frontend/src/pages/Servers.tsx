import { useQuery } from '@tanstack/react-query'
import { mcpClient } from '../api/mcp-client'
import { ServerStatus } from '../components/dashboard/ServerStatus'

export default function Servers() {
  const { data: servers, isLoading } = useQuery({
    queryKey: ['servers'],
    queryFn: () => mcpClient.getServers(),
  })

  if (isLoading) {
    return <div>Loading servers...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">MCP Servers</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {servers?.map((server) => (
            <ServerStatus key={server.name} server={server} />
          ))}
        </div>
      </div>
    </div>
  )
}







