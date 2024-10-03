# commands/balance.py

from telegram import Update
from telegram.ext import CallbackContext
import ccxt
from config import API_KEY, API_SECRET

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

def balance(update: Update, context: CallbackContext) -> None:
    try:
        balance_info = exchange.fetch_balance()
        spot_balance = balance_info['total']

        message = "Spot Balance:\n"
        for asset, amount in spot_balance.items():
            if amount > 0:
                message += f"{asset}: {amount}\n"

        update.message.reply_text(message)
    except Exception as e:
        update.message.reply_text(f'Error fetching balance: {e}')
