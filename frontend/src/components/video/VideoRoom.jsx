/**VideoRoom - Wrapper component for video consultation room*/
import { VideoSDKPlayer } from './VideoSDKPlayer'

export function VideoRoom({
  roomId,
  token,
  participantName,
  onRecordingStopped,
  onJoin,
  onLeave,
  className = ''
}) {
  if (!roomId || !token) {
    return (
      <div className={`p-4 bg-gray-50 border border-gray-200 rounded-lg ${className}`}>
        <p className="text-gray-600 text-center">
          Room ID and token required to join consultation
        </p>
      </div>
    )
  }

  return (
    <div className={`video-room-container ${className}`}>
      <VideoSDKPlayer
        roomId={roomId}
        token={token}
        participantName={participantName}
        onRecordingStopped={onRecordingStopped}
        onJoin={onJoin}
        onLeave={onLeave}
      />
    </div>
  )
}




