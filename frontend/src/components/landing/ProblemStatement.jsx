// Problem Statement Component - Modern SaaS style with visual impact
import { Card } from '../common/Card'

export function ProblemStatement({ headline, description, problems, result }) {
  return (
    <section className="py-20 px-4 bg-white relative">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-6">
            <span className="text-3xl">⚠️</span>
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

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
          {problems && problems.map((problem, idx) => (
            <Card 
              key={idx} 
              className="border-l-4 border-red-500 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 bg-white"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-red-100 flex items-center justify-center">
                  <span className="text-xl">{problem.icon || '❌'}</span>
                </div>
                <div className="flex-1">
                  <p className="text-gray-800 leading-relaxed font-medium">
                    {problem.text}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {result && (
          <div className="max-w-4xl mx-auto">
            <Card className="bg-gradient-to-r from-red-50 to-orange-50 border-2 border-red-200 p-6">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-red-500 flex items-center justify-center">
                  <span className="text-2xl text-white">💸</span>
                </div>
                <p className="text-xl font-semibold text-gray-900 leading-relaxed">
                  {result}
                </p>
              </div>
            </Card>
          </div>
        )}
      </div>
    </section>
  )
}

