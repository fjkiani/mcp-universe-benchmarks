// Metric Card - Display key performance indicators
export function MetricCard({ metric, size = 'default' }) {
  const sizeClasses = {
    small: 'p-4',
    default: 'p-6',
    large: 'p-8'
  }

  return (
    <div className={`bg-gradient-to-br from-white to-gray-50 rounded-2xl ${sizeClasses[size]} shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 border-2 border-gray-100 hover:border-blue-200 group`}>
      {/* Icon */}
      {metric.icon && (
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-blue-100 to-purple-100 mb-4 group-hover:scale-110 transition-transform">
          <span className="text-2xl">{metric.icon}</span>
        </div>
      )}

      {/* Value */}
      <div className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
        {metric.value}
      </div>

      {/* Label */}
      <div className="text-sm font-semibold text-gray-900 mb-2">
        {metric.label}
      </div>

      {/* Description */}
      {metric.description && (
        <p className="text-xs text-gray-600 leading-relaxed">
          {metric.description}
        </p>
      )}

      {/* Change indicator */}
      {metric.change && (
        <div className={`mt-3 inline-flex items-center gap-1 text-xs font-medium ${
          metric.change > 0 ? 'text-green-600' : 'text-red-600'
        }`}>
          <span>{metric.change > 0 ? '↑' : '↓'}</span>
          <span>{Math.abs(metric.change)}%</span>
        </div>
      )}
    </div>
  )
}

