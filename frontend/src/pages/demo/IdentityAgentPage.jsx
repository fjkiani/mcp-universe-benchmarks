/**
 * IdentityAgentPage — Live Identity Security Agent Demo 🔐
 *
 * Three verticals: MFA Auth | RBAC Check | Compliance Audit
 * Chat input → real identity agent → action trace + risk score + remediation
 */
import { useState, useRef, useEffect } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const VERTICAL_CONFIG = {
    mfa_auth: {
        label: '🔐 MFA Authentication',
        color: 'violet',
        gradient: 'from-violet-600 to-indigo-600',
        cardBg: 'bg-violet-950/40',
        border: 'border-violet-500/30',
        badge: 'bg-violet-500/20 text-violet-300',
        glow: 'shadow-violet-500/20',
        description: 'Multi-factor auth, lockout detection, session management, risk scoring',
        scenarios: [
            {
                label: '✅ Valid user + MFA',
                message: 'User alice@corp.com is authenticating from NYC with valid credentials and correct MFA code.',
                context: { user_id: 'alice_001', credentials_valid: true, mfa_provided: true, failed_attempts: 0, current_location: 'New York' }
            },
            {
                label: '🔒 Account lockout (5 attempts)',
                message: 'User bob@corp.com has failed login 5 times in the last 3 minutes. Evaluate and remediate.',
                context: { user_id: 'bob_002', credentials_valid: false, mfa_provided: false, failed_attempts: 5 }
            },
            {
                label: '🚨 Impossible travel detected',
                message: 'User carol@corp.com authenticated from NYC 8 minutes ago, now attempting login from Tokyo.',
                context: { user_id: 'carol_003', credentials_valid: true, mfa_provided: false, failed_attempts: 0, last_login_location: 'New York', current_location: 'Tokyo' }
            },
            {
                label: '⚠️ MFA required (no code)',
                message: 'User dave@corp.com has correct password but has not provided MFA. What is the auth decision?',
                context: { user_id: 'dave_004', credentials_valid: true, mfa_provided: false, failed_attempts: 0 }
            }
        ]
    },
    rbac_check: {
        label: '👤 RBAC Access Control',
        color: 'cyan',
        gradient: 'from-cyan-600 to-teal-600',
        cardBg: 'bg-cyan-950/40',
        border: 'border-cyan-500/30',
        badge: 'bg-cyan-500/20 text-cyan-300',
        glow: 'shadow-cyan-500/20',
        description: 'Role inheritance, permission evaluation, least-privilege enforcement',
        scenarios: [
            {
                label: '✅ Manager accessing HR data',
                message: 'Manager role user trying to access hr_data. Evaluate via role inheritance.',
                context: { user_id: 'mgr_001', roles: ['manager'], resource: 'hr_data', action: 'read' }
            },
            {
                label: '❌ Employee accessing financials',
                message: 'Employee-level user trying to read financial_records. Should this be blocked?',
                context: { user_id: 'emp_002', roles: ['employee'], resource: 'financial_records', action: 'read' }
            },
            {
                label: '⚠️ Over-permissioned user',
                message: 'User has executive + manager + supervisor + employee roles. Flag over-permissioning.',
                context: { user_id: 'power_003', roles: ['executive', 'manager', 'supervisor', 'employee'], resource: 'financial_records', action: 'admin' }
            },
            {
                label: '🕐 Off-hours access attempt',
                message: 'Supervisor accessing audit_logs at 2:30 AM. Evaluate with time-based policy.',
                context: {
                    user_id: 'sup_004', roles: ['supervisor'], resource: 'audit_logs', action: 'read',
                    time_of_request: new Date(new Date().setHours(2, 30, 0, 0)).toISOString()
                }
            }
        ]
    },
    compliance_audit: {
        label: '📋 Compliance Audit',
        color: 'emerald',
        gradient: 'from-emerald-600 to-green-600',
        cardBg: 'bg-emerald-950/40',
        border: 'border-emerald-500/30',
        badge: 'bg-emerald-500/20 text-emerald-300',
        glow: 'shadow-emerald-500/20',
        description: 'SOC2/GDPR audit trail analysis, anomaly detection, tamper checking',
        scenarios: [
            {
                label: '✅ Clean audit trail',
                message: 'Audit user eve@corp.com login event for SOC2 compliance.',
                context: {
                    user_id: 'eve_001',
                    events: [{ event_id: 'e001', event_type: 'login', timestamp: new Date().toISOString(), location: 'NYC', actor_auth_verified: true, data_classification: 'internal', consent_verified: true }]
                }
            },
            {
                label: '🚨 Impossible travel in logs',
                message: 'Audit user frank@corp.com — NYC login then London data access 3 minutes later.',
                context: {
                    user_id: 'frank_002',
                    events: [
                        { event_id: 'e001', event_type: 'login', timestamp: new Date().toISOString(), location: 'NYC', actor_auth_verified: true, data_classification: 'internal', consent_verified: true },
                        { event_id: 'e002', event_type: 'pii_access', timestamp: new Date(Date.now() + 180000).toISOString(), location: 'London', actor_auth_verified: true, data_classification: 'pii', consent_verified: true }
                    ]
                }
            },
            {
                label: '⚠️ GDPR violation — PII without consent',
                message: 'User grace accessed PII data without consent verification. Audit and flag.',
                context: {
                    user_id: 'grace_003',
                    events: [{ event_id: 'e001', event_type: 'pii_access', timestamp: new Date().toISOString(), location: 'NYC', actor_auth_verified: true, data_classification: 'pii', consent_verified: false }]
                }
            },
            {
                label: '🔴 Audit log tampering detected',
                message: 'Check henry@corp.com audit logs for tampering (duplicate event IDs).',
                context: {
                    user_id: 'henry_004', check_tampering: true,
                    events: [
                        { event_id: 'e001', event_type: 'login', timestamp: new Date().toISOString(), location: 'NYC', actor_auth_verified: true, data_classification: 'internal', consent_verified: true },
                        { event_id: 'e001', event_type: 'data_delete', timestamp: new Date().toISOString(), location: 'NYC', actor_auth_verified: true, data_classification: 'sensitive', consent_verified: true }
                    ]
                }
            }
        ]
    }
}

const TOOL_ICONS = {
    evaluate_authentication: '🔐',
    evaluate_rbac: '🛡️',
    generate_audit_log: '📋',
    apply_remediation: '🔧',
    default: '⚙️'
}

const RISK_STYLES = {
    LOW: 'bg-green-500/20 text-green-300 border border-green-500/40',
    MEDIUM: 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/40',
    HIGH: 'bg-orange-500/20 text-orange-300 border border-orange-500/40',
    CRITICAL: 'bg-red-500/20 text-red-300 border border-red-500/40'
}

const AUTH_STATUS_STYLES = {
    granted: 'bg-green-500/20 text-green-300 border-green-500/40',
    denied: 'bg-red-500/20 text-red-300 border-red-500/40',
    locked: 'bg-red-700/30 text-red-200 border-red-600/40',
    mfa_required: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40'
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
                        {action.latency_ms != null && (
                            <span className="text-xs text-gray-600">{action.latency_ms}ms</span>
                        )}
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

function IdentityResponseCard({ response, vertical }) {
    const config = VERTICAL_CONFIG[vertical]
    if (!response) return null

    return (
        <div className={`rounded-xl border ${config.border} ${config.cardBg} p-5 space-y-4 shadow-lg ${config.glow}`}>
            {/* Risk + Status badges */}
            <div className="flex flex-wrap items-center gap-2">
                {response.risk_level && (
                    <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${RISK_STYLES[response.risk_level] || ''}`}>
                        ⬤ {response.risk_level} RISK {response.risk_score != null ? `(${response.risk_score}/100)` : ''}
                    </span>
                )}
                {response.auth_status && (
                    <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${AUTH_STATUS_STYLES[response.auth_status] || ''}`}>
                        {response.auth_status === 'granted' ? '✅' : response.auth_status === 'locked' ? '🔒' : response.auth_status === 'mfa_required' ? '📱' : '❌'} {response.auth_status.toUpperCase()}
                    </span>
                )}
                {response.access_granted != null && (
                    <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${response.access_granted ? 'bg-green-500/20 text-green-300 border-green-500/40' : 'bg-red-500/20 text-red-300 border-red-500/40'}`}>
                        {response.access_granted ? '✅ ACCESS GRANTED' : '❌ ACCESS DENIED'}
                    </span>
                )}
                {response.compliance_status && (
                    <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${response.compliance_status === 'compliant' ? 'bg-green-500/20 text-green-300 border-green-500/40'
                            : response.compliance_status === 'non_compliant' ? 'bg-red-500/20 text-red-300 border-red-500/40'
                                : 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40'
                        }`}>
                        {response.compliance_status === 'compliant' ? '✅' : response.compliance_status === 'non_compliant' ? '🚨' : '⚠️'} {response.compliance_status.toUpperCase().replace('_', ' ')}
                    </span>
                )}
                {response.anomaly_detected && (
                    <span className="text-xs font-bold px-2.5 py-1 rounded-full border bg-red-700/30 text-red-300 border-red-600/40">
                        🚨 ANOMALY DETECTED
                    </span>
                )}
                {response.remediation_applied && (
                    <span className="text-xs font-bold px-2.5 py-1 rounded-full border bg-blue-500/20 text-blue-300 border-blue-500/40">
                        🔧 AUTO-REMEDIATED
                    </span>
                )}
            </div>

            {/* Agent message */}
            <p className="text-gray-200 leading-relaxed text-sm">{response.message}</p>

            {/* Key identity fields */}
            {(response.session_token || response.applied_roles?.length > 0 || response.remediation_suggested) && (
                <div className="grid grid-cols-1 gap-2 text-sm">
                    {response.session_token && (
                        <div className="bg-gray-800/50 rounded-lg p-3">
                            <p className="text-gray-500 text-xs mb-1">Session Token</p>
                            <p className="text-green-400 font-mono text-xs truncate">{response.session_token}</p>
                            {response.session_expiry && (
                                <p className="text-gray-500 text-xs mt-1">Expires: {new Date(response.session_expiry).toLocaleTimeString()}</p>
                            )}
                        </div>
                    )}
                    {response.applied_roles?.length > 0 && (
                        <div className="bg-gray-800/50 rounded-lg p-3">
                            <p className="text-gray-500 text-xs mb-1">Effective Roles (incl. inheritance)</p>
                            <div className="flex flex-wrap gap-1 mt-1">
                                {response.applied_roles.map(r => (
                                    <span key={r} className="text-xs bg-cyan-900/40 text-cyan-300 px-2 py-0.5 rounded-full border border-cyan-800/30">{r}</span>
                                ))}
                            </div>
                        </div>
                    )}
                    {response.remediation_suggested && (
                        <div className="bg-blue-950/30 rounded-lg p-3 border border-blue-800/30">
                            <p className="text-gray-500 text-xs mb-1">🔧 Suggested Remediation</p>
                            <p className="text-blue-300 text-xs font-mono">{response.remediation_suggested}</p>
                        </div>
                    )}
                </div>
            )}

            <ActionTrace actions={response.actions} />
        </div>
    )
}

export default function IdentityAgentPage() {
    const [vertical, setVertical] = useState('mfa_auth')
    const [message, setMessage] = useState('')
    const [scenarioContext, setScenarioContext] = useState(null)
    const [loading, setLoading] = useState(false)
    const [response, setResponse] = useState(null)
    const [error, setError] = useState(null)
    const [apiHealth, setApiHealth] = useState(null)
    const textareaRef = useRef(null)
    const config = VERTICAL_CONFIG[vertical]

    useEffect(() => {
        fetch(`${API_BASE}/api/v1/identity/agent/health`)
            .then(r => r.json()).then(setApiHealth).catch(() => setApiHealth(null))
    }, [])

    const handleSubmit = async () => {
        if (!message.trim() || loading) return
        setLoading(true); setError(null); setResponse(null)
        try {
            const res = await fetch(`${API_BASE}/api/v1/identity/agent/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message.trim(), vertical, scenario_context: scenarioContext })
            })
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || `HTTP ${res.status}`) }
            setResponse(await res.json())
        } catch (e) { setError(e.message) } finally { setLoading(false) }
    }

    const handleScenario = (s) => {
        setMessage(s.message); setScenarioContext(s.context)
        setResponse(null); setError(null)
        textareaRef.current?.focus()
    }

    return (
        <div className="min-h-screen bg-gray-950 text-white">
            {/* Header */}
            <div className="border-b border-gray-800/60 px-6 py-4 flex items-center justify-between bg-gray-900/40 backdrop-blur">
                <div>
                    <div className="flex items-center gap-3">
                        <span className="text-2xl">🔐</span>
                        <div>
                            <h1 className="text-xl font-bold text-white tracking-tight">Identity Security Agent</h1>
                            <p className="text-xs text-gray-400">Enterprise MFA · RBAC · Compliance · Autonomous Remediation</p>
                        </div>
                    </div>
                </div>
                {apiHealth && (
                    <div className="flex items-center gap-2 text-xs">
                        <span className={`px-2.5 py-1 rounded-full font-medium ${apiHealth.openai_configured ? 'bg-green-500/20 text-green-400' : 'bg-gray-700/40 text-gray-500'}`}>
                            {apiHealth.openai_configured ? '●' : '○'} GPT-4o
                        </span>
                        <span className="px-2.5 py-1 rounded-full font-medium bg-violet-500/20 text-violet-300">
                            {apiHealth.benchmark_tasks} benchmark tasks
                        </span>
                        <a href="/identity/benchmark" className="px-2.5 py-1 rounded-full font-medium bg-gray-700/40 text-gray-300 hover:bg-gray-700 transition-colors">
                            📊 Benchmark →
                        </a>
                    </div>
                )}
            </div>

            <div className="max-w-6xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-5 gap-6">
                {/* Left sidebar */}
                <div className="lg:col-span-2 space-y-5">
                    {/* Vertical tabs */}
                    <div className="space-y-2">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Security Domain</p>
                        {Object.entries(VERTICAL_CONFIG).map(([key, cfg]) => (
                            <button
                                key={key}
                                onClick={() => { setVertical(key); setResponse(null); setError(null); setMessage(''); setScenarioContext(null) }}
                                className={`w-full text-left px-4 py-3.5 rounded-xl border transition-all ${vertical === key
                                        ? `bg-gradient-to-r ${cfg.gradient} text-white border-transparent shadow-lg`
                                        : 'border-gray-700/50 text-gray-400 hover:border-gray-600 hover:text-gray-200 bg-gray-900/40'
                                    }`}
                            >
                                <div className="font-semibold text-sm">{cfg.label}</div>
                                {vertical === key && <div className="text-xs opacity-70 mt-0.5">{cfg.description}</div>}
                            </button>
                        ))}
                    </div>

                    {/* Scenarios */}
                    <div className="space-y-2">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Test Scenarios</p>
                        {config.scenarios.map((s, i) => (
                            <button
                                key={i}
                                onClick={() => handleScenario(s)}
                                className={`w-full text-left text-xs px-3.5 py-2.5 rounded-lg border transition-all leading-relaxed ${message === s.message
                                        ? `${config.border} ${config.badge}`
                                        : 'border-gray-700/30 text-gray-500 hover:text-gray-300 hover:border-gray-600 bg-gray-900/20'
                                    }`}
                            >
                                {s.label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Right panel */}
                <div className="lg:col-span-3 space-y-5">
                    <div className={`rounded-xl border ${config.border} bg-gray-900/50 p-4 space-y-3`}>
                        <div className={`text-xs font-semibold px-2.5 py-1 inline-flex rounded-full ${config.badge}`}>
                            {config.label}
                        </div>
                        <textarea
                            ref={textareaRef}
                            value={message}
                            onChange={e => setMessage(e.target.value)}
                            onKeyDown={e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleSubmit() }}
                            placeholder={`Describe an identity scenario... (⌘+Enter to run)`}
                            rows={4}
                            className="w-full bg-gray-800/50 border border-gray-700/50 rounded-lg px-4 py-3 text-sm text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-gray-500 transition-colors"
                        />
                        {scenarioContext && (
                            <div className="bg-gray-900/60 rounded-lg px-3 py-2 border border-gray-700/30">
                                <p className="text-xs text-gray-500 mb-1">Scenario Context (auto-populated)</p>
                                <pre className="text-xs text-gray-500 overflow-auto max-h-16">{JSON.stringify(scenarioContext, null, 2)}</pre>
                            </div>
                        )}
                        <button
                            onClick={handleSubmit}
                            disabled={!message.trim() || loading}
                            className={`w-full py-3 rounded-lg font-semibold text-sm transition-all shadow-lg ${loading || !message.trim()
                                    ? 'bg-gray-700/50 text-gray-500 cursor-not-allowed'
                                    : `bg-gradient-to-r ${config.gradient} text-white hover:opacity-90`
                                }`}
                        >
                            {loading ? (
                                <span className="flex items-center justify-center gap-2">
                                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                    Agent processing...
                                </span>
                            ) : 'Run Identity Agent →'}
                        </button>
                    </div>

                    {error && (
                        <div className="rounded-xl border border-red-800/40 bg-red-950/20 px-4 py-3 text-sm text-red-300">
                            <span className="font-semibold">Error: </span>{error}
                        </div>
                    )}

                    {response && <IdentityResponseCard response={response} vertical={vertical} />}

                    {!loading && !response && !error && (
                        <div className="rounded-xl border border-gray-800 bg-gray-900/20 p-8 text-center space-y-3">
                            <p className="text-3xl">🛡️</p>
                            <p className="text-gray-400 text-sm font-medium">Select a scenario or describe an identity situation</p>
                            <p className="text-gray-600 text-xs">The agent evaluates auth, RBAC, and compliance — then suggests auto-remediation</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
