from playwright.sync_api import sync_playwright
import time

URL = "https://www.kabum.com.br/produto/633107/ssd-kingston-1tb-padrao-nv3-m-2-2280-nvme-4-0-gen-4x4-leitura-6000-e-gravacao-4000mbps-ultra-rapido-snv3s-1000g"
ULTIMO_PRECO = None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless=True roda sem abrir navegador
    page = browser.new_page()

    while True:
        page.goto(URL)
        page.wait_for_selector("h4.text-4xl.text-secondary-500")  # espera o elemento aparecer

        preco_texto = page.query_selector("h4.text-4xl.text-secondary-500").inner_text().strip()
        preco_num = float(preco_texto.replace("R$", "").replace(".", "").replace(",", "."))

        if ULTIMO_PRECO is None:
            ULTIMO_PRECO = preco_num

        if preco_num != ULTIMO_PRECO:
            print(f"Preço mudou! Agora é R${preco_num:.2f}")
            ULTIMO_PRECO = preco_num
        else:
            print(f"Preço continua o mesmo: R${preco_num:.2f}")

        time.sleep(60)  # espera 60 segundos antes de checar de novo
