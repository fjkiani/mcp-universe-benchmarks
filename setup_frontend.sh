#!/bin/bash

# Frontend Setup Script
# Generates api-status.json and installs frontend dependencies

echo "=========================================="
echo "Frontend Setup"
echo "=========================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
CENTRAL_DIR="$SCRIPT_DIR/central"

echo "Project root: $SCRIPT_DIR"
echo "Frontend directory: $FRONTEND_DIR"

# Step 1: Generate api-status.json
echo ""
echo "Step 1: Generating api-status.json..."
echo ""

if [ -d "$CENTRAL_DIR" ] && [ -f "$CENTRAL_DIR/frontend-sync.py" ]; then
    cd "$CENTRAL_DIR" || exit 1
    
    # Check if Python 3 is available
    if command -v python3 &> /dev/null; then
        python3 frontend-sync.py
        
        if [ $? -eq 0 ]; then
            echo "✅ api-status.json generated!"
        else
            echo "⚠️  Warning: frontend-sync.py failed, but api-status.json may already exist"
        fi
    else
        echo "⚠️  Warning: python3 not found, skipping frontend-sync.py"
        echo "   (api-status.json may already exist)"
    fi
else
    echo "⚠️  Warning: frontend-sync.py not found, skipping"
    echo "   (api-status.json may already exist)"
fi

# Step 2: Install npm dependencies
echo ""
echo "Step 2: Installing npm dependencies..."
echo ""

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Error: Frontend directory not found at $FRONTEND_DIR"
    exit 1
fi

cd "$FRONTEND_DIR" || exit 1

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found in frontend directory"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
    
    if [ $? -eq 0 ]; then
        echo "✅ npm dependencies installed!"
    else
        echo "❌ Error installing npm dependencies"
        exit 1
    fi
else
    echo "✅ node_modules already exists (skipping npm install)"
fi

echo ""
echo "=========================================="
echo "✅ Frontend setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start frontend: cd frontend && npm run dev"
echo "  2. Or use: ./start_frontend.sh"
echo ""

