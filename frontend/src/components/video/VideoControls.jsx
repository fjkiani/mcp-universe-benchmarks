/**VideoControls - Modular control buttons for video consultation*/
import { Button } from '../common/Button'

export function VideoControls({
  isMicOn,
  isCameraOn,
  isRecording,
  onToggleMic,
  onToggleCamera,
  onStartRecording,
  onStopRecording,
  onLeave,
  className = ''
}) {
  return (
    <div className={`flex gap-2 flex-wrap ${className}`}>
      <Button
        onClick={onToggleMic}
        variant={isMicOn ? 'primary' : 'secondary'}
        className="flex items-center gap-2"
      >
        <span>{isMicOn ? '🎤' : '🔇'}</span>
        <span>{isMicOn ? 'Mic On' : 'Mic Off'}</span>
      </Button>
      
      <Button
        onClick={onToggleCamera}
        variant={isCameraOn ? 'primary' : 'secondary'}
        className="flex items-center gap-2"
      >
        <span>{isCameraOn ? '📹' : '📷'}</span>
        <span>{isCameraOn ? 'Camera On' : 'Camera Off'}</span>
      </Button>
      
      {isRecording ? (
        <Button
          onClick={onStopRecording}
          variant="danger"
          className="flex items-center gap-2"
        >
          <span>⏹️</span>
          <span>Stop Recording</span>
        </Button>
      ) : (
        <Button
          onClick={onStartRecording}
          variant="primary"
          className="flex items-center gap-2"
        >
          <span>🔴</span>
          <span>Start Recording</span>
        </Button>
      )}
      
      <Button
        onClick={onLeave}
        variant="secondary"
        className="flex items-center gap-2"
      >
        <span>🚪</span>
        <span>Leave</span>
      </Button>
    </div>
  )
}

