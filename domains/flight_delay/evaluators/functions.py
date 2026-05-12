"""
Evaluation functions for flight delay tasks
"""
# pylint: disable=broad-exception-caught,unused-argument
import json
from typing import Any, Tuple
from lbx_cli.mcpuniverse.evaluator.functions import compare_func
from lbx_cli.mcpuniverse.common.context import Context


##################################################################################
# Comparison Functions for Flight Delay
##################################################################################


@compare_func(name="flight_delay.validate_all_fields")
async def flight_delay__validate_all_fields(llm_response: Any, expected_values: Any, op_args: Any, **kwargs) -> Tuple[bool, str]:
    """
    Validate all required fields in flight delay response.
    
    Checks:
    - flight_number matches expected value
    - delay_probability is a valid percentage (0-100)
    - confidence level is present
    - recommendation is present and makes sense
    
    Args:
        llm_response: The agent's response (FunctionResult with .result attribute)
        expected_values: Expected values dict
        op_args: Additional arguments with expected flight_number
        
    Returns:
        Tuple of (passed: bool, reason: str)
    """
    try:
        # Extract the actual response
        if hasattr(llm_response, 'result'):
            response = llm_response.result
        else:
            response = llm_response
        
        # Parse JSON response
        if isinstance(response, str):
            try:
                data = json.loads(response)
            except json.JSONDecodeError:
                return False, "Response is not valid JSON"
        elif isinstance(response, dict):
            data = response
        else:
            return False, f"Unexpected response type: {type(response)}"
        
        # Get expected flight number
        expected_flight = op_args.get("flight_number", "")
        
        # Validate required fields exist
        required_fields = ["flight_number", "delay_probability", "confidence", "recommendation"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate flight_number
        if data["flight_number"] != expected_flight:
            return False, f"Flight number mismatch: expected '{expected_flight}', got '{data['flight_number']}'"
        
        # Validate delay_probability is a valid percentage
        try:
            delay_prob = data["delay_probability"]
            # Handle both string and numeric formats
            if isinstance(delay_prob, str):
                # Remove % sign if present
                delay_prob = delay_prob.replace("%", "").strip()
                delay_prob = float(delay_prob)
            else:
                delay_prob = float(delay_prob)
            
            if not (0 <= delay_prob <= 100):
                return False, f"Delay probability must be between 0-100, got {delay_prob}"
        except (ValueError, TypeError):
            return False, f"Invalid delay_probability format: {data['delay_probability']}"
        
        # Validate confidence is non-empty
        confidence = str(data.get("confidence", "")).strip()
        if not confidence or confidence.lower() in ["", "none", "null"]:
            return False, "Confidence level is empty or invalid"
        
        # Validate recommendation is non-empty and meaningful
        recommendation = str(data.get("recommendation", "")).strip()
        if not recommendation or len(recommendation) < 10:
            return False, "Recommendation is too short or empty"
        
        # All validations passed
        return True, ""
        
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"

# Utils Function for Flight Delay
@compare_func(name="flight_delay.check_field_presence")
async def flight_delay__check_field_presence(llm_response: Any, expected_values: Any, op_args: Any, **kwargs) -> Tuple[bool, str]:
    """
    Simple check for field presence in response.
    
    Args:
        llm_response: The agent's response
        expected_values: Not used
        op_args: Dict with 'required_fields' list
        
    Returns:
        Tuple of (passed: bool, reason: str)
    """
    try:
        # Extract the actual response
        if hasattr(llm_response, 'result'):
            response = llm_response.result
        else:
            response = llm_response
        
        # Parse JSON response
        if isinstance(response, str):
            try:
                data = json.loads(response)
            except json.JSONDecodeError:
                return False, "Response is not valid JSON"
        elif isinstance(response, dict):
            data = response
        else:
            return False, f"Unexpected response type: {type(response)}"
        
        # Check required fields
        required_fields = op_args.get("required_fields", [])
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return False, f"Missing or empty fields: {', '.join(missing_fields)}"
        
        return True, ""
        
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"
