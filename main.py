# main.py
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from basic_bot.trade import trade
from basic_bot.balance import balance
from config import TELEGRAM_TOKEN

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /trade to start trading or /balance to check your account balance.')

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("trade", trade))
    dispatcher.add_handler(CommandHandler("balance", balance))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
