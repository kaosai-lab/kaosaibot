#!/usr/bin/env python3
"""
Set webhook for Render deployment
"""
import os
import sys
from dotenv import load_dotenv
import httpx

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_WEBHOOK_SECRET:
    print("❌ Error: Missing environment variables in .env file!")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python setup_render_webhook.py <render_url>")
    print("Example: python setup_render_webhook.py https://kaosaibot.onrender.com")
    sys.exit(1)

render_url = sys.argv[1].rstrip("/")
webhook_url = f"{render_url}/webhook"

print(f"🔗 Setting webhook to: {webhook_url}")
print("")

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
        print(f"\n🎉 Your bot is now configured on Render!")
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
