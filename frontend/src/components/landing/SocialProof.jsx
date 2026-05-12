// Social Proof Component - Shows backed by industry leaders

import { Card } from '../common/Card'

export function SocialProof({ headline, poweredBy, builtOn }) {
  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            {headline}
          </h2>
        </div>

        {poweredBy && poweredBy.length > 0 && (
          <div className="mb-12">
            <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">
              Powered by:
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {poweredBy.map((item, idx) => (
                <Card key={idx} className="text-center">
                  <h4 className="font-bold text-lg text-gray-900 mb-2">
                    {item.name}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {item.description}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        )}

        {builtOn && builtOn.length > 0 && (
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">
              Built on:
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {builtOn.map((item, idx) => (
                <Card key={idx} className="text-center">
                  <h4 className="font-bold text-lg text-gray-900 mb-2">
                    {item.name}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {item.description}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}

