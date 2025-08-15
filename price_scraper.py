import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

load_dotenv()

MAX_RETRIES = 3

def get_price():
    url = os.getenv("PRODUCT_URL")
    selector = os.getenv("PRICE_SELECTOR")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Tenta abrir a página até MAX_RETRIES vezes
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                page.goto(url, timeout=15000)
                break
            except Exception as e:
                print(f"Tentativa {attempt} - Erro ao carregar a página: {e}")
                if attempt == MAX_RETRIES:
                    browser.close()
                    raise RuntimeError("Não foi possível carregar a página após várias tentativas.")

        # Tenta pegar o preço
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                page.wait_for_selector(selector, timeout=10000)
                price_text = page.query_selector(selector).inner_text().strip()
                # Converte para float
                price_value = float(price_text.replace(".", "").replace(",", ".").replace("R$", "").strip())
                browser.close()
                return price_value
            except PlaywrightTimeoutError:
                print(f"Tentativa {attempt} - Timeout ao buscar o preço")
            except Exception as e:
                print(f"Tentativa {attempt} - Erro ao pegar o preço: {e}")

        browser.close()
        raise RuntimeError("Não foi possível obter o preço após várias tentativas")
