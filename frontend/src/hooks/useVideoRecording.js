/**useVideoRecording - Hook for managing video recording state*/
import { useState } from 'react'

const API_BASE = 'http://localhost:8000'

export function useVideoRecording(roomId) {
  const [recordingId, setRecordingId] = useState(null)
  const [isRecording, setIsRecording] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const startRecording = async () => {
    if (!roomId) {
      setError('Room ID is required')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/api/v1/video/recordings/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ room_id: roomId })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to start recording')
      }

      const data = await response.json()
      setRecordingId(data.recording_id)
      setIsRecording(true)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const stopRecording = async () => {
    if (!roomId || !recordingId) {
      setError('Room ID and recording ID are required')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/api/v1/video/recordings/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: roomId,
          recording_id: recordingId
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to stop recording')
      }

      const data = await response.json()
      setIsRecording(false)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    recordingId,
    isRecording,
    loading,
    error,
    startRecording,
    stopRecording
  }
}

