import os
import requests
import asyncio
from telegram import Bot

# Usa variabili d'ambiente per proteggere i dati sensibili
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
    raise ValueError("⚠️ ERRORE: Le variabili TELEGRAM_BOT_TOKEN e CHAT_ID devono essere impostate!")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# API di CoinGecko per ottenere il prezzo di Pi Network
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=pi-network&vs_currencies=usd"

last_price = None  # Memorizza l'ultimo prezzo registrato
THRESHOLD = 0.10  # 10% di variazione


async def send_telegram_message(msg_text):
    """Invia un messaggio al gruppo Telegram in modo asincrono."""
    print(f"[DEBUG] Invio messaggio: {msg_text}")
    await bot.send_message(chat_id=CHAT_ID, text=msg_text)


def get_pi_price():
    """Ottiene il prezzo attuale di Pi Network da CoinGecko."""
    try:
        response = requests.get(COINGECKO_API_URL)
        data = response.json()
        price = data["pi-network"]["usd"]
        print(f"[DEBUG] Prezzo attuale di Pi Network: ${price}")
        return price
    except Exception as e:
        print("[ERRORE] Problema nel recupero del prezzo:", e)
        return None


async def main():
    print("[DEBUG] Il bot ha avviato il loop e sta funzionando!")  # 🔹 Debug avvio
    await send_telegram_message("🚀 Il bot è attivo su Railway e sta funzionando!")

    global last_price
    while True:
        print("[DEBUG] Controllo del prezzo...")
        current_price = get_pi_price()

        if current_price is not None:
            if last_price is None:
                last_price = current_price

            variation = abs((current_price - last_price) / last_price)
            print(f"[DEBUG] Variazione: {variation * 100:.2f}%")

            if variation >= THRESHOLD:
                msg_text = f"⚠️ Variazione del prezzo di Pi Network!\n\n💰 Prezzo attuale: ${current_price:.4f}\n📉 Variazione del {variation * 100:.2f}%"
                await send_telegram_message(msg_text)
                last_price = current_price

        await asyncio.sleep(60)  # Controlla il prezzo ogni minuto


# Avvia il bot Telegram
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
