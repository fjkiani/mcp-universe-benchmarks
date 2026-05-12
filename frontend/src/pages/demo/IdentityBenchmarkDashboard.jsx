/**
 * IdentityBenchmarkDashboard — Security Posture Intelligence 📊
 *
 * Shows: overall pass rate, category drilldown, per-task results,
 * anomaly alerts, and autonomous remediation console.
 */
import { useState, useEffect, useCallback } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const CATEGORY_META = {
    auth: { label: 'Authentication', icon: '🔐', color: 'violet', gradient: 'from-violet-500 to-indigo-500', bg: 'bg-violet-950/30', border: 'border-violet-500/30' },
    rbac: { label: 'Access Control', icon: '👤', color: 'cyan', gradient: 'from-cyan-500 to-teal-500', bg: 'bg-cyan-950/30', border: 'border-cyan-500/30' },
    compliance: { label: 'Compliance', icon: '📋', color: 'emerald', gradient: 'from-emerald-500 to-green-500', bg: 'bg-emerald-950/30', border: 'border-emerald-500/30' }
}

const COMPLEXITY_BADGE = {
    simple: 'bg-gray-700/40 text-gray-400',
    moderate: 'bg-yellow-900/40 text-yellow-400',
    complex: 'bg-orange-900/40 text-orange-400',
    hard: 'bg-red-900/40 text-red-400'
}

function RiskGauge({ score }) {
    const pct = Math.min(100, Math.max(0, score))
    const color = pct < 30 ? '#22c55e' : pct < 60 ? '#eab308' : pct < 80 ? '#f97316' : '#ef4444'
    const label = pct < 30 ? 'LOW' : pct < 60 ? 'MEDIUM' : pct < 80 ? 'HIGH' : 'CRITICAL'
    const circumference = 2 * Math.PI * 36

    return (
        <div className="flex flex-col items-center gap-2">
            <div className="relative w-24 h-24">
                <svg className="w-24 h-24 -rotate-90" viewBox="0 0 88 88">
                    <circle cx="44" cy="44" r="36" fill="none" stroke="#1f2937" strokeWidth="8" />
                    <circle
                        cx="44" cy="44" r="36" fill="none" stroke={color} strokeWidth="8"
                        strokeDasharray={circumference}
                        strokeDashoffset={circumference * (1 - pct / 100)}
                        strokeLinecap="round"
                        style={{ transition: 'stroke-dashoffset 0.8s ease' }}
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-2xl font-bold text-white">{pct}</span>
                    <span className="text-xs text-gray-400">/ 100</span>
                </div>
            </div>
            <span className="text-xs font-bold" style={{ color }}>{label} RISK</span>
        </div>
    )
}

function PassRateBar({ rate, label, color }) {
    const pct = Math.min(100, Math.max(0, rate || 0))
    const barColor = pct >= 70 ? 'bg-green-500' : pct >= 40 ? 'bg-yellow-500' : 'bg-red-500'

    return (
        <div className="space-y-1.5">
            <div className="flex justify-between items-center">
                <span className="text-sm text-gray-300 font-medium">{label}</span>
                <span className={`text-sm font-bold ${pct >= 70 ? 'text-green-400' : pct >= 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {pct}%
                </span>
            </div>
            <div className="w-full bg-gray-800/60 rounded-full h-2.5 overflow-hidden">
                <div
                    className={`h-2.5 rounded-full transition-all duration-700 ${barColor}`}
                    style={{ width: `${pct}%` }}
                />
            </div>
        </div>
    )
}

function TaskResultRow({ result, index }) {
    const [open, setOpen] = useState(false)
    const cat = CATEGORY_META[result.category] || CATEGORY_META.auth

    return (
        <div
            className={`rounded-lg border transition-all cursor-pointer ${result.passed ? 'border-gray-700/40 bg-gray-800/30 hover:bg-gray-800/50' : 'border-red-800/30 bg-red-950/10 hover:bg-red-950/20'}`}
            onClick={() => setOpen(!open)}
        >
            <div className="flex items-center gap-3 px-4 py-3">
                <span className="text-base">{cat.icon}</span>
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                        <span className="text-sm font-mono text-gray-300 truncate">{result.task_id}</span>
                        <span className={`text-xs px-1.5 py-0.5 rounded ${COMPLEXITY_BADGE[result.response?.vertical] || 'bg-gray-700/40 text-gray-400'}`}>
                            {result.category}
                        </span>
                    </div>
                    <p className="text-xs text-gray-500 truncate mt-0.5">{result.reason}</p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                    <span className="text-xs text-gray-600">{result.latency_ms}ms</span>
                    {result.passed
                        ? <span className="text-green-400 text-lg">✓</span>
                        : <span className="text-red-400 text-lg">✗</span>
                    }
                    <span className="text-xs text-gray-600">{open ? '▲' : '▼'}</span>
                </div>
            </div>
            {open && (
                <div className="px-4 pb-3 border-t border-gray-700/20">
                    <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                        {result.response?.risk_level && (
                            <div className="bg-gray-900/50 rounded p-2">
                                <p className="text-gray-500 mb-1">Risk Level</p>
                                <p className="text-gray-300 font-mono">{result.response.risk_level} ({result.response.risk_score}/100)</p>
                            </div>
                        )}
                        {result.response?.auth_status && (
                            <div className="bg-gray-900/50 rounded p-2">
                                <p className="text-gray-500 mb-1">Auth Status</p>
                                <p className="text-gray-300 font-mono">{result.response.auth_status}</p>
                            </div>
                        )}
                        {result.response?.compliance_status && (
                            <div className="bg-gray-900/50 rounded p-2">
                                <p className="text-gray-500 mb-1">Compliance</p>
                                <p className="text-gray-300 font-mono">{result.response.compliance_status}</p>
                            </div>
                        )}
                        {result.response?.access_granted != null && (
                            <div className="bg-gray-900/50 rounded p-2">
                                <p className="text-gray-500 mb-1">Access</p>
                                <p className="text-gray-300 font-mono">{result.response.access_granted ? 'GRANTED' : 'DENIED'}</p>
                            </div>
                        )}
                    </div>
                    {result.response?.remediation_suggested && (
                        <div className="mt-2 bg-blue-950/20 rounded p-2 border border-blue-800/20">
                            <p className="text-xs text-blue-400 font-medium">🔧 Remediation: {result.response.remediation_suggested}</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

function RemediationConsole({ results }) {
    const failures = (results || []).filter(r => !r.passed)
    if (!failures.length) return (
        <div className="rounded-xl border border-green-800/20 bg-green-950/10 p-6 text-center">
            <p className="text-2xl mb-2">✅</p>
            <p className="text-green-400 font-medium">All tests passing</p>
            <p className="text-gray-500 text-xs mt-1">No remediation required</p>
        </div>
    )

    const REMEDIATION_MAP = {
        auth: [
            { icon: '🔒', issue: 'Auth failures detected', action: 'enforce_adaptive_mfa', cmd: 'okta.enableAdaptiveMFA(affectedUsers)', auto: true },
            { icon: '🚨', issue: 'Lockout policy misconfigured', action: 'reset_lockout_policy', cmd: 'okta.updateLockoutPolicy({ threshold: 3, window: 300 })', auto: true }
        ],
        rbac: [
            { icon: '👤', issue: 'RBAC policy gap', action: 'prune_excess_permissions', cmd: 'okta.updateAccessPolicy(userId, minPrivilege)', auto: false },
            { icon: '🕐', issue: 'Time-based controls missing', action: 'add_time_restrictions', cmd: 'okta.applyTimePolicy(roles, BusinessHours)', auto: true }
        ],
        compliance: [
            { icon: '🚨', issue: 'Anomalies in audit trail', action: 'force_session_kill', cmd: 'okta.revokeUserSessions(flaggedUsers)', auto: true },
            { icon: '⚠️', issue: 'GDPR data access without consent', action: 'audit_consent_flags', cmd: 'gdpr.auditConsentFlags(lastNEvents=100)', auto: false }
        ]
    }

    const failedCats = [...new Set(failures.map(f => f.category))]
    const remediations = failedCats.flatMap(c => REMEDIATION_MAP[c] || [])

    return (
        <div className="space-y-3">
            <div className="flex items-center gap-2 mb-4">
                <span className="text-red-400 text-lg">⚠️</span>
                <p className="text-sm font-semibold text-red-300">{failures.length} failing test{failures.length > 1 ? 's' : ''} — remediation available</p>
            </div>
            {remediations.map((r, i) => (
                <div key={i} className={`rounded-lg border p-4 ${r.auto ? 'border-blue-700/30 bg-blue-950/20' : 'border-yellow-700/30 bg-yellow-950/10'}`}>
                    <div className="flex items-start justify-between gap-3">
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <span>{r.icon}</span>
                                <p className="text-sm font-medium text-gray-200">{r.issue}</p>
                                {r.auto && (
                                    <span className="text-xs bg-blue-500/20 text-blue-300 px-1.5 py-0.5 rounded border border-blue-500/20">AUTO-APPLY</span>
                                )}
                            </div>
                            <code className="text-xs text-gray-400 bg-gray-900/50 px-2 py-1 rounded block mt-2">{r.cmd}</code>
                        </div>
                        <button className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-all shrink-0 ${r.auto ? 'bg-blue-600 hover:bg-blue-500 text-white' : 'bg-gray-700 hover:bg-gray-600 text-gray-300'}`}>
                            {r.auto ? '▶ Apply' : '📋 Review'}
                        </button>
                    </div>
                </div>
            ))}
        </div>
    )
}

export default function IdentityBenchmarkDashboard() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [running, setRunning] = useState(false)
    const [activeTab, setActiveTab] = useState('overview')
    const [filterCat, setFilterCat] = useState('all')

    const loadLatest = useCallback(async () => {
        setLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/v1/identity/agent/benchmark/latest`)
            if (res.ok) setData(await res.json())
        } catch (e) { console.error(e) } finally { setLoading(false) }
    }, [])

    const runBenchmark = async () => {
        setRunning(true)
        try {
            const res = await fetch(`${API_BASE}/api/v1/identity/agent/benchmark/run`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({})
            })
            if (res.ok) setData(await res.json())
        } catch (e) { console.error(e) } finally { setRunning(false) }
    }

    useEffect(() => { loadLatest() }, [loadLatest])

    const passRate = data?.pass_rate || 0
    const riskScore = data ? Math.round((1 - passRate / 100) * 100) : 0

    const filteredResults = (data?.results || []).filter(r => filterCat === 'all' || r.category === filterCat)

    return (
        <div className="min-h-screen bg-gray-950 text-white">
            {/* Header */}
            <div className="border-b border-gray-800/60 px-6 py-4 flex items-center justify-between bg-gray-900/40 backdrop-blur sticky top-0 z-10">
                <div className="flex items-center gap-3">
                    <span className="text-2xl">📊</span>
                    <div>
                        <h1 className="text-xl font-bold text-white tracking-tight">Identity Benchmark</h1>
                        <p className="text-xs text-gray-400">Security posture intelligence · Continuous evaluation</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    {data && (
                        <span className="text-xs text-gray-500">
                            Last run: {new Date(data.timestamp).toLocaleTimeString()}
                        </span>
                    )}
                    <button
                        onClick={runBenchmark}
                        disabled={running}
                        className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${running ? 'bg-gray-700 text-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white hover:opacity-90 shadow-lg'
                            }`}
                    >
                        {running ? (
                            <span className="flex items-center gap-2">
                                <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                Running...
                            </span>
                        ) : '▶ Run Benchmark'}
                    </button>
                    <a href="/identity" className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors">
                        🔐 Live Agent →
                    </a>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-6 py-8 space-y-6">
                {loading && !data ? (
                    <div className="flex items-center justify-center h-64">
                        <div className="text-center space-y-3">
                            <div className="w-10 h-10 border-2 border-violet-500/30 border-t-violet-500 rounded-full animate-spin mx-auto" />
                            <p className="text-gray-400 text-sm">Loading benchmark results...</p>
                        </div>
                    </div>
                ) : data ? (
                    <>
                        {/* Top stats */}
                        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
                            {/* Risk gauge */}
                            <div className="col-span-2 lg:col-span-1 flex items-center justify-center bg-gray-900/50 rounded-xl border border-gray-700/40 p-5">
                                <RiskGauge score={riskScore} />
                            </div>

                            {/* Overall pass rate */}
                            <div className="bg-gray-900/50 rounded-xl border border-gray-700/40 p-5 text-center">
                                <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Pass Rate</p>
                                <p className={`text-4xl font-bold ${passRate >= 70 ? 'text-green-400' : passRate >= 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                                    {passRate}%
                                </p>
                                <p className="text-xs text-gray-500 mt-1">{data.passed}/{data.total_tasks} tasks</p>
                            </div>

                            {/* Category cards */}
                            {Object.entries(data.by_category || {}).map(([cat, stats]) => {
                                const meta = CATEGORY_META[cat] || CATEGORY_META.auth
                                return (
                                    <div key={cat} className={`rounded-xl border ${meta.border} ${meta.bg} p-4 text-center`}>
                                        <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{meta.label}</p>
                                        <p className={`text-3xl font-bold ${stats.pass_rate >= 70 ? 'text-green-400' : stats.pass_rate >= 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                                            {stats.pass_rate}%
                                        </p>
                                        <p className="text-xs text-gray-500 mt-1">{stats.passed}/{stats.total}</p>
                                    </div>
                                )
                            })}
                        </div>

                        {/* Risk summary banner */}
                        <div className={`rounded-xl border px-5 py-3 text-sm font-medium ${passRate >= 70 ? 'border-green-800/30 bg-green-950/20 text-green-300'
                                : passRate >= 40 ? 'border-yellow-800/30 bg-yellow-950/20 text-yellow-300'
                                    : 'border-red-800/30 bg-red-950/20 text-red-300'
                            }`}>
                            {data.risk_summary}
                        </div>

                        {/* Pass rate bars */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                            {Object.entries(data.by_category || {}).map(([cat, stats]) => {
                                const meta = CATEGORY_META[cat] || CATEGORY_META.auth
                                return (
                                    <div key={cat} className="bg-gray-900/40 rounded-xl border border-gray-700/30 p-5 space-y-3">
                                        <div className="flex items-center gap-2">
                                            <span className="text-xl">{meta.icon}</span>
                                            <p className="font-semibold text-gray-200">{meta.label}</p>
                                        </div>
                                        <PassRateBar rate={stats.pass_rate} label={`${stats.passed}/${stats.total} tasks`} />
                                        <p className="text-xs text-gray-600">{stats.total - stats.passed} failures need attention</p>
                                    </div>
                                )
                            })}
                        </div>

                        {/* Tab navigation */}
                        <div className="flex items-center gap-1 border-b border-gray-700/30">
                            {['overview', 'results', 'remediation'].map(tab => (
                                <button
                                    key={tab}
                                    onClick={() => setActiveTab(tab)}
                                    className={`px-4 py-2 text-sm font-medium capitalize transition-colors border-b-2 -mb-px ${activeTab === tab
                                            ? 'border-violet-500 text-violet-300'
                                            : 'border-transparent text-gray-500 hover:text-gray-300'
                                        }`}
                                >
                                    {tab === 'overview' ? '📈 Overview' : tab === 'results' ? '📋 Task Results' : '🔧 Remediation'}
                                </button>
                            ))}
                        </div>

                        {/* Tab content */}
                        {activeTab === 'overview' && (
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                <div className="bg-gray-900/40 rounded-xl border border-gray-700/30 p-5">
                                    <h3 className="text-sm font-semibold text-gray-300 mb-4">Benchmark Run Details</h3>
                                    <div className="space-y-2 text-sm">
                                        {[
                                            { label: 'Run ID', value: data.run_id },
                                            { label: 'Timestamp', value: new Date(data.timestamp).toLocaleString() },
                                            { label: 'Total Tasks', value: data.total_tasks },
                                            { label: 'Passed', value: data.passed, c: 'text-green-400' },
                                            { label: 'Failed', value: data.failed, c: 'text-red-400' },
                                            { label: 'Overall Pass Rate', value: `${data.pass_rate}%`, c: passRate >= 70 ? 'text-green-400' : 'text-yellow-400' }
                                        ].map(({ label, value, c = 'text-gray-300' }) => (
                                            <div key={label} className="flex justify-between">
                                                <span className="text-gray-500">{label}</span>
                                                <span className={`font-mono ${c}`}>{value}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                                <div className="bg-gray-900/40 rounded-xl border border-gray-700/30 p-5">
                                    <h3 className="text-sm font-semibold text-gray-300 mb-4">Benchmark Quality Standards</h3>
                                    <div className="space-y-3 text-xs text-gray-400">
                                        {[
                                            { check: passRate >= 30 && passRate <= 70, label: 'Discriminative difficulty (30-70% target)', pass: passRate >= 30 && passRate <= 70 },
                                            { check: data.failed > 0, label: 'No trivially easy tasks (some failures expected)', pass: data.failed > 0 },
                                            { check: data.by_category?.auth?.pass_rate > 0, label: 'Auth evaluation working', pass: data.by_category?.auth?.pass_rate > 0 },
                                            { check: data.by_category?.rbac?.pass_rate > 0, label: 'RBAC engine working', pass: data.by_category?.rbac?.pass_rate > 0 },
                                            { check: data.by_category?.compliance?.pass_rate > 0, label: 'Compliance audit working', pass: data.by_category?.compliance?.pass_rate > 0 }
                                        ].map((item, i) => (
                                            <div key={i} className="flex items-center gap-2">
                                                <span className={item.pass ? 'text-green-400' : 'text-red-400'}>{item.pass ? '✓' : '✗'}</span>
                                                <span className={item.pass ? 'text-gray-300' : 'text-gray-500'}>{item.label}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'results' && (
                            <div className="space-y-3">
                                <div className="flex items-center gap-2">
                                    <p className="text-xs text-gray-500 font-medium">Filter:</p>
                                    {['all', 'auth', 'rbac', 'compliance'].map(cat => (
                                        <button
                                            key={cat}
                                            onClick={() => setFilterCat(cat)}
                                            className={`text-xs px-3 py-1 rounded-full border transition-colors ${filterCat === cat ? 'border-violet-500/60 bg-violet-500/20 text-violet-300' : 'border-gray-700/40 text-gray-500 hover:text-gray-300'
                                                }`}
                                        >
                                            {cat === 'all' ? 'All' : (CATEGORY_META[cat]?.icon + ' ' + CATEGORY_META[cat]?.label)}
                                        </button>
                                    ))}
                                    <span className="text-xs text-gray-600 ml-auto">{filteredResults.length} tasks</span>
                                </div>
                                {filteredResults.map((r, i) => <TaskResultRow key={r.task_id} result={r} index={i} />)}
                            </div>
                        )}

                        {activeTab === 'remediation' && (
                            <RemediationConsole results={data.results} />
                        )}
                    </>
                ) : (
                    <div className="text-center py-16 space-y-4">
                        <p className="text-4xl">🛡️</p>
                        <p className="text-gray-400">No benchmark data yet</p>
                        <button onClick={runBenchmark} className="px-6 py-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-lg text-sm font-semibold text-white hover:opacity-90">
                            Run First Benchmark →
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}
