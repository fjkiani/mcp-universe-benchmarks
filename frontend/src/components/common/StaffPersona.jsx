// Reusable Staff Persona Card
// Shows a staff member with their role and transformation story

import { Card } from './Card'

export function StaffPersona({ 
  name,
  role,
  avatar,
  before,
  after,
  onLearnMore,
  className = ''
}) {
  return (
    <Card className={`group hover:shadow-xl transition-all duration-300 ${className}`}>
      <div className="text-center mb-4">
        {/* Avatar */}
        <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-4xl shadow-lg group-hover:scale-110 transition-transform">
          {avatar}
        </div>
        
        {/* Name and Role */}
        <h3 className="text-xl font-bold text-gray-900 mb-1">{name}</h3>
        <p className="text-sm text-gray-600">{role}</p>
      </div>

      {/* Before/After */}
      <div className="space-y-3 mb-4">
        {/* Before */}
        <div className="bg-red-50 rounded-lg p-3 border-l-4 border-red-400">
          <div className="text-xs font-semibold text-red-800 mb-1">BEFORE</div>
          <p className="text-sm text-gray-700">{before}</p>
        </div>

        {/* Arrow */}
        <div className="text-center">
          <span className="text-2xl">↓</span>
        </div>

        {/* After */}
        <div className="bg-green-50 rounded-lg p-3 border-l-4 border-green-400">
          <div className="text-xs font-semibold text-green-800 mb-1">NOW</div>
          <p className="text-sm text-gray-700">{after}</p>
        </div>
      </div>

      {/* Learn More Button */}
      {onLearnMore && (
        <button
          onClick={onLearnMore}
          className="w-full px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-semibold hover:shadow-lg transition-all transform hover:scale-105"
        >
          See {name}'s Day →
        </button>
      )}
    </Card>
  )
}





