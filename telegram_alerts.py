import requests
import os
token = os.environ.get("TELEGRAM_BOT_TOKEN", "No chat id found")
base_url = f"https://api.telegram.org/bot{token}/"

def sendMessage(text):
    params = {
        "chat_id": os.environ.get("TELEGRAM_CHATID", "No bot token found"),
        "text": text
    }
    requests.get(f"{base_url}sendMessage", params= params)
    return