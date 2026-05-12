// How It Works Component - Reusable step-by-step section

import { Card } from '../common/Card'

export function HowItWorks({ headline, subheadline, steps }) {
  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            {headline}
          </h2>
          {subheadline && (
            <p className="text-xl text-gray-600">
              {subheadline}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps && steps.map((step, idx) => (
            <Card key={idx} className="text-center relative">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div className="bg-blue-600 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold text-lg">
                  {step.number}
                </div>
              </div>
              <div className="pt-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {step.title}
                </h3>
                <p className="text-gray-600">
                  {step.description}
                </p>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

