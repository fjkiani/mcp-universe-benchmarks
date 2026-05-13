"""
ZOA Skill Contracts — defines the input/output schemas and tool lists
for each ZOA agent. Used by the L1-L4 benchmark runner to test each
agent before deployment.
"""

from typing import Any

ZOA_SKILL_CONTRACTS: dict[str, dict[str, Any]] = {
    "zoa-billing-agent": {
        "skill_id": "zoa-billing-agent",
        "skill_name": "ZOA Billing Agent",
        "skill_description": (
            "Invoice Reaver — processes invoices via multimodal OCR, auto-generates "
            "payment follow-ups, detects fraud via pattern analysis, and generates "
            "structured invoice JSON from contracts."
        ),
        "skill_category": "Finance",
        "primary_llm_role": "vision",
        "fallback_llm_role": "reasoning",
        "input_schema": {
            "type": "object",
            "properties": {
                "invoice_data": {
                    "type": "object",
                    "description": "Raw invoice data including vendor, line items, amounts, dates",
                    "properties": {
                        "vendor": {"type": "string"},
                        "line_items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {"type": "string"},
                                    "quantity": {"type": "number"},
                                    "unit_price": {"type": "number"},
                                    "total": {"type": "number"},
                                },
                            },
                        },
                        "total_amount": {"type": "number"},
                        "currency": {"type": "string"},
                        "due_date": {"type": "string", "format": "date"},
                    },
                    "required": ["vendor", "line_items", "total_amount"],
                }
            },
            "required": ["invoice_data"],
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "invoice_id": {"type": "string"},
                "line_items": {"type": "array"},
                "total": {"type": "number"},
                "status": {"type": "string", "enum": ["valid", "flagged", "rejected"]},
                "anomalies": {"type": "array"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            },
            "required": ["invoice_id", "status", "confidence"],
        },
        "tools": [
            {
                "name": "extract_line_items",
                "description": "Extract structured line items from invoice text or image",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "raw_text": {"type": "string"},
                        "currency": {"type": "string"},
                    },
                    "required": ["raw_text"],
                },
            },
            {
                "name": "validate_amounts",
                "description": "Validate that line item totals sum to invoice total",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "line_items": {"type": "array"},
                        "claimed_total": {"type": "number"},
                    },
                    "required": ["line_items", "claimed_total"],
                },
            },
            {
                "name": "flag_anomaly",
                "description": "Flag a suspicious pattern in the invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "anomaly_type": {
                            "type": "string",
                            "enum": ["duplicate", "inflated", "missing_vendor", "round_number_fraud"],
                        },
                        "confidence": {"type": "number"},
                        "details": {"type": "string"},
                    },
                    "required": ["anomaly_type", "confidence"],
                },
            },
        ],
        "adversarial_scenarios": [
            "Process an invoice where line items don't sum to the total",
            "Detect a duplicate invoice submission",
            "Handle an invoice with a missing vendor name",
        ],
        "success_criteria": "Correctly identifies valid vs fraudulent invoices with >80% accuracy",
    },

    "zoa-scheduling-agent": {
        "skill_id": "zoa-scheduling-agent",
        "skill_name": "ZOA Scheduling Agent",
        "skill_description": (
            "Time Optimizer — finds optimal meeting slots by analyzing participant "
            "availability and ROI of time, books meetings with auto-generated agendas, "
            "handles declines intelligently."
        ),
        "skill_category": "Productivity",
        "primary_llm_role": "reasoning",
        "fallback_llm_role": "manager",
        "input_schema": {
            "type": "object",
            "properties": {
                "participants": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of participant IDs or names",
                },
                "duration_mins": {"type": "integer", "minimum": 15, "maximum": 480},
                "context": {"type": "string", "description": "Meeting purpose and priority"},
                "constraints": {
                    "type": "object",
                    "properties": {
                        "earliest": {"type": "string", "format": "date-time"},
                        "latest": {"type": "string", "format": "date-time"},
                        "timezone": {"type": "string"},
                    },
                },
            },
            "required": ["participants", "duration_mins", "context"],
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "slot": {"type": "object"},
                "participants": {"type": "array"},
                "agenda_items": {"type": "array"},
                "roi_score": {"type": "number", "minimum": 0, "maximum": 10},
                "alternatives": {"type": "array"},
            },
            "required": ["slot", "roi_score"],
        },
        "tools": [
            {
                "name": "check_availability",
                "description": "Check participant availability for a time slot",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "participant_id": {"type": "string"},
                        "start_time": {"type": "string", "format": "date-time"},
                        "end_time": {"type": "string", "format": "date-time"},
                    },
                    "required": ["participant_id", "start_time", "end_time"],
                },
            },
            {
                "name": "calculate_roi",
                "description": "Calculate the ROI score of a meeting given participants and context",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "participants": {"type": "array"},
                        "duration_mins": {"type": "integer"},
                        "context": {"type": "string"},
                    },
                    "required": ["participants", "duration_mins", "context"],
                },
            },
            {
                "name": "book_slot",
                "description": "Confirm and book a meeting slot",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "slot": {"type": "object"},
                        "agenda": {"type": "string"},
                        "participants": {"type": "array"},
                    },
                    "required": ["slot", "participants"],
                },
            },
        ],
        "adversarial_scenarios": [
            "All participants are unavailable — find the best alternative",
            "Meeting context is vague — ask for clarification before booking",
            "Participant declines — reschedule without losing all attendees",
        ],
        "success_criteria": "Books meeting in optimal slot with ROI score > 6/10",
    },

    "zoa-payroll-agent": {
        "skill_id": "zoa-payroll-agent",
        "skill_name": "ZOA Payroll Agent",
        "skill_description": (
            "Wage Calculator — computes gross/net pay with deductions, detects "
            "performance anomalies from productivity metrics, manages commission holds, "
            "and recommends compensation adjustments."
        ),
        "skill_category": "HR & Payroll",
        "primary_llm_role": "code",
        "fallback_llm_role": "reasoning",
        "input_schema": {
            "type": "object",
            "properties": {
                "employees": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "hours": {"type": "number"},
                            "rate": {"type": "number"},
                            "role": {"type": "string"},
                            "deductions": {"type": "number"},
                        },
                        "required": ["id", "name", "hours", "rate"],
                    },
                },
                "period": {"type": "string", "description": "Pay period e.g. 2026-Q2"},
            },
            "required": ["employees", "period"],
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "period": {"type": "string"},
                "employees": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "gross": {"type": "number"},
                            "deductions": {"type": "number"},
                            "net": {"type": "number"},
                        },
                    },
                },
                "total_payroll": {"type": "number"},
            },
            "required": ["period", "employees", "total_payroll"],
        },
        "tools": [
            {
                "name": "calculate_gross",
                "description": "Calculate gross pay for an employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "hours": {"type": "number"},
                        "rate": {"type": "number"},
                        "overtime_hours": {"type": "number"},
                    },
                    "required": ["hours", "rate"],
                },
            },
            {
                "name": "apply_deductions",
                "description": "Apply tax and benefit deductions to gross pay",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "gross": {"type": "number"},
                        "deduction_rate": {"type": "number"},
                        "fixed_deductions": {"type": "number"},
                    },
                    "required": ["gross", "deduction_rate"],
                },
            },
            {
                "name": "flag_anomaly",
                "description": "Flag a payroll anomaly for review",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string"},
                        "anomaly_type": {
                            "type": "string",
                            "enum": ["overtime_spike", "duplicate_payment", "rate_mismatch", "missing_hours"],
                        },
                        "details": {"type": "string"},
                    },
                    "required": ["employee_id", "anomaly_type"],
                },
            },
        ],
        "adversarial_scenarios": [
            "Employee has 0 hours logged — handle gracefully",
            "Deduction rate exceeds gross pay — flag and halt",
            "Duplicate employee ID in the list — detect and deduplicate",
        ],
        "success_criteria": "Calculates payroll with <0.01% error rate, flags all anomalies",
    },

    "zoa-hr-agent": {
        "skill_id": "zoa-hr-agent",
        "skill_name": "ZOA HR Agent",
        "skill_description": (
            "Talent Optimizer — screens resumes against role requirements, conducts "
            "structured performance reviews, generates exit documentation, and flags "
            "performance issues to the ZOA context bus."
        ),
        "skill_category": "HR & Payroll",
        "primary_llm_role": "reasoning",
        "fallback_llm_role": "manager",
        "input_schema": {
            "type": "object",
            "properties": {
                "resume_text": {"type": "string"},
                "role_requirements": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "required_skills": {"type": "array", "items": {"type": "string"}},
                        "min_years_experience": {"type": "integer"},
                        "nice_to_have": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["title", "required_skills"],
                },
            },
            "required": ["resume_text", "role_requirements"],
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "candidate_score": {"type": "number", "minimum": 0, "maximum": 100},
                "strengths": {"type": "array"},
                "gaps": {"type": "array"},
                "recommendation": {
                    "type": "string",
                    "enum": ["strong_yes", "yes", "maybe", "no"],
                },
                "interview_questions": {"type": "array"},
            },
            "required": ["candidate_score", "recommendation"],
        },
        "tools": [
            {
                "name": "extract_skills",
                "description": "Extract skills and experience from resume text",
                "parameters": {
                    "type": "object",
                    "properties": {"resume_text": {"type": "string"}},
                    "required": ["resume_text"],
                },
            },
            {
                "name": "score_candidate",
                "description": "Score candidate against role requirements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_skills": {"type": "array"},
                        "required_skills": {"type": "array"},
                        "years_experience": {"type": "integer"},
                        "min_years": {"type": "integer"},
                    },
                    "required": ["candidate_skills", "required_skills"],
                },
            },
        ],
        "adversarial_scenarios": [
            "Resume has no relevant skills — score fairly without hallucinating qualifications",
            "Role requirements are contradictory — flag the conflict",
            "Resume contains personal information — handle without bias",
        ],
        "success_criteria": "Scores candidates accurately with <10% variance from human reviewers",
    },

    "zoa-procurement-agent": {
        "skill_id": "zoa-procurement-agent",
        "skill_name": "ZOA Procurement Agent",
        "skill_description": (
            "Supply Optimizer — scans receipts and invoices via OCR, generates "
            "game-theory-based supplier negotiation strategies, monitors inventory "
            "against thresholds and triggers auto-orders."
        ),
        "skill_category": "Operations",
        "primary_llm_role": "ocr",
        "fallback_llm_role": "reasoning",
        "input_schema": {
            "type": "object",
            "properties": {
                "receipt_data": {"type": "string", "description": "Raw receipt text or base64 image"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "current_stock": {"type": "number"},
                            "unit": {"type": "string"},
                        },
                    },
                },
                "thresholds": {
                    "type": "object",
                    "description": "Map of item name to minimum stock threshold",
                },
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "vendor": {"type": "string"},
                "items": {"type": "array"},
                "total": {"type": "number"},
                "date": {"type": "string"},
                "category": {"type": "string"},
                "reimbursable": {"type": "boolean"},
            },
        },
        "tools": [
            {
                "name": "ocr_extract",
                "description": "Extract structured data from receipt image or text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "raw_data": {"type": "string"},
                        "format": {"type": "string", "enum": ["text", "base64_image"]},
                    },
                    "required": ["raw_data"],
                },
            },
            {
                "name": "check_stock_level",
                "description": "Check if an item is below its reorder threshold",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_name": {"type": "string"},
                        "current_stock": {"type": "number"},
                        "threshold": {"type": "number"},
                    },
                    "required": ["item_name", "current_stock", "threshold"],
                },
            },
            {
                "name": "place_order",
                "description": "Place an auto-order for an item below threshold",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item": {"type": "string"},
                        "quantity": {"type": "number"},
                        "supplier": {"type": "string"},
                        "urgency": {"type": "string", "enum": ["standard", "express", "critical"]},
                    },
                    "required": ["item", "quantity", "supplier"],
                },
            },
        ],
        "adversarial_scenarios": [
            "Receipt is illegible — return partial data with confidence score",
            "All items are below threshold — prioritize orders by criticality",
            "Supplier is unavailable — find alternative",
        ],
        "success_criteria": "Extracts receipt data with >90% accuracy, triggers correct auto-orders",
    },

    "zoa-compliance-agent": {
        "skill_id": "zoa-compliance-agent",
        "skill_name": "ZOA Compliance Agent",
        "skill_description": (
            "Regulation Navigator — interprets regulatory text to extract actionable "
            "requirements, generates audit-ready documentation, assesses operational "
            "risk by jurisdiction, and responds to fraud/compliance alerts."
        ),
        "skill_category": "Legal & Compliance",
        "primary_llm_role": "thinking",
        "fallback_llm_role": "reasoning",
        "input_schema": {
            "type": "object",
            "properties": {
                "regulation_text": {"type": "string"},
                "business_context": {"type": "string"},
                "jurisdiction": {"type": "string"},
                "operation": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "requirements": {"type": "array"},
                "applicable_sections": {"type": "array"},
                "risk_level": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                "action_items": {"type": "array"},
                "deadline": {"type": "string"},
            },
            "required": ["risk_level", "action_items"],
        },
        "tools": [
            {
                "name": "extract_requirements",
                "description": "Extract mandatory requirements from regulation text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "regulation_text": {"type": "string"},
                        "jurisdiction": {"type": "string"},
                    },
                    "required": ["regulation_text"],
                },
            },
            {
                "name": "assess_risk",
                "description": "Assess the risk level of an operation under a regulation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string"},
                        "requirements": {"type": "array"},
                        "current_compliance": {"type": "object"},
                    },
                    "required": ["operation", "requirements"],
                },
            },
            {
                "name": "generate_action_plan",
                "description": "Generate a prioritized action plan to achieve compliance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "gaps": {"type": "array"},
                        "deadline": {"type": "string"},
                        "resources_available": {"type": "object"},
                    },
                    "required": ["gaps"],
                },
            },
        ],
        "adversarial_scenarios": [
            "Regulation text is ambiguous — flag ambiguity rather than guessing",
            "Jurisdiction is unknown — ask for clarification",
            "Operation clearly violates regulation — report accurately without softening",
        ],
        "success_criteria": "Correctly identifies compliance requirements with <5% false negative rate on risk flags",
    },
}


def get_contract(skill_id: str) -> dict | None:
    """Return the skill contract for a given skill ID."""
    return ZOA_SKILL_CONTRACTS.get(skill_id)


def list_contracts() -> list[str]:
    """Return all registered ZOA skill IDs."""
    return list(ZOA_SKILL_CONTRACTS.keys())
