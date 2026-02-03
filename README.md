# KaosaiBot

A Telegram bot powered by Anthropic's Claude AI, built with FastAPI.

## Setup

1. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

4. **Edit `.env` and add your credentials:**
   - `TELEGRAM_BOT_TOKEN`: Get from [@BotFather](https://t.me/BotFather)
   - `ANTHROPIC_API_KEY`: Get from [Anthropic Console](https://console.anthropic.com/)
   - `TELEGRAM_WEBHOOK_SECRET`: Generate a random secret string

## Running Locally

**Make sure your virtual environment is activated** (`source venv/bin/activate`)

### Quick Start (Recommended)

Use the helper script to start everything automatically:

```bash
./start_local.sh
```

This script will:
- Start the FastAPI server
- Start ngrok tunnel
- Display the webhook URL
- Provide instructions to set up the webhook

### Manual Setup

1. **Start the development server:**
   ```bash
   uvicorn main:app --reload
   ```
   The server will start on `http://127.0.0.1:8000`

2. **Install ngrok locally** (if not installed):
   ```bash
   ./install_ngrok_local.sh
   ```
   Then sign up at https://dashboard.ngrok.com and configure:
   ```bash
   ./ngrok config add-authtoken YOUR_TOKEN
   ```

3. **Start ngrok** (in another terminal):
   ```bash
   ./start_ngrok.sh
   ```
   Or: `./ngrok http 8000`

4. **Set up the webhook:**
   ```bash
   python auto_setup_webhook.py
   ```
   This automatically detects your ngrok URL and sets the webhook.

4. **Test your bot** by sending a message to it on Telegram!

### Test the Health Endpoint

```bash
curl http://localhost:8000/
```

Should return: `{"ok": true}`

## Production Deployment

### Heroku

1. Set environment variables:
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   heroku config:set ANTHROPIC_API_KEY=your_key
   heroku config:set TELEGRAM_WEBHOOK_SECRET=your_secret
   ```

2. Set webhook:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://your-app.herokuapp.com/webhook",
       "secret_token": "<YOUR_WEBHOOK_SECRET>"
     }'
   ```

### Render

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/kaosaibot.git
   git push -u origin main
   ```

2. **Create Web Service on Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect GitHub and select repository
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set environment variables** in Render dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `ANTHROPIC_API_KEY`
   - `TELEGRAM_WEBHOOK_SECRET`

4. **Wait for deployment** (2-5 minutes)

5. **Set webhook:**
   ```bash
   python setup_render_webhook.py https://your-app.onrender.com
   ```

6. **Test your bot!**

**Note:** Free tier spins down after 15 min inactivity. Use UptimeRobot to keep it awake.

## Helper Scripts

- `install_ngrok_local.sh` - Install ngrok in project directory
- `start_ngrok.sh` - Start ngrok tunnel
- `auto_setup_webhook.py` - Auto-detect ngrok URL and set webhook
- `setup_render_webhook.py` - Set webhook for Render deployment
- `check_status.py` - Check bot and webhook status

## Troubleshooting

### Bot not responding
- Check webhook status: `python check_status.py`
- Verify `.env` file has all three variables set
- Make sure ngrok is running: `./start_ngrok.sh`
- Restart server after changing `.env` file

### Port already in use
- Change port: `uvicorn main:app --port 8001`
- Update ngrok: `./ngrok http 8001`
