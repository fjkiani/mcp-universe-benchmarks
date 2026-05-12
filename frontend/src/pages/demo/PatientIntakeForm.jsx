// Patient Intake Form - Create FHIR Patient and register in NexHealth
import { useState } from 'react'
import { Card } from '../../components/common/Card'
import { ENDPOINTS } from '../../api/config'

export default function PatientIntakeForm() {
  const [formData, setFormData] = useState({
    firstName: 'Sarah',
    lastName: 'Johnson',
    dob: '1985-03-22',
    phone: '+13055550100',
    email: 'sarah.johnson@example.com',
    insurance: {
      carrier: 'Blue Cross Blue Shield',
      memberId: 'A12B34567',
      groupNumber: 'GRP-9921'
    }
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
      const response = await fetch(ENDPOINTS.createPatient, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to create patient')
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
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Patient Intake & Registration</h2>
        <p className="text-gray-600">
          Create a new patient record in FHIR format and register in NexHealth EHR
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                First Name *
              </label>
              <input
                type="text"
                value={formData.firstName}
                onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="John"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Last Name *
              </label>
              <input
                type="text"
                value={formData.lastName}
                onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Doe"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date of Birth *
              </label>
              <input
                type="date"
                value={formData.dob}
                onChange={(e) => setFormData({ ...formData, dob: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Phone *
              </label>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="555-123-4567"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="john.doe@example.com"
              />
            </div>
          </div>

          <div className="border-t pt-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Insurance Information</h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Insurance Carrier *
                </label>
                <select
                  value={formData.insurance.carrier}
                  onChange={(e) => setFormData({
                    ...formData,
                    insurance: { ...formData.insurance, carrier: e.target.value }
                  })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select Carrier</option>
                  <option value="Blue Cross Blue Shield">Blue Cross Blue Shield</option>
                  <option value="Aetna">Aetna</option>
                  <option value="UnitedHealthcare">UnitedHealthcare</option>
                  <option value="Medicare">Medicare</option>
                  <option value="Medicaid">Medicaid</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Member ID *
                </label>
                <input
                  type="text"
                  value={formData.insurance.memberId}
                  onChange={(e) => setFormData({
                    ...formData,
                    insurance: { ...formData.insurance, memberId: e.target.value }
                  })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="ABC123"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Group Number
                </label>
                <input
                  type="text"
                  value={formData.insurance.groupNumber}
                  onChange={(e) => setFormData({
                    ...formData,
                    insurance: { ...formData.insurance, groupNumber: e.target.value }
                  })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="GRP999"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating Patient...' : 'Create Patient Record'}
          </button>
        </form>
      </Card>

      {/* Results Display */}
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
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-green-900">✅ Patient Registered</h3>
              <span className="px-3 py-1 bg-green-600 text-white rounded-full text-sm font-bold">FHIR R4</span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Medical Record #</p>
                <p className="text-2xl font-black text-green-700 font-mono">{result.mrn}</p>
              </div>
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">NexHealth Patient ID</p>
                <p className="text-xl font-bold text-gray-700 font-mono">{result.nexhealth_patient_id || '—'}</p>
              </div>
            </div>
            <details className="mt-2">
              <summary className="cursor-pointer text-sm font-semibold text-green-900 hover:text-green-700">View FHIR R4 Resource ↓</summary>
              <pre className="mt-2 p-4 bg-white rounded-lg border border-green-200 overflow-auto text-xs">{JSON.stringify(result.fhir_resource, null, 2)}</pre>
            </details>
          </div>
        </Card>
      )}
    </div>
  )
}




