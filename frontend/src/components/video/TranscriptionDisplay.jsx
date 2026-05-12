/**TranscriptionDisplay - Display transcription and medical entities*/
import { Card } from '../common/Card'
import { Badge } from '../common/Badge'

export function TranscriptionDisplay({
  transcription,
  medicalEntities,
  confidence,
  loading = false,
  className = ''
}) {
  if (loading) {
    return (
      <Card className={className}>
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Transcribing audio...</p>
        </div>
      </Card>
    )
  }

  if (!transcription) {
    return null
  }

  return (
    <Card className={className}>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Transcription Results</h3>
          {confidence && (
            <Badge status="success">
              {Math.round(confidence * 100)}% Confidence
            </Badge>
          )}
        </div>

        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
            {transcription}
          </p>
        </div>

        {medicalEntities && Object.keys(medicalEntities).length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">Medical Entities</h4>
            <div className="space-y-2">
              {Object.entries(medicalEntities).map(([key, values]) => {
                if (!values || values.length === 0) return null
                return (
                  <div key={key} className="flex items-start gap-2">
                    <span className="font-medium text-gray-700 capitalize min-w-[100px]">
                      {key.replace(/_/g, ' ')}:
                    </span>
                    <div className="flex flex-wrap gap-2">
                      {Array.isArray(values) ? (
                        values.map((value, idx) => (
                          <Badge key={idx} status="info">
                            {value}
                          </Badge>
                        ))
                      ) : (
                        <Badge status="info">{String(values)}</Badge>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </Card>
  )
}

