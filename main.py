from flask import Flask, request
import requests
import os
from replies import get_reply

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    if not update or "message" not in update:
        return "ok"

    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    reply = get_reply(text)

    requests.post(URL, json={"chat_id": chat_id, "text": reply})
    return "ok"

@app.route("/")
def home():
    return "Bot is running!"
