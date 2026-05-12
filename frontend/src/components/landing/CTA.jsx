// CTA Component - Reusable call-to-action section

import { Button } from '../common/Button'

export function CTA({ headline, subheadline, primaryCTA, note, secondaryCTAs }) {
  return (
    <section className="py-16 px-4 bg-gradient-to-r from-blue-600 to-blue-700">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl font-bold text-white mb-4">
          {headline}
        </h2>
        {subheadline && (
          <p className="text-xl text-blue-100 mb-8">
            {subheadline}
          </p>
        )}

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-4">
          {primaryCTA && (
            <Button
              variant="secondary"
              size="lg"
              onClick={() => window.location.href = primaryCTA.link || '#'}
              className="bg-white text-blue-600 hover:bg-gray-100 w-full sm:w-auto"
            >
              {primaryCTA.text} →
            </Button>
          )}

          {secondaryCTAs && secondaryCTAs.map((cta, idx) => (
            <Button
              key={idx}
              variant="outline"
              size="lg"
              onClick={() => window.location.href = cta.link || '#'}
              className="border-white text-white hover:bg-blue-600 w-full sm:w-auto"
            >
              {cta.text}
            </Button>
          ))}
        </div>

        {note && (
          <p className="text-sm text-blue-100">
            {note}
          </p>
        )}
      </div>
    </section>
  )
}

