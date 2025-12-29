import os
import time
import requests

users = {}

def get_user(chat_id):
    if chat_id not in users:
        users[chat_id] = {"balance": 0, "upi": None}

def get_balance(chat_id):
    return users.get(chat_id, {}).get("balance", 0)

def add_balance(chat_id, amount):
    get_user(chat_id)
    users[chat_id]["balance"] += amount

def set_upi(chat_id, upi):
    get_user(chat_id)
    users[chat_id]["upi"] = upi

BOT_TOKEN = "8182545842:AAEM8YuxlCy1PUggh8pE4uYU7L2S1q4ftE4"
API_KEY = "9ef4aadd63ffb7759f17d3b0486d45cfa9d9dba4"

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

offset = 0
print("Bot started...")

while True:
    updates = get_updates(offset)

    if "result" in updates:
        for update in updates["result"]:
            offset = update["update_id"] + 1  # 🔥 VERY IMPORTANT

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            get_user(chat_id)  # ensure user exists

if text == "/balance":
    bal = get_balance(chat_id)
    send_message(chat_id, f"💰 Your Balance: ₹{bal}\nMinimum withdrawal: ₹500")

elif text == "/withdraw":
    bal = get_balance(chat_id)
    if bal < 500:
        send_message(chat_id, "❌ Minimum ₹500 required for withdrawal")
    else:
        send_message(chat_id, "💳 Send your UPI ID (example: name@paytm)")

elif "@" in text and len(text) > 5:
    set_upi(chat_id, text)
    send_message(chat_id, "✅ UPI saved! Payment will be processed manually.")

elif text.startswith("http"):
    short = shorten_link(text)

    # 👇 YAHI EARNING ADD HOTI HAI (TEMP DEMO)
    add_balance(chat_id, 10)

    send_message(
        chat_id,
        f"🔗 Your short link:\n{short}\n\n💸 ₹10 added to your balance"
    )

else:
    send_message(chat_id, "👋 Send me any link to shorten")

    time.sleep(1)
