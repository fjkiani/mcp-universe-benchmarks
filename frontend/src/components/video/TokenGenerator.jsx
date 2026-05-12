/**TokenGenerator - Handle token generation for video participants*/
import { useState } from 'react'
import { Button } from '../common/Button'
import { Card } from '../common/Card'

const API_BASE = 'http://localhost:8000'

export function TokenGenerator({
  roomId,
  participantName,
  role = 'participant',
  onTokenGenerated,
  label = 'Generate Token',
  className = ''
}) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    if (!roomId) {
      setError('Room ID is required')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/api/v1/video/generate-token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: roomId,
          participant_name: participantName,
          participant_role: role
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate token')
      }

      const data = await response.json()
      onTokenGenerated(data.token, data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={className}>
      {error && (
        <div className="mb-2 text-red-600 text-sm">{error}</div>
      )}
      <Button
        onClick={handleGenerate}
        disabled={loading || !roomId}
        variant="primary"
      >
        {loading ? 'Generating...' : label}
      </Button>
    </div>
  )
}




