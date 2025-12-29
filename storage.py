import json, os

FILE = "users.json"

if not os.path.exists(FILE):
    with open(FILE,"w") as f:
        json.dump({}, f)

def load():
    with open(FILE) as f:
        return json.load(f)

def save(data):
    with open(FILE,"w") as f:
        json.dump(data, f)

def get_user(uid):
    data = load()
    uid = str(uid)
    if uid not in data:
        data[uid] = {"balance":0, "upi":""}
        save(data)
    return data[uid]

def add_balance(uid, amt):
    data = load()
    uid = str(uid)
    data[uid]["balance"] += amt
    save(data)

def set_upi(uid, upi):
    data = load()
    uid = str(uid)
    data[uid]["upi"] = upi
    save(data)

def get_balance(uid):
    return get_user(uid)["balance"]
