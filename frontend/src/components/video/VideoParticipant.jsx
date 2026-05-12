/**VideoParticipant - Display a single participant's video stream*/
import { useEffect, useRef } from 'react'

export function VideoParticipant({
  participantId,
  name,
  stream,
  isMicOn = false,
  isCameraOn = false,
  className = ''
}) {
  const videoRef = useRef(null)

  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = new MediaStream([stream.track])
    }
  }, [stream])

  return (
    <div className={`relative bg-gray-900 rounded-lg overflow-hidden ${className}`}>
      {isCameraOn && stream ? (
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted={false}
          className="w-full h-full object-cover"
        />
      ) : (
        <div className="w-full h-64 flex items-center justify-center bg-gray-800">
          <div className="text-center text-white">
            <div className="text-6xl mb-2">👤</div>
            <div className="text-lg font-semibold">{name}</div>
            {!isCameraOn && <div className="text-sm text-gray-400 mt-1">Camera off</div>}
          </div>
        </div>
      )}
      
      {/* Participant info overlay */}
      <div className="absolute bottom-2 left-2 bg-black bg-opacity-60 text-white px-3 py-1 rounded text-sm flex items-center gap-2">
        {isMicOn ? '🎤' : '🔇'} {name}
      </div>
    </div>
  )
}




