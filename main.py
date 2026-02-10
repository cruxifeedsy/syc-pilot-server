import os
from flask import Flask, request
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "SYC Pilot Bot is Running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Only allow authorized user
        if chat_id != AUTHORIZED_USER_ID:
            send_message(chat_id, "❌ Unauthorized user")
            return "ok"

        if text == "/start":
            send_message(chat_id, "🚀 SYC PILOT BOT IS LIVE")
        else:
            send_message(chat_id, f"Received: {text}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)