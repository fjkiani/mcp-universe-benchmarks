// Before/After Comparison - Day in the life of office staff
// Interactive timeline showing transformation
// Tangible, relatable scenarios

import { useState } from 'react'
import { Card } from '../common/Card'

const STAFF_SCENARIOS = [
  {
    id: 'sarah',
    name: 'Sarah',
    role: 'Front Desk Receptionist',
    avatar: '👩‍💼',
    before: {
      title: "Sarah's Day Before",
      subtitle: 'Overwhelmed and reactive',
      timeline: [
        { time: '8:00 AM', task: 'Arrives, already 15 voicemails waiting', mood: '😰', type: 'stressful' },
        { time: '8:30 AM', task: 'Returns calls while phone keeps ringing', mood: '📞', type: 'chaotic' },
        { time: '10:00 AM', task: 'Still on hold with insurance company', mood: '⏱️', type: 'waste' },
        { time: '12:00 PM', task: 'Rushes through lunch at desk', mood: '🥪', type: 'stressful' },
        { time: '2:00 PM', task: 'Manually entering appointments into EHR', mood: '⌨️', type: 'tedious' },
        { time: '4:00 PM', task: 'Dealing with scheduling conflicts from errors', mood: '😓', type: 'stressful' },
        { time: '5:30 PM', task: 'Leaves exhausted, tasks still incomplete', mood: '😔', type: 'stressful' }
      ],
      stats: {
        calls: '20 calls handled',
        appts: '15 appointments booked',
        errors: '3-4 scheduling errors',
        satisfaction: 'Burned out'
      }
    },
    after: {
      title: "Sarah's Day With AI Assistant",
      subtitle: 'Focused and proactive',
      timeline: [
        { time: '8:00 AM', task: 'Reviews overnight activity (AI handled all messages)', mood: '☕', type: 'relaxed' },
        { time: '8:30 AM', task: 'Focuses on complex patient cases', mood: '💬', type: 'productive' },
        { time: '10:00 AM', task: 'Builds relationships with patients in person', mood: '🤝', type: 'fulfilling' },
        { time: '12:00 PM', task: 'Actual lunch break away from desk', mood: '🍽️', type: 'relaxed' },
        { time: '2:00 PM', task: 'Coordinates care for complex cases', mood: '📋', type: 'productive' },
        { time: '4:00 PM', task: 'Training new staff member', mood: '👥', type: 'fulfilling' },
        { time: '5:00 PM', task: 'Leaves on time, everything complete', mood: '😊', type: 'satisfied' }
      ],
      stats: {
        calls: '100 calls handled (by AI)',
        appts: '240 appointments booked (by AI)',
        errors: '0 scheduling errors',
        satisfaction: 'Energized and fulfilled'
      }
    }
  },
  {
    id: 'mike',
    name: 'Mike',
    role: 'Scheduling Coordinator',
    avatar: '📅',
    before: {
      title: "Mike's Day Before",
      subtitle: 'Constant phone calls and manual entry',
      timeline: [
        { time: '8:00 AM', task: 'Opens multiple systems to start scheduling', mood: '💻', type: 'tedious' },
        { time: '9:00 AM', task: 'Manually checking provider schedules', mood: '🔍', type: 'tedious' },
        { time: '11:00 AM', task: 'Booking appointments one at a time (12 min each)', mood: '📞', type: 'slow' },
        { time: '1:00 PM', task: 'Fixing double-bookings from this morning', mood: '😣', type: 'stressful' },
        { time: '3:00 PM', task: 'Sending confirmation emails manually', mood: '📧', type: 'tedious' },
        { time: '5:00 PM', task: 'Only completed 10 appointments today', mood: '😞', type: 'frustrated' }
      ],
      stats: {
        appts: '10 appointments/day',
        time: '12 minutes per appointment',
        errors: '2-3 conflicts/day',
        satisfaction: 'Frustrated by pace'
      }
    },
    after: {
      title: "Mike's Day With AI Assistant",
      subtitle: 'Strategic scheduling coordinator',
      timeline: [
        { time: '8:00 AM', task: 'Reviews AI-booked appointments (500+ done overnight)', mood: '📊', type: 'productive' },
        { time: '9:00 AM', task: 'Optimizes provider schedules for efficiency', mood: '⚙️', type: 'strategic' },
        { time: '11:00 AM', task: 'Handles VIP and complex scheduling requests', mood: '⭐', type: 'fulfilling' },
        { time: '1:00 PM', task: 'Analyzing patterns to improve wait times', mood: '📈', type: 'strategic' },
        { time: '3:00 PM', task: "Planning next month's provider schedules", mood: '📅', type: 'productive' },
        { time: '4:30 PM', task: 'Everything on track, no backlog', mood: '✅', type: 'satisfied' }
      ],
      stats: {
        appts: '2,400 appointments/day (by AI)',
        time: '3 seconds per appointment',
        errors: '0 conflicts',
        satisfaction: 'Empowered and strategic'
      }
    }
  },
  {
    id: 'lisa',
    name: 'Lisa',
    role: 'Insurance Verification Specialist',
    avatar: '💳',
    before: {
      title: "Lisa's Day Before",
      subtitle: 'On hold with insurance all day',
      timeline: [
        { time: '8:00 AM', task: 'Stack of 30 verifications to complete', mood: '📚', type: 'overwhelmed' },
        { time: '8:15 AM', task: 'First call: on hold for 18 minutes', mood: '⏱️', type: 'waste' },
        { time: '10:00 AM', task: 'Only verified 4 patients so far', mood: '😓', type: 'slow' },
        { time: '12:00 PM', task: 'Working through lunch to catch up', mood: '🥪', type: 'stressful' },
        { time: '3:00 PM', task: 'Still on hold, getting disconnected', mood: '😤', type: 'frustrating' },
        { time: '5:30 PM', task: 'Only completed 12 out of 30', mood: '😞', type: 'incomplete' }
      ],
      stats: {
        verifications: '12 per day',
        time: '15 minutes per check',
        holds: '2+ hours on hold',
        satisfaction: 'Exhausted and behind'
      }
    },
    after: {
      title: "Lisa's Day With AI Assistant",
      subtitle: 'Complex case specialist',
      timeline: [
        { time: '8:00 AM', task: 'Reviews 500+ verifications completed by AI', mood: '☕', type: 'relaxed' },
        { time: '9:00 AM', task: 'Focuses on complex prior authorizations', mood: '🔍', type: 'productive' },
        { time: '11:00 AM', task: 'Calls only cases that need human expertise', mood: '📞', type: 'strategic' },
        { time: '1:00 PM', task: 'Actual lunch break', mood: '🍽️', type: 'relaxed' },
        { time: '2:00 PM', task: 'Training team on new insurance policies', mood: '👥', type: 'fulfilling' },
        { time: '4:00 PM', task: 'All verifications complete, ahead of schedule', mood: '✅', type: 'accomplished' }
      ],
      stats: {
        verifications: '5,000+ per day (by AI)',
        time: '2 seconds per check',
        holds: '0 minutes on hold',
        satisfaction: 'Empowered expert'
      }
    }
  }
]

export function BeforeAfterComparison() {
  const [selectedStaff, setSelectedStaff] = useState(STAFF_SCENARIOS[0])
  const [viewMode, setViewMode] = useState('before') // 'before' or 'after'

  const timeline = viewMode === 'before' ? selectedStaff.before : selectedStaff.after

  return (
    <section className="py-20 px-4 bg-gradient-to-br from-gray-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 mb-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium">
            <span className="mr-2">📅</span>
            A Day in Your Office
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            See the <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Real Transformation</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your staff doesn&apos;t work harder—they work smarter. Here&apos;s what a typical day looks like before and after.
          </p>
        </div>

        {/* Staff Selector */}
        <div className="flex justify-center gap-4 mb-8">
          {STAFF_SCENARIOS.map((staff) => (
            <button
              key={staff.id}
              onClick={() => setSelectedStaff(staff)}
              className={`flex flex-col items-center gap-2 p-4 rounded-lg transition-all ${
                selectedStaff.id === staff.id
                  ? 'bg-blue-100 ring-2 ring-blue-500 shadow-lg'
                  : 'bg-white hover:bg-gray-50 border-2 border-gray-200'
              }`}
            >
              <div className="text-4xl">{staff.avatar}</div>
              <div>
                <div className={`text-sm font-bold ${
                  selectedStaff.id === staff.id ? 'text-blue-900' : 'text-gray-900'
                }`}>
                  {staff.name}
                </div>
                <div className="text-xs text-gray-600">{staff.role}</div>
              </div>
            </button>
          ))}
        </div>

        {/* Before/After Toggle */}
        <div className="flex items-center justify-center gap-4 mb-12">
          <button
            onClick={() => setViewMode('before')}
            className={`px-8 py-4 rounded-lg font-semibold transition-all ${
              viewMode === 'before'
                ? 'bg-red-500 text-white shadow-lg scale-105'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            😰 Before (Without AI)
          </button>
          
          <div className="text-2xl">→</div>

          <button
            onClick={() => setViewMode('after')}
            className={`px-8 py-4 rounded-lg font-semibold transition-all ${
              viewMode === 'after'
                ? 'bg-green-500 text-white shadow-lg scale-105'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            😊 After (With AI)
          </button>
        </div>

        {/* Timeline */}
        <Card className={`${
          viewMode === 'before' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'
        } border-2 mb-8`}>
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-3">{selectedStaff.avatar}</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">{timeline.title}</h3>
            <p className={`text-lg font-medium ${
              viewMode === 'before' ? 'text-red-700' : 'text-green-700'
            }`}>
              {timeline.subtitle}
            </p>
          </div>

          {/* Timeline */}
          <div className="space-y-4 mb-8">
            {timeline.timeline.map((event, idx) => (
              <div
                key={idx}
                className={`flex items-start gap-4 p-4 rounded-lg transition-all ${
                  event.type === 'stressful' ? 'bg-red-100 border-l-4 border-red-400' :
                  event.type === 'tedious' ? 'bg-orange-100 border-l-4 border-orange-400' :
                  event.type === 'waste' ? 'bg-gray-200 border-l-4 border-gray-400' :
                  event.type === 'productive' ? 'bg-green-100 border-l-4 border-green-400' :
                  event.type === 'fulfilling' ? 'bg-blue-100 border-l-4 border-blue-400' :
                  event.type === 'strategic' ? 'bg-purple-100 border-l-4 border-purple-400' :
                  event.type === 'relaxed' ? 'bg-teal-100 border-l-4 border-teal-400' :
                  'bg-white border-l-4 border-gray-300'
                }`}
              >
                <div className="flex-shrink-0 w-20 text-sm font-semibold text-gray-700">
                  {event.time}
                </div>
                <div className="flex-grow">
                  <p className="text-gray-900 font-medium">{event.task}</p>
                </div>
                <div className="flex-shrink-0 text-2xl">{event.mood}</div>
              </div>
            ))}
          </div>

          {/* Stats Summary */}
          <div className={`grid grid-cols-2 md:grid-cols-4 gap-4 p-6 rounded-lg ${
            viewMode === 'before' ? 'bg-red-100' : 'bg-green-100'
          }`}>
            {Object.entries(timeline.stats).map(([key, value]) => (
              <div key={key} className="text-center">
                <div className={`text-2xl font-bold ${
                  viewMode === 'before' ? 'text-red-700' : 'text-green-700'
                }`}>
                  {value}
                </div>
                <div className="text-xs text-gray-600 mt-1 capitalize">
                  {key.replace(/([A-Z])/g, ' $1').trim()}
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Summary */}
        <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0 max-w-4xl mx-auto">
          <div className="text-center">
            <div className="text-4xl mb-4">✨</div>
            <h3 className="text-2xl font-bold mb-4">The Difference Is Clear</h3>
            <p className="text-lg opacity-90 leading-relaxed">
              Your staff spends less time on repetitive tasks and more time doing what they love—helping patients. Same great team, dramatically better day.
            </p>
          </div>
        </Card>
      </div>
    </section>
  )
}


