/** Display metadata for each threat tier */
export const TIER_META = {
    1: { label: 'JWT Confusion', icon: '🔑', badge: 'bg-violet-500/20 text-violet-300', border: 'border-violet-500/30' },
    2: { label: 'Session / OAuth', icon: '🔄', badge: 'bg-blue-500/20 text-blue-300', border: 'border-blue-500/30' },
    3: { label: 'RBAC Escalation', icon: '👤', badge: 'bg-cyan-500/20 text-cyan-300', border: 'border-cyan-500/30' },
    4: { label: 'Audit Evasion', icon: '📋', badge: 'bg-yellow-500/20 text-yellow-300', border: 'border-yellow-500/30' },
    5: { label: 'Data Exfiltration', icon: '💀', badge: 'bg-orange-500/20 text-orange-300', border: 'border-orange-500/30' },
    6: { label: 'Zero-Day', icon: '🚨', badge: 'bg-red-500/20 text-red-300', border: 'border-red-500/30' },
}

/** Severity → Tailwind styles */
export const SEV_STYLES = {
    CRITICAL: { bar: 'bg-red-500', text: 'text-red-300', border: 'border-red-500/40', bg: 'bg-red-950/30', glow: 'shadow-red-500/20' },
    HIGH: { bar: 'bg-orange-500', text: 'text-orange-300', border: 'border-orange-500/40', bg: 'bg-orange-950/20', glow: 'shadow-orange-500/20' },
    MEDIUM: { bar: 'bg-yellow-500', text: 'text-yellow-300', border: 'border-yellow-500/40', bg: 'bg-yellow-950/20', glow: '' },
    LOW: { bar: 'bg-green-500', text: 'text-green-300', border: 'border-green-500/40', bg: 'bg-green-950/20', glow: '' },
}

/** Recommended action → label + style */
export const ACTION_STYLES = {
    BLOCK_AND_ALERT: { label: '🔴 BLOCK & ALERT', className: 'bg-red-600 text-white' },
    CHALLENGE_AND_LOG: { label: '🟡 CHALLENGE & LOG', className: 'bg-yellow-600 text-white' },
    LOG_AND_MONITOR: { label: '🟠 LOG & MONITOR', className: 'bg-orange-600 text-white' },
    ALLOW: { label: '🟢 ALLOW', className: 'bg-green-700 text-white' },
}
