// Reusable Benefit Card Component
// Shows a benefit with icon, title, description, and optional stats

import { Card } from './Card'

export function BenefitCard({ 
  icon, 
  title, 
  description, 
  stat, 
  statLabel,
  color = 'blue',
  gradient = 'from-blue-500 to-cyan-500',
  className = ''
}) {
  return (
    <Card className={`group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 ${className}`}>
      <div className="flex flex-col h-full">
        {/* Icon and Title */}
        <div className="flex items-start gap-4 mb-4">
          <div className={`flex-shrink-0 w-12 h-12 rounded-lg bg-gradient-to-br ${gradient} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform`}>
            <span className="text-2xl">{icon}</span>
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-gray-900 mb-1">{title}</h3>
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 leading-relaxed mb-4 flex-grow">
          {description}
        </p>

        {/* Stat */}
        {stat && (
          <div className={`mt-auto pt-4 border-t border-gray-100`}>
            <div className={`text-3xl font-bold bg-gradient-to-r ${gradient} bg-clip-text text-transparent`}>
              {stat}
            </div>
            {statLabel && (
              <div className="text-sm text-gray-500 mt-1">{statLabel}</div>
            )}
          </div>
        )}
      </div>
    </Card>
  )
}





