import os
import threading
import time

import requests
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return "AI Factory Bot is running!"


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_URL = f"https://api.telegram.org/bot{TOKEN}/" if TOKEN else ""

offset = 0


def send_message(chat_id, text):
    if not API_URL:
        return
    try:
        requests.post(
            API_URL + "sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
    except Exception:
        pass


def process_message(msg):
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    if text == "/start":
        send_message(
            chat_id,
            "AI Factory Bot v2.0\n/web сайт\n/bot бот\n/app приложение\n/history",
        )
    elif text.startswith("/web") or text.startswith("/bot") or text.startswith("/app"):
        parts = text.split(" ", 1)
        cmd = parts[0].replace("/", "")
        desc = parts[1] if len(parts) > 1 else "проект"
        send_message(chat_id, f"Запускаю {cmd}: {desc}")
    elif text == "/history":
        send_message(chat_id, "История пока недоступна")
    else:
        send_message(chat_id, "Команды: /web, /bot, /app, /history")


def bot_loop():
    global offset
    if not TOKEN:
        return
    while True:
        try:
            resp = requests.get(
                API_URL + "getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=35,
            ).json()
            if resp["ok"]:
                for upd in resp["result"]:
                    offset = upd["update_id"] + 1
                    if "message" in upd:
                        process_message(upd["message"])
        except Exception:
            time.sleep(5)


threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
