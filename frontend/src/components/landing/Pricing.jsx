// Pricing Component - Reusable pricing section
// Accepts pricing tiers from domain constants

import { Card } from '../common/Card'
import { Button } from '../common/Button'
import { Badge } from '../common/Badge'

export function Pricing({ headline, tiers, includedInAll }) {
  if (!tiers || tiers.length === 0) return null

  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            {headline}
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {tiers.map((tier, idx) => (
            <Card 
              key={idx} 
              className={`relative ${tier.popular ? 'border-2 border-blue-500 shadow-lg' : ''}`}
            >
              {tier.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge status="info">Most Popular</Badge>
                </div>
              )}
              
              <div className="text-center mb-6 pt-4">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {tier.name}
                </h3>
                <div className="text-3xl font-bold text-blue-600 mb-4">
                  {tier.price}
                </div>
              </div>

              <ul className="space-y-3 mb-6">
                {tier.features.map((feature, fidx) => (
                  <li key={fidx} className="flex items-start gap-2">
                    <span className="text-green-600 mt-0.5">✓</span>
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <Button
                variant={tier.popular ? 'primary' : 'outline'}
                className="w-full"
                onClick={() => window.location.href = '/signup'}
              >
                Get Started
              </Button>
            </Card>
          ))}
        </div>

        {includedInAll && includedInAll.length > 0 && (
          <div className="text-center">
            <p className="text-gray-600 mb-4">
              <span className="font-semibold">All plans include:</span>
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              {includedInAll.map((item, idx) => (
                <Badge key={idx} status="success" className="text-sm">
                  ✓ {item}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}

