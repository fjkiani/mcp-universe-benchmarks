// Reusable Before/After Comparison Card
// Shows a clear visual comparison with toggle

import { useState } from 'react'
import { Card } from './Card'

export function BeforeAfterCard({ 
  before, 
  after,
  className = ''
}) {
  const [isAfter, setIsAfter] = useState(false)

  const current = isAfter ? after : before

  return (
    <Card className={`relative overflow-hidden ${className}`}>
      {/* Toggle */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className={`text-sm font-semibold ${!isAfter ? 'text-red-600' : 'text-gray-400'}`}>
            Before
          </span>
          <button
            onClick={() => setIsAfter(!isAfter)}
            className={`relative w-14 h-7 rounded-full transition-colors ${
              isAfter ? 'bg-green-500' : 'bg-red-500'
            }`}
            aria-label="Toggle before/after"
          >
            <div className={`absolute top-1 w-5 h-5 rounded-full bg-white shadow-md transition-transform ${
              isAfter ? 'translate-x-8' : 'translate-x-1'
            }`} />
          </button>
          <span className={`text-sm font-semibold ${isAfter ? 'text-green-600' : 'text-gray-400'}`}>
            After
          </span>
        </div>

        {/* Badge */}
        <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
          isAfter ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {isAfter ? after.badge : before.badge}
        </div>
      </div>

      {/* Content */}
      <div className={`transition-all duration-300 ${
        isAfter ? 'bg-green-50' : 'bg-red-50'
      } rounded-lg p-6`}>
        {/* Icon and Title */}
        <div className="flex items-center gap-3 mb-4">
          <span className="text-4xl">{current.icon}</span>
          <h3 className="text-xl font-bold text-gray-900">{current.title}</h3>
        </div>

        {/* Description */}
        <p className="text-gray-700 mb-4 leading-relaxed">
          {current.description}
        </p>

        {/* Stats */}
        {current.stats && (
          <div className="grid grid-cols-2 gap-4">
            {current.stats.map((stat, idx) => (
              <div key={idx} className="bg-white rounded-lg p-3">
                <div className={`text-2xl font-bold ${
                  isAfter ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stat.value}
                </div>
                <div className="text-xs text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Card>
  )
}





