// Hero Component - Component-Driven, Visual-First
// Uses config.visual and config.behavior for intelligent rendering
import { Button } from '../common/Button'

export function Hero({ config }) {
  // Support both old props (backward compat) and new config structure
  const content = config?.content || {
    headline: config?.headline || "AI Healthcare Receptionist",
    subheadline: config?.subheadline || "",
    primaryCTA: config?.primaryCTA || {},
    secondaryCTAs: config?.secondaryCTAs || [],
    badge: config?.badge || {}
  }
  
  const visual = config?.visual || {
    background: { type: "animated-blobs", colors: ["blue", "purple", "pink"] },
    headline: { gradient: "", size: "text-5xl md:text-7xl" },
    stats: []
  }
  
  const behavior = config?.behavior || {}

  return (
    <section className={`relative pt-24 pb-20 px-4 overflow-hidden ${visual.background?.gradient || 'bg-gradient-to-b from-white via-blue-50/50 to-white'}`}>
      {/* Animated Background Blobs */}
      {visual.background?.type === "animated-blobs" && (
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {visual.background.colors?.map((color, idx) => (
            <div
              key={idx}
              className={`absolute w-80 h-80 bg-${color}-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob`}
              style={{
                top: idx === 0 ? '-10rem' : idx === 1 ? '50%' : 'auto',
                right: idx === 0 ? '-10rem' : 'auto',
                left: idx === 1 ? '-10rem' : idx === 2 ? '50%' : 'auto',
                bottom: idx === 2 ? '-10rem' : 'auto',
                animationDelay: `${idx * 2}s`
              }}
            />
          ))}
        </div>
      )}

      <div className="relative max-w-7xl mx-auto text-center">
        {/* Badge with Visual Properties */}
        {content.badge && (
          <div className={`inline-flex items-center px-4 py-2 mb-8 rounded-full ${visual.badge?.gradient || 'bg-blue-100'} ${visual.badge?.border || ''} ${visual.badge?.animation || ''} text-blue-800 text-sm font-medium`}>
            {content.badge.icon && <span className="mr-2">{content.badge.icon}</span>}
            {content.badge.text}
          </div>
        )}

        {/* Headline with Gradient */}
        <h1 className={`${visual.headline?.size || 'text-5xl md:text-7xl'} font-bold mb-6 leading-tight ${visual.headline?.gradient || 'text-gray-900'}`}>
          {content.headline}
        </h1>
        
        <p className="text-xl md:text-2xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
          {content.subheadline}
        </p>
        
        {/* CTA Buttons with Behavior */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-6">
          {content.primaryCTA && (
            <Button
              variant="primary"
              size="lg"
              onClick={() => window.location.href = content.primaryCTA.link || '#'}
              className={`w-full sm:w-auto text-lg px-8 py-4 shadow-lg transition-all transform ${behavior.ctaHover || 'hover:scale-105 hover:shadow-xl'}`}
            >
              {content.primaryCTA.text || 'Get Started'} →
            </Button>
          )}
          
          {content.secondaryCTAs?.map((cta, idx) => (
            <Button
              key={idx}
              variant="outline"
              size="lg"
              onClick={() => window.location.href = cta.link || '#'}
              className="w-full sm:w-auto text-lg px-8 py-4 border-2 hover:border-gray-400 transition-all"
            >
              {cta.text} →
            </Button>
          ))}
        </div>
        
        {content.primaryCTA?.note && (
          <p className="text-sm text-gray-500">
            {content.primaryCTA.note}
          </p>
        )}

        {/* Stats with Visual Properties */}
        {visual.stats && visual.stats.length > 0 && (
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            {visual.stats.map((stat, idx) => (
              <div
                key={idx}
                className={`text-center ${behavior.statsHover || 'hover:scale-110'} transition-transform ${stat.delay || ''}`}
              >
                <div className={`text-3xl font-bold bg-gradient-to-r ${stat.gradient} bg-clip-text text-transparent ${stat.animation || ''}`}>
                  {stat.value}
                </div>
                <div className="text-sm text-gray-600 mt-1 flex items-center justify-center gap-1">
                  {stat.icon && <span>{stat.icon}</span>}
                  <span>{stat.label}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

