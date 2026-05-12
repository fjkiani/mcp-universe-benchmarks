"""
Error Type Classification for Evaluators

Separates two error classes (Manager's request):
1. Parse/Infrastructure Errors (JSON parsing, data structure issues)
2. Validation/Business Logic Errors (LLM performance, task completion)
"""

from enum import Enum

class ErrorType(Enum):
    """Error classification types"""
    PARSE_ERROR = "parse_error"  # JSON parsing, data structure issues
    VALIDATION_ERROR = "validation_error"  # Business logic, LLM performance






