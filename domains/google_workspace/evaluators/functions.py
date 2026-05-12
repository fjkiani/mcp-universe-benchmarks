"""
Evaluation functions for Google Slides tasks
"""
# pylint: disable=broad-exception-caught,unused-argument
import os
import json
from pathlib import Path
from typing import Any, Tuple
import google.auth
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from lbx_cli.mcpuniverse.evaluator.functions import compare_func, FunctionResult

# Constants (same as server.py)
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']

# Get project root (4 levels up from domains/google_slides/evaluators/functions.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Environment variables for configuration (same as server.py)
TOKEN_PATH = os.environ.get('TOKEN_PATH', str(PROJECT_ROOT / 'token.json'))
CREDENTIALS_PATH = os.environ.get('CREDENTIALS_PATH', str(PROJECT_ROOT / 'credentials.json'))
GOOGLE_SERVICE_ACCOUNT_PATH = os.environ.get('GOOGLE_SERVICE_ACCOUNT_PATH', str(PROJECT_ROOT / 'service_account.json'))


def get_slides_service():
    """
    Get authenticated Google Slides service.
    
    Supports multiple authentication methods in order of preference:
    1. Service account JSON file - best for automation and CI/CD
    2. Application Default Credentials (ADC) - includes Workload Identity in GCP/GitHub Actions
    3. OAuth 2.0 (user credentials) - fallback for local development
    
    Uses environment variables (same as server.py):
    - GOOGLE_SERVICE_ACCOUNT_PATH: Path to service account JSON
    - CREDENTIALS_PATH: Path to OAuth client credentials
    - TOKEN_PATH: Path to OAuth token cache
    
    Returns:
        Google Slides API service object
    
    Raises:
        ValueError: If no authentication method is available
    """
    creds = None
    
    # Method 1: Try service account file first (PRIMARY - best for CI/CD and automation)
    if os.path.exists(GOOGLE_SERVICE_ACCOUNT_PATH):
        try:
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_SERVICE_ACCOUNT_PATH,
                scopes=SCOPES
            )
            print(f"✅ Using service account authentication: {GOOGLE_SERVICE_ACCOUNT_PATH}")
            return build('slides', 'v1', credentials=creds)
        except Exception as e:
            print(f"⚠️  Service account authentication failed: {e}")
            print("   Falling back to other methods...")
    
    # Method 2: Try Application Default Credentials (for CI/CD with Workload Identity)
    try:
        creds, project = google.auth.default(scopes=SCOPES)
        print(f"✅ Using Application Default Credentials (project: {project})")
        return build('slides', 'v1', credentials=creds)
    except google.auth.exceptions.DefaultCredentialsError:
        print("⚠️  No Application Default Credentials found")
    except Exception as e:
        print(f"⚠️  ADC failed: {e}")
    
    # Method 3: Fallback to OAuth flow (for local development)
    if os.path.exists(CREDENTIALS_PATH):
        try:
            print("🔐 Using OAuth authentication flow...")
            
            # Load existing token
            if os.path.exists(TOKEN_PATH):
                try:
                    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
                except Exception as e:
                    print(f"⚠️  Could not load token: {e}")
            
            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    # Refresh the token
                    try:
                        print("🔄 Refreshing OAuth token...")
                        creds.refresh(Request())
                        print("✅ Token refreshed")
                    except Exception as e:
                        print(f"⚠️  Could not refresh token: {e}")
                        creds = None
                
                # Run OAuth flow if needed
                if not creds:
                    print("   A browser window will open for you to authorize access.")
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                        creds = flow.run_local_server(port=0)
                        print("✅ OAuth authentication successful!")
                        
                        # Save the credentials for next time
                        with open(TOKEN_PATH, 'w') as token:
                            token.write(creds.to_json())
                        print(f"💾 Token saved to {TOKEN_PATH}")
                    except Exception as e:
                        print(f"❌ OAuth flow failed: {e}")
                        creds = None
            
            if creds:
                print(f"✅ Using OAuth 2.0 credentials")
                return build('slides', 'v1', credentials=creds)
        except Exception as e:
            print(f"⚠️  OAuth authentication failed: {e}")
    
    # No authentication method available
    error_msg = (
        "❌ No authentication method available for Google Slides API.\n\n"
        "Please set up one of the following:\n\n"
        "1. Service account (RECOMMENDED for CI/CD):\n"
        f"   - Set GOOGLE_SERVICE_ACCOUNT_PATH={GOOGLE_SERVICE_ACCOUNT_PATH}\n"
        f"   - File exists: {os.path.exists(GOOGLE_SERVICE_ACCOUNT_PATH)}\n\n"
        "2. Application Default Credentials:\n"
        "   - In GitHub Actions: Use google-github-actions/auth@v2\n"
        "   - Locally: Run `gcloud auth application-default login`\n\n"
        "3. OAuth 2.0 (for local development):\n"
        f"   - Set CREDENTIALS_PATH={CREDENTIALS_PATH}\n"
        f"   - File exists: {os.path.exists(CREDENTIALS_PATH)}\n"
        f"   - Token path: {TOKEN_PATH}\n"
        f"   - Token exists: {os.path.exists(TOKEN_PATH)}\n\n"
        "Environment variables:\n"
        f"  GOOGLE_SERVICE_ACCOUNT_PATH={GOOGLE_SERVICE_ACCOUNT_PATH}\n"
        f"  CREDENTIALS_PATH={CREDENTIALS_PATH}\n"
        f"  TOKEN_PATH={TOKEN_PATH}"
    )
    raise ValueError(error_msg)


def get_presentation_content(presentation_id: str) -> str:
    """
    Get the content of a Google Slides presentation.

    Args:
        presentation_id: The ID of the presentation

    Returns:
        JSON string containing the presentation content
    """
    try:
        service = get_slides_service()
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        print('Got presentation content')
        # Extract slides content
        slides_content = []
        for slide in presentation.get('slides', []):
            slide_data = {
                'slide_id': slide.get('objectId', ''),
                'page_elements': []
            }

            # Process page elements (text boxes, shapes, etc.)
            for element in slide.get('pageElements', []):
                element_data = {
                    'element_id': element.get('objectId', ''),
                    'element_type': None,
                    'content': '',
                    'position': element.get('transform', {})
                }

                # Handle text elements
                if 'shape' in element:
                    shape = element['shape']
                    if 'text' in shape and 'textElements' in shape['text']:
                        text_content = ""
                        for text_element in shape['text']['textElements']:
                            if 'textRun' in text_element:
                                text_content += text_element['textRun'].get('content', '')
                        element_data['element_type'] = 'text'
                        element_data['content'] = text_content.strip()

                # Handle images
                elif 'image' in element:
                    element_data['element_type'] = 'image'
                    element_data['content'] = element['image'].get('sourceUrl', '')

                # Handle tables
                elif 'table' in element:
                    element_data['element_type'] = 'table'
                    table_data = []
                    for row in element['table'].get('tableRows', []):
                        row_data = []
                        for cell in row.get('tableCells', []):
                            cell_text = ""
                            for text_element in cell.get('text', {}).get('textElements', []):
                                if 'textRun' in text_element:
                                    cell_text += text_element['textRun'].get('content', '')
                            row_data.append(cell_text.strip())
                        table_data.append(row_data)
                    element_data['content'] = table_data

                slide_data['page_elements'].append(element_data)

            slides_content.append(slide_data)
        return json.dumps({
            "presentation_id": presentation_id,
            "title": presentation.get('title', ''),
            "slides": slides_content,
            "slide_count": len(slides_content)
        })
    except Exception as e:
        error_msg = str(e)
        if "insufficient authentication scopes" in error_msg.lower():
            print(f"❌ Error: Insufficient authentication scopes for Google Slides API")
            print(f"   Run this command to fix:")
            print(f"   gcloud auth application-default login --scopes=https://www.googleapis.com/auth/presentations")
        print(f"Error getting presentation content: {e}")
        return ""


def get_presentation_title(presentation_id: str) -> str:
    """
    Get the title of a Google Slides presentation.

    Args:
        presentation_id: The ID of the presentation

    Returns:
        The presentation title
    """
    try:
        service = get_slides_service()
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        return presentation.get('title', '')
    except Exception as e:
        print(f"Error getting presentation title: {e}")
        return ""


@compare_func(name="google_slides.check_presentation_creation")
async def check_presentation_creation(llm_response: Any, expected_values: Any, op_args: Any, **kwargs) -> Tuple[bool, str]:
    """
    Check if a Google Slides presentation was successfully created.

    This evaluator checks:
    1. The agent provides a presentation ID
    2. The presentation exists and is accessible
    3. The presentation has a reasonable title
    4. The presentation has some content (if expected)

    Args:
        llm_response: The agent's response
        expected_values: Expected values (not used)
        op_args: Configuration dict with:
            - expected_title_pattern: Pattern that should match the presentation title (optional)
            - require_content: Whether the presentation must have content (default: True)
            - min_slides: Minimum number of slides if content is required (default: 1)

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    # Extract the actual response
    if hasattr(llm_response, 'result'):
        user_output_dict = llm_response.result
    else:
        user_output_dict = llm_response
    
    # Parse JSON if it's a string
    if isinstance(user_output_dict, str):
        try:
            import json
            user_output_dict = json.loads(user_output_dict)
        except json.JSONDecodeError:
            pass

    # Extract configuration
    expected_title_pattern = op_args.get('expected_title_pattern', '')
    require_content = op_args.get('require_content', True)
    min_slides = op_args.get('min_slides', 1)

    # Check format - expect presentation_id in output
    if 'presentation_id' not in user_output_dict:
        return False, "Output format error: Missing key 'presentation_id'. Agent should provide the ID of the created presentation."

    presentation_id = user_output_dict['presentation_id']

    # Validate presentation_id format (should be a non-empty string)
    if not isinstance(presentation_id, str) or not presentation_id.strip():
        return False, f"Invalid presentation_id: Expected non-empty string, got {presentation_id}"

    # Try to get the presentation info
    try:
        title = get_presentation_title(presentation_id)
        content = get_presentation_content(presentation_id)

        if not title:
            return False, f"Presentation {presentation_id} does not exist or is not accessible"

        # Check title pattern if provided
        if expected_title_pattern:
            if expected_title_pattern.lower() not in title.lower():
                return False, f"Presentation title '{title}' does not match expected pattern '{expected_title_pattern}'"

        # Check content if required
        if require_content:
            if not content:
                return False, f"Presentation has no content or is not accessible"

            # Parse content to check slide count
            try:
                content_data = json.loads(content)
                slide_count = content_data.get('slide_count', 0)
                if slide_count < min_slides:
                    return False, f"Presentation has only {slide_count} slides, expected at least {min_slides}"
            except json.JSONDecodeError:
                return False, f"Could not parse presentation content"

        # Success!
        return True, f"Presentation created successfully. Title: '{title}', Content accessible"

    except Exception as e:
        return False, f"Error accessing presentation {presentation_id}: {str(e)}. Make sure the service account has access to this presentation."


@compare_func(name="google_slides.check_presentation_content")
async def check_presentation_content(llm_response: Any, expected_values: Any, op_args: Any, **kwargs) -> Tuple[bool, str]:
    """
    Check if a Google Slides presentation contains expected content.

    This evaluator checks:
    1. The agent provides a presentation ID
    2. The presentation exists and is accessible
    3. The presentation contains expected text content
    4. The presentation has the expected number of slides

    Args:
        llm_response: The agent's response
        expected_values: Expected values (not used)
        op_args: Configuration dict with:
            - expected_text: Text that should be present in the presentation
            - case_sensitive: Whether text matching should be case sensitive (default: False)
            - min_slides: Minimum expected number of slides (default: 1)
            - expected_slides: Exact number of slides expected (optional)

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    # Extract the actual response
    if hasattr(llm_response, 'result'):
        user_output_dict = llm_response.result
    else:
        user_output_dict = llm_response
    
    # Parse JSON if it's a string
    if isinstance(user_output_dict, str):
        try:
            import json
            user_output_dict = json.loads(user_output_dict)
        except json.JSONDecodeError:
            pass

    # Extract configuration
    expected_text = op_args.get('expected_text', '')
    case_sensitive = op_args.get('case_sensitive', False)
    min_slides = op_args.get('min_slides', 1)
    expected_slides = op_args.get('expected_slides', None)

    # Check format - expect presentation_id in output
    if 'presentation_id' not in user_output_dict:
        return False, "Output format error: Missing key 'presentation_id'. Agent should provide the ID of the presentation."

    presentation_id = user_output_dict['presentation_id']

    # Validate presentation_id format (should be a non-empty string)
    if not isinstance(presentation_id, str) or not presentation_id.strip():
        return False, f"Invalid presentation_id: Expected non-empty string, got {presentation_id}"

    # Try to get the presentation content
    try:
        content = get_presentation_content(presentation_id)

        if not content:
            return False, f"Presentation {presentation_id} is empty or not accessible"

        # Parse the content
        try:
            content_data = json.loads(content)
        except json.JSONDecodeError:
            return False, f"Could not parse presentation content for {presentation_id}"

        # Check slide count
        slide_count = content_data.get('slide_count', 0)
        if slide_count < min_slides:
            return False, f"Presentation has only {slide_count} slides, expected at least {min_slides}"

        if expected_slides is not None and slide_count != expected_slides:
            return False, f"Presentation has {slide_count} slides, expected exactly {expected_slides}"

        # Check for expected text if provided
        if expected_text:
            # Combine title and all slide content for text search
            full_text = content_data.get('title', '') + ' ' + str(content_data.get('slides', []))

            if case_sensitive:
                text_found = expected_text in full_text
            else:
                text_found = expected_text.lower() in full_text.lower()

            if not text_found:
                return False, f"Expected text '{expected_text}' not found in presentation. Content preview: {full_text[:200]}..."

        # Success!
        return True, f"Presentation content verified. Slides: {slide_count}, Content accessible"

    except Exception as e:
        return False, f"Error accessing presentation {presentation_id}: {str(e)}. Make sure the service account has access to this presentation."


@compare_func(name="google_slides.evaluate_faang_presentation")
async def evaluate_faang_presentation(llm_response: Any, expected_values: Any, op_args: Any, **kwargs) -> Tuple[bool, str]:
    """
    Evaluate a FAANG companies presentation for completeness.

    This evaluator checks:
    1. The agent provides a presentation ID
    2. The presentation exists and is accessible
    3. FAANG-related content is present
    4. Financial data is included
    5. The presentation has sufficient slides

    Args:
        llm_response: The agent's response (FunctionResult with .result attribute)
        expected_values: Expected values (not used)
        op_args: Configuration dict with:
            - min_slides: Minimum number of slides expected (default: 5)
            - require_financial_data: Whether financial data is required (default: True)

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    # Extract the actual response
    if hasattr(llm_response, 'result'):
        user_output_dict = llm_response.result
    else:
        user_output_dict = llm_response
    
    # Parse JSON if it's a string
    if isinstance(user_output_dict, str):
        try:
            user_output_dict = json.loads(user_output_dict)
        except json.JSONDecodeError:
            pass  # Keep as string if not valid JSON

    # Extract configuration
    min_slides = op_args.get('min_slides', 5)
    require_financial_data = op_args.get('require_financial_data', True)

    # Check format - expect presentation_id in output
    if 'presentation_id' not in user_output_dict:
        return False, "Output format error: Missing key 'presentation_id'. Agent should provide the ID of the FAANG presentation."

    presentation_id = user_output_dict['presentation_id']

    # Validate presentation_id format (should be a non-empty string)
    if not isinstance(presentation_id, str) or not presentation_id.strip():
        return False, f"Invalid presentation_id: Expected non-empty string, got {presentation_id}"

    # Try to get the presentation content
    try:
        content = get_presentation_content(presentation_id)

        if not content:
            return False, f"Presentation {presentation_id} is empty or not accessible"

        # Parse the content
        try:
            content_data = json.loads(content)
        except json.JSONDecodeError:
            return False, f"Could not parse presentation content for {presentation_id}"

        # Check slide count
        slide_count = content_data.get('slide_count', 0)
        if slide_count < min_slides:
            return False, f"FAANG presentation has only {slide_count} slides, expected at least {min_slides}"

        # Check for FAANG companies (basic check without specific list)
        full_text = content_data.get('title', '') + ' ' + str(content_data.get('slides', []))
        faang_keywords = ['meta', 'facebook', 'apple', 'amazon', 'netflix', 'google', 'alphabet', 'faang']
        found_keywords = []
        for keyword in faang_keywords:
            if keyword.lower() in full_text.lower():
                found_keywords.append(keyword)

        if not found_keywords:
            return False, f"No FAANG-related content found in presentation. Expected keywords like: {faang_keywords}"

        # Check for financial terms if required
        if require_financial_data:
            financial_terms = ['revenue', 'profit', 'earnings', 'market cap', 'stock', 'financial', 'quarterly', 'annual', 'billion', 'million']
            found_financial_terms = []
            for term in financial_terms:
                if term.lower() in full_text.lower():
                    found_financial_terms.append(term)

            if not found_financial_terms:
                return False, f"No financial data found in presentation. Expected terms like: {financial_terms}"

        # Check for structured content (slides should have elements)
        slides = content_data.get('slides', [])
        slides_with_content = 0
        for slide in slides:
            if slide.get('page_elements') and len(slide['page_elements']) > 0:
                slides_with_content += 1

        if slides_with_content < min_slides:
            return False, f"Only {slides_with_content} slides have content, expected at least {min_slides}"

        # Success!
        return True, f"FAANG presentation verified. Keywords found: {found_keywords}, Slides: {slide_count}, Content slides: {slides_with_content}"

    except Exception as e:
        return False, f"Error accessing presentation {presentation_id}: {str(e)}. Make sure the service account has access to this presentation."


@compare_func(name="google_slides.check_presentation_list")
async def check_presentation_list(llm_response: Any, expected_values: Any, op_args: Any, **kwargs) -> Tuple[bool, str]:
    """
    Check if the agent successfully listed Google Slides presentations.

    Args:
        llm_response: The agent's response
        expected_values: Expected values (not used)
        op_args: Configuration dict with:
            - min_presentations: Minimum number of presentations expected (default: 1)
            - expected_titles: List of presentation titles that should be present (optional)

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    # Extract the actual response
    if hasattr(llm_response, 'result'):
        user_output_dict = llm_response.result
    else:
        user_output_dict = llm_response
    
    # Parse JSON if it's a string
    if isinstance(user_output_dict, str):
        try:
            user_output_dict = json.loads(user_output_dict)
        except json.JSONDecodeError:
            pass

    # Extract configuration
    min_presentations = op_args.get('min_presentations', 1)
    expected_titles = op_args.get('expected_titles', [])

    # Check if the output contains presentation information
    # The agent might return the raw JSON or parse it into a more readable format
    if 'presentations' in user_output_dict:
        presentations = user_output_dict['presentations']
    elif 'presentation_list' in user_output_dict:
        presentations = user_output_dict['presentation_list']
    else:
        return False, "Output format error: Missing presentation list. Expected 'presentations' or 'presentation_list' key."

    if not isinstance(presentations, list):
        return False, f"Presentation list should be an array, got {type(presentations)}"

    # Check minimum number of presentations
    if len(presentations) < min_presentations:
        return False, f"Expected at least {min_presentations} presentations, found {len(presentations)}"

    # Check for expected titles if provided
    if expected_titles:
        found_titles = []
        for pres in presentations:
            if isinstance(pres, dict) and 'title' in pres:
                found_titles.append(pres['title'])
            elif isinstance(pres, str):
                found_titles.append(pres)

        missing_titles = []
        for expected_title in expected_titles:
            if not any(expected_title.lower() in found_title.lower() for found_title in found_titles):
                missing_titles.append(expected_title)

        if missing_titles:
            return False, f"Expected presentation titles not found: {missing_titles}. Found titles: {found_titles}"

    return True, f"Presentation list verified. Found {len(presentations)} presentations"
