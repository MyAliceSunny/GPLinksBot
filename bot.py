import os
import time
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def get_updates(offset=None):
    url = BASE_URL + "/getUpdates"
    params = {"timeout": 100}
    if offset:
        params["offset"] = offset
    return requests.get(url, params=params).json()

def shorten_link(link):
    url = "https://gplinks.in/api"
    params = {"api": API_KEY, "url": link}
    r = requests.get(url, params=params).json()
    return r.get("shortenedUrl", "❌ Error generating link")

offset = None
print("Bot started...")

while True:
    updates = get_updates(offset)
    if "result" in updates:
        for update in updates["result"]:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text.startswith("http"):
                short = shorten_link(text)
                send_message(chat_id, f"🔗 Your short link:\n{short}")
            else:
                send_message(chat_id, "👋 Send me any link to shorten 🔗")

    time.sleep(2)
