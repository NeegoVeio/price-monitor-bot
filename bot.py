import schedule
import time
import os
from dotenv import load_dotenv
from notifier import notify_discord, notify_telegram
from utils import load_last_price, save_last_price
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import sys

load_dotenv()

URL = os.getenv("PRODUCT_URL")
SELECTOR = os.getenv("PRICE_SELECTOR")
INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
MAX_RETRIES = 3
FAIL_LIMIT = 3  # número de falhas consecutivas antes de parar o bot

fail_count = 0  # contador de falhas consecutivas

# Inicializa o navegador globalmente
playwright_instance = sync_playwright().start()
browser = playwright_instance.chromium.launch(headless=True)
page = browser.new_page()

def send_error_notification(message):
    print(f"⚠️ {message}")
    notify_discord(f"⚠️ BOT ERRO: {message}")
    notify_telegram(f"⚠️ BOT ERRO: {message}")

def safe_goto(url):
    """Tenta abrir/recarregar a página, retorna True se conseguir, False se falhar."""
    global page
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            page.goto(url, timeout=15000)
            return True
        except Exception as e:
            send_error_notification(f"Tentativa {attempt} - erro ao carregar a página: {e}")
            try:
                page.close()
            except:
                pass
            page = browser.new_page()
    send_error_notification("❌ Falha crítica: não foi possível carregar a página após várias tentativas.")
    return False

def get_price():
    """Pega o preço atual de forma segura, com retries."""
    global page
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            page.reload()
            page.wait_for_selector(SELECTOR, timeout=10000)
            price_text = page.query_selector(SELECTOR).inner_text().strip()
            price_value = float(price_text.replace(".", "").replace(",", ".").replace("R$", "").strip())
            return price_value
        except PlaywrightTimeoutError:
            send_error_notification(f"Tentativa {attempt} - Timeout ao buscar o preço")
        except Exception as e:
            send_error_notification(f"Tentativa {attempt} - Erro ao pegar o preço: {e}")
    return None

def check_price():
    global fail_count
    try:
        current_price = get_price()
        if current_price is None:
            fail_count += 1
            print(f"❌ Falha ao obter preço. Contador de falhas: {fail_count}/{FAIL_LIMIT}")
            if fail_count >= FAIL_LIMIT:
                send_error_notification("❌ Número máximo de falhas alcançado. O bot será encerrado.")
                cleanup_and_exit()
            return

        # Se conseguiu pegar o preço, zera o contador de falhas
        fail_count = 0

        last_price = load_last_price()
        print(f"💲 Preço atual: R$ {current_price:.2f}")

        if last_price is None:
            print("📌 Nenhum histórico encontrado. Salvando primeiro preço.")
            save_last_price(current_price)
            return

        if current_price < last_price:
            print("📉 Preço caiu! Enviando notificação...")
            message = f"Preço caiu de R$ {last_price:.2f} para R$ {current_price:.2f}!\n{URL}"
            notify_discord(message)
            notify_telegram(message)

        save_last_price(current_price)

    except Exception as e:
        send_error_notification(f"Erro inesperado na checagem: {e}")
        safe_goto(URL)

def cleanup_and_exit():
    """Fecha navegador e encerra o script."""
    try:
        page.close()
        browser.close()
        playwright_instance.stop()
    finally:
        sys.exit()

# Inicializa a página antes do loop
if not safe_goto(URL):
    fail_count += 1
    if fail_count >= FAIL_LIMIT:
        send_error_notification("❌ Falha ao carregar página inicial. O bot será encerrado.")
        cleanup_and_exit()

# Agenda a checagem
schedule.every(INTERVAL).minutes.do(check_price)

print(f"🔍 Bot iniciado. Checando preço a cada {INTERVAL} minutos...")

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
finally:
    cleanup_and_exit()
