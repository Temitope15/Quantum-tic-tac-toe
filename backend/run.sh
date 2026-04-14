#!/bin/bash

# Exit on error
set -e

echo "⚛️ Starting Quantum Tic-Tac-Toe Backend..."

# Check if venv exists in current directory (backend/)
if [ -d "venv" ]; then
    echo "✅ Activating Virtual Environment..."
    source venv/bin/activate
else
    echo "❌ Error: Virtual environment 'venv' not found."
    echo "Please run 'python -m venv venv' and install requirements first."
    exit 1
fi

# Run the FastAPI server
echo "🚀 Launching FastAPI server on http://localhost:8000"
uvicorn api:app --reload --port 8000
