#!/bin/bash
# Frontend development server for Unix/macOS

echo "Starting Frontend Development Server..."
echo ""
echo "The dashboard will be available at: http://localhost:3000"
echo "API endpoint: http://localhost:8000/api"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

cd "$(dirname "$0")/frontend"

if [ ! -d "node_modules" ]; then
    echo "ERROR: Dependencies not installed"
    echo "Please run: bash frontend-install.sh"
    exit 1
fi

npm run dev
