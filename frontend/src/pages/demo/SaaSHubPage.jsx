import { useNavigate } from 'react-router-dom'
import { Navbar } from '../../components/layout/Navbar'

export default function SaaSHubPage() {
    const navigate = useNavigate()

    const PILLARS = [
        {
            id: 'agent',
            title: 'Reception Intelligence',
            description: 'Autonomous AI agents handling psychiatric triage, dental scheduling, and patient intake.',
            icon: '🧠',
            path: '/demo/agent',
            status: 'Live',
            metrics: [
                { label: 'Uptime', value: '99.9%' },
                { label: 'Booking Rate', value: '82%' }
            ],
            color: 'blue'
        },
        {
            id: 'identity',
            title: 'Identity Audit Engine',
            description: 'MFA enforcement, RBAC anomaly detection, and continuous compliance monitoring.',
            icon: '🛡️',
            path: '/identity/benchmark',
            status: 'Active',
            metrics: [
                { label: 'Threats Blocked', value: '1.2k' },
                { label: 'Risk Score', value: '12/100' }
            ],
            color: 'purple'
        },
        {
            id: 'ops',
            title: 'Revenue & Operations',
            description: 'High-level business intelligence, operational metrics, and server health tracking.',
            icon: '📈',
            path: '/dashboard',
            status: 'Live',
            metrics: [
                { label: 'Savings', value: '$12k/mo' },
                { label: 'Efficiency', value: '+340%' }
            ],
            color: 'emerald'
        }
    ]

    return (
        <div className="min-h-screen bg-gray-950 text-white font-sans selection:bg-blue-500/30">
            <Navbar />

            {/* Background Glows */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-900/20 blur-[120px] rounded-full" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-900/20 blur-[120px] rounded-full" />
            </div>

            <main className="relative pt-32 pb-20 px-6 max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-16 text-center lg:text-left">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold mb-6 tracking-widest uppercase">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                        </span>
                        Connected Zeta Hub
                    </div>
                    <h1 className="text-5xl lg:text-7xl font-bold mb-6 tracking-tight bg-gradient-to-r from-white via-white to-gray-500 bg-clip-text text-transparent">
                        The Whole SaaS. <br />
                        <span className="text-gray-600">Unified.</span>
                    </h1>
                    <p className="text-xl text-gray-400 max-w-2xl leading-relaxed">
                        Alpha command center for Receptionist Intelligence, Identity Security, and Operational Intelligence. No drift. No academic framing. Just results.
                    </p>
                </div>

                {/* Pillars Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                    {PILLARS.map((p) => (
                        <div
                            key={p.id}
                            onClick={() => navigate(p.path)}
                            className="group relative p-8 rounded-3xl bg-gray-900/40 border border-gray-800 hover:border-gray-700 transition-all cursor-pointer backdrop-blur-xl hover:translate-y-[-4px] overflow-hidden"
                        >
                            {/* Pillar Glow */}
                            <div className={`absolute top-0 right-0 w-32 h-32 bg-${p.color}-500/5 blur-[60px] group-hover:bg-${p.color}-500/10 transition-all`} />

                            <div className="relative z-10">
                                <div className="flex justify-between items-start mb-6">
                                    <span className="text-4xl grayscale group-hover:grayscale-0 transition-all">{p.icon}</span>
                                    <div className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-widest border border-${p.color}-500/30 text-${p.color}-400 bg-${p.color}-500/5`}>
                                        {p.status}
                                    </div>
                                </div>

                                <h3 className="text-2xl font-bold mb-3 text-white group-hover:text-blue-400 transition-colors uppercase tracking-tight">{p.title}</h3>
                                <p className="text-gray-500 text-sm leading-relaxed mb-8">
                                    {p.description}
                                </p>

                                <div className="grid grid-cols-2 gap-4 border-t border-gray-800 pt-6">
                                    {p.metrics.map(m => (
                                        <div key={m.label}>
                                            <p className="text-[10px] text-gray-600 uppercase font-bold tracking-widest mb-1">{m.label}</p>
                                            <p className="text-lg font-mono text-gray-300 group-hover:text-white transition-colors">{m.value}</p>
                                        </div>
                                    ))}
                                </div>

                                <div className="mt-8 flex items-center text-xs font-bold text-gray-400 uppercase tracking-widest group-hover:text-blue-400 transition-colors">
                                    Open Portal <span className="ml-2 group-hover:ml-4 transition-all">→</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* System Health Strip */}
                <div className="p-4 rounded-2xl bg-gray-900/20 border border-gray-800/50 flex flex-wrap items-center justify-between gap-6 text-xs font-mono text-gray-600">
                    <div className="flex items-center gap-4">
                        <span className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]" />
                            Main.py API: 8001
                        </span>
                        <span className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]" />
                            Vite Frontend: 5173
                        </span>
                        <span className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]" />
                            GPT-4o Intelligence Active
                        </span>
                    </div>
                    <div className="uppercase tracking-[0.2em]">
                        Zeta Protocol v2.5.0-ALPHA
                    </div>
                </div>
            </main>
        </div>
    )
}
