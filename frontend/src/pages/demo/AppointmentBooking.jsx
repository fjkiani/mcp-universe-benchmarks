// Appointment Booking - Book appointment in NexHealth EHR
import { useState } from 'react'
import { Card } from '../../components/common/Card'
import { ENDPOINTS } from '../../api/config'

export default function AppointmentBooking() {
  const [formData, setFormData] = useState({
    patientId: 'PT-001',
    providerId: 'dr_kim_101',
    date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    time: '09:00',
    reason: 'Lower back pain radiating to left leg',
    appointmentType: 'general'
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
      const response = await fetch(ENDPOINTS.bookAppointment, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to book appointment')
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
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Appointment Booking</h2>
        <p className="text-gray-600">
          Book appointments directly in NexHealth EHR with real-time provider availability
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Patient ID (MRN) *
              </label>
              <input
                type="text"
                value={formData.patientId}
                onChange={(e) => setFormData({ ...formData, patientId: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="MRN-12345"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Provider ID *
              </label>
              <input
                type="text"
                value={formData.providerId}
                onChange={(e) => setFormData({ ...formData, providerId: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="dr_smith"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date *
              </label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Time *
              </label>
              <input
                type="time"
                value={formData.time}
                onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Reason for Visit *
              </label>
              <input
                type="text"
                value={formData.reason}
                onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Annual physical"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Appointment Type
              </label>
              <select
                value={formData.appointmentType}
                onChange={(e) => setFormData({ ...formData, appointmentType: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="general">General</option>
                <option value="follow-up">Follow-up</option>
                <option value="consultation">Consultation</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50"
          >
            {loading ? 'Booking Appointment...' : 'Book Appointment'}
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

      {result && result.success && (
        <Card className="bg-green-50 border-green-200">
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <span className="text-2xl">✅</span>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-green-900 mb-2">Appointment Booked Successfully!</h3>
                <div className="space-y-2 text-green-800">
                  <p><strong>Appointment ID:</strong> {result.appointment_id}</p>
                  <p><strong>Confirmation Sent:</strong> {result.confirmation_sent ? 'Yes' : 'No'}</p>
                </div>
              </div>
            </div>

            <details className="mt-4">
              <summary className="cursor-pointer text-sm font-semibold text-green-900 hover:text-green-700">
                View FHIR Appointment Resource
              </summary>
              <pre className="mt-2 p-4 bg-white rounded-lg border border-green-200 overflow-auto text-xs">
                {JSON.stringify(result.fhir_appointment, null, 2)}
              </pre>
            </details>
          </div>
        </Card>
      )}
    </div>
  )
}




