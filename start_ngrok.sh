#!/bin/bash

# Script to start ngrok using local binary if available

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$PROJECT_DIR/ngrok" ]; then
    echo "🚀 Starting ngrok (local)..."
    "$PROJECT_DIR/ngrok" http 8000
elif command -v ngrok &> /dev/null; then
    echo "🚀 Starting ngrok (system)..."
    ngrok http 8000
else
    echo "❌ ngrok not found!"
    echo ""
    echo "Install ngrok locally:"
    echo "  ./install_ngrok_local.sh"
    echo ""
    echo "Or install system-wide:"
    echo "  brew install ngrok"
    exit 1
fi
