#!/bin/bash
# Setup script for macOS/Linux

echo "Creating Python virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt

echo "Setup complete!"
echo ""
echo "To start the backend, run:"
echo "  source .venv/bin/activate"
echo "  uvicorn backend.app.main:app --reload --port 8000"
echo ""
echo "Backend API docs will be available at: http://localhost:8000/docs"
