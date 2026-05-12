#!/bin/bash

# Complete Setup Script
# Sets up both backend and frontend

echo "=========================================="
echo "Complete System Setup"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Project root: $SCRIPT_DIR"
echo ""

# Step 1: Setup Backend
echo "=========================================="
echo "STEP 1: Backend Setup"
echo "=========================================="
echo ""

bash "$SCRIPT_DIR/setup_backend.sh"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Backend setup failed!"
    exit 1
fi

echo ""
echo "=========================================="
echo "STEP 2: Frontend Setup"
echo "=========================================="
echo ""

bash "$SCRIPT_DIR/setup_frontend.sh"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Frontend setup failed!"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Complete Setup Finished!"
echo "=========================================="
echo ""
echo "Everything is ready! 🚀"
echo ""
echo "Next steps:"
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    python3 main.py"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "Or use the convenience scripts:"
echo "  ./start_backend.sh   (in one terminal)"
echo "  ./start_frontend.sh  (in another terminal)"
echo ""
echo "Then visit:"
echo "  - Frontend: http://localhost:5173"
echo "  - Backend API: http://localhost:8000/docs"
echo ""

