// Solution Component - Modern SaaS style with visual impact
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

export function Solution({ headline, description, whatItDoes, whatItReplaces }) {
  return (
    <section className="py-20 px-4 bg-gradient-to-b from-gray-50 to-white relative">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-6">
            <span className="text-3xl">✨</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            {headline}
          </h2>
          {description && (
            <p 
              className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed"
              dangerouslySetInnerHTML={{ __html: description }}
            />
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* What It Does */}
          {whatItDoes && (
            <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center">
                  <span className="text-xl">✅</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900">What it does:</h3>
              </div>
              <ul className="space-y-4">
                {whatItDoes.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-3 group">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                      <span className="text-white text-xs">✓</span>
                    </div>
                    <span className="text-gray-800 leading-relaxed font-medium group-hover:text-green-700 transition-colors">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {/* What It Replaces */}
          {whatItReplaces && (
            <Card className="bg-gradient-to-br from-red-50 to-orange-50 border-2 border-red-200 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-red-500 flex items-center justify-center">
                  <span className="text-xl">❌</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900">What it replaces:</h3>
              </div>
              <ul className="space-y-4">
                {whatItReplaces.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-3 group">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-red-500 flex items-center justify-center mt-0.5">
                      <span className="text-white text-xs">×</span>
                    </div>
                    <span className="text-gray-800 leading-relaxed font-medium line-through group-hover:text-red-700 transition-colors">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            </Card>
          )}
        </div>
      </div>
    </section>
  )
}

