// Technical Architecture Component - Shows MCP architecture and tech stack

import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

export function TechnicalArchitecture({ headline, subheadline, description, whyMCP, stack }) {
  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            {headline}
          </h2>
          {subheadline && (
            <p className="text-xl text-gray-600 mb-4">
              {subheadline}
            </p>
          )}
          {description && (
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              {description}
            </p>
          )}
        </div>

        {/* Why MCP */}
        {whyMCP && whyMCP.length > 0 && (
          <div className="mb-12">
            <h3 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
              Why MCP?
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {whyMCP.map((reason, idx) => (
                <Card key={idx} className="text-center">
                  <Badge status="success" className="mb-3">✅</Badge>
                  <p className="text-sm text-gray-700">{reason}</p>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Stack Diagram */}
        {stack && (
          <Card className="bg-white">
            <h3 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
              Our Stack
            </h3>
            {stack.description && (
              <p className="text-gray-600 mb-6 text-center">
                {stack.description}
              </p>
            )}
            
            {stack.components && (
              <div className="space-y-4">
                {stack.components.map((component, idx) => (
                  <div key={idx} className="border-l-4 border-blue-500 pl-4 py-2">
                    <h4 className="font-semibold text-gray-900 mb-1">
                      {component.name}
                    </h4>
                    <p className="text-sm text-gray-600">
                      {component.description}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </Card>
        )}
      </div>
    </section>
  )
}

