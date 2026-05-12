// Use Cases Component - Shows ROI and use cases

import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

export function UseCases({ useCases }) {
  if (!useCases || useCases.length === 0) return null

  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Use Cases
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {useCases.map((useCase, idx) => (
            <Card key={idx} title={useCase.title} className="h-full">
              <div className="space-y-4">
                {useCase.challenge && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Challenge:</h4>
                    <p className="text-sm text-gray-600">{useCase.challenge}</p>
                  </div>
                )}

                {useCase.before && (
                  <div>
                    <h4 className="font-semibold text-red-900 mb-2">Before:</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      {useCase.before.costs.map((cost, cidx) => (
                        <li key={cidx} className="flex items-start gap-2">
                          <span>❌</span>
                          <span>{cost}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {useCase.after && (
                  <div>
                    <h4 className="font-semibold text-green-900 mb-2">After:</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      {useCase.after.costs.map((cost, cidx) => (
                        <li key={cidx} className="flex items-start gap-2">
                          <span>✅</span>
                          <span>{cost}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {useCase.solution && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Solution:</h4>
                    <p className="text-sm text-gray-600">{useCase.solution}</p>
                  </div>
                )}

                {useCase.result && (
                  <div className="pt-4 border-t border-gray-200">
                    {Array.isArray(useCase.result) ? (
                      <ul className="space-y-1 text-sm text-gray-600">
                        {useCase.result.map((r, ridx) => (
                          <li key={ridx} className="flex items-start gap-2">
                            <span>✓</span>
                            <span>{r}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <Badge status="success" className="text-sm">
                        {useCase.result}
                      </Badge>
                    )}
                  </div>
                )}

                {useCase.roi && (
                  <div className="pt-4 border-t border-gray-200">
                    <Badge status="info" className="text-sm font-bold">
                      {useCase.roi}
                    </Badge>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

