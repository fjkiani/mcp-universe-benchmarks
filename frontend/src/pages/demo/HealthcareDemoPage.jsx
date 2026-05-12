// Healthcare Production Demo - Main navigation page
// Real end-to-end workflows using MCP servers

import { useState } from 'react'
import { Navbar } from '../../components/layout/Navbar'
import PatientIntakeForm from './PatientIntakeForm'
import AppointmentBooking from './AppointmentBooking'
import InsuranceVerification from './InsuranceVerification'
import ClinicalTriage from './ClinicalTriage'
import HipaaSMS from './HipaaSMS'
import VideoConsultation from './VideoConsultation'
import MedicalTranscription from './MedicalTranscription'

const DEMO_FEATURES = [
  { id: 'patient-intake', name: 'Patient Intake', icon: '👤', component: PatientIntakeForm },
  { id: 'appointment', name: 'Appointment Booking', icon: '📅', component: AppointmentBooking },
  { id: 'insurance', name: 'Insurance Verification', icon: '💳', component: InsuranceVerification },
  { id: 'triage', name: 'Clinical Triage', icon: '🚨', component: ClinicalTriage },
  { id: 'sms', name: 'HIPAA SMS', icon: '💬', component: HipaaSMS },
  { id: 'video', name: 'Video Consultation', icon: '📹', component: VideoConsultation },
  { id: 'transcribe', name: 'Medical Transcription', icon: '🎤', component: MedicalTranscription },
]

export default function HealthcareDemoPage() {
  const [activeFeature, setActiveFeature] = useState('patient-intake')
  
  const ActiveComponent = DEMO_FEATURES.find(f => f.id === activeFeature)?.component || PatientIntakeForm

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      {/* Header */}
      <section className="pt-24 pb-8 px-4 bg-gradient-to-br from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Healthcare Receptionist - Live Production Demo
            </h1>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Real end-to-end workflows using MCP servers. Each feature performs actual operations, not mocks.
            </p>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <section className="bg-white border-b border-gray-200 sticky top-16 z-40">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex overflow-x-auto gap-2 py-4">
            {DEMO_FEATURES.map((feature) => (
              <button
                key={feature.id}
                onClick={() => setActiveFeature(feature.id)}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold whitespace-nowrap transition-all ${
                  activeFeature === feature.id
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <span className="text-xl">{feature.icon}</span>
                <span>{feature.name}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Active Feature Component */}
      <section className="py-12 px-4">
        <div className="max-w-5xl mx-auto">
          <ActiveComponent />
        </div>
      </section>

      {/* Footer Info */}
      <section className="py-8 px-4 bg-gray-100 border-t border-gray-200">
        <div className="max-w-7xl mx-auto text-center text-sm text-gray-600">
          <p>
            <strong>Note:</strong> This is a production demo using real MCP servers. 
            All operations are live and will create actual records in connected systems.
          </p>
        </div>
      </section>
    </div>
  )
}




