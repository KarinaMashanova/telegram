from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        reply = f"Ты написал: {text}"
        requests.post(URL, json={"chat_id": chat_id, "text": reply})
    return "ok"

@app.route("/")
def home():
    return "Bot is running!"
