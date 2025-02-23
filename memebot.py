import requests
import time
import asyncio
from telegram import Bot

# Configura il tuo bot Telegram
TELEGRAM_BOT_TOKEN = "7757079154:AAEKdNe3pdLySYODGi08Vum0ucq9rtyLQgQ"
CHAT_ID = "-1002287171993"  # ID del gruppo dove inviare i messaggi
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# API di CoinGecko per ottenere il prezzo di Pi Network
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=pi-network&vs_currencies=usd"

last_price = None  # Memorizza l'ultimo prezzo registrato
THRESHOLD = 0.10  # 10% di variazione


async def send_telegram_message(msg_text):
    """Invia un messaggio al gruppo Telegram in modo asincrono."""
    print(f"[DEBUG] Invio messaggio: {msg_text}")  # 🔹 Aggiunto debug
    await bot.send_message(chat_id=CHAT_ID, text=msg_text)


def get_pi_price():
    """Ottiene il prezzo attuale di Pi Network da CoinGecko."""
    try:
        response = requests.get(COINGECKO_API_URL)
        data = response.json()
        price = data["pi-network"]["usd"]
        print(f"[DEBUG] Prezzo attuale di Pi Network: ${price}")  # 🔹 Debug prezzo
        return price
    except Exception as e:
        print("[ERRORE] Problema nel recupero del prezzo:", e)
        return None


async def main():
    global last_price
    while True:
        print("[DEBUG] Controllo del prezzo...")  # 🔹 Debug loop
        current_price = get_pi_price()

        if current_price is not None:
            if last_price is None:
                last_price = current_price

            variation = abs((current_price - last_price) / last_price)
            print(f"[DEBUG] Variazione: {variation * 100:.2f}%")  # 🔹 Debug variazione prezzo

            if variation >= THRESHOLD:
                msg_text = f"⚠️ Variazione del prezzo di Pi Network!\n\n💰 Prezzo attuale: ${current_price:.4f}\n📉 Variazione del {variation * 100:.2f}%"
                await send_telegram_message(msg_text)
                last_price = current_price  # Aggiorna il prezzo registrato

        await asyncio.sleep(60)  # Controlla il prezzo ogni minuto


if __name__ == "__main__":
    asyncio.run(main())
import threading
import time
import os

# Keep-Alive Trick per Render (finta app web)
def keep_alive():
    import http.server
    import socketserver

    PORT = int(os.environ.get("PORT", 8080))  # Render cercherà questa porta
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server Keep-Alive in esecuzione sulla porta {PORT}")
        httpd.serve_forever()

# Avvia il Keep-Alive Server in un thread separato
threading.Thread(target=keep_alive, daemon=True).start()

# Esegui il codice principale del bot Telegram
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Assicurati che questa sia la tua funzione principale
