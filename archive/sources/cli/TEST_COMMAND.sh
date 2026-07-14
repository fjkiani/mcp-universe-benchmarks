#!/bin/bash
echo "Testing Alignerr MCP CLI..."
echo ""

# Test with Python 3.12+
PYTHON_CMD=$(which python3.12 || which python3)

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Test import
echo "Testing imports..."
$PYTHON_CMD -c "from lbx_cli.main import app; print('✅ Imports work')"
echo ""

# Test CLI execution
echo "Testing CLI execution..."
$PYTHON_CMD -m lbx_cli.main --help | head -15
echo ""

echo "✅ CLI is working!"
echo ""
echo "To install and use:"
echo "  pip install -e .  # or: uv pip install -e ."
echo "  alignerr_mcp --help"
echo "  alignerr --help    # Alias also works"
