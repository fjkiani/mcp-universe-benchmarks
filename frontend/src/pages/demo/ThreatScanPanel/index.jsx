/**
 * ThreatScanPanel — Live 6-tier attack detector
 *
 * Composed from:
 *  - constants.js     → tier metadata, severity + action styles
 *  - scenarios.js     → 12 pre-built CVE-mapped attack scenarios
 *  - ThreatCard.jsx   → expandable threat card with evidence drilldown
 *  - ScenarioButton.jsx → scenario picker with active state
 */
import { useState } from 'react'
import { TIER_META, SEV_STYLES, ACTION_STYLES } from './constants'
import { ATTACK_SCENARIOS } from './scenarios'
import ThreatCard from './ThreatCard'
import ScenarioButton from './ScenarioButton'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const SEV_ORDER = { CRITICAL: 4, HIGH: 3, MEDIUM: 2, LOW: 1 }

export default function ThreatScanPanel() {
    const [customPayload, setCustomPayload] = useState('')
    const [selectedScenario, setSelectedScenario] = useState(null)
    const [activeScenarioIdx, setActiveScenarioIdx] = useState(null)
    const [scanning, setScanning] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleScenario = (scenario, idx) => {
        setSelectedScenario(scenario)
        setActiveScenarioIdx(idx)
        setCustomPayload(JSON.stringify(scenario.payload, null, 2))
        setResult(null)
        setError(null)
    }

    const handleScan = async () => {
        setScanning(true); setError(null); setResult(null)
        try {
            let payload
            try { payload = JSON.parse(customPayload) }
            catch { throw new Error('Invalid JSON — check the payload editor') }

            const res = await fetch(`${API_BASE}/api/v1/identity/threat/scan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            if (!res.ok) {
                const e = await res.json().catch(() => ({}))
                throw new Error(e.detail || `HTTP ${res.status}`)
            }
            setResult(await res.json())
        } catch (e) {
            setError(e.message)
        } finally {
            setScanning(false)
        }
    }

    // Sort threats by severity descending
    const sortedThreats = result?.threats
        ? [...result.threats].sort((a, b) => (SEV_ORDER[b.severity] || 0) - (SEV_ORDER[a.severity] || 0))
        : []

    const actionStyle = result ? (ACTION_STYLES[result.recommended_action] || ACTION_STYLES.ALLOW) : null

    return (
        <div className="min-h-screen bg-gray-950 text-white">

            {/* ── Header ──────────────────────────────────────────────────────── */}
            <div className="border-b border-gray-800/60 px-6 py-4 bg-gray-900/40 backdrop-blur sticky top-0 z-10">
                <div className="flex items-center justify-between max-w-7xl mx-auto">
                    <div className="flex items-center gap-3">
                        <span className="text-2xl">🛡️</span>
                        <div>
                            <h1 className="text-xl font-bold tracking-tight">Threat Detection Engine</h1>
                            <p className="text-xs text-gray-400">
                                6-tier scanner · JWT · OAuth · RBAC · Audit · Exfil · Zero-Day
                            </p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2 text-xs flex-wrap">
                        {Object.entries(TIER_META).map(([t, meta]) => (
                            <span key={t} className={`px-2 py-1 rounded-full ${meta.badge} hidden lg:inline-flex items-center gap-1`}>
                                {meta.icon} T{t}
                            </span>
                        ))}
                        <a href="/identity" className="ml-2 px-3 py-1.5 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors">
                            🔐 Agent
                        </a>
                        <a href="/identity/benchmark" className="px-3 py-1.5 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors">
                            📊 Benchmark
                        </a>
                    </div>
                </div>
            </div>

            {/* ── Body ────────────────────────────────────────────────────────── */}
            <div className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-5 gap-6">

                {/* Scenario picker */}
                <div className="lg:col-span-2 space-y-3">
                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Attack Scenarios</p>
                    <p className="text-xs text-gray-600">Each scenario maps to a real CVE or breach. Click → load → scan.</p>
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

                {/* Scanner panel */}
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
                                    : 'bg-gradient-to-r from-red-700 to-red-600 text-white hover:opacity-90 active:scale-95'
                                }`}
                        >
                            {scanning ? (
                                <span className="flex items-center justify-center gap-2">
                                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                    Scanning 6 tiers...
                                </span>
                            ) : '🔴 Run Threat Scan  ⌘↵'}
                        </button>
                    </div>

                    {/* Error */}
                    {error && (
                        <div className="rounded-xl border border-red-800/40 bg-red-950/20 px-4 py-3 text-sm text-red-300">
                            <span className="font-semibold">Error: </span>{error}
                        </div>
                    )}

                    {/* Results */}
                    {result && (
                        <div className="space-y-4">
                            {/* Summary */}
                            <div className={`rounded-xl p-4 flex items-center justify-between gap-4 ${result.clean
                                    ? 'bg-green-950/20 border border-green-800/30'
                                    : 'bg-red-950/20 border border-red-800/30'
                                }`}>
                                <div>
                                    <p className="font-bold text-lg text-white">
                                        {result.clean
                                            ? '✅ No threats detected'
                                            : `🚨 ${result.threats_found} threat${result.threats_found > 1 ? 's' : ''} detected`}
                                    </p>
                                    <p className="text-xs text-gray-400 mt-0.5">
                                        {new Date(result.scanned_at).toLocaleTimeString()}
                                    </p>
                                </div>
                                {actionStyle && (
                                    <span className={`text-sm font-bold px-4 py-2 rounded-lg shrink-0 ${actionStyle.className}`}>
                                        {actionStyle.label}
                                    </span>
                                )}
                            </div>

                            {/* Threat cards */}
                            {sortedThreats.length > 0 && (
                                <div className="space-y-3">
                                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                        Threats — sorted by severity
                                    </p>
                                    {sortedThreats.map((threat, i) => (
                                        <ThreatCard key={i} threat={threat} />
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {/* Empty state */}
                    {!result && !scanning && !error && (
                        <div className="rounded-xl border border-gray-800 bg-gray-900/20 p-10 text-center space-y-3">
                            <p className="text-4xl">🔴</p>
                            <p className="text-gray-400 font-medium">Select an attack scenario or paste a custom payload</p>
                            <p className="text-gray-600 text-xs">
                                Checks JWT alg, OAuth flows, RBAC ownership, audit integrity, token scope, MFA fatigue, and more
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
