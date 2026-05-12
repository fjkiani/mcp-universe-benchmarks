import { Suspense, lazy } from 'react'
import { Routes, Route } from 'react-router-dom'

// Lazy load all route components for code splitting and faster initial load
const HealthcareReceptionistLanding = lazy(() => import('./domains/healthcare-receptionist/LandingPage'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Servers = lazy(() => import('./pages/Servers'))
const Tasks = lazy(() => import('./pages/Tasks'))
const Showcase = lazy(() => import('./pages/Showcase'))
const HomePage = lazy(() => import('./pages/HomePage'))
const ProductPage = lazy(() => import('./pages/ProductPage'))
const HowItWorksPage = lazy(() => import('./pages/HowItWorksPage'))
const CapabilitiesPage = lazy(() => import('./pages/CapabilitiesPage'))
const HealthcareDemoPage = lazy(() => import('./pages/demo/HealthcareDemoPage'))
const AgentHubPage = lazy(() => import('./pages/demo/AgentHubPage'))
const IdentityAgentPage = lazy(() => import('./pages/demo/IdentityAgentPage'))
const IdentityBenchmarkDashboard = lazy(() => import('./pages/demo/IdentityBenchmarkDashboard'))
const ThreatScanPanel = lazy(() => import('./pages/demo/ThreatScanPanel/index'))
const SaaSHubPage = lazy(() => import('./pages/demo/SaaSHubPage'))


// Loading fallback component
function LoadingFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <div className="text-gray-600">Loading...</div>
      </div>
    </div>
  )
}

function App() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <Routes>
        {/* Universal SaaS Portal — The 'Whole SaaS' Hub as the primary entry point */}
        <Route path="/" element={<SaaSHubPage />} />

        {/* Original infinite scroll landing page (accessible via /landing) */}
        <Route path="/landing" element={<HealthcareReceptionistLanding />} />
        <Route path="/healthcare-receptionist" element={<HealthcareReceptionistLanding />} />

        {/* Multi-page structure (available as alternative routes) */}
        <Route path="/focused-home" element={<HomePage />} />
        <Route path="/product" element={<ProductPage />} />
        <Route path="/how-it-works" element={<HowItWorksPage />} />
        <Route path="/capabilities" element={<CapabilitiesPage />} />

        {/* Production Demo - Real end-to-end workflows */}
        <Route path="/demo" element={<HealthcareDemoPage />} />

        {/* AI Agent Hub - Psychiatric Telehealth + Dental (real agent, not static forms) */}
        <Route path="/demo/agent" element={<AgentHubPage />} />

        {/* Universal SaaS Portal — The 'Whole SaaS' Hub */}
        <Route path="/portal" element={<SaaSHubPage />} />

        {/* Identity Security Agent — MFA, RBAC, Compliance */}
        <Route path="/identity" element={<IdentityAgentPage />} />
        <Route path="/identity/benchmark" element={<IdentityBenchmarkDashboard />} />
        <Route path="/identity/threats" element={<ThreatScanPanel />} />

        {/* Dashboard and admin pages */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/servers" element={<Servers />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/showcase" element={<Showcase />} />
      </Routes>
    </Suspense>
  )
}

export default App


