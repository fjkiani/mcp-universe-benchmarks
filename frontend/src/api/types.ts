// TypeScript types for API responses

export interface ServerStatus {
  name: string
  status: 'ready' | 'testing' | 'failed' | 'pending'
  structure: boolean
  syntax: boolean
  apiKeys: boolean
  dependencies: boolean
  testsPassed: number
  testsFailed: number
  lastTested?: string
  tools: string[]
}

export interface SprintMetrics {
  currentSprint: string
  passRate: number
  tasksCompleted: number
  tasksTotal: number
  serversTested: number
  serversTotal: number
  priorities: Priority[]
}

export interface Priority {
  id: string
  name: string
  status: 'pending' | 'in_progress' | 'completed'
  tasks: number
  completed: number
}

export interface TaskStatus {
  id: string
  name: string
  category: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  servers: string[]
  passRate?: number
  lastTested?: string
}

export interface TestResult {
  server: string
  test: string
  status: 'passed' | 'failed'
  message?: string
  duration?: number
}







