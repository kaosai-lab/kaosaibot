import os
import httpx
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

if not TELEGRAM_BOT_TOKEN or not ANTHROPIC_API_KEY or not TELEGRAM_WEBHOOK_SECRET:
    # Railway will still deploy, but bot will not work until variables are set
    pass

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

@app.get("/")
def health():
    return {"ok": True}

async def send_telegram_message(chat_id: int, text: str) -> None:
    url = f"{TELEGRAM_API_BASE}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()

async def call_claude(user_text: str) -> str:
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 600,
        "messages": [
            {"role": "user", "content": user_text}
        ],
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(ANTHROPIC_MESSAGES_URL, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    content = data.get("content", [])
    if not content:
        return "I could not generate a response."
    return content[0].get("text", "I could not generate a response.")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    secret_header = request.headers.get("x-telegram-bot-api-secret-token")
    if secret_header != TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="unauthorized")

    update = await request.json()

    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"ok": True}

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text")

    if not chat_id or not text:
        return {"ok": True}

    try:
        reply = await call_claude(text)
        await send_telegram_message(chat_id, reply)
    except Exception:
        await send_telegram_message(chat_id, "Error. Try again.")
    return {"ok": True}
