// Insurance Verification - Check eligibility
import { useState } from 'react'
import { Card } from '../../components/common/Card'
import { ENDPOINTS } from '../../api/config'

export default function InsuranceVerification() {
  const [formData, setFormData] = useState({
    patientId: 'PT-001',
    procedureCode: '99214',
    insurance: { carrier: 'BlueCross BlueShield', memberId: 'A12B34567' }
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
      const response = await fetch(ENDPOINTS.verifyInsurance, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to verify insurance')
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
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Insurance Verification</h2>
        <p className="text-gray-600">Check insurance eligibility and prior authorization requirements</p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Patient ID *</label>
            <input type="text" value={formData.patientId} onChange={(e) => setFormData({ ...formData, patientId: e.target.value })} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Procedure Code</label>
            <input type="text" value={formData.procedureCode} onChange={(e) => setFormData({ ...formData, procedureCode: e.target.value })} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" placeholder="CPT-70553" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Insurance Carrier *</label>
              <input type="text" value={formData.insurance.carrier} onChange={(e) => setFormData({ ...formData, insurance: { ...formData.insurance, carrier: e.target.value } })} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Member ID *</label>
              <input type="text" value={formData.insurance.memberId} onChange={(e) => setFormData({ ...formData, insurance: { ...formData.insurance, memberId: e.target.value } })} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          <button type="submit" disabled={loading} className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50">
            {loading ? 'Verifying...' : 'Verify Insurance'}
          </button>
        </form>
      </Card>

      {error && (
        <Card className="bg-red-50 border-red-200">
          <div className="flex items-center gap-2 text-red-700"><span className="text-xl">❌</span><p>{error}</p></div>
        </Card>
      )}
      {result && (
        <Card className="bg-green-50 border-green-200">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-green-900">Eligibility Result</h3>
              <span className={`px-3 py-1 rounded-full text-sm font-bold ${result.coverage_active ? 'bg-green-600 text-white' : 'bg-red-600 text-white'}`}>
                {result.coverage_active ? '✅ ACTIVE' : '❌ INACTIVE'}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Copay</p>
                <p className="text-2xl font-black text-green-700">{result.benefits?.copay || result.estimated_cost || '—'}</p>
              </div>
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Deductible</p>
                <p className="text-2xl font-black text-green-700">{result.benefits?.deductible || '—'}</p>
              </div>
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Out-of-Pocket Max</p>
                <p className="text-xl font-bold text-gray-700">{result.benefits?.out_of_pocket_max || '—'}</p>
              </div>
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Prior Auth Required</p>
                <p className="text-xl font-bold {result.requires_prior_auth ? 'text-orange-600' : 'text-green-700'}">
                  {result.requires_prior_auth ? '⚠️ YES' : '✅ NO'}
                </p>
              </div>
            </div>
            {result.message && <p className="text-xs text-gray-500 italic border-t border-green-200 pt-3">{result.message}</p>}
          </div>
        </Card>
      )}
    </div>
  )
}




