# Bot Monitor de Preços | Price Monitor Bot

## 🇧🇷 Português

Um bot simples e eficiente que monitora automaticamente o preço de qualquer produto online.  
Informe o link do produto e ele verificará o valor em intervalos configurados (por padrão, a cada 1 hora).  
Quando o preço cair, você receberá uma notificação instantânea no Discord ou Telegram.

Ideal para caçadores de promoções e para quem não quer perder a oportunidade de economizar!  

---

## 🇺🇸 English

A simple and efficient bot that automatically tracks the price of any online product.  
Just provide the product link, and it will check the price at a set interval (by default, every 1 hour).  
When the price drops, you’ll instantly receive a notification on Discord or Telegram.

Perfect for deal hunters and anyone who doesn’t want to miss the chance to save money!  

---

## 🇧🇷 Estrutura básica do bot

- **Entrada:** Link do produto que você deseja monitorar.
- **Função de coleta:** Acessa o site e obtém o preço atual (scraping ou API, se disponível).
- **Agendamento:** Executa a coleta a cada X tempo (ex.: 1 hora) usando algo como `schedule` ou `cron`.
- **Comparação:** Verifica se o preço caiu em relação ao último valor salvo.
- **Notificação:** Envia um alerta no Discord ou Telegram.

---

## 🇺🇸 Basic bot structure

- **Input:** Link to the product you want to monitor.
- **Collection function:** Accesses the website and retrieves the current price (scraping or API, if available).
- **Scheduling:** Runs the collection every X amount of time (e.g., 1 hour) using something like `schedule` or a cron job.
- **Comparison:** Checks if the price has decreased compared to the last saved value.
- **Notification:** Sends an alert on Discord or Telegram.


