import { TIER_META } from './constants'

/**
 * Scenario selector button — shows tier icon, label, and description.
 * Highlights when active.
 */
export default function ScenarioButton({ scenario, active, onClick }) {
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
                <span className="text-sm shrink-0">{tier.icon}</span>
                <div className="min-w-0">
                    <p className="text-xs font-medium truncate">{scenario.label}</p>
                    <p className="text-xs text-gray-600 truncate">{scenario.description}</p>
                </div>
            </div>
        </button>
    )
}
