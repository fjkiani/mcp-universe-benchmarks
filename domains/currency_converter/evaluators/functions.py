"""
Evaluation functions for currency_converter domain
"""
# pylint: disable=broad-exception-caught,unused-argument
import json
from typing import Any, Tuple
from lbx_cli.mcpuniverse.evaluator.functions import compare_func


##################################################################################
# Comparison Functions for Currency Converter
##################################################################################


@compare_func(name="currency_converter.validate_conversion")
async def currency_converter__validate_conversion(
    llm_response: Any, expected_values: Any, op_args: Any, **kwargs
) -> Tuple[bool, str]:
    """
    Validate currency conversion response.
    
    Checks:
    - All required fields present (from_currency, to_currency, amount, converted_amount)
    - Currencies match expected values
    - Amount matches expected value
    - Converted amount is present and numeric
    
    Args:
        llm_response: The agent's response (FunctionResult with .result attribute)
        expected_values: Expected values dict
        op_args: Additional arguments with expected from/to currencies and amount
        
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
        
        # Get expected values from op_args
        expected_from = op_args.get("from_currency", "")
        expected_to = op_args.get("to_currency", "")
        expected_amount = str(op_args.get("amount", ""))
        
        # Validate required fields exist
        required_fields = ["from_currency", "to_currency", "amount", "converted_amount"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate from_currency
        if str(data["from_currency"]).upper() != expected_from.upper():
            return False, f"from_currency mismatch: expected '{expected_from}', got '{data['from_currency']}'"
        
        # Validate to_currency
        if str(data["to_currency"]).upper() != expected_to.upper():
            return False, f"to_currency mismatch: expected '{expected_to}', got '{data['to_currency']}'"
        
        # Validate amount
        try:
            response_amount = str(data["amount"]).replace(",", "")  # Remove commas
            if response_amount != expected_amount:
                return False, f"amount mismatch: expected '{expected_amount}', got '{data['amount']}'"
        except (ValueError, TypeError):
            return False, f"Invalid amount format: {data['amount']}"
        
        # Validate converted_amount is numeric and reasonable
        try:
            converted = float(str(data["converted_amount"]).replace(",", ""))
            original = float(expected_amount)
            
            # Sanity check: converted amount should be positive and non-zero
            if converted <= 0:
                return False, f"converted_amount must be positive, got {converted}"
            
            # Optional: Check if conversion rate is reasonable (0.1x to 10x range)
            # This prevents obvious errors like converting $100 to 0.01 EUR
            ratio = converted / original
            if ratio < 0.1 or ratio > 10:
                return False, f"Suspicious conversion rate: {original} {expected_from} → {converted} {expected_to} (ratio: {ratio:.2f})"
            
        except (ValueError, TypeError):
            return False, f"Invalid converted_amount format: {data['converted_amount']}"
        
        # All validations passed
        return True, ""
        
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="currency_converter.check_required_fields")
async def currency_converter__check_required_fields(
    llm_response: Any, expected_values: Any, op_args: Any, **kwargs
) -> Tuple[bool, str]:
    """
    Simple check for required fields in currency conversion response.
    
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
        required_fields = op_args.get("required_fields", ["from_currency", "to_currency", "amount", "converted_amount"])
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return False, f"Missing or empty fields: {', '.join(missing_fields)}"
        
        return True, ""
        
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"
