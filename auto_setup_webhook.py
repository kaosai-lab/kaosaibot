#!/usr/bin/env python3
"""
Automatically detect ngrok URL and set webhook
"""
import os
import sys
import json
from dotenv import load_dotenv
import httpx

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_WEBHOOK_SECRET:
    print("❌ Error: Missing environment variables in .env file!")
    sys.exit(1)

print("🔍 Looking for ngrok tunnel...")

# Try to get ngrok URL
try:
    ngrok_response = httpx.get("http://localhost:4040/api/tunnels", timeout=2)
    ngrok_data = ngrok_response.json()
    
    tunnels = ngrok_data.get("tunnels", [])
    if not tunnels:
        print("❌ No ngrok tunnels found!")
        print("\nPlease start ngrok first:")
        print("  ngrok http 8000")
        sys.exit(1)
    
    # Get HTTPS tunnel (prefer HTTPS over HTTP)
    https_tunnel = next((t for t in tunnels if t.get("proto") == "https"), None)
    tunnel = https_tunnel or tunnels[0]
    
    ngrok_url = tunnel.get("public_url")
    print(f"✅ Found ngrok URL: {ngrok_url}")
    
except httpx.RequestError:
    print("❌ ngrok is not running!")
    print("\nPlease start ngrok in another terminal:")
    print("  ngrok http 8000")
    sys.exit(1)

# Set webhook
webhook_url = f"{ngrok_url}/webhook"
print(f"\n🔗 Setting webhook to: {webhook_url}")

try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    payload = {
        "url": webhook_url,
        "secret_token": TELEGRAM_WEBHOOK_SECRET
    }
    
    response = httpx.post(url, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if data.get("ok"):
        print("✅ Webhook set successfully!")
        print(f"\n🎉 Your bot is now ready!")
        print(f"   Send a message to @kaosaibot on Telegram to test it.")
        
        # Show webhook info
        info_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
        info_response = httpx.get(info_url, timeout=10)
        info_data = info_response.json()
        
        if info_data.get("ok"):
            info = info_data.get("result", {})
            print(f"\n📋 Webhook Info:")
            print(f"   URL: {info.get('url', 'N/A')}")
            print(f"   Pending updates: {info.get('pending_update_count', 0)}")
    else:
        print(f"❌ Failed to set webhook: {data.get('description', 'Unknown error')}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
