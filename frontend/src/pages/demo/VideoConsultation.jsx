/**VideoConsultation - Complete telehealth session with embedded player and auto-transcription*/
import { useState } from 'react'
import { Card } from '../../components/common/Card'
import { VideoRoom, TokenGenerator, TranscriptionDisplay } from '../../components/video'
import { ENDPOINTS, API_BASE } from '../../api/config'

export default function VideoConsultation() {
  // Room creation state
  const [formData, setFormData] = useState({
    patientId: 'PT-001',
    providerId: 'dr_kim_101',
    appointmentId: 'APPT-85936'
  })
  const [roomData, setRoomData] = useState(null)
  const [roomLoading, setRoomLoading] = useState(false)
  const [roomError, setRoomError] = useState(null)

  // Token state
  const [patientToken, setPatientToken] = useState(null)
  const [providerToken, setProviderToken] = useState(null)

  // Recording state
  const [recordingId, setRecordingId] = useState(null)

  // Transcription state
  const [transcription, setTranscription] = useState(null)
  const [transcriptionLoading, setTranscriptionLoading] = useState(false)

  // Create video room
  const handleCreateRoom = async (e) => {
    e.preventDefault()
    setRoomLoading(true)
    setRoomError(null)
    setRoomData(null)
    setPatientToken(null)
    setProviderToken(null)
    setTranscription(null)

    try {
      const response = await fetch(ENDPOINTS.createVideoRoom, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to create video room')
      }

      const data = await response.json()
      setRoomData(data)
    } catch (err) {
      setRoomError(err.message)
    } finally {
      setRoomLoading(false)
    }
  }

  // Handle token generation
  const handleTokenGenerated = (token, data) => {
    // This will be called by TokenGenerator component
    return token
  }

  // Handle recording stopped - auto-transcribe
  const handleRecordingStopped = async (recordingUrl, stoppedRecordingId) => {
    if (!roomData || !stoppedRecordingId) return

    setTranscriptionLoading(true)
    try {
      const response = await fetch(`${API_BASE}/api/v1/video/transcribe-recording`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: roomData.room_id,
          recording_id: stoppedRecordingId
        })
      })

      if (!response.ok) {
        throw new Error('Failed to transcribe recording')
      }

      const data = await response.json()
      setTranscription(data)
    } catch (err) {
      console.error('Transcription error:', err)
    } finally {
      setTranscriptionLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Video Consultation</h2>
        <p className="text-gray-600">Create VideoSDK room for telehealth consultation with embedded player and auto-transcription</p>
      </div>

      {/* Room Creation Form */}
      <Card>
        <form onSubmit={handleCreateRoom} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Patient ID *</label>
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
              <label className="block text-sm font-semibold text-gray-700 mb-2">Provider ID *</label>
              <input
                type="text"
                value={formData.providerId}
                onChange={(e) => setFormData({ ...formData, providerId: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="dr_smith"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-semibold text-gray-700 mb-2">Appointment ID (optional)</label>
              <input
                type="text"
                value={formData.appointmentId}
                onChange={(e) => setFormData({ ...formData, appointmentId: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="appt_xxx"
              />
            </div>
          </div>
          <button
            type="submit"
            disabled={roomLoading}
            className="w-full px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50"
          >
            {roomLoading ? 'Creating Room...' : 'Create Video Room'}
          </button>
        </form>
      </Card>

      {/* Error Display */}
      {roomError && (
        <Card className="bg-red-50 border-red-200">
          <div className="text-red-700">❌ {roomError}</div>
        </Card>
      )}

      {/* Video Consultation Session */}
      {roomData && roomData.success && (
        <div className="space-y-6">
          <Card className="bg-green-50 border-green-200">
            <div className="text-green-800">
              <p className="font-semibold mb-2">✅ Room Created Successfully!</p>
              <p className="text-sm">Room ID: {roomData.room_id}</p>
            </div>
          </Card>

          {/* Patient View */}
          <Card>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-gray-900">Patient View</h3>
                {!patientToken && (
                  <TokenGenerator
                    roomId={roomData.room_id}
                    participantName="Patient"
                    role="participant"
                    onTokenGenerated={(token) => setPatientToken(token)}
                    label="Join as Patient"
                  />
                )}
              </div>
              {patientToken ? (
                <VideoRoom
                  roomId={roomData.room_id}
                  token={patientToken}
                  participantName="Patient"
                  onRecordingStopped={handleRecordingStopped}
                />
              ) : (
                <div className="p-8 bg-gray-50 rounded-lg text-center text-gray-600">
                  Click "Join as Patient" to start video consultation
                </div>
              )}
            </div>
          </Card>

          {/* Provider View */}
          <Card>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-gray-900">Provider View</h3>
                {!providerToken && (
                  <TokenGenerator
                    roomId={roomData.room_id}
                    participantName="Dr. Smith"
                    role="moderator"
                    onTokenGenerated={(token) => setProviderToken(token)}
                    label="Join as Provider"
                  />
                )}
              </div>
              {providerToken ? (
                <VideoRoom
                  roomId={roomData.room_id}
                  token={providerToken}
                  participantName="Dr. Smith"
                  onRecordingStopped={handleRecordingStopped}
                />
              ) : (
                <div className="p-8 bg-gray-50 rounded-lg text-center text-gray-600">
                  Click "Join as Provider" to start video consultation
                </div>
              )}
            </div>
          </Card>

          {/* Transcription Results */}
          <TranscriptionDisplay
            transcription={transcription?.transcription}
            medicalEntities={transcription?.medical_entities}
            confidence={transcription?.confidence}
            loading={transcriptionLoading}
          />
        </div>
      )}
    </div>
  )
}
