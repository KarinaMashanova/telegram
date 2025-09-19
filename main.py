from flask import Flask, request
import requests
import os
from replies import get_reply

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# указываем нужные айди
ALLOWED_CHAT_ID = -1003064609445   # группа
ALLOWED_THREAD_ID = 3              # конкретная тема

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    if not update or "message" not in update:
        return "ok"

    msg = update["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    thread_id = msg.get("message_thread_id")

    # 1) Если это личка → всегда отвечаем
    if msg["chat"]["type"] == "private":
        reply = get_reply(text)
        requests.post(URL, json={"chat_id": chat_id, "text": reply})
        return "ok"

    # 2) Если это группа → проверяем что совпадает и чат, и тема
    if chat_id == ALLOWED_CHAT_ID and thread_id == ALLOWED_THREAD_ID:
        reply = get_reply(text)
        requests.post(URL, json={
            "chat_id": chat_id,
            "text": reply,
            "message_thread_id": thread_id
        })

    return "ok"


@app.route("/")
def home():
    return "Bot is running!"
