// HIPAA SMS - Send compliant SMS
import { useState } from 'react'
import { Card } from '../../components/common/Card'
import { ENDPOINTS } from '../../api/config'

export default function HipaaSMS() {
  const [formData, setFormData] = useState({
    phone: '+15551234567',
    message: 'Your appointment with Dr. Smith for diabetes treatment is Nov 15 at 2pm. MRN: 12345.'
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
      const response = await fetch(ENDPOINTS.sendSms, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to send SMS')
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
        <h2 className="text-3xl font-bold text-gray-900 mb-2">HIPAA-Compliant SMS</h2>
        <p className="text-gray-600">Send SMS with automatic PHI detection and filtering</p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Phone Number *</label>
            <input type="tel" value={formData.phone} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" placeholder="+15551234567" />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Message *</label>
            <textarea value={formData.message} onChange={(e) => setFormData({ ...formData, message: e.target.value })} required rows={4} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" placeholder="Your appointment with Dr. Smith for diabetes is Nov 15 at 2pm" />
          </div>
          <button type="submit" disabled={loading} className="w-full px-6 py-3 bg-gradient-to-r from-teal-600 to-cyan-600 text-white rounded-lg font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50">
            {loading ? 'Sending...' : 'Send HIPAA SMS'}
          </button>
        </form>
      </Card>

      {error && (
        <Card className="bg-red-50 border-red-200">
          <div className="flex items-center gap-2 text-red-700"><span>❌</span><p>{error}</p></div>
        </Card>
      )}
      {result && result.success && (
        <div className="space-y-4">
          <Card className="bg-green-50 border-green-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-green-900 text-lg">✅ SMS Dispatched</h3>
              <span className="px-3 py-1 bg-green-600 text-white rounded-full text-sm font-bold">HIPAA Compliant</span>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">PHI Detected & Redacted</p>
                {result.phi_detected?.length > 0
                  ? <div className="flex flex-wrap gap-2">{result.phi_detected.map((p, i) => <span key={i} className="px-2 py-1 bg-orange-100 text-orange-800 border border-orange-300 rounded text-sm font-semibold">{p}</span>)}</div>
                  : <span className="text-sm text-gray-500">None detected</span>
                }
              </div>
              <div className="bg-white rounded-lg p-3 border border-green-200">
                <p className="text-xs font-bold text-gray-500 uppercase mb-1">Message Sent</p>
                <p className="text-sm text-gray-800">{result.message_sent || formData.message}</p>
              </div>
              {result.message_sid && <p className="text-xs text-gray-400 font-mono">Twilio SID: {result.message_sid}</p>}
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}




