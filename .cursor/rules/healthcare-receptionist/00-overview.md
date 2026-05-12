# Healthcare Receptionist Domain - Overview

## Domain Summary

**Healthcare-specific receptionist testing HIPAA-compliant workflows, clinical appointment scheduling, patient intake, insurance verification, and care coordination.**

### Quick Stats
- **Tasks:** 40 (8 intake, 10 scheduling, 8 insurance, 8 triage, 6 orchestration)
- **Target Pass@1:** 35-45% (discriminative)
- **MCP Servers:** 7 (all existing)
- **Standards:** FHIR R4, HL7 v2.x, HIPAA
- **Market:** $4.5T US healthcare

### Key Differentiators
1. **No external APIs** - uses existing MCP servers
2. **Healthcare standards compliance** (FHIR, HL7, HIPAA)
3. **Safety-critical testing** (clinical triage)
4. **Production-ready** (immediate use cases)

## Architecture Components

```
healthcare-receptionist/
├── 00-overview.md (this file)
├── 01-architecture.md (system design)
├── 02-mcp-servers.md (server integrations)
├── 03-fhir-schemas.md (FHIR R4 resource definitions)
├── 04-task-categories.md (40 tasks breakdown)
├── 05-evaluators.md (evaluation logic)
├── 06-hipaa-compliance.md (privacy & security)
├── 07-implementation-guide.md (build steps)
├── 08-api-contracts.md (interfaces & contracts)
└── 09-deployment.md (production deployment)
```

## Development Phases

### Phase 1: Foundation (Week 1-2)
- FHIR schema definitions
- MCP server integrations
- Basic evaluators
- 18 core tasks (intake + scheduling)

### Phase 2: Complex Logic (Week 3-4)
- Insurance authorization logic
- Clinical triage algorithms
- Safety-critical evaluators
- 16 complex tasks (insurance + triage)

### Phase 3: Orchestration (Week 5)
- Multi-channel workflows
- HIPAA compliance validation
- End-to-end care coordination
- 6 orchestration tasks

### Phase 4: Hardening (Week 6)
- Local testing (target 40% pass rate)
- Add hard edge cases if needed
- Documentation & production readiness

## Quick Reference

| Category | Tasks | Pass@1 | Complexity |
|----------|-------|--------|------------|
| Patient Intake | 8 | 65% | Moderate-High |
| Appointment Scheduling | 10 | 50% | High |
| Insurance & Authorization | 8 | 30% | Very High |
| Clinical Triage | 8 | 25% | Extreme |
| Multi-Channel | 6 | 20% | Extreme |
| **Total** | **40** | **40%** | **Very High** |

## Related Documentation
- See `01-architecture.md` for system design
- See `03-fhir-schemas.md` for data models
- See `07-implementation-guide.md` for build instructions

