// Metrics Chart Component - Reusable chart wrapper
import { LineChart, Line, BarChart, Bar, AreaChart, Area, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export function MetricsChart({ type = 'line', data, config }) {
  const colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444']

  const renderChart = () => {
    switch (type) {
      case 'line':
        return (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey={config?.xAxis || 'name'} stroke="#6b7280" />
            <YAxis stroke="#6b7280" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px'
              }} 
            />
            <Legend />
            {config?.lines?.map((line, idx) => (
              <Line 
                key={line.dataKey}
                type="monotone" 
                dataKey={line.dataKey} 
                stroke={line.color || colors[idx % colors.length]}
                strokeWidth={2}
                dot={{ fill: line.color || colors[idx % colors.length], r: 4 }}
                name={line.name}
              />
            ))}
          </LineChart>
        )

      case 'bar':
        return (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey={config?.xAxis || 'name'} stroke="#6b7280" />
            <YAxis stroke="#6b7280" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px'
              }} 
            />
            <Legend />
            {config?.bars?.map((bar, idx) => (
              <Bar 
                key={bar.dataKey}
                dataKey={bar.dataKey} 
                fill={bar.color || colors[idx % colors.length]}
                name={bar.name}
                radius={[8, 8, 0, 0]}
              />
            ))}
          </BarChart>
        )

      case 'area':
        return (
          <AreaChart data={data}>
            <defs>
              {config?.areas?.map((area, idx) => (
                <linearGradient key={area.dataKey} id={`color${idx}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={area.color || colors[idx % colors.length]} stopOpacity={0.8}/>
                  <stop offset="95%" stopColor={area.color || colors[idx % colors.length]} stopOpacity={0.1}/>
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey={config?.xAxis || 'name'} stroke="#6b7280" />
            <YAxis stroke="#6b7280" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px'
              }} 
            />
            <Legend />
            {config?.areas?.map((area, idx) => (
              <Area 
                key={area.dataKey}
                type="monotone" 
                dataKey={area.dataKey} 
                stroke={area.color || colors[idx % colors.length]}
                fill={`url(#color${idx})`}
                name={area.name}
              />
            ))}
          </AreaChart>
        )

      case 'pie':
        return (
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey={config?.dataKey || 'value'}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        )

      default:
        return null
    }
  }

  return (
    <div className="w-full h-full">
      <ResponsiveContainer width="100%" height={config?.height || 300}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  )
}

