#!/usr/bin/env python3
"""
Diagnostic script to check bot status
"""
import os
import sys
from dotenv import load_dotenv
import httpx

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN not set in .env file!")
    sys.exit(1)

print("🔍 Checking Bot Status...")
print("=" * 50)

# Check webhook info
try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if data.get("ok"):
        info = data.get("result", {})
        webhook_url = info.get("url", "")
        
        print(f"\n📋 Webhook Status:")
        if webhook_url:
            print(f"   ✅ Webhook URL: {webhook_url}")
            print(f"   Pending updates: {info.get('pending_update_count', 0)}")
            
            if info.get('last_error_date'):
                print(f"   ⚠️  Last error: {info.get('last_error_message', 'Unknown')}")
                print(f"   ⚠️  Error date: {info.get('last_error_date', 'Unknown')}")
            else:
                print(f"   ✅ No errors")
        else:
            print(f"   ❌ Webhook NOT SET - This is why your bot isn't responding!")
            print(f"\n   You need to:")
            print(f"   1. Start ngrok: ngrok http 8000")
            print(f"   2. Copy the HTTPS URL")
            print(f"   3. Run: python setup_webhook.py <ngrok_url>")
        
        # Check bot info
        bot_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        bot_response = httpx.get(bot_url, timeout=10)
        bot_data = bot_response.json()
        
        if bot_data.get("ok"):
            bot_info = bot_data.get("result", {})
            print(f"\n🤖 Bot Info:")
            print(f"   Username: @{bot_info.get('username', 'N/A')}")
            print(f"   Name: {bot_info.get('first_name', 'N/A')}")
            print(f"   ID: {bot_info.get('id', 'N/A')}")
        
except Exception as e:
    print(f"❌ Error checking status: {e}")

print("\n" + "=" * 50)
