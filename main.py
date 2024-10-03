
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext,Filters, MessageHandler
from trade_balance.trade import trade, handle_trade, handle_order_type, handle_amount, handle_price
from trade_balance.balance import balance
from config import TELEGRAM_TOKEN

def start(update: Update, context: CallbackContext) -> None:
    """Welcomes the user and provides options for trading or checking balance."""
    update.message.reply_text('Welcome! Use /trade to start trading or /balance to check your account balance.')

def main():
    """Main function to run the Telegram bot."""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("trade", trade))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_order_type))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_amount))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_price))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
