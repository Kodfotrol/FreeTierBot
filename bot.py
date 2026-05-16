import requests
import time

TOKEN = "8761774819:AAFYhj0Uuo-wyfnLgiCZVZfc21xDCIYE8e8"
API_URL = f"https://api.telegram.org/bot{TOKEN}/"
FACTORY_URL = "http://127.0.0.1:8000"

offset = 0

def send_message(chat_id, text):
    try:
        requests.post(API_URL + "sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, timeout=10)
    except:
        pass

def send_photo(chat_id, photo_path):
    try:
        with open(photo_path, "rb") as f:
            requests.post(API_URL + "sendPhoto", data={"chat_id": chat_id}, files={"photo": f})
    except Exception as e:
        send_message(chat_id, f"шибка отправки фото: {e}")

def send_video(chat_id, video_path):
    try:
        with open(video_path, "rb") as f:
            requests.post(API_URL + "sendVideo", data={"chat_id": chat_id}, files={"video": f})
    except Exception as e:
        send_message(chat_id, f"шибка отправки видео: {e}")

def process_message(msg):
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    
    if text == "/start":
        send_message(chat_id, "🤖 <b>AI Factory Pro</b> — твой персональный завод нейросетей!\n\n"
                     "<b>енерация:</b>\n"
                     "/image описание — картинка\n"
                     "/video описание — видео\n"
                     "/web описание — сайт\n"
                     "/bot описание — бот\n"
                     "/app описание — приложение\n"
                     "/history — история генераций")
        return
    
    if text == "/history":
        try:
            resp = requests.get(f"{FACTORY_URL}/generations/", timeout=5).json()
            if resp:
                msg = "<b>📋 стория генераций:</b>\n\n"
                for item in resp[-5:]:
                    msg += f"• {item['type']}: {item['description'][:40]}... (<i>{item['status']}</i>)\n"
            else:
                msg = "ока пусто."
            send_message(chat_id, msg)
        except:
            send_message(chat_id, "❌ шибка подключения к API.")
        return
    
    # пределяем тип генерации
    cmd_map = {"/image": "image", "/video": "video", "/web": "web", "/bot": "bot", "/app": "app"}
    cmd = None
    gen_type = None
    for c, t in cmd_map.items():
        if text.startswith(c):
            cmd = c
            gen_type = t
            break
    
    if cmd:
        desc = text[len(cmd):].strip() or "случайный проект"
        send_message(chat_id, f"⏳ енерирую {gen_type}... то может занять до минуты.")
        try:
            resp = requests.post(f"{FACTORY_URL}/generate/", json={"type": gen_type, "description": desc}, timeout=180).json()
            if resp["status"] == "done":
                file_path = resp["path"]
                send_message(chat_id, f"✅ <b>отово!</b> ID: {resp['id']}\nтправляю файл...")
                if gen_type == "image":
                    send_photo(chat_id, file_path)
                elif gen_type == "video":
                    send_video(chat_id, file_path)
                else:
                    send_message(chat_id, f"📁 айлы созданы: {file_path}\nспользуй /download {resp['id']} для скачивания.")
            else:
                send_message(chat_id, f"❌ шибка генерации: {resp.get('error', 'еизвестно')}")
        except Exception as e:
            send_message(chat_id, f"❌ шибка: {str(e)[:100]}")
    else:
        send_message(chat_id, "🤔 еизвестная команда. спользуй /image, /video, /web, /bot, /app или /history")

def main():
    global offset
    print("AI Factory Pro Bot started!")
    while True:
        try:
            resp = requests.get(API_URL + "getUpdates", params={"offset": offset, "timeout": 30}, timeout=35).json()
            if resp["ok"]:
                for upd in resp["result"]:
                    offset = upd["update_id"] + 1
                    if "message" in upd:
                        process_message(upd["message"])
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
