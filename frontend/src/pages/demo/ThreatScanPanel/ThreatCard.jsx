import { useState } from 'react'
import { TIER_META, SEV_STYLES } from './constants'

/**
 * Expandable threat card — shows severity, attack class, evidence,
 * attacker technique, CVE reference, mitigation, and Okta rule.
 */
export default function ThreatCard({ threat }) {
    const [open, setOpen] = useState(false)
    const tier = TIER_META[threat.tier] || TIER_META[1]
    const sev = SEV_STYLES[threat.severity] || SEV_STYLES.LOW

    return (
        <div
            className={`rounded-xl border ${sev.border} ${sev.bg} shadow-lg ${sev.glow} cursor-pointer transition-all`}
            onClick={() => setOpen(!open)}
        >
            {/* Header row */}
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

            {/* Expanded details */}
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
                            <p className="text-xs text-gray-500 mb-1">CVE / Reference</p>
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
                            <pre className="text-xs text-gray-400 bg-gray-900/60 rounded p-2 overflow-auto max-h-32">
                                {JSON.stringify(threat.evidence, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
