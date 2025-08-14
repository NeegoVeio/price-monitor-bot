import requests
from bs4 import BeautifulSoup
import os  
from dotenv import load_dotenv

load_dotenv()

def get_price():
    url = os.getenv("PRODUCT_URL")
    selector = os.getenv("PRICE_SELECTOR")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses

    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.select_one(selector)

    if not price_element:
        raise ValueError("Não foi possível encontrar o preço na página.")
    
    price_text = "".join([c for c in price_element.get_text() if c.isdigit() or c in ",."])
    price_value = float(price_text.replace(".", ".").replace(",", "."))

    return price_value