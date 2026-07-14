# Contributing to LBX MCP Servers

Thank you for your interest in contributing! This document provides guidelines for adding new MCP servers or improving existing ones.

## Adding a New Server

### 1. Create Server Directory

```bash
cd servers
mkdir my_new_server
cd my_new_server
```

### 2. Required Files

Every server must have:

- `pyproject.toml` - Package configuration and dependencies
- `README.md` - Server documentation
- `server.py` - Main server implementation
- `__init__.py` - Package initialization
- `__main__.py` - CLI entry point

### 3. Server Template

#### pyproject.toml

```toml
[project]
name = "lbx-mcp-my-server"
version = "1.0.0"
description = "Brief description of what your server does"
readme = "README.md"
requires-python = ">=3.12"
authors = [
    { name = "Your Name" }
]
dependencies = [
    "mcp>=1.9.4",
    "python-dotenv>=1.0.0",
    # Add your dependencies here
]

[project.scripts]
my-server = "my_server.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["my_server"]
```

#### README.md

```markdown
# My Server Name

Brief description of server functionality.

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`bash
cd my_server
pip install -e .
\`\`\`

## Configuration

\`\`\`bash
export MY_API_KEY=your_key_here
\`\`\`

## Usage

\`\`\`bash
python -m my_server
\`\`\`

## Available Tools

- `tool-name` - Tool description

## License

BSD 3-Clause
```

#### server.py

```python
"""My MCP Server implementation."""

import os
from mcp.server import Server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

load_dotenv()

# Initialize server
server = Server("my-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="my-tool",
            description="Tool description",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "my-tool":
        param = arguments.get("param")
        # Implement your logic here
        result = f"Processed: {param}"
        return [TextContent(type="text", text=result)]
    
    raise ValueError(f"Unknown tool: {name}")

def main():
    """Run the server."""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(run())

if __name__ == "__main__":
    main()
```

#### __init__.py

```python
"""My Server MCP Server."""

__version__ = "1.0.0"
```

#### __main__.py

```python
"""CLI entry point for My Server."""

from my_server.server import main

if __name__ == "__main__":
    main()
```

### 4. Testing

Add tests in `test_server.py`:

```python
"""Tests for My Server."""

import pytest
from my_server.server import server

def test_list_tools():
    """Test that tools are listed correctly."""
    tools = await server.list_tools()
    assert len(tools) > 0
    assert any(tool.name == "my-tool" for tool in tools)
```

### 5. Documentation

Your README.md should include:

- **Description**: What does the server do?
- **Features**: List key features
- **Installation**: How to install
- **Configuration**: Required environment variables/API keys
- **Usage**: How to run the server
- **Available Tools**: List all tools with descriptions
- **Examples**: Usage examples
- **Dependencies**: List special requirements
- **License**: Include license information

## Code Standards

### Python Style

- Follow PEP 8
- Use type hints
- Add docstrings for all public functions
- Keep functions focused and small

### Error Handling

```python
# Good: Specific error handling
try:
    result = api_call()
except APIError as e:
    return [TextContent(type="text", text=f"API Error: {str(e)}")]
except Exception as e:
    return [TextContent(type="text", text=f"Error: {str(e)}")]
```

### Environment Variables

```python
# Good: Use python-dotenv and provide defaults
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### Async/Await

```python
# Good: Use async for I/O operations
async def fetch_data(query: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"q": query})
        return response.json()
```

## Testing Guidelines

### Unit Tests

```python
import pytest

@pytest.mark.asyncio
async def test_tool_call():
    result = await server.call_tool("my-tool", {"param": "test"})
    assert len(result) > 0
    assert "test" in result[0].text
```

### Integration Tests

```python
@pytest.mark.integration
async def test_api_integration():
    # Test actual API calls (may require API keys)
    result = await fetch_data("test query")
    assert result is not None
```

## Dependencies

### Adding Dependencies

Add to `pyproject.toml`:

```toml
dependencies = [
    "mcp>=1.9.4",
    "python-dotenv>=1.0.0",
    "httpx>=0.28.0",  # For HTTP requests
    "your-library>=1.0.0",
]
```

### Version Pinning

- Use `>=` for minimum versions
- Pin exact versions only if necessary
- Test with latest versions

## Pull Request Process

1. **Fork** the repository
2. **Create branch**: `git checkout -b feature/my-new-server`
3. **Implement** your server following the template
4. **Test** thoroughly
5. **Document** in README
6. **Submit PR** with:
   - Clear description
   - Usage examples
   - Test results
   - Screenshots (if applicable)

### PR Checklist

- [ ] All required files present
- [ ] README.md complete
- [ ] Tests added and passing
- [ ] Dependencies documented
- [ ] Code follows style guide
- [ ] No sensitive data (API keys, etc.)
- [ ] Example usage included

## Code Review

Maintainers will review for:

- **Functionality**: Does it work correctly?
- **Code Quality**: Is it clean and maintainable?
- **Documentation**: Is it well documented?
- **Testing**: Are there adequate tests?
- **Security**: No security vulnerabilities?
- **Performance**: Reasonable performance?

## Questions?

- Check existing server implementations for examples
- Open an issue for clarification
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (BSD 3-Clause).

Thank you for contributing! 🎉

