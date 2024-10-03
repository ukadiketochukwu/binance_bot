# strategies/order_management.py

import ccxt
from config import API_KEY, API_SECRET

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

def create_market_order(symbol, amount, side='buy'):
    try:
        if side == 'buy':
            exchange.create_market_buy_order(symbol, amount)
        elif side == 'sell':
            exchange.create_market_sell_order(symbol, amount)
        return f"Executed {side} market order for {amount} of {symbol}."
    except Exception as e:
        return f"Error executing market order: {e}"

def create_limit_order(symbol, amount, price, side='buy'):
    try:
        if side == 'buy':
            exchange.create_limit_buy_order(symbol, amount, price)
        elif side == 'sell':
            exchange.create_limit_sell_order(symbol, amount, price)
        return f"Placed {side} limit order for {amount} of {symbol} at {price}."
    except Exception as e:
        return f"Error placing limit order: {e}"
