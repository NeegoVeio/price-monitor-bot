import json
import os

# Nome do arquivo que vai guardar o histórico de preços
HISTORY_FILE = "price_history.json"

def load_last_price():
    """Carrega o último preço salvo do arquivo JSON."""
    if not os.path.exists(HISTORY_FILE):
        return None
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("last_price")
    
def save_last_price(price: float):
    """Salva o preço atual no arquivo JSON."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_price": price}, f)
