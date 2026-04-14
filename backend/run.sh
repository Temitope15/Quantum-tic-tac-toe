#!/bin/bash

# Exit on error
set -e

echo "⚛️ Starting Quantum Tic-Tac-Toe Backend..."

# Use PORT from environment or default to 8000
PORT_TO_USE=${PORT:-8000}

# Local vs Production determination
if [ -z "$RENDER" ]; then
    echo "🏠 Running in Local Mode..."
    if [ -d "venv" ]; then
        echo "✅ Activating Virtual Environment..."
        source venv/bin/activate
    fi
    # In local mode, we often want reload active via the DEBUG env var
    export DEBUG=True
else
    echo "🌐 Running in Production Mode (Render)..."
    export DEBUG=False
fi

# Run the FastAPI server via the api.py entry point
echo "🚀 Launching FastAPI server on port $PORT_TO_USE"
python api.py
