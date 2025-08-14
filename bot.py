import schedule
import time
from price_scraper import get_price
from notifier import notify_discord, notify_telegram
from utils import load_last_price, save_last_price
import os
from dotenv import load_dotenv

load_dotenv()

def check_price():
    try:
        current_price = get_price()
        last_price = load_last_price()

        print(f"💲 Preço atual: R$ {current_price:.2f}")
        
        if last_price is None:
            print("📌 Nenhum histórico encontrado. Salvando primeiro preço.")
            save_last_price(current_price)
            return

        if current_price < last_price:
            print("📉 Preço caiu! Enviando notificação...")
            message = f"Preço caiu de R$ {last_price:.2f} para R$ {current_price:.2f}!\n{os.getenv('PRODUCT_URL')}"
            notify_discord(message)
            notify_telegram(message)

        save_last_price(current_price)

    except Exception as e:
        print(f"❌ Erro ao verificar preço: {e}")

# Intervalo de checagem
interval = int(os.getenv("CHECK_INTERVAL", 60))
schedule.every(interval).minutes.do(check_price)

print(f"🔍 Bot iniciado. Checando preço a cada {interval} minutos...")

while True:
    schedule.run_pending()
    time.sleep(1)
