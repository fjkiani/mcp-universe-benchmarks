// Features Showcase - Replaces monolithic Features.jsx with specialized components
// Each capability gets its own interactive, visual component
// NEW: Doctor-friendly, benefit-first storytelling components

// Core Product Understanding (New - Priority 1)
import { SaaSExplainer } from './SaaSExplainer'
import { AILayerExplainer } from './AILayerExplainer'
import { BeforeAfterComparison } from './BeforeAfterComparison'

// Enhanced Team & Agent Showcase
import { AITeamShowcase } from './AITeamShowcase'
import { AgentFlowDiagram } from './AgentFlowDiagram'

// Interactive Capability Demos
import { EHRIntegrationShowcase } from './EHRIntegrationShowcase'
import { AppointmentSchedulingDemo } from './AppointmentSchedulingDemo'
import { InsuranceVerificationFlow } from './InsuranceVerificationFlow'
import { TelehealthPlatformShowcase } from './TelehealthPlatformShowcase'
import { TriageAccuracyDisplay } from './TriageAccuracyDisplay'

// Trust & Compliance
import { HIPAAComplianceCenter } from './HIPAAComplianceCenter'
import { TwentyFourSevenCoverage } from './TwentyFourSevenCoverage'

// Technical Details (For technical buyers)
import { MCPServersShowcase } from './MCPServersShowcase'
import { TaskValidationDashboard } from './TaskValidationDashboard'

export function FeaturesShowcase() {
  return (
    <div className="space-y-0">
      {/* PHASE 1: Understand the Product (SaaS First, Then AI) */}
      <SaaSExplainer />
      <AILayerExplainer />
      
      {/* PHASE 2: See the Transformation (Real Stories) */}
      <BeforeAfterComparison />
      
      {/* PHASE 3: Meet Your New Team (Human + AI Partnership) */}
      <AITeamShowcase />
      <AgentFlowDiagram />
      
      {/* PHASE 4: See It In Action (Interactive Demos) */}
      <AppointmentSchedulingDemo />
      <InsuranceVerificationFlow />
      <EHRIntegrationShowcase />
      <TelehealthPlatformShowcase />
      <TriageAccuracyDisplay />
      
      {/* PHASE 5: Trust & Reliability */}
      <HIPAAComplianceCenter />
      <TwentyFourSevenCoverage />
      
      {/* PHASE 6: Technical Details (Progressive Disclosure) */}
      <MCPServersShowcase />
      <TaskValidationDashboard />
    </div>
  )
}
