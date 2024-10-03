import ccxt
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

api_key = ''
api_secret = ''
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})


TELEGRAM_TOKEN = ''


user_state = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /trade to start trading.')

def trade(update: Update, context: CallbackContext) -> None:
    user_state[update.effective_user.id] = {}
    update.message.reply_text('What coin/token would you like to trade? (e.g., BTC/USDT)')

def handle_coin(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_state[user_id]['coin'] = update.message.text
    update.message.reply_text('Choose trading type: /spot or /futures')

def spot(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    coin = user_state[user_id].get('coin')
    if not coin:
        update.message.reply_text('Please provide a coin/token first using /trade.')
        return
    update.message.reply_text(f'Starting spot trade for {coin}. How much do you want to buy?')

def futures(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    coin = user_state[user_id].get('coin')
    if not coin:
        update.message.reply_text('Please provide a coin/token first using /trade.')
        return
    user_state[user_id]['type'] = 'futures'
    update.message.reply_text(f'Select leverage for futures trading on {coin}.')

def handle_leverage(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    leverage = update.message.text
    user_state[user_id]['leverage'] = leverage
    coin = user_state[user_id].get('coin')
    
    if user_state[user_id].get('type') == 'futures':
        update.message.reply_text(f'Setting leverage to {leverage}x for {coin}. How much do you want to buy?')
    else:
        update.message.reply_text(f'Spot trade for {coin} selected. How much do you want to buy?')

def handle_amount(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    amount = update.message.text
    coin = user_state[user_id].get('coin')
    trade_type = user_state[user_id].get('type')

    try:
        if trade_type == 'futures':
            leverage = user_state[user_id].get('leverage')
            exchange.fapiPrivate_post_leverage({'symbol': coin.replace('/', ''), 'leverage': leverage})
            exchange.create_market_buy_order(coin, amount) 
            update.message.reply_text(f'Bought {amount} of {coin} on futures with {leverage}x leverage.')
        else:
            exchange.create_market_buy_order(coin, amount) 
            update.message.reply_text(f'Bought {amount} of {coin} on spot market.')
    except Exception as e:
        update.message.reply_text(f'Error: {e}')


def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("trade", trade))
    dispatcher.add_handler(CommandHandler("spot", spot))
    dispatcher.add_handler(CommandHandler("futures", futures))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_coin))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_leverage))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_amount))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
