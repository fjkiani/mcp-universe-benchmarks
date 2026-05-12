"""
Mock Agent Responses for Testing

Provides mock LLM responses in various formats for testing evaluators
without requiring live LLM API keys.
"""

import json
from typing import Any, Dict


class MockFunctionResult:
    """Mock Pydantic FunctionResult object."""
    
    def __init__(self, data: Dict):
        self._data = data
    
    def model_dump(self):
        return {"result": self._data}
    
    def dict(self):
        return {"result": self._data}
    
    @property
    def __dict__(self):
        return {"result": self._data}


# Patient Intake Mock Responses
MOCK_PATIENT_INTAKE_RESPONSE = {
    "patient": {
        "resourceType": "Patient",
        "identifier": [{"value": "MRN-12345"}],
        "name": [{"family": "Doe", "given": ["John"]}],
        "birthDate": "1985-03-15",
        "telecom": [
            {"system": "phone", "value": "555-1234"},
            {"system": "email", "value": "john.doe@example.com"}
        ]
    },
    "appointment": {
        "provider": "Dr. Smith",
        "date": "2025-11-10",
        "time": "14:00"
    },
    "intake_form_sent": True
}

MOCK_PATIENT_INTAKE_PYDANTIC = MockFunctionResult(MOCK_PATIENT_INTAKE_RESPONSE)

MOCK_PATIENT_INTAKE_JSON_STRING = json.dumps(MOCK_PATIENT_INTAKE_RESPONSE)


# Appointment Scheduling Mock Responses
MOCK_APPOINTMENT_RESPONSE = {
    "appointment": {
        "resourceType": "Appointment",
        "status": "booked",
        "start": "2025-11-11T14:00:00-05:00",
        "end": "2025-11-11T14:30:00-05:00"
    },
    "confirmation_sent": True
}

MOCK_APPOINTMENT_PYDANTIC = MockFunctionResult(MOCK_APPOINTMENT_RESPONSE)

MOCK_APPOINTMENT_JSON_STRING = json.dumps(MOCK_APPOINTMENT_RESPONSE)


# Triage Mock Responses
MOCK_TRIAGE_EMERGENT_RESPONSE = {
    "triage_category": "EMERGENT",
    "recommended_action": "call_911",
    "patient_advised": "Call 911 immediately for chest pain evaluation",
    "FHIR_observation_created": True
}

MOCK_TRIAGE_EMERGENT_PYDANTIC = MockFunctionResult(MOCK_TRIAGE_EMERGENT_RESPONSE)

MOCK_TRIAGE_EMERGENT_JSON_STRING = json.dumps(MOCK_TRIAGE_EMERGENT_RESPONSE)


# Transcription Mock Responses
MOCK_TRANSCRIPTION_RESPONSE = {
    "transcript": "Patient reports chest pain for the past 2 hours...",
    "medical_entities": [
        {"type": "symptom", "value": "chest pain"},
        {"type": "duration", "value": "2 hours"},
        {"type": "severity", "value": "moderate"}
    ],
    "FHIR_observation": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "8867-4",
                "display": "Heart rate"
            }]
        }
    },
    "transcription_accuracy": 0.933
}

MOCK_TRANSCRIPTION_PYDANTIC = MockFunctionResult(MOCK_TRANSCRIPTION_RESPONSE)

MOCK_TRANSCRIPTION_JSON_STRING = json.dumps(MOCK_TRANSCRIPTION_RESPONSE)


# Video Consultation Mock Responses
MOCK_VIDEO_CONSULTATION_RESPONSE = {
    "video_room": {
        "room_id": "room-abc123",
        "status": "active"
    },
    "patient_token": "token-xyz789",
    "room_link": "https://videosdk.live/room/abc123",
    "sms_sent": True,
    "recording_enabled": True
}

MOCK_VIDEO_CONSULTATION_PYDANTIC = MockFunctionResult(MOCK_VIDEO_CONSULTATION_RESPONSE)

MOCK_VIDEO_CONSULTATION_JSON_STRING = json.dumps(MOCK_VIDEO_CONSULTATION_RESPONSE)


# Invalid Responses (for testing error handling)
MOCK_INVALID_MISSING_FIELD = {
    "appointment": {
        "provider": "Dr. Smith",
        "date": "2025-11-10"
        # Missing "time" field
    }
}

MOCK_INVALID_WRONG_TYPE = {
    "patient": "not a dict",  # Should be dict
    "appointment": {}
}

MOCK_INVALID_EMPTY = {}

MOCK_INVALID_NULL = None


def get_mock_response(response_type: str, format_type: str = "simple") -> Any:
    """
    Get mock response in specified format.
    
    Args:
        response_type: Type of response (patient_intake, appointment, triage, etc.)
        format_type: Format (simple, pydantic, json_string)
    
    Returns:
        Mock response in specified format
    """
    responses = {
        "patient_intake": MOCK_PATIENT_INTAKE_RESPONSE,
        "appointment": MOCK_APPOINTMENT_RESPONSE,
        "triage": MOCK_TRIAGE_EMERGENT_RESPONSE,
        "transcription": MOCK_TRANSCRIPTION_RESPONSE,
        "video_consultation": MOCK_VIDEO_CONSULTATION_RESPONSE,
    }
    
    pydantic_responses = {
        "patient_intake": MOCK_PATIENT_INTAKE_PYDANTIC,
        "appointment": MOCK_APPOINTMENT_PYDANTIC,
        "triage": MOCK_TRIAGE_EMERGENT_PYDANTIC,
        "transcription": MOCK_TRANSCRIPTION_PYDANTIC,
        "video_consultation": MOCK_VIDEO_CONSULTATION_PYDANTIC,
    }
    
    json_string_responses = {
        "patient_intake": MOCK_PATIENT_INTAKE_JSON_STRING,
        "appointment": MOCK_APPOINTMENT_JSON_STRING,
        "triage": MOCK_TRIAGE_EMERGENT_JSON_STRING,
        "transcription": MOCK_TRANSCRIPTION_JSON_STRING,
        "video_consultation": MOCK_VIDEO_CONSULTATION_JSON_STRING,
    }
    
    if format_type == "simple":
        return responses.get(response_type, {})
    elif format_type == "pydantic":
        return pydantic_responses.get(response_type, MockFunctionResult({}))
    elif format_type == "json_string":
        return json_string_responses.get(response_type, "{}")
    else:
        return responses.get(response_type, {})






