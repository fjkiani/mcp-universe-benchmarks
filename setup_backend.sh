#!/bin/bash

# Backend Setup Script
# Installs all Python dependencies for the backend

echo "=========================================="
echo "Backend Setup - Installing Dependencies"
echo "=========================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"

echo "Project root: $SCRIPT_DIR"
echo "Backend directory: $BACKEND_DIR"

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Error: Backend directory not found at $BACKEND_DIR"
    exit 1
fi

# Change to backend directory
cd "$BACKEND_DIR" || exit 1

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found in backend directory"
    exit 1
fi

echo ""
echo "Installing Python dependencies..."
echo ""

# Install dependencies
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Backend dependencies installed!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Start backend: cd backend && python3 main.py"
    echo "  2. Or use: ./start_backend.sh"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Error installing dependencies"
    echo "=========================================="
    echo ""
    echo "Try running: pip3 install -r backend/requirements.txt"
    exit 1
fi

