import os
import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Factory Bot is running!"

TOKEN = "8761774819:AAFYhj0Uuo-wyfnLgiCZVZfc21xDCIYE8e8"
API_URL = f"https://api.telegram.org/bot{TOKEN}/"

offset = 0

def send_message(chat_id, text):
    try:
        requests.post(API_URL + "sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def process_message(msg):
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    if text == "/start":
        send_message(chat_id, "AI Factory Bot v2.0\n/web сайт\n/bot бот\n/app приложение\n/history")
    elif text.startswith("/web") or text.startswith("/bot") or text.startswith("/app"):
        parts = text.split(" ", 1)
        cmd = parts[0].replace("/", "")
        desc = parts[1] if len(parts) > 1 else "проект"
        send_message(chat_id, f"апускаю {cmd}: {desc}")
    elif text == "/history":
        send_message(chat_id, "стория пока недоступна")
    else:
        send_message(chat_id, "оманды: /web, /bot, /app, /history")

def bot_loop():
    global offset
    while True:
        try:
            resp = requests.get(API_URL + "getUpdates", params={"offset": offset, "timeout": 30}, timeout=35).json()
            if resp["ok"]:
                for upd in resp["result"]:
                    offset = upd["update_id"] + 1
                    if "message" in upd:
                        process_message(upd["message"])
        except:
            time.sleep(5)

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
