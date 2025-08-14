import requests
import os
from dotenv import load_dotenv

load_dotenv()

def notify_discord(message: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url:
        print("⚠️ Webhook do Discord não configurado.")
        return
    payload = {"content": message}
    r = requests.post(webhook_url, json=payload)
    print("✅ Notificação enviada para Discord." if r.status_code == 204 else f"❌ Erro: {r.status_code}")


def notify_telegram(message: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("⚠️ Token ou Chat ID do Telegram não configurado.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    r = requests.post(url, json=payload)
    print("✅ Notificação enviada para Telegram." if r.status_code == 200 else f"❌ Erro: {r.status_code}")
