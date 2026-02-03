#!/bin/bash

# Script to install ngrok locally in the project directory

echo "📥 Installing ngrok in project directory..."
echo ""

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    NGROK_ARCH="arm64"
    echo "Detected: Apple Silicon (ARM64)"
else
    NGROK_ARCH="amd64"
    echo "Detected: Intel (AMD64)"
fi

echo "Downloading ngrok..."
curl -L "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-${NGROK_ARCH}.zip" -o ngrok.zip

if [ $? -ne 0 ]; then
    echo "❌ Download failed. Please download manually from: https://ngrok.com/download"
    exit 1
fi

echo "Extracting..."
unzip -q ngrok.zip

# Make it executable
chmod +x ngrok

# Cleanup zip file
rm ngrok.zip

echo ""
echo "✅ ngrok installed successfully in project directory!"
echo ""
echo "Location: $PROJECT_DIR/ngrok"
echo ""
echo "Next steps:"
echo "1. Sign up at https://dashboard.ngrok.com (free)"
echo "2. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken"
echo "3. Run: ./ngrok config add-authtoken YOUR_TOKEN"
echo "4. Start ngrok: ./ngrok http 8000"
echo "5. Set webhook: python auto_setup_webhook.py"
