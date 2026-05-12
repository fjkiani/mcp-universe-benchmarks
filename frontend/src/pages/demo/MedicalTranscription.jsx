// Medical Transcription - Transcribe audio with entity extraction
import { useState } from 'react'
import { Card } from '../../components/common/Card'
import { ENDPOINTS } from '../../api/config'

export default function MedicalTranscription() {
  const [formData, setFormData] = useState({
    audio_url: 'https://assembly.ai/sports_injuries.mp3',
    patient_id: 'PT-001'
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(ENDPOINTS.transcribeAudio, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to transcribe audio')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Medical Transcription</h2>
        <p className="text-gray-600">Transcribe medical audio with entity extraction (93.3% accuracy)</p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Audio URL *</label>
            <input type="url" value={formData.audio_url} onChange={(e) => setFormData({ ...formData, audio_url: e.target.value })} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" placeholder="https://example.com/audio.mp3" />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Patient ID (optional)</label>
            <input type="text" value={formData.patient_id} onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
          <button type="submit" disabled={loading} className="w-full px-6 py-3 bg-gradient-to-r from-amber-600 to-yellow-600 text-white rounded-lg font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50">
            {loading ? 'Transcribing...' : 'Transcribe Audio'}
          </button>
        </form>
      </Card>

      {error && <Card className="bg-red-50 border-red-200"><div className="text-red-700">❌ {error}</div></Card>}
      {result && result.success && (
        <div className="space-y-4">
          <Card className="bg-green-50 border-green-200">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-green-900 text-lg">Transcript</h3>
                <span className="px-3 py-1 bg-green-600 text-white rounded-full text-sm font-bold">
                  {Math.round((result.confidence || 0) * 100)}% Confidence
                </span>
              </div>
              <p className="p-4 bg-white rounded-lg border border-green-200 text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{result.transcription}</p>
            </div>
          </Card>
          {result.medical_entities && (
            <Card>
              <h3 className="font-bold text-gray-900 mb-3">Extracted Medical Entities</h3>
              <div className="space-y-3">
                {Object.entries(result.medical_entities).map(([type, values]) =>
                  values?.length > 0 && (
                    <div key={type}>
                      <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">{type.replace(/_/g, ' ')}</p>
                      <div className="flex flex-wrap gap-2">
                        {values.map((v, i) => (
                          <span key={i} className="px-3 py-1 bg-amber-100 text-amber-800 border border-amber-300 rounded-full text-sm font-semibold">{v}</span>
                        ))}
                      </div>
                    </div>
                  )
                )}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}




