// FAQ Component - Reusable FAQ section
// Accepts array of Q&A objects

import { Card } from '../common/Card'
import { useState } from 'react'

export function FAQ({ faqs }) {
  const [openIndex, setOpenIndex] = useState(null)

  if (!faqs || faqs.length === 0) return null

  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Frequently Asked Questions
          </h2>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, idx) => (
            <Card 
              key={idx}
              className="cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {faq.question}
                  </h3>
                  {openIndex === idx && (
                    <p className="text-gray-600">
                      {faq.answer}
                    </p>
                  )}
                </div>
                <button className="text-gray-400 text-2xl">
                  {openIndex === idx ? '−' : '+'}
                </button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

