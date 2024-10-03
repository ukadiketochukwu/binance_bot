# commands/trade.py
import ccxt
from telegram import Update
from telegram.ext import CallbackContext
from config import API_KEY, API_SECRET

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'options': {
        'defaultType': 'future'
    }
})

user_state = {}

def trade(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_state[user_id] = {}
    update.message.reply_text('What coin/token would you like to trade? (e.g., BTC/USDT)')
