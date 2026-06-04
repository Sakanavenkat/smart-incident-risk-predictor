#!/bin/bash
# Frontend installation script for Unix/macOS

echo "Installing Frontend Dependencies..."
echo ""

cd "$(dirname "$0")/frontend"

if [ ! -d "node_modules" ]; then
    echo "[1/2] Installing npm packages..."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: npm install failed"
        exit 1
    fi
fi

echo ""
echo "[2/2] Installation complete!"
echo ""
echo "To start the frontend development server, run:"
echo "  bash frontend-run.sh"
echo ""
