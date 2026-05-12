/**
 * ThreatScanPanel — Live Attack Detector 🔴
 *
 * Real-time 6-tier threat detection UI. Feed any identity request payload
 * and get instant threat classification, severity, evidence, and mitigation.
 *
 * T1: JWT Algorithm Confusion
 * T2: Session & OAuth Attacks
 * T3: RBAC Privilege Escalation
 * T4: Audit Trail Evasion
 * T5: Data Exfiltration
 * T6: Zero-Day (MFA fatigue, device flow, timing attacks)
 */
import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const TIER_META = {
    1: { label: 'JWT Confusion', icon: '🔑', color: 'violet', bg: 'bg-violet-950/40', border: 'border-violet-500/30', badge: 'bg-violet-500/20 text-violet-300' },
    2: { label: 'Session / OAuth', icon: '🔄', color: 'blue', bg: 'bg-blue-950/40', border: 'border-blue-500/30', badge: 'bg-blue-500/20 text-blue-300' },
    3: { label: 'RBAC Escalation', icon: '👤', color: 'cyan', bg: 'bg-cyan-950/40', border: 'border-cyan-500/30', badge: 'bg-cyan-500/20 text-cyan-300' },
    4: { label: 'Audit Evasion', icon: '📋', color: 'yellow', bg: 'bg-yellow-950/30', border: 'border-yellow-500/30', badge: 'bg-yellow-500/20 text-yellow-300' },
    5: { label: 'Data Exfiltration', icon: '💀', color: 'orange', bg: 'bg-orange-950/30', border: 'border-orange-500/30', badge: 'bg-orange-500/20 text-orange-300' },
    6: { label: 'Zero-Day', icon: '🚨', color: 'red', bg: 'bg-red-950/30', border: 'border-red-500/30', badge: 'bg-red-500/20 text-red-300' },
}

const SEV_STYLES = {
    CRITICAL: { bar: 'bg-red-500', text: 'text-red-300', border: 'border-red-500/40', bg: 'bg-red-950/30', glow: 'shadow-red-500/20' },
    HIGH: { bar: 'bg-orange-500', text: 'text-orange-300', border: 'border-orange-500/40', bg: 'bg-orange-950/20', glow: 'shadow-orange-500/20' },
    MEDIUM: { bar: 'bg-yellow-500', text: 'text-yellow-300', border: 'border-yellow-500/40', bg: 'bg-yellow-950/20', glow: 'shadow-yellow-500/20' },
    LOW: { bar: 'bg-green-500', text: 'text-green-300', border: 'border-green-500/40', bg: 'bg-green-950/20', glow: '' },
}

const ACTION_STYLES = {
    BLOCK_AND_ALERT: { label: '🔴 BLOCK & ALERT', className: 'bg-red-600 text-white' },
    CHALLENGE_AND_LOG: { label: '🟡 CHALLENGE & LOG', className: 'bg-yellow-600 text-white' },
    LOG_AND_MONITOR: { label: '🟠 LOG & MONITOR', className: 'bg-orange-600 text-white' },
    ALLOW: { label: '🟢 ALLOW', className: 'bg-green-700 text-white' },
}

// Pre-built attack scenarios — each one fires a real detection
const ATTACK_SCENARIOS = [
    {
        tier: 1,
        label: 'JWT alg:none bypass',
        description: 'Token with alg:none — no signature required',
        payload: {
            jwt_token: 'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiJ9.'
        }
    },
    {
        tier: 1,
        label: 'RS256 → HS256 confusion',
        description: 'HS256 token when RS256 expected — key confusion attack',
        payload: {
            jwt_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdHRhY2tlciIsInJvbGUiOiJhZG1pbiJ9.fakesignaturefromrsapubkey'
        }
    },
    {
        tier: 2,
        label: 'OAuth refresh token replay',
        description: 'Stolen token replayed from different IP',
        payload: {
            token_id: 'demo_refresh_tok_001',
            ip: '9.8.7.6',
            device_id: 'attacker-device'
        }
    },
    {
        tier: 2,
        label: 'OAuth redirect URI hijack',
        description: 'Redirect to GitHub Pages subdomain (subdomain takeover)',
        payload: {
            redirect_uri: 'https://staging.corp.github.io/oauth/callback',
            registered_domains: ['corp.com', 'app.corp.com']
        }
    },
    {
        tier: 3,
        label: 'IDOR cross-tenant access',
        description: 'Tenant A user accessing Tenant B resources',
        payload: {
            requesting_user_id: 'user_tenant_a',
            requesting_user_tenant: 'tenant_a',
            target_resource_id: 'financial_rec_007',
            target_resource_owner_id: 'user_tenant_b',
            target_resource_tenant: 'tenant_b'
        }
    },
    {
        tier: 3,
        label: 'Mass assignment — role escalation',
        description: 'PATCH request with role:admin field injection',
        payload: {
            submitted_fields: { name: 'Alice', email: 'alice@corp.com', role: 'admin', is_superuser: true, bypass_mfa: true },
            allowed_fields: ['name', 'email']
        }
    },
    {
        tier: 4,
        label: 'CRLF log injection',
        description: 'Username contains CRLF to inject fake audit entries',
        payload: {
            username: 'alice\r\n2024-01-15 [AUDIT] user=root action=DELETE_ALL_USERS success=true\r\n'
        }
    },
    {
        tier: 5,
        label: 'Token scope creep',
        description: 'read:profile token used to access PII data',
        payload: {
            token_scopes: ['read:profile', 'read:reports'],
            requested_resource: 'pii_data',
            requested_action: 'read'
        }
    },
    {
        tier: 5,
        label: 'Credential stuffing — OpenBullet pattern',
        description: 'High-velocity failures across many unique usernames from one IP',
        payload: {
            ip: '45.33.32.156',
            username: 'victim007@corp.com',
            login_success: false
        }
    },
    {
        tier: 6,
        label: 'MFA push fatigue — Uber 2022 pattern',
        description: 'Bombing user with push notifications until accidental approval',
        payload: {
            mfa_push_user_id: 'demo_victim_user'
        }
    },
    {
        tier: 6,
        label: 'Device flow phishing',
        description: 'Polling from attacker IP, approval from victim IP',
        payload: {
            device_code: 'DEMO-DEVICE-CODE-XYZ',
            ip: '1.2.3.4',
            approval_ip: '98.76.54.32'
        }
    },
    {
        tier: 2,
        label: 'Session fixation (SPA)',
        description: 'Token not rotated after login — fixation vulnerability',
        payload: {
            pre_auth_token: 'planted_token_abc123',
            post_auth_token: 'planted_token_abc123',
            storage_origin: 'https://evil-cors-site.com'
        }
    },
]

function ThreatCard({ threat, index }) {
    const [open, setOpen] = useState(false)
    const tier = TIER_META[threat.tier] || TIER_META[1]
    const sev = SEV_STYLES[threat.severity] || SEV_STYLES.LOW

    return (
        <div
            className={`rounded-xl border ${sev.border} ${sev.bg} shadow-lg ${sev.glow} cursor-pointer transition-all`}
            onClick={() => setOpen(!open)}
        >
            <div className="flex items-start gap-3 p-4">
                <div className={`mt-0.5 w-8 h-8 rounded-lg flex items-center justify-center text-sm ${tier.badge} shrink-0`}>
                    {tier.icon}
                </div>
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${sev.border} ${sev.text} ${sev.bg}`}>
                            {threat.severity}
                        </span>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${tier.badge}`}>
                            T{threat.tier}: {tier.label}
                        </span>
                        <span className="text-sm font-semibold text-gray-200">{threat.attack_class}</span>
                    </div>
                    <p className="text-xs text-gray-400 mt-1 leading-relaxed line-clamp-2">
                        {threat.mitigation || threat.attacker_technique || 'Threat detected.'}
                    </p>
                </div>
                <span className="text-gray-600 text-xs shrink-0 mt-1">{open ? '▲' : '▼'}</span>
            </div>

            {open && (
                <div className="px-4 pb-4 space-y-3 border-t border-gray-700/20 pt-3">
                    {threat.attacker_technique && (
                        <div>
                            <p className="text-xs text-gray-500 mb-1 font-medium">🧠 Attacker Technique</p>
                            <p className="text-xs text-gray-300 leading-relaxed">{threat.attacker_technique}</p>
                        </div>
                    )}
                    {threat.cve && (
                        <div className="bg-gray-900/40 rounded px-3 py-2">
                            <p className="text-xs text-gray-500 mb-1">CVE / Incident Reference</p>
                            <p className="text-xs text-yellow-300 font-mono">{threat.cve}</p>
                        </div>
                    )}
                    {threat.incident_ref && (
                        <div className="bg-gray-900/40 rounded px-3 py-2">
                            <p className="text-xs text-gray-500 mb-1">Real-World Incident</p>
                            <p className="text-xs text-orange-300">{threat.incident_ref}</p>
                        </div>
                    )}
                    {threat.mitigation && (
                        <div className={`rounded-lg border ${sev.border} px-3 py-2`}>
                            <p className="text-xs text-gray-500 mb-1 font-medium">🛡️ Mitigation</p>
                            <p className="text-xs text-gray-300">{threat.mitigation}</p>
                        </div>
                    )}
                    {threat.okta_rule && (
                        <div className="bg-blue-950/20 rounded-lg border border-blue-700/20 px-3 py-2">
                            <p className="text-xs text-blue-400 font-medium mb-1">⚙️ Okta Rule</p>
                            <p className="text-xs text-blue-300">{threat.okta_rule}</p>
                        </div>
                    )}
                    {threat.evidence && (
                        <div>
                            <p className="text-xs text-gray-500 mb-1 font-medium">🔍 Evidence</p>
                            <pre className="text-xs text-gray-400 bg-gray-900/60 rounded p-2 overflow-auto max-h-28">
                                {JSON.stringify(threat.evidence, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

function ScenarioButton({ scenario, active, onClick }) {
    const tier = TIER_META[scenario.tier]
    return (
        <button
            onClick={onClick}
            className={`w-full text-left px-3.5 py-2.5 rounded-lg border transition-all ${active
                    ? `${tier.border} ${tier.badge}`
                    : 'border-gray-700/30 text-gray-500 hover:text-gray-300 hover:border-gray-600 bg-gray-900/20'
                }`}
        >
            <div className="flex items-center gap-2">
                <span className="text-sm">{tier.icon}</span>
                <div className="min-w-0">
                    <p className="text-xs font-medium truncate">{scenario.label}</p>
                    <p className="text-xs text-gray-600 truncate">{scenario.description}</p>
                </div>
            </div>
        </button>
    )
}

export default function ThreatScanPanel() {
    const [selectedScenario, setSelectedScenario] = useState(null)
    const [customPayload, setCustomPayload] = useState('')
    const [scanning, setScanning] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)
    const [activeScenarioIdx, setActiveScenarioIdx] = useState(null)

    const handleScenario = (scenario, idx) => {
        setSelectedScenario(scenario)
        setActiveScenarioIdx(idx)
        setCustomPayload(JSON.stringify(scenario.payload, null, 2))
        setResult(null); setError(null)
    }

    const handleScan = async () => {
        setScanning(true); setError(null); setResult(null)
        try {
            let payload
            try { payload = JSON.parse(customPayload) }
            catch { throw new Error('Invalid JSON payload') }

            const res = await fetch(`${API_BASE}/api/v1/identity/threat/scan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || `HTTP ${res.status}`) }
            setResult(await res.json())
        } catch (e) { setError(e.message) } finally { setScanning(false) }
    }

    const sevOrder = { CRITICAL: 4, HIGH: 3, MEDIUM: 2, LOW: 1 }
    const sortedThreats = result?.threats
        ? [...result.threats].sort((a, b) => (sevOrder[b.severity] || 0) - (sevOrder[a.severity] || 0))
        : []

    const tierGroups = Object.keys(TIER_META).map(t => parseInt(t)).map(t => ({
        tier: t,
        threats: sortedThreats.filter(th => th.tier === t)
    })).filter(g => g.threats.length > 0)

    const actionStyle = result ? (ACTION_STYLES[result.recommended_action] || ACTION_STYLES.ALLOW) : null

    return (
        <div className="min-h-screen bg-gray-950 text-white">
            {/* Header */}
            <div className="border-b border-gray-800/60 px-6 py-4 bg-gray-900/40 backdrop-blur sticky top-0 z-10">
                <div className="flex items-center justify-between max-w-7xl mx-auto">
                    <div className="flex items-center gap-3">
                        <span className="text-2xl">🛡️</span>
                        <div>
                            <h1 className="text-xl font-bold tracking-tight">Threat Detection Engine</h1>
                            <p className="text-xs text-gray-400">6-tier real-time scanner · JWT · OAuth · RBAC · Audit · Exfil · Zero-Day</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                        {Object.entries(TIER_META).map(([t, meta]) => (
                            <span key={t} className={`px-2 py-1 rounded-full ${meta.badge} hidden md:inline-flex items-center gap-1`}>
                                {meta.icon} T{t}
                            </span>
                        ))}
                        <a href="/identity" className="ml-2 px-3 py-1.5 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors">
                            🔐 Agent →
                        </a>
                        <a href="/identity/benchmark" className="px-3 py-1.5 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors">
                            📊 Benchmark →
                        </a>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-5 gap-6">

                {/* Left: attack scenario picker */}
                <div className="lg:col-span-2 space-y-3">
                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Attack Scenarios</p>
                    <p className="text-xs text-gray-600">Each scenario simulates a real CVE or incident. Click to load, then scan.</p>
                    <div className="space-y-1.5">
                        {ATTACK_SCENARIOS.map((s, i) => (
                            <ScenarioButton
                                key={i}
                                scenario={s}
                                active={activeScenarioIdx === i}
                                onClick={() => handleScenario(s, i)}
                            />
                        ))}
                    </div>
                </div>

                {/* Right: scanner */}
                <div className="lg:col-span-3 space-y-5">
                    {/* Payload editor */}
                    <div className="rounded-xl border border-gray-700/40 bg-gray-900/40 p-4 space-y-3">
                        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                            Request Payload{selectedScenario ? ` — ${selectedScenario.label}` : ''}
                        </p>
                        <textarea
                            value={customPayload}
                            onChange={e => setCustomPayload(e.target.value)}
                            onKeyDown={e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleScan() }}
                            placeholder={'{\n  "jwt_token": "...",\n  "ip": "...",\n  "username": "..."\n}'}
                            rows={8}
                            spellCheck={false}
                            className="w-full bg-gray-800/60 border border-gray-700/50 rounded-lg px-4 py-3 text-sm text-gray-200 font-mono placeholder-gray-700 resize-none focus:outline-none focus:border-gray-500 transition-colors"
                        />
                        <button
                            onClick={handleScan}
                            disabled={!customPayload.trim() || scanning}
                            className={`w-full py-3 rounded-lg font-semibold text-sm transition-all shadow-lg ${scanning || !customPayload.trim()
                                    ? 'bg-gray-700/50 text-gray-500 cursor-not-allowed'
                                    : 'bg-gradient-to-r from-red-700 to-red-600 text-white hover:opacity-90'
                                }`}
                        >
                            {scanning ? (
                                <span className="flex items-center justify-center gap-2">
                                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                    Scanning all 6 tiers...
                                </span>
                            ) : '🔴 Run Threat Scan →'}
                        </button>
                    </div>

                    {error && (
                        <div className="rounded-xl border border-red-800/40 bg-red-950/20 px-4 py-3 text-sm text-red-300">
                            <span className="font-semibold">Error: </span>{error}
                        </div>
                    )}

                    {/* Results */}
                    {result && (
                        <div className="space-y-4">
                            {/* Summary bar */}
                            <div className={`rounded-xl p-4 flex items-center justify-between gap-4 ${result.clean ? 'bg-green-950/20 border border-green-800/30' : 'bg-red-950/20 border border-red-800/30'
                                }`}>
                                <div>
                                    <p className="font-bold text-lg text-white">
                                        {result.clean ? '✅ No threats detected' : `🚨 ${result.threats_found} threat${result.threats_found > 1 ? 's' : ''} detected`}
                                    </p>
                                    <p className="text-xs text-gray-400 mt-0.5">
                                        Scanned at {new Date(result.scanned_at).toLocaleTimeString()}
                                    </p>
                                </div>
                                {actionStyle && (
                                    <span className={`text-sm font-bold px-4 py-2 rounded-lg shrink-0 ${actionStyle.className}`}>
                                        {actionStyle.label}
                                    </span>
                                )}
                            </div>

                            {/* Threats by tier */}
                            {sortedThreats.length > 0 && (
                                <div className="space-y-3">
                                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                        Threats Found — Sorted by Severity
                                    </p>
                                    {sortedThreats.map((threat, i) => (
                                        <ThreatCard key={i} threat={threat} index={i} />
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {!result && !scanning && !error && (
                        <div className="rounded-xl border border-gray-800 bg-gray-900/20 p-10 text-center space-y-3">
                            <p className="text-4xl">🔴</p>
                            <p className="text-gray-400 font-medium">Select an attack scenario or paste a custom payload</p>
                            <p className="text-gray-600 text-xs">
                                Scanner checks JWT alg, OAuth flows, RBAC, audit integrity, scope, MFA fatigue, and more
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
