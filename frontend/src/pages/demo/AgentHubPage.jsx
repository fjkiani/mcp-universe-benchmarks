/**
 * AgentHubPage — Healthcare AI Receptionist Demo 🏥
 *
 * Two verticals: Psychiatric Telehealth | Dental
 * Chat input → real agent → NexHealth + VideoSDK + Twilio + AssemblyAI
 * Action trace shows every tool call the agent made
 */
import { useState, useRef, useEffect } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const VERTICAL_CONFIG = {
    psychiatric_telehealth: {
        label: '🧠 Psychiatric Telehealth',
        color: 'indigo',
        gradient: 'from-indigo-600 to-purple-600',
        cardBg: 'bg-indigo-950/50',
        border: 'border-indigo-500/30',
        badge: 'bg-indigo-500/20 text-indigo-300',
        scenarios: [
            "I've been struggling with severe anxiety and panic attacks for months. I'd like to speak with a psychiatrist via video.",
            "I think I need help. I've been feeling really hopeless and having dark thoughts.",
            "I need ADHD medication management — looking for a psychiatrist who does telehealth.",
            "I've been diagnosed with bipolar disorder and need a new psychiatrist after moving here."
        ]
    },
    dental: {
        label: '🦷 Dental Office',
        color: 'teal',
        gradient: 'from-teal-600 to-emerald-600',
        cardBg: 'bg-teal-950/50',
        border: 'border-teal-500/30',
        badge: 'bg-teal-500/20 text-teal-300',
        scenarios: [
            "I have a severe toothache that's been throbbing for 2 days. It's waking me up at night.",
            "I need to schedule my 6-month cleaning and checkup. My insurance just renewed.",
            "I broke a tooth on something hard yesterday. There's a sharp edge I can feel.",
            "I lost a crown and need to get it re-cemented as soon as possible."
        ]
    }
}

const TOOL_ICONS = {
    triage_patient: '🔍',
    check_provider_availability: '📅',
    book_appointment: '✅',
    create_telehealth_room: '📹',
    send_confirmation_sms: '📱',
    default: '⚙️'
}

const URGENCY_STYLES = {
    EMERGENT: 'bg-red-500/20 text-red-300 border border-red-500/40',
    URGENT: 'bg-orange-500/20 text-orange-300 border border-orange-500/40',
    ROUTINE: 'bg-green-500/20 text-green-300 border border-green-500/40'
}

function ActionTrace({ actions }) {
    const [expanded, setExpanded] = useState(null)
    if (!actions?.length) return null

    return (
        <div className="mt-4 space-y-2">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Agent Trace</p>
            {actions.map((action, i) => (
                <div
                    key={i}
                    className={`rounded-lg border transition-all cursor-pointer ${action.success ? 'border-gray-700/50 bg-gray-800/40' : 'border-red-800/40 bg-red-950/20'
                        }`}
                    onClick={() => setExpanded(expanded === i ? null : i)}
                >
                    <div className="flex items-center gap-2 px-3 py-2">
                        <span className="text-base">{TOOL_ICONS[action.tool] || TOOL_ICONS.default}</span>
                        <span className="text-sm font-mono text-gray-300 flex-1">{action.tool}</span>
                        {action.success
                            ? <span className="text-xs text-green-400">✓</span>
                            : <span className="text-xs text-red-400">✗</span>
                        }
                        <span className="text-xs text-gray-600">{expanded === i ? '▲' : '▼'}</span>
                    </div>
                    {expanded === i && (
                        <div className="px-3 pb-3 space-y-2 border-t border-gray-700/30">
                            <div className="mt-2">
                                <p className="text-xs text-gray-500 mb-1">Args</p>
                                <pre className="text-xs text-gray-400 bg-gray-900/60 rounded p-2 overflow-auto max-h-24">
                                    {JSON.stringify(action.args, null, 2)}
                                </pre>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 mb-1">Result</p>
                                <pre className="text-xs text-gray-400 bg-gray-900/60 rounded p-2 overflow-auto max-h-32">
                                    {JSON.stringify(action.result, null, 2)}
                                </pre>
                            </div>
                        </div>
                    )}
                </div>
            ))}
        </div>
    )
}

function AgentResponseCard({ response, vertical, onJoinVideo }) {
    const config = VERTICAL_CONFIG[vertical]
    if (!response) return null

    return (
        <div className={`rounded-xl border ${config.border} ${config.cardBg} p-5 space-y-4`}>
            {/* Urgency badge */}
            {response.urgency && (
                <div className="flex items-center gap-2">
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${URGENCY_STYLES[response.urgency] || ''}`}>
                        {response.urgency}
                    </span>
                    {response.booking_confirmed && (
                        <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-green-500/20 text-green-300 border border-green-500/40">
                            ✅ Booked
                        </span>
                    )}
                    {response.sms_sent && (
                        <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/40">
                            📱 SMS Sent
                        </span>
                    )}
                </div>
            )}

            {/* Agent message */}
            <p className="text-gray-200 leading-relaxed">{response.message}</p>

            {/* Appointment details */}
            {response.appointment_id && (
                <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="bg-gray-800/50 rounded-lg p-3">
                        <p className="text-gray-500 text-xs mb-1">Appointment ID</p>
                        <p className="text-gray-200 font-mono text-xs">{response.appointment_id}</p>
                    </div>
                    {response.video_patient_link && (
                        <div className="bg-indigo-900/30 rounded-lg p-3 flex flex-col justify-between">
                            <p className="text-gray-500 text-xs mb-1">Telehealth Room</p>
                            <button
                                onClick={() => setActiveVideoUrl(response.video_patient_link)}
                                className="text-white hover:text-indigo-200 text-xs font-bold bg-indigo-600 hover:bg-indigo-500 rounded py-1.5 px-3 transition-colors text-center w-full"
                            >
                                Enter Session 📹
                            </button>
                        </div>
                    )}
                </div>
            )}

            {/* Action trace */}
            <ActionTrace actions={response.actions} />
        </div>
    )
}

export default function AgentHubPage() {
    const [vertical, setVertical] = useState('psychiatric_telehealth')
    const [message, setMessage] = useState('')
    const [loading, setLoading] = useState(false)
    const [response, setResponse] = useState(null)
    const [error, setError] = useState(null)
    const [apiHealth, setApiHealth] = useState(null)
    const [activeVideoUrl, setActiveVideoUrl] = useState(null)
    const textareaRef = useRef(null)

    const config = VERTICAL_CONFIG[vertical]

    // Check API health on mount
    useEffect(() => {
        fetch(`${API_BASE}/api/v1/agent/health`)
            .then(r => r.json())
            .then(data => setApiHealth(data))
            .catch(() => setApiHealth(null))
    }, [])

    const handleSubmit = async () => {
        if (!message.trim() || loading) return
        setLoading(true)
        setError(null)
        setResponse(null)

        try {
            const res = await fetch(`${API_BASE}/api/v1/agent/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message.trim(),
                    vertical,
                    patient_id: 'DEMO-' + Math.random().toString(36).slice(2, 8).toUpperCase(),
                    patient_phone: '+15551234567',
                    patient_name: 'Demo Patient'
                })
            })

            if (!res.ok) {
                const err = await res.json().catch(() => ({}))
                throw new Error(err.detail || `HTTP ${res.status}`)
            }

            const data = await res.json()
            setResponse(data)
        } catch (e) {
            setError(e.message)
        } finally {
            setLoading(false)
        }
    }

    const handleScenario = (text) => {
        setMessage(text)
        setResponse(null)
        setError(null)
        textareaRef.current?.focus()
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
            handleSubmit()
        }
    }

    return (
        <div className="min-h-screen bg-gray-950 text-white">
            {/* Header */}
            <div className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
                <div>
                    <h1 className="text-xl font-bold text-white">Healthcare AI Receptionist</h1>
                    <p className="text-sm text-gray-400">Real workflows. Real APIs. Not a static demo.</p>
                </div>

                {/* API Health */}
                {apiHealth && (
                    <div className="flex items-center gap-2 text-xs">
                        {[
                            { key: 'nexhealth_configured', label: 'NexHealth' },
                            { key: 'videosdk_configured', label: 'VideoSDK' },
                            { key: 'twilio_configured', label: 'Twilio' },
                            { key: 'openai_configured', label: 'OpenAI' },
                        ].map(({ key, label }) => (
                            <span
                                key={key}
                                className={`px-2 py-0.5 rounded-full ${apiHealth[key]
                                    ? 'bg-green-500/20 text-green-400'
                                    : 'bg-gray-700/40 text-gray-500'
                                    }`}
                            >
                                {apiHealth[key] ? '●' : '○'} {label}
                            </span>
                        ))}
                        {apiHealth.mock_mode && (
                            <span className="px-2 py-0.5 rounded-full bg-yellow-500/20 text-yellow-400">
                                ⚠ Mock Mode
                            </span>
                        )}
                    </div>
                )}
            </div>

            <div className="max-w-5xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-5 gap-6">

                {/* Left: Vertical selector + scenarios */}
                <div className="lg:col-span-2 space-y-5">
                    {/* Vertical tabs */}
                    <div className="space-y-2">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Select Vertical</p>
                        {Object.entries(VERTICAL_CONFIG).map(([key, cfg]) => (
                            <button
                                key={key}
                                onClick={() => { setVertical(key); setResponse(null); setError(null); setMessage('') }}
                                className={`w-full text-left px-4 py-3 rounded-xl border transition-all font-medium text-sm ${vertical === key
                                    ? `bg-gradient-to-r ${cfg.gradient} text-white border-transparent shadow-lg`
                                    : 'border-gray-700/50 text-gray-400 hover:border-gray-600 hover:text-gray-200 bg-gray-900/40'
                                    }`}
                            >
                                {cfg.label}
                            </button>
                        ))}
                    </div>

                    {/* Pre-loaded scenarios */}
                    <div className="space-y-2">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Quick Scenarios</p>
                        {config.scenarios.map((scenario, i) => (
                            <button
                                key={i}
                                onClick={() => handleScenario(scenario)}
                                className={`w-full text-left text-xs px-3 py-2.5 rounded-lg border transition-all leading-relaxed ${message === scenario
                                    ? `${config.border} ${config.badge}`
                                    : 'border-gray-700/30 text-gray-500 hover:text-gray-300 hover:border-gray-600 bg-gray-900/20'
                                    }`}
                            >
                                {scenario.slice(0, 80)}...
                            </button>
                        ))}
                    </div>
                </div>

                {/* Right: Chat input + response OR Video Room */}
                <div className="lg:col-span-3 space-y-5">

                    {activeVideoUrl ? (
                        <div className="rounded-xl border border-indigo-500/50 bg-gray-900 overflow-hidden shadow-2xl flex flex-col h-[600px]">
                            <div className="bg-gray-800 border-b border-gray-700 px-4 py-3 flex items-center justify-between">
                                <span className="text-sm font-bold text-white flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                                    Live Telehealth Session
                                </span>
                                <button
                                    onClick={() => setActiveVideoUrl(null)}
                                    className="text-xs font-semibold px-3 py-1 bg-gray-700 hover:bg-red-600 text-white rounded transition-colors"
                                >
                                    End Call
                                </button>
                            </div>
                            <iframe
                                src={activeVideoUrl}
                                allow="camera; microphone; fullscreen; speaker; display-capture"
                                className="w-full flex-1 border-none"
                                title="VideoSDK Room"
                            />
                        </div>
                    ) : (
                        <>
                            {/* Input area */}
                            <div className={`rounded-xl border ${config.border} bg-gray-900/50 p-4 space-y-3`}>
                                <div className="flex items-center gap-2 mb-1">
                                    <div className={`text-xs font-semibold px-2 py-0.5 rounded-full ${config.badge}`}>
                                        {config.label}
                                    </div>
                                </div>

                                <textarea
                                    ref={textareaRef}
                                    value={message}
                                    onChange={e => setMessage(e.target.value)}
                                    onKeyDown={handleKeyDown}
                                    placeholder={
                                        vertical === 'psychiatric_telehealth'
                                            ? "Describe what your patient is experiencing... (⌘+Enter to send)"
                                            : "Describe the dental issue or what the patient needs... (⌘+Enter to send)"
                                    }
                                    rows={4}
                                    className="w-full bg-gray-800/50 border border-gray-700/50 rounded-lg px-4 py-3 text-sm text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-gray-500 transition-colors"
                                />

                                <button
                                    onClick={handleSubmit}
                                    disabled={!message.trim() || loading}
                                    className={`w-full py-3 rounded-lg font-semibold text-sm transition-all ${loading || !message.trim()
                                        ? 'bg-gray-700/50 text-gray-500 cursor-not-allowed'
                                        : `bg-gradient-to-r ${config.gradient} text-white hover:opacity-90 shadow-lg`
                                        }`}
                                >
                                    {loading ? (
                                        <span className="flex items-center justify-center gap-2">
                                            <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                            Agent running...
                                        </span>
                                    ) : (
                                        'Run Agent →'
                                    )}
                                </button>
                            </div>

                            {/* Error */}
                            {error && (
                                <div className="rounded-xl border border-red-800/40 bg-red-950/20 px-4 py-3 text-sm text-red-300">
                                    <span className="font-semibold">Error: </span>{error}
                                </div>
                            )}

                            {/* Response */}
                            {response && (
                                <AgentResponseCard
                                    response={response}
                                    vertical={vertical}
                                    onJoinVideo={setActiveVideoUrl}
                                />
                            )}

                            {/* Empty state */}
                            {!loading && !response && !error && (
                                <div className="rounded-xl border border-gray-800 bg-gray-900/20 p-8 text-center space-y-2">
                                    <p className="text-2xl">🏥</p>
                                    <p className="text-gray-400 text-sm">Select a scenario or type a patient request</p>
                                    <p className="text-gray-600 text-xs">The agent will triage, find a provider, book, and send SMS in real-time</p>
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}
