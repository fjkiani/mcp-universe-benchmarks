"""Telehealth Analysis Service - Generates structured insights from transcripts"""
import os
import json
import cohere
from pydantic import BaseModel, Field
from typing import List

# Keep OpenAI key variable for potential agnostic fallback later, but use Cohere now
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")


class ActionItem(BaseModel):
    task: str = Field(description="The specific action to be taken")
    assignee: str = Field(description="Who is responsible: 'patient' or 'provider'")
    urgency: str = Field(description="Urgency level: 'high', 'medium', or 'low'")

class TelehealthAnalysis(BaseModel):
    clinical_summary: str = Field(description="A concise, professional medical summary of the visit (SOAP format preferred for subjective/objective).")
    key_takeaways: List[str] = Field(description="3-5 bullet points of the most important takeaways for the patient.")
    action_items: List[ActionItem] = Field(description="Specific next steps assigned to either patient or provider.")
    recommended_follow_up: str = Field(description="When the patient should be seen next, e.g., '2 weeks', '6 months', 'as needed'.")

async def analyze_transcript(transcript: str, patient_name: str, provider_name: str) -> dict:
    """Analyze a telehealth transcript and return structured insights."""
    if not COHERE_API_KEY:
        print("[Telehealth Analysis] No COHERE_API_KEY found, falling back to mock")
        # Return a rich mock analysis if no real API key is present
        return {
            "clinical_summary": f"Patient {patient_name} presented to Dr. {provider_name} via telehealth. Reported intermittent anxiety and sleep difficulties over the past 3 weeks. Denies suicidal ideation or acute distress. Currently not on any daily medications. Heart rate was occasionally elevated during panic episodes. Past medical history significant for generalized anxiety disorder.",
            "key_takeaways": [
                "Patient is experiencing a minor flare-up of generalized anxiety.",
                "Sleep hygiene modifications should be the first-line approach.",
                "No acute pharmacological intervention is required at this moment."
            ],
            "action_items": [
                {
                    "task": "Implement a strict 10 PM bedtime routine without screens.",
                    "assignee": "patient",
                    "urgency": "medium"
                },
                {
                    "task": "Order basic metabolic panel and thyroid function labs.",
                    "assignee": "provider",
                    "urgency": "low"
                },
                {
                    "task": "Schedule CBT therapy intake session.",
                    "assignee": "patient",
                    "urgency": "high"
                }
            ],
            "recommended_follow_up": "4 weeks",
            "source": "demo_mock_analysis"
        }

    try:
        co = cohere.ClientV2(api_key=COHERE_API_KEY)
        
        system_prompt = """You are an expert AI clinical assistant reviewing a telehealth transcript. 
        Your job is to generate a structured post-visit summary, including the clinical overview, key takeaways for the patient, and specific assigned action items.
        Maintain a highly professional, empathetic, and culturally competent medical tone."""

        user_prompt = f"Patient: {patient_name}\nProvider: {provider_name}\n\nTranscript:\n{transcript}"

        # Convert Pydantic model to JSON Schema for Cohere
        response_schema = TelehealthAnalysis.model_json_schema()

        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={
                "type": "json_object",
                "schema": response_schema
            },
            temperature=0.2
        )

        # Cohere returns a JSON string in the message text when using structured outputs
        result_text = response.message.content[0].text
        return json.loads(result_text)
    except Exception as e:
        print(f"[Telehealth Analysis] Error: {e}")
        return {
            "error": "Failed to analyze transcript"
        }
