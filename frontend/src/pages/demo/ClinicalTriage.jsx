// Clinical Triage - Safety-critical routing
import { useState } from 'react'
import { Card } from '../../components/common/Card'
import { ENDPOINTS } from '../../api/config'

export default function ClinicalTriage() {
  const [formData, setFormData] = useState({
    chiefComplaint: 'Chest pain radiating to left arm',
    duration: '2 hours',
    severity: '8',
    symptoms: ['shortness of breath', 'diaphoresis']
  })
  const [currentSymptom, setCurrentSymptom] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const addSymptom = () => {
    if (currentSymptom.trim()) {
      setFormData({
        ...formData,
        symptoms: [...formData.symptoms, currentSymptom.trim()]
      })
      setCurrentSymptom('')
    }
  }

  const removeSymptom = (index) => {
    setFormData({
      ...formData,
      symptoms: formData.symptoms.filter((_, i) => i !== index)
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(ENDPOINTS.triage, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to perform triage')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getUrgencyColor = (urgency) => {
    if (urgency === 'EMERGENT') return 'bg-red-600'
    if (urgency === 'URGENT') return 'bg-orange-600'
    return 'bg-blue-600'
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Clinical Triage Assessment</h2>
        <p className="text-gray-600">
          Assess patient urgency and route appropriately. Safety-critical: 100% accuracy on emergencies.
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Chief Complaint *
            </label>
            <input
              type="text"
              value={formData.chiefComplaint}
              onChange={(e) => setFormData({ ...formData, chiefComplaint: e.target.value })}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., chest pain, fever, headache"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Duration
              </label>
              <input
                type="text"
                value={formData.duration}
                onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., 2 hours, 3 days"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Severity (1-10 scale)
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={formData.severity}
                onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="8"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Additional Symptoms
            </label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={currentSymptom}
                onChange={(e) => setCurrentSymptom(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSymptom())}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Add symptom and press Enter"
              />
              <button
                type="button"
                onClick={addSymptom}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                Add
              </button>
            </div>
            {formData.symptoms.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.symptoms.map((symptom, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                  >
                    {symptom}
                    <button
                      type="button"
                      onClick={() => removeSymptom(index)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full px-6 py-3 bg-gradient-to-r from-red-600 to-orange-600 text-white rounded-lg font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50"
          >
            {loading ? 'Assessing...' : 'Assess Urgency & Route'}
          </button>
        </form>
      </Card>

      {error && (
        <Card className="bg-red-50 border-red-200">
          <div className="flex items-start gap-3">
            <span className="text-2xl">❌</span>
            <div>
              <h3 className="text-lg font-bold text-red-900 mb-2">Error</h3>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        </Card>
      )}

      {result && (
        <Card className={`${getUrgencyColor(result.urgency)} text-white`}>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <span className="text-2xl">
                {result.urgency === 'EMERGENT' ? '🚨' : result.urgency === 'URGENT' ? '⚠️' : 'ℹ️'}
              </span>
              <div className="flex-1">
                <h3 className="text-2xl font-bold mb-2">Urgency: {result.urgency}</h3>
                <p className="text-lg opacity-90 mb-4">{result.advice}</p>
                <div className="space-y-2 text-sm">
                  <p><strong>Recommended Action:</strong> {result.recommended_action.replace('_', ' ').toUpperCase()}</p>
                  <p><strong>Routing:</strong> {result.routing}</p>
                  <p><strong>Safety Protocol:</strong> {result.safety_protocol}</p>
                </div>
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}




