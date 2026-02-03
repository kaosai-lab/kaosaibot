#!/usr/bin/env python3
"""
Helper script to set up Telegram webhook
"""
import os
import sys
import json
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_WEBHOOK_SECRET:
    print("❌ Error: TELEGRAM_BOT_TOKEN or TELEGRAM_WEBHOOK_SECRET not set in .env file!")
    sys.exit(1)

def set_webhook(webhook_url: str):
    """Set Telegram webhook"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    
    payload = {
        "url": webhook_url,
        "secret_token": TELEGRAM_WEBHOOK_SECRET
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            print("✅ Webhook set successfully!")
            print(f"   URL: {webhook_url}")
            return True
        else:
            print(f"❌ Failed to set webhook: {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_webhook_info():
    """Get current webhook info"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            info = data.get("result", {})
            print("\n📋 Current Webhook Info:")
            print(f"   URL: {info.get('url', 'Not set')}")
            print(f"   Pending updates: {info.get('pending_update_count', 0)}")
            if info.get('last_error_date'):
                print(f"   Last error: {info.get('last_error_message', 'Unknown')}")
            return info
    except Exception as e:
        print(f"❌ Error getting webhook info: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_webhook.py <webhook_url>")
        print("Example: python setup_webhook.py https://abc123.ngrok.io/webhook")
        print("\nCurrent webhook status:")
        get_webhook_info()
        sys.exit(1)
    
    webhook_url = sys.argv[1]
    
    # Ensure URL ends with /webhook
    if not webhook_url.endswith("/webhook"):
        webhook_url = webhook_url.rstrip("/") + "/webhook"
    
    print(f"Setting webhook to: {webhook_url}\n")
    
    if set_webhook(webhook_url):
        get_webhook_info()
        print("\n✨ Your bot is ready! Send a message to test it.")
