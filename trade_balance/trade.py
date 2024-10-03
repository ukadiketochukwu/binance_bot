# commands/trade.py

from telegram import Update
from telegram.ext import CallbackContext
from order_indicator.order_management import create_market_order, create_limit_order
from config import API_KEY, API_SECRET
import ccxt

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

user_state = {}

def trade(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_state[user_id] = {}
    update.message.reply_text('What coin/token would you like to trade? (e.g., BTC/USDT)')
    user_state[user_id]['state'] = 'awaiting_coin'

def handle_trade(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    if user_id not in user_state or 'state' not in user_state[user_id]:
        update.message.reply_text("Please start the trade process again using /trade.")
        return
    
    coin = user_state[user_id].get('coin', update.message.text)
    user_state[user_id]['coin'] = coin
    
    update.message.reply_text("Do you want to place a /market or /limit order?")
    user_state[user_id]['state'] = 'awaiting_order_type'

def handle_order_type(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    if user_id not in user_state or 'state' not in user_state[user_id]:
        update.message.reply_text("Please start the trade process again using /trade.")
        return

    order_type = update.message.text.lower()
    
    if order_type not in ['market', 'limit']:
        update.message.reply_text("Please choose either /market or /limit.")
        return

    user_state[user_id]['order_type'] = order_type
    
    update.message.reply_text(f"How much of {user_state[user_id]['coin']} do you want to trade?")
    user_state[user_id]['state'] = 'awaiting_amount'

def handle_amount(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    if user_id not in user_state or 'state' not in user_state[user_id]:
        update.message.reply_text("Please start the trade process again using /trade.")
        return
    
    amount = update.message.text
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        update.message.reply_text("Please enter a valid amount.")
        return

    user_state[user_id]['amount'] = amount
    
    if user_state[user_id]['order_type'] == 'limit':
        update.message.reply_text("What price do you want to set for the limit order?")
        user_state[user_id]['state'] = 'awaiting_price'
    else:
        execute_trade(update, context, amount)
    
def handle_price(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    if user_id not in user_state or 'state' not in user_state[user_id]:
        update.message.reply_text("Please start the trade process again using /trade.")
        return

    price = update.message.text
    
    try:
        price = float(price)
        if price <= 0:
            raise ValueError
    except ValueError:
        update.message.reply_text("Please enter a valid price.")
        return
    
    user_state[user_id]['price'] = price
    
    execute_trade(update, context, user_state[user_id]['amount'], price)

def execute_trade(update: Update, context: CallbackContext, amount, price=None) -> None:
    user_id = update.effective_user.id
    coin = user_state[user_id]['coin']
    order_type = user_state[user_id]['order_type']

    if order_type == 'market':
        result = create_market_order(coin, amount)
        update.message.reply_text(result)
    elif order_type == 'limit':
        result = create_limit_order(coin, amount, price)
        update.message.reply_text(result)
    
    del user_state[user_id]
