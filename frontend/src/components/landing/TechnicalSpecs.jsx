// Technical Specifications Component - Shows API, integrations, compliance

import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

export function TechnicalSpecs({ headline, api, ehrs, integrations, compliance }) {
  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            {headline}
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* API & Integration */}
          {api && (
            <Card title="API & Integration">
              <div className="space-y-3">
                {api.features.map((feature, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <span className="text-green-600 mt-0.5">✓</span>
                    <span className="text-gray-700">{feature}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Supported EHRs */}
          {ehrs && (
            <Card title="Supported EHRs">
              <p className="text-gray-700 mb-3">{ehrs.description}</p>
              <div className="flex flex-wrap gap-2">
                {ehrs.list.map((ehr, idx) => (
                  <Badge key={idx} status="info" className="text-xs">
                    {ehr}
                  </Badge>
                ))}
              </div>
            </Card>
          )}

          {/* Supported Integrations */}
          {integrations && (
            <Card title="Supported Integrations">
              <div className="space-y-2">
                {integrations.map((integration, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <span className="text-gray-700 font-medium">{integration.name}</span>
                    <Badge status="success" className="text-xs">
                      {integration.type}
                    </Badge>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Compliance */}
          {compliance && (
            <Card title="Compliance">
              <div className="space-y-3">
                {compliance.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <Badge status="success" className="mt-0.5">✓</Badge>
                    <span className="text-gray-700">{item}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      </div>
    </section>
  )
}

