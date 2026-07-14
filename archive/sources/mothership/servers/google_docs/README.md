# Google Docs MCP Server

A Model Context Protocol (MCP) server for interacting with Google Docs. This server provides tools to create, read, update, and manage Google Documents.

## Features

- **List Documents**: List all Google Documents in a specified folder or "My Drive"
- **Read Content**: Get the full content of a document
- **Create Documents**: Create new Google Documents with optional initial content
- **Update Content**: Replace all content in a document
- **Append Content**: Add content to the end of a document
- **Insert Text**: Insert text at specific positions
- **Replace Text**: Find and replace text throughout a document
- **Copy Documents**: Create copies of existing documents
- **Delete Documents**: Remove documents
- **Share Documents**: Share documents with specific email addresses
- **Get Document Info**: Retrieve metadata about documents

## Authentication

The server supports two authentication methods:

### Service Account (Recommended)
Set the `SERVICE_ACCOUNT_PATH` environment variable to point to your service account JSON file:

```bash
export SERVICE_ACCOUNT_PATH="/path/to/your/service-account.json"
```

### OAuth Flow
If no service account is provided, the server will use OAuth flow:
1. Set `CREDENTIALS_PATH` to your OAuth credentials file
2. The server will handle the OAuth flow and save tokens

## Environment Variables

- `SERVICE_ACCOUNT_PATH`: Path to service account JSON file
- `CREDENTIALS_PATH`: Path to OAuth credentials file (default: `credentials.json`)
- `TOKEN_PATH`: Path to store OAuth tokens (default: `token.json`)
- `DRIVE_FOLDER_ID`: Google Drive folder ID to work within (optional)

## Required Scopes

The server requires the following Google API scopes:
- `https://www.googleapis.com/auth/documents` - Read and write access to Google Docs
- `https://www.googleapis.com/auth/drive` - Access to Google Drive for file management

## Installation

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

## Usage

Run the server:

```bash
python -m mcpuniverse.mcp.servers.google_docs
```

Or with specific transport:

```bash
python -m mcpuniverse.mcp.servers.google_docs --transport stdio
```

## Available Tools

### `get_document_content`
Get the content of a Google Document.

**Parameters:**
- `document_id` (string): The ID of the document

**Returns:** JSON object with document content and metadata

### `update_document_content`
Replace all content in a Google Document.

**Parameters:**
- `document_id` (string): The ID of the document
- `content` (string): The new content to insert

### `append_to_document`
Add content to the end of a Google Document.

**Parameters:**
- `document_id` (string): The ID of the document
- `content` (string): The content to append

### `insert_text_at_position`
Insert text at a specific position in a Google Document.

**Parameters:**
- `document_id` (string): The ID of the document
- `content` (string): The content to insert
- `position` (integer): The character position to insert at (0-based)

### `replace_text`
Replace all occurrences of specific text in a Google Document.

**Parameters:**
- `document_id` (string): The ID of the document
- `search_text` (string): The text to search for and replace
- `replacement_text` (string): The text to replace it with

### `create_document`
Create a new Google Document.

**Parameters:**
- `title` (string): The title of the new document
- `content` (string, optional): Initial content for the document

### `list_documents`
List all Google Documents in a Google Drive folder.

**Parameters:**
- `folder_id` (string, optional): Google Drive folder ID to search in

**Returns:** JSON array of documents with IDs, titles, and timestamps

**Note:** If no folder_id is provided, uses the configured Google Drive folder. If no folder is configured, lists documents from 'My Drive'

### `copy_document`
Create a copy of an existing Google Document.

**Parameters:**
- `source_document_id` (string): The ID of the source document
- `new_title` (string): The title for the new document

### `delete_document`
Delete a Google Document.

**Parameters:**
- `document_id` (string): The ID of the document to delete

### `share_document`
Share a Google Document with a specific email address.

**Parameters:**
- `document_id` (string): The ID of the document
- `email` (string): The email address to share with
- `role` (string, optional): The role to grant ('reader', 'writer', 'commenter')

### `get_document_info`
Get metadata about a Google Document.

**Parameters:**
- `document_id` (string): The ID of the document

**Returns:** JSON object with document metadata

## Error Handling

The server includes comprehensive error handling and will return detailed error messages in JSON format when operations fail. Common errors include:

- Authentication failures
- Document not found
- Permission denied
- Invalid document ID format
- API quota exceeded

## Examples

### Create and populate a document
```python
# Create a new document
result = await create_document("My New Document", "Hello, World!")

# Get the document ID
doc_id = result['document_id']

# Append more content
await append_to_document(doc_id, "\n\nThis is additional content.")
```

### Read and modify existing document
```python
# Get document content
content = await get_document_content("your-document-id")

# Replace specific text
await replace_text("your-document-id", "old text", "new text")
```

### List and manage documents
```python
# List all documents in a specific folder
docs = await list_documents("1hlaYYv7EdN2eEy0nvQR6pPWOuGFezE99")

# List all documents using configured folder
docs = await list_documents()

# Copy a document
await copy_document("source-doc-id", "Copy of Document")

# Share a document
await share_document("doc-id", "user@example.com", "writer")
```
