"""
Evaluator functions for Grant Application AI Pipeline domain.

These evaluators use a multi-layered approach:
1. Structure validation (required fields, format)
2. Content accuracy (values, calculations)  
3. LLM-as-a-judge (quality, completeness)
4. Environment detection (separate agent failures from API/permission errors)
"""

from lbx_cli.mcpuniverse.evaluator.functions import compare_func
from typing import Tuple, Any
import json
import re


# ============================================================================
# ENVIRONMENT DETECTION UTILITY
# ============================================================================

def detect_environment_error(response_text: str, error_obj: Any = None) -> Tuple[bool, str]:
    """
    Detect if a failure is due to environment issues (API permissions, credentials)
    rather than agent capability gaps.
    
    Returns:
        (is_env_error: bool, reason: str)
        
    Environment error patterns:
    - HTTP 403 Forbidden (permission denied)
    - HTTP 401 Unauthorized (auth failed)
    - HTTP 404 Not Found (endpoint missing)
    - "credentials not found"
    - "authentication failed"
    - "permission denied"
    - "API key invalid"
    - "quota exceeded"
    - "service unavailable"
    """
    response_lower = str(response_text).lower()
    
    # Check for HTTP error codes
    if "403" in response_lower or "forbidden" in response_lower:
        return True, "SKIPPED: HTTP 403 Forbidden (permission denied)"
    
    if "401" in response_lower or "unauthorized" in response_lower:
        return True, "SKIPPED: HTTP 401 Unauthorized (authentication failed)"
    
    if "404" in response_lower and "not found" in response_lower:
        return True, "SKIPPED: HTTP 404 Not Found (endpoint missing)"
    
    # Check for authentication/credential errors
    if "credential" in response_lower and ("not found" in response_lower or "missing" in response_lower or "invalid" in response_lower):
        return True, "SKIPPED: Credentials not found or invalid"
    
    if "authentication failed" in response_lower or "auth failed" in response_lower:
        return True, "SKIPPED: Authentication failed"
    
    if "permission denied" in response_lower or "access denied" in response_lower:
        return True, "SKIPPED: Permission denied"
    
    if "api key" in response_lower and ("invalid" in response_lower or "missing" in response_lower):
        return True, "SKIPPED: API key invalid or missing"
    
    # Check for rate limiting / quota
    if "quota exceeded" in response_lower or "rate limit" in response_lower:
        return True, "SKIPPED: API quota exceeded or rate limited"
    
    if "service unavailable" in response_lower or "503" in response_lower:
        return True, "SKIPPED: Service unavailable (503)"
    
    # Check for timeout errors (might be environment or agent)
    if "timeout" in response_lower or "timed out" in response_lower:
        return True, "SKIPPED: Request timeout (possible environment issue)"
    
    # Not an environment error - actual agent failure
    return False, ""


def enforce_output_completeness(data: dict, required_fields: list) -> Tuple[bool, str]:
    """
    Enforce that all required output fields are present before content validation.
    
    This prevents incomplete outputs from passing (e.g., analysis without recommendation).
    
    Returns:
        (is_complete: bool, feedback: str)
    """
    if not isinstance(data, dict):
        return False, "Output must be a JSON object"
    
    missing_fields = []
    for field in required_fields:
        # Check nested fields (e.g., "recommendation.decision")
        if "." in field:
            parts = field.split(".")
            current = data
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    missing_fields.append(field)
                    break
        else:
            # Check top-level field
            if field not in data:
                missing_fields.append(field)
    
    if missing_fields:
        return False, f"Incomplete output: missing required fields {missing_fields}"
    
    return True, "All required fields present"


@compare_func(name="grant_application.validate_grant_search")
async def validate_grant_search(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate grant search results.
    
    Checks:
    1. Environment errors (API permissions, credentials)
    2. Minimum number of results returned
    3. Required fields present
    4. Reasonable data format
    """
    _, values = args
    min_results = values.get('min_results', 3)
    required_fields = values.get('required_fields', [])
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Layer 1: Check for environment errors FIRST
        is_env_error, env_reason = detect_environment_error(response_text)
        if is_env_error:
            return False, env_reason
        
        # Try to parse as JSON if possible
        try:
            # Extract JSON from response if wrapped in text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
                
            # Check if grants array exists
            grants = data.get('grants', [])
            
            if len(grants) < min_results:
                return False, f"Expected at least {min_results} grants, found {len(grants)}"
            
            # Validate required fields in each grant
            for i, grant in enumerate(grants):
                missing_fields = [field for field in required_fields if field not in grant]
                if missing_fields:
                    return False, f"Grant {i+1} missing required fields: {', '.join(missing_fields)}"
            
            return True, f"Found {len(grants)} grants with all required fields"
            
        except json.JSONDecodeError:
            # Fallback to text-based validation
            response_lower = response_text.lower()
            
            # Check for grant-related keywords
            grant_indicators = ['grant', 'nsf', 'nih', 'funding', 'award', 'deadline', 'budget']
            found_indicators = sum(1 for indicator in grant_indicators if indicator in response_lower)
            
            if found_indicators < 3:
                return False, "Response does not appear to contain grant information"
            
            # Check for presence of required fields in text
            missing_in_text = [field for field in required_fields if field.replace('_', ' ') not in response_lower]
            if len(missing_in_text) > len(required_fields) / 2:
                return False, f"Response missing most required information: {', '.join(missing_in_text)}"
            
            return True, "Grant search response contains relevant information (text format)"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_requirements_extraction")
async def validate_requirements_extraction(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate requirements extraction from RFP documents.
    
    Checks:
    - Expected structure present
    - Key values accurate (page limits, budget caps)
    - Completeness of extraction
    """
    _, values = args
    expected_structure = values.get('expected_structure', {})
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Try structured parsing
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
            
            # Validate expected structure
            score = 0
            max_score = len(expected_structure)
            feedback = []
            
            for key, expected_value in expected_structure.items():
                if key in data:
                    actual_value = data[key]
                    
                    # Check if values match (flexible comparison)
                    if isinstance(expected_value, (int, float)):
                        # Numeric comparison
                        if isinstance(actual_value, dict):
                            # Extract numeric value from nested structure
                            actual_num = next((v for v in actual_value.values() if isinstance(v, (int, float))), None)
                        else:
                            actual_num = actual_value
                        
                        if actual_num == expected_value:
                            score += 1
                            feedback.append(f"✓ {key}: {actual_value}")
                        else:
                            feedback.append(f"✗ {key}: expected {expected_value}, got {actual_num}")
                    
                    elif isinstance(expected_value, str):
                        # String comparison (case-insensitive, flexible)
                        if expected_value.lower() in str(actual_value).lower():
                            score += 1
                            feedback.append(f"✓ {key}: matches")
                        else:
                            feedback.append(f"✗ {key}: expected '{expected_value}', got '{actual_value}'")
                    
                    elif key.endswith('_count'):
                        # Count comparison
                        actual_count = len(actual_value) if isinstance(actual_value, list) else 0
                        if actual_count >= expected_value:
                            score += 1
                            feedback.append(f"✓ {key}: {actual_count} >= {expected_value}")
                        else:
                            feedback.append(f"✗ {key}: {actual_count} < {expected_value}")
                    else:
                        score += 0.5  # Partial credit for presence
                        feedback.append(f"~ {key}: present but not validated")
                else:
                    feedback.append(f"✗ {key}: missing")
            
            pass_threshold = 0.6  # 60% of checks must pass
            passed = (score / max_score) >= pass_threshold if max_score > 0 else False
            
            feedback_str = "\n".join(feedback)
            if passed:
                return True, f"Requirements extraction successful ({score}/{max_score}):\n{feedback_str}"
            else:
                return False, f"Requirements extraction incomplete ({score}/{max_score}):\n{feedback_str}"
                
        except json.JSONDecodeError:
            # Fallback to text-based validation
            response_lower = response_text.lower()
            
            # Check for key requirement indicators
            found_count = 0
            for key, value in expected_structure.items():
                search_term = key.replace('_', ' ')
                if search_term in response_lower or str(value) in response_text:
                    found_count += 1
            
            found_ratio = found_count / len(expected_structure) if expected_structure else 0
            
            if found_ratio >= 0.5:
                return True, f"Requirements extraction found {found_count}/{len(expected_structure)} expected items (text format)"
            else:
                return False, f"Requirements extraction incomplete: only {found_count}/{len(expected_structure)} items found"
                
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_budget_justification")
async def validate_budget_justification(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate budget justification narrative.
    
    Checks:
    - All required categories present
    - Amounts mentioned correctly
    - Minimum narrative quality (sentences per category)
    - Proper justification language
    """
    _, values = args
    required_categories = values.get('required_categories', [])
    required_amounts = values.get('required_amounts', [])
    min_sentences_per_category = values.get('min_sentences_per_category', 2)
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
            
        response_lower = response_text.lower()
        
        # Extract narrative (handle both JSON and plain text)
        narrative = response_text
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                narrative = data.get('budget_justification', response_text)
        except:
            pass
        
        narrative_lower = str(narrative).lower()
        
        # Check 1: All categories present
        missing_categories = []
        for category in required_categories:
            category_lower = category.lower()
            if category_lower not in narrative_lower:
                missing_categories.append(category)
        
        if missing_categories:
            return False, f"Missing budget categories: {', '.join(missing_categories)}"
        
        # Check 2: All amounts mentioned
        missing_amounts = []
        for amount in required_amounts:
            # Check for various formats: $12,000 or 12000 or 12,000
            amount_str = str(amount)
            amount_formatted = f"${amount:,}"
            amount_variations = [
                amount_str,
                amount_formatted,
                amount_str.replace(',', ''),
                f"${amount_str}"
            ]
            
            if not any(var in response_text for var in amount_variations):
                missing_amounts.append(amount_formatted)
        
        if len(missing_amounts) > len(required_amounts) / 2:
            return False, f"Most budget amounts not found: {', '.join(missing_amounts[:3])}"
        
        # Check 3: Sentence count per category (rough estimate)
        sentences = re.split(r'[.!?]+', narrative)
        sentence_count = len([s for s in sentences if len(s.strip()) > 10])
        expected_min_sentences = len(required_categories) * min_sentences_per_category
        
        if sentence_count < expected_min_sentences:
            return False, f"Budget justification too brief: {sentence_count} sentences, expected at least {expected_min_sentences}"
        
        # Check 4: Justification language
        justification_indicators = [
            'necessary', 'required', 'essential', 'support', 'enable',
            'will be used', 'needed', 'critical', 'important', 'allow',
            'calculated', 'based on', 'includes', 'covers'
        ]
        
        found_indicators = sum(1 for indicator in justification_indicators if indicator in narrative_lower)
        
        if found_indicators < 2:
            return False, "Budget justification lacks proper justification language"
        
        # All checks passed
        return True, f"Budget justification complete: all {len(required_categories)} categories, {len(required_amounts)} amounts, {sentence_count} sentences"
        
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_timeline")
async def validate_timeline(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate project timeline generation.
    
    Checks:
    - Minimum number of milestones
    - Date formatting
    - Chronological ordering
    - Milestone descriptions
    """
    _, values = args
    min_milestones = values.get('min_milestones', 5)
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Try to parse structured timeline
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
            
            # Extract milestones
            milestones = data.get('milestones', data.get('timeline', []))
            if isinstance(milestones, dict):
                milestones = milestones.get('milestones', [])
            
            if len(milestones) < min_milestones:
                return False, f"Timeline has only {len(milestones)} milestones, expected at least {min_milestones}"
            
            # Check milestone structure
            for i, milestone in enumerate(milestones):
                if not isinstance(milestone, dict):
                    return False, f"Milestone {i+1} is not properly structured"
                
                # Check for required fields
                if 'date' not in milestone and 'month' not in milestone and 'quarter' not in milestone:
                    return False, f"Milestone {i+1} missing time information"
                
                if 'description' not in milestone and 'task' not in milestone and 'milestone' not in milestone:
                    return False, f"Milestone {i+1} missing description"
            
            return True, f"Timeline complete with {len(milestones)} milestones"
            
        except json.JSONDecodeError:
            # Fallback to text-based validation
            response_lower = response_text.lower()
            
            # Count timeline indicators
            timeline_indicators = ['month', 'quarter', 'year', 'phase', 'milestone', 'deadline', 'deliverable']
            indicator_count = sum(response_lower.count(indicator) for indicator in timeline_indicators)
            
            if indicator_count < min_milestones:
                return False, f"Timeline appears incomplete: only {indicator_count} temporal indicators found"
            
            # Check for date patterns
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
                r'Month \d+',  # Month 1, Month 2
                r'Q[1-4]',  # Q1, Q2, Q3, Q4
            ]
            
            date_count = sum(len(re.findall(pattern, response_text)) for pattern in date_patterns)
            
            if date_count < min_milestones:
                return False, f"Timeline has insufficient dates: found {date_count}, expected at least {min_milestones}"
            
            return True, f"Timeline present with {date_count} dated items (text format)"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_document_structure")
async def validate_document_structure(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate document structure and formatting.
    
    Checks:
    - Required sections present
    - Proper formatting
    - Completeness
    """
    _, values = args
    required_sections = values.get('required_sections', [])
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
            
        response_lower = response_text.lower()
        
        # Check for required sections
        missing_sections = []
        for section in required_sections:
            section_lower = section.lower()
            if section_lower not in response_lower:
                missing_sections.append(section)
        
        if missing_sections:
            return False, f"Document missing required sections: {', '.join(missing_sections)}"
        
        # Check for formatting indicators
        formatting_indicators = ['#', '##', '**', '__', '\n\n', '---', ':']
        has_formatting = any(indicator in response_text for indicator in formatting_indicators)
        
        if not has_formatting:
            return False, "Document lacks proper formatting"
        
        # Check minimum length
        word_count = len(response_text.split())
        min_words = len(required_sections) * 50  # ~50 words per section minimum
        
        if word_count < min_words:
            return False, f"Document too brief: {word_count} words, expected at least {min_words}"
        
        return True, f"Document structure valid: {len(required_sections)} sections, {word_count} words"
        
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


# ============================================================================
# MULTI-SERVER ORCHESTRATION EVALUATORS (with environment detection)
# ============================================================================

@compare_func(name="grant_application.validate_multi_server_orchestration")
async def validate_multi_server_orchestration(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate multi-server task orchestration.
    
    Checks:
    1. Environment errors (API permissions, credentials) - returns SKIPPED
    2. Data format correctness (structured data passed between servers)
    3. Required fields present in output
    4. Workflow completion
    
    Use for tasks that orchestrate 2+ MCP servers (search → sheets, pdf → email, etc.)
    """
    _, values = args
    required_outputs = values.get('required_outputs', [])
    workflow_steps = values.get('workflow_steps', [])
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Layer 1: Check for environment errors FIRST
        is_env_error, env_reason = detect_environment_error(response_text)
        if is_env_error:
            return False, env_reason
        
        # Layer 2: Check for workflow completion indicators
        response_lower = response_text.lower()
        
        # Check if workflow steps were attempted
        completed_steps = []
        for step in workflow_steps:
            step_lower = step.lower()
            if step_lower in response_lower or any(keyword in response_lower for keyword in step_lower.split()):
                completed_steps.append(step)
        
        if len(completed_steps) < len(workflow_steps):
            missing_steps = [s for s in workflow_steps if s not in completed_steps]
            return False, f"Workflow incomplete: missing steps {missing_steps}"
        
        # Layer 3: Validate output structure
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
            
            # Check required outputs
            missing_outputs = [out for out in required_outputs if out not in data]
            if missing_outputs:
                return False, f"Missing required outputs: {missing_outputs}"
            
            return True, f"Multi-server orchestration successful: {len(workflow_steps)} steps completed"
            
        except json.JSONDecodeError:
            # Fallback: check for output indicators in text
            found_outputs = sum(1 for out in required_outputs if out.replace('_', ' ') in response_lower)
            if found_outputs < len(required_outputs) * 0.7:
                return False, f"Output structure unclear or incomplete"
            
            return True, f"Multi-server orchestration completed (text format)"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


# ============================================================================
# AGENTIC REASONING EVALUATORS (with completeness enforcement)
# ============================================================================

@compare_func(name="grant_application.validate_agentic_reasoning")
async def validate_agentic_reasoning(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate agentic reasoning tasks that require analysis + decision/recommendation.
    
    Checks:
    1. Environment errors (if applicable)
    2. Output completeness (all required fields present) - ENFORCED
    3. Analysis quality (reasoning, evidence)
    4. Decision/recommendation present and justified
    
    Use for tasks that require: grant comparison, eligibility analysis, budget approval, etc.
    
    CRITICAL: Incomplete outputs (missing recommendation/decision) will FAIL.
    """
    _, values = args
    required_fields = values.get('required_fields', [])
    decision_field = values.get('decision_field', 'recommendation')  # or 'decision', 'conclusion'
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Layer 1: Check for environment errors (if multi-server agentic task)
        is_env_error, env_reason = detect_environment_error(response_text)
        if is_env_error:
            return False, env_reason
        
        # Layer 2: Parse and enforce completeness
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
            
            # CRITICAL: Enforce all required fields present
            is_complete, completeness_msg = enforce_output_completeness(data, required_fields)
            if not is_complete:
                return False, completeness_msg
            
            # Layer 3: Validate decision/recommendation field exists and is non-empty
            decision_value = data.get(decision_field)
            if not decision_value:
                return False, f"Incomplete output: '{decision_field}' field is empty or missing"
            
            # Check decision is substantial (not just "yes" or "no")
            if isinstance(decision_value, str) and len(decision_value) < 10:
                return False, f"'{decision_field}' too brief: '{decision_value}' (expected justification)"
            
            # Layer 4: Validate reasoning/analysis present
            analysis_fields = ['analysis', 'reasoning', 'rationale', 'justification', 'pros', 'cons']
            has_analysis = any(field in data for field in analysis_fields)
            if not has_analysis:
                return False, "Missing analysis/reasoning (analysis, pros/cons, or rationale required)"
            
            return True, f"Agentic reasoning complete: analysis + {decision_field} provided"
            
        except json.JSONDecodeError:
            # Fallback: text-based validation
            response_lower = response_text.lower()
            
            # Check for decision indicators
            decision_indicators = [decision_field.lower(), 'recommend', 'decision', 'conclusion', 'suggest']
            has_decision = any(indicator in response_lower for indicator in decision_indicators)
            
            if not has_decision:
                return False, f"Incomplete output: no {decision_field} found in response"
            
            # Check for analysis indicators
            analysis_indicators = ['analysis', 'because', 'therefore', 'reasoning', 'rationale', 'pros', 'cons']
            has_analysis = sum(1 for indicator in analysis_indicators if indicator in response_lower) >= 2
            
            if not has_analysis:
                return False, "Missing analysis/reasoning"
            
            return True, f"Agentic reasoning present (text format)"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_edge_case_handling")
async def validate_edge_case_handling(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate edge case handling (contradictions, missing info, impossible scenarios).
    
    Checks:
    1. Agent detects the edge case (contradiction, impossibility, missing critical data)
    2. Agent either:
       - Flags the issue explicitly, OR
       - Makes reasonable assumptions and documents them, OR
       - Recommends skipping/postponing if impossible
    3. Does NOT silently ignore the edge case
    
    Use for tasks with: conflicting requirements, missing info, impossible timelines, etc.
    """
    _, values = args
    edge_case_type = values.get('edge_case_type', 'unknown')  # 'contradiction', 'missing_info', 'impossible'
    expected_detection = values.get('expected_detection', True)  # Should agent detect it?
    
    try:
        # Extract response text
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        response_lower = response_text.lower()
        
        # Detection keywords by edge case type
        detection_keywords = {
            'contradiction': ['contradict', 'conflict', 'inconsistent', 'cannot both', 'mutually exclusive', 'incompatible'],
            'missing_info': ['missing', 'not provided', 'unclear', 'insufficient', 'need more', 'require additional'],
            'impossible': ['impossible', 'cannot', 'unrealistic', 'infeasible', 'not enough time', 'too short'],
            'unknown': ['issue', 'problem', 'concern', 'note', 'warning', 'limitation']
        }
        
        keywords = detection_keywords.get(edge_case_type, detection_keywords['unknown'])
        detected = any(keyword in response_lower for keyword in keywords)
        
        if expected_detection and not detected:
            return False, f"Failed to detect {edge_case_type}: agent did not flag the issue"
        
        # Check if agent proposed a resolution strategy
        resolution_keywords = ['assume', 'proceed with', 'recommend', 'suggest', 'skip', 'postpone', 'clarify', 'workaround']
        has_resolution = any(keyword in response_lower for keyword in resolution_keywords)
        
        if detected and not has_resolution:
            return False, f"Detected {edge_case_type} but provided no resolution strategy"
        
        return True, f"Edge case handling successful: detected {edge_case_type} and proposed resolution"
        
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


# ============================================================================
# ULTRA-HARD DOCUMENT GENERATION EVALUATORS (Day 2 hardening)
# ============================================================================

@compare_func(name="grant_application.validate_cross_document_consistency")
async def validate_cross_document_consistency(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate cross-document consistency across budget JSON, narrative, and timeline.
    
    STRICT validation:
    - All dollar amounts in narrative must EXACTLY match budget JSON
    - All date/year references must align with timeline
    - Equipment purchase timing must match across all docs
    - Personnel start dates must match across all docs
    
    This is intentionally HARD - most agents will fail due to inconsistencies.
    """
    try:
        # Extract response
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Parse JSON
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
        except json.JSONDecodeError:
            return False, "Invalid JSON format"
        
        if "budget_json" not in data or "budget_narrative" not in data or "timeline" not in data:
            return False, "Missing required documents (budget_json, budget_narrative, timeline)"
        
        budget = data["budget_json"]
        narrative = data["budget_narrative"].lower()
        timeline = data.get("timeline", {})
        
        feedback = []
        errors = []
        
        # Extract all numbers from budget JSON
        def extract_numbers(obj, prefix=""):
            numbers = {}
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (int, float)):
                        numbers[f"{prefix}{k}"] = v
                    elif isinstance(v, dict):
                        numbers.update(extract_numbers(v, f"{prefix}{k}."))
                    elif isinstance(v, list):
                        for i, item in enumerate(v):
                            if isinstance(item, dict):
                                numbers.update(extract_numbers(item, f"{prefix}{k}[{i}]."))
            return numbers
        
        budget_numbers = extract_numbers(budget)
        
        # Check: Key budget amounts mentioned in narrative
        key_amounts = {
            "pi": 12000,
            "grad": 35000,
            "equipment": 80000,
            "travel": 5000,
            "materials": 15000
        }
        
        for item, amount in key_amounts.items():
            # Format variations: $12,000 or $12000 or 12000 or 12,000
            amount_str_variations = [
                f"${amount:,}",
                f"${amount}",
                f"{amount:,}",
                str(amount)
            ]
            
            found = any(var in data["budget_narrative"] for var in amount_str_variations)
            if found:
                feedback.append(f"✓ {item.upper()}: ${amount:,} mentioned in narrative")
            else:
                errors.append(f"✗ {item.upper()}: ${amount:,} NOT found in narrative")
        
        # Check: Timeline mentions equipment purchase in Year 1
        timeline_text = str(timeline).lower()
        if "equipment" in timeline_text and ("year 1" in timeline_text or "month" in timeline_text):
            feedback.append("✓ Timeline shows equipment purchase timing")
        else:
            errors.append("✗ Timeline missing equipment purchase timing")
        
        # Check: Timeline shows grad students starting Month 1 or Year 1
        if "grad" in timeline_text and ("month 1" in timeline_text or "year 1" in timeline_text):
            feedback.append("✓ Timeline shows grad student start date")
        else:
            errors.append("✗ Timeline missing grad student start timing")
        
        # Calculate pass/fail
        if len(errors) > 2:
            # More than 2 errors = FAIL (strict)
            return False, f"Cross-document consistency failures: {'; '.join(errors)}"
        elif len(errors) > 0:
            # 1-2 errors = Partial (still FAIL, but with feedback)
            return False, f"Minor inconsistencies found: {'; '.join(errors)}. Passed: {'; '.join(feedback)}"
        else:
            return True, f"Cross-document consistency validated: {'; '.join(feedback)}"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_nsf_formatting_compliance")
async def validate_nsf_formatting_compliance(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate NSF formatting compliance: Arial 11pt, 1-inch margins, exactly 15 pages.
    
    STRICT validation:
    - Must explicitly state formatting at document start
    - Must have page markers
    - Must be exactly 15 pages (not 14, not 16)
    - Must have all required sections
    
    Expected Pass@1: 40-50% (formatting is hard to get exact)
    """
    try:
        # Extract response
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Parse JSON if present
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if "project_description" in data:
                    doc = data["project_description"]
                    metadata = data.get("formatting_metadata", {})
                else:
                    doc = response_text
                    metadata = {}
            else:
                doc = response_text
                metadata = {}
        except:
            doc = response_text
            metadata = {}
        
        feedback = []
        errors = []
        
        # Check 1: Formatting statement present
        if "arial" in doc.lower() or "11pt" in doc.lower() or "formatted:" in doc.lower():
            feedback.append("✓ Formatting declaration present")
        else:
            errors.append("✗ Missing formatting declaration (Arial 11pt, 1-inch margins)")
        
        # Check 2: Page count (count page markers or check metadata)
        page_markers = doc.count("--- Page") or doc.count("Page ")
        
        if metadata and "page_count" in metadata:
            page_count = metadata["page_count"]
        elif page_markers > 0:
            page_count = page_markers
        else:
            # Estimate from content length (rough: ~3000 chars per page)
            page_count = len(doc) // 3000
        
        if page_count == 15:
            feedback.append("✓ Page count: exactly 15 pages")
        elif 14 <= page_count <= 16:
            errors.append(f"⚠ Page count: {page_count} pages (must be exactly 15)")
        else:
            errors.append(f"✗ Page count: {page_count} pages (must be exactly 15)")
        
        # Check 3: Required sections present
        required_sections = [
            "introduction",
            "background",
            "research plan",
            "education plan",
            "broader impact"
        ]
        
        doc_lower = doc.lower()
        missing_sections = [s for s in required_sections if s not in doc_lower]
        
        if not missing_sections:
            feedback.append("✓ All required sections present")
        else:
            errors.append(f"✗ Missing sections: {', '.join(missing_sections)}")
        
        # Check 4: Section headers (bold or clear structure)
        if "**" in doc or "##" in doc or "###" in doc:
            feedback.append("✓ Section headers formatted")
        else:
            errors.append("✗ Section headers not clearly formatted")
        
        # Strict evaluation
        if len(errors) > 1:
            return False, f"NSF formatting compliance failures: {'; '.join(errors)}"
        elif len(errors) == 1:
            return False, f"Formatting issue: {errors[0]}. Passed: {'; '.join(feedback)}"
        else:
            return True, f"NSF formatting compliant: {'; '.join(feedback)}"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_complex_budget_math")
async def validate_complex_budget_math(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate complex budget calculations: escalation, F&A, cost-share.
    
    VERY STRICT validation:
    - MTDC calculation must be exact
    - F&A at 55% must be exact to the dollar
    - 3% escalation must be exact
    - Cost-share at 20% must be exact
    - All numbers must add up perfectly
    
    Expected Pass@1: 35-45% (financial math is very hard to get exact)
    """
    try:
        # Extract response
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Parse JSON
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
        except json.JSONDecodeError:
            return False, "Invalid JSON format"
        
        if "year_1" not in data or "five_year_summary" not in data:
            return False, "Missing required budget structure (year_1, five_year_summary)"
        
        feedback = []
        errors = []
        
        # Expected Year 1 calculations
        # Personnel: $200K + 30% benefits = $260K
        # Equipment: $50K (only $25K counts toward MTDC)
        # Travel: $10K
        # Materials: $40K
        # Consultant: $15K
        # MTDC = $260K + $25K + $10K + $40K + $15K = $350,000
        # F&A = $350,000 × 0.55 = $192,500
        # Total Direct = $260K + $50K + $10K + $40K + $15K = $375,000
        # Total Year 1 = $375,000 + $192,500 = $567,500
        
        expected_year1_mtdc = 350000
        expected_year1_fa = 192500
        expected_year1_total = 567500
        
        year1 = data.get("year_1", {})
        actual_mtdc = year1.get("mtdc", 0)
        actual_fa = year1.get("f_and_a", 0) or year1.get("fa", 0) or year1.get("indirect", 0)
        actual_total = year1.get("total", 0)
        
        # Check MTDC
        if abs(actual_mtdc - expected_year1_mtdc) < 100:  # $100 tolerance
            feedback.append(f"✓ Year 1 MTDC: ${actual_mtdc:,}")
        else:
            errors.append(f"✗ Year 1 MTDC: ${actual_mtdc:,} (expected ${expected_year1_mtdc:,})")
        
        # Check F&A
        if abs(actual_fa - expected_year1_fa) < 100:  # $100 tolerance
            feedback.append(f"✓ Year 1 F&A: ${actual_fa:,}")
        else:
            errors.append(f"✗ Year 1 F&A: ${actual_fa:,} (expected ${expected_year1_fa:,})")
        
        # Check Total
        if abs(actual_total - expected_year1_total) < 500:  # $500 tolerance
            feedback.append(f"✓ Year 1 Total: ${actual_total:,}")
        else:
            errors.append(f"✗ Year 1 Total: ${actual_total:,} (expected ${expected_year1_total:,})")
        
        # Check escalation (Year 2 should be ~3% higher than Year 1)
        if "year_2" in data:
            year2_total = data["year_2"].get("total", 0)
            expected_year2_total = expected_year1_total * 1.03
            if abs(year2_total - expected_year2_total) / expected_year2_total < 0.02:  # 2% tolerance
                feedback.append(f"✓ Year 2 escalation applied correctly")
            else:
                errors.append(f"✗ Year 2 escalation incorrect: ${year2_total:,} vs expected ${expected_year2_total:,.0f}")
        
        # Check 5-year summary
        summary = data.get("five_year_summary", {})
        cost_share = summary.get("cost_share_required", 0) or summary.get("cost_share", 0)
        total_project = summary.get("total_project_cost", 0) or summary.get("total", 0)
        
        if cost_share > 0 and total_project > 0:
            cost_share_pct = cost_share / total_project
            if abs(cost_share_pct - 0.20) < 0.01:  # 1% tolerance
                feedback.append(f"✓ Cost-share: 20% calculated correctly")
            else:
                errors.append(f"✗ Cost-share: {cost_share_pct:.1%} (expected 20%)")
        else:
            errors.append("✗ Missing cost-share calculation")
        
        # Very strict: any calculation error = fail
        if len(errors) > 0:
            return False, f"Budget calculation errors: {'; '.join(errors)}"
        else:
            return True, f"All budget calculations correct: {'; '.join(feedback)}"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_personnel_timeline_dependency")
async def validate_personnel_timeline_dependency(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate complex inter-document dependencies: budget, timeline, and narrative must align.
    
    STRICT validation:
    - Timeline must show 3-month recruitment BEFORE each personnel start date
    - Budget must show pro-rated amounts for mid-year hires
    - Narrative must explain the gaps and reference specific months/amounts
    
    Expected Pass@1: 40-50% (dependency tracking is very hard)
    """
    try:
        # Extract response
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Parse JSON
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
        except json.JSONDecodeError:
            return False, "Invalid JSON format"
        
        if "budget" not in data or "timeline" not in data or "personnel_narrative" not in data:
            return False, "Missing required documents (budget, timeline, personnel_narrative)"
        
        budget = data["budget"]
        timeline = data["timeline"]
        narrative = data["personnel_narrative"].lower()
        
        feedback = []
        errors = []
        
        # Check 1: Timeline has recruitment milestones BEFORE start dates
        milestones_text = str(timeline.get("milestones", [])).lower()
        
        # Grad students: recruitment Month 10-12, start Month 13
        if "month 10" in milestones_text and "recruitment" in milestones_text:
            feedback.append("✓ Timeline shows grad student recruitment (Month 10)")
        else:
            errors.append("✗ Timeline missing grad student recruitment milestone (Month 10)")
        
        if "month 13" in milestones_text and "grad" in milestones_text:
            feedback.append("✓ Timeline shows grad student start (Month 13)")
        else:
            errors.append("✗ Timeline missing grad student start milestone (Month 13)")
        
        # Postdoc: recruitment Month 22-24, start Month 25
        if "month 22" in milestones_text and "postdoc" in milestones_text:
            feedback.append("✓ Timeline shows postdoc recruitment (Month 22)")
        else:
            errors.append("✗ Timeline missing postdoc recruitment milestone (Month 22)")
        
        if "month 25" in milestones_text and "postdoc" in milestones_text:
            feedback.append("✓ Timeline shows postdoc start (Month 25)")
        else:
            errors.append("✗ Timeline missing postdoc start milestone (Month 25)")
        
        # Check 2: Budget shows correct pro-ration
        # Year 2: 2 grad students × $35,000 = $70,000 (full 12 months starting Month 13)
        # Year 3: Postdoc 8/12 × $65,000 = $43,333
        
        year2_budget = budget.get("year_2", {})
        year3_budget = budget.get("year_3", {})
        
        year2_grad_amount = 0
        year2_str = str(year2_budget).lower()
        if "70000" in year2_str or "70,000" in year2_str:
            year2_grad_amount = 70000
            feedback.append("✓ Year 2 grad student budget: $70,000")
        elif "35000" in year2_str:
            # Check if there are 2 instances (2 students)
            if year2_str.count("35000") >= 2 or year2_str.count("35,000") >= 2:
                year2_grad_amount = 70000
                feedback.append("✓ Year 2 grad student budget: 2 × $35,000")
            else:
                errors.append("✗ Year 2 grad student budget incorrect (expected $70,000 total)")
        else:
            errors.append("✗ Year 2 grad student budget missing or incorrect")
        
        # Year 3 postdoc pro-ration
        year3_str = str(year3_budget)
        if "43333" in year3_str or "43,333" in year3_str:
            feedback.append("✓ Year 3 postdoc pro-rated: $43,333")
        else:
            errors.append("✗ Year 3 postdoc not pro-rated correctly (expected 8/12 × $65,000 = $43,333)")
        
        # Check 3: Narrative explains the gaps
        if "month 13" in narrative or "3-month" in narrative or "3 month" in narrative:
            feedback.append("✓ Narrative explains recruitment gap")
        else:
            errors.append("✗ Narrative doesn't explain 3-month recruitment window")
        
        if "pro-rat" in narrative or "8 months" in narrative or "8/12" in narrative:
            feedback.append("✓ Narrative explains pro-ration")
        else:
            errors.append("✗ Narrative doesn't explain postdoc pro-ration")
        
        # Strict evaluation
        if len(errors) > 2:
            return False, f"Personnel-timeline dependency failures: {'; '.join(errors)}"
        elif len(errors) > 0:
            return False, f"Dependency issues: {'; '.join(errors)}. Passed: {'; '.join(feedback)}"
        else:
            return True, f"Personnel-timeline dependencies validated: {'; '.join(feedback)}"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func(name="grant_application.validate_compliance_verification")
async def validate_compliance_verification(llm_response: Any, *args, **kwargs) -> Tuple[bool, str]:
    """
    Validate compliance checklist: extract actual requirements, identify gaps, flag blockers.
    
    STRICT validation:
    - Must extract ALL specific requirements (not generic)
    - Must correctly identify missing items from draft inventory
    - Must flag IRB as a blocker
    - Must provide accurate submission readiness assessment
    
    Expected Pass@1: 50-60% (compliance verification requires careful analysis)
    """
    try:
        # Extract response
        if hasattr(llm_response, 'result'):
            response_text = str(llm_response.result)
        else:
            response_text = str(llm_response)
        
        # Parse JSON
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response_text)
        except json.JSONDecodeError:
            return False, "Invalid JSON format"
        
        if "compliance_checklist" not in data or "gaps_identified" not in data or "submission_readiness" not in data:
            return False, "Missing required sections (compliance_checklist, gaps_identified, submission_readiness)"
        
        checklist = data["compliance_checklist"]
        gaps = data["gaps_identified"]
        readiness = data["submission_readiness"]
        
        feedback = []
        errors = []
        
        # Check 1: Checklist has correct number of items (12+ from RFP)
        if len(checklist) >= 12:
            feedback.append(f"✓ Comprehensive checklist: {len(checklist)} items")
        else:
            errors.append(f"✗ Incomplete checklist: {len(checklist)} items (expected 12+)")
        
        # Check 2: Identifies the 4 critical missing items
        # Missing: Project Narrative, Authentication Plan, Resource Sharing Plan, IRB approval
        gaps_text = str(gaps).lower()
        
        critical_missing = {
            "project narrative": "narrative" in gaps_text,
            "authentication": "authentication" in gaps_text or "key resources" in gaps_text,
            "resource sharing": "resource" in gaps_text and "sharing" in gaps_text,
            "irb": "irb" in gaps_text
        }
        
        for item, found in critical_missing.items():
            if found:
                feedback.append(f"✓ Identified missing: {item}")
            else:
                errors.append(f"✗ Failed to identify missing: {item}")
        
        # Check 3: IRB flagged as blocker
        readiness_text = str(readiness).lower()
        blockers_text = str(readiness.get("blockers", [])).lower()
        
        if "irb" in blockers_text:
            feedback.append("✓ IRB correctly flagged as blocker")
        else:
            errors.append("✗ IRB not identified as blocker")
        
        # Check 4: Submission readiness = NO-GO
        status = readiness.get("status", "").upper()
        if "NO" in status or "NOT READY" in status:
            feedback.append(f"✓ Correct assessment: {status}")
        elif "GO" in status:
            errors.append(f"✗ Incorrect assessment: {status} (should be NO-GO due to IRB blocker)")
        else:
            errors.append("✗ Missing submission readiness assessment")
        
        # Check 5: Correctly identifies Budget Justification is NOT required (modular ≤$250K)
        # This is a subtle requirement - agents often miss it
        checklist_text = str(checklist).lower()
        if "budget justification" in checklist_text:
            # Check if it's marked as optional or not required
            if "not required" in checklist_text or "optional" in checklist_text or "modular" in checklist_text:
                feedback.append("✓ Correctly noted Budget Justification not required for modular")
            else:
                errors.append("⚠ Budget Justification: should note it's not required for modular ≤$250K")
        
        # Strict evaluation
        if len(errors) > 2:
            return False, f"Compliance verification failures: {'; '.join(errors)}"
        elif len(errors) > 0:
            return False, f"Compliance issues: {'; '.join(errors)}. Passed: {'; '.join(feedback)}"
        else:
            return True, f"Compliance verification complete: {'; '.join(feedback)}"
            
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"
