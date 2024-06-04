import ccxt
import config
import schedule
import pandas as pd
import logging
import warnings
import numpy as np
from datetime import datetime
import time
import os

pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your exchange credentials in config.py or environment variables
exchanges = {
    'binanceus': ccxt.binanceus({
        'apiKey': os.getenv('BINANCEUS_API_KEY', config.BINANCEUS_API_KEY),
        'secret': os.getenv('BINANCEUS_SECRET_KEY', config.BINANCEUS_SECRET_KEY)
    }),
    'binance': ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY', config.BINANCE_API_KEY),
        'secret': os.getenv('BINANCE_SECRET_KEY', config.BINANCE_SECRET_KEY)
    }),
    'coinbasepro': ccxt.coinbasepro({
        'apiKey': os.getenv('COINBASEPRO_API_KEY', config.COINBASEPRO_API_KEY),
        'secret': os.getenv('COINBASEPRO_SECRET_KEY', config.COINBASEPRO_SECRET_KEY),
        'password': os.getenv('COINBASEPRO_PASSWORD', config.COINBASEPRO_PASSWORD)
    }),
    'kraken': ccxt.kraken({
        'apiKey': os.getenv('KRAKEN_API_KEY', config.KRAKEN_API_KEY),
        'secret': os.getenv('KRAKEN_SECRET_KEY', config.KRAKEN_SECRET_KEY)
    })
}

in_position = False

def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])
    return data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

def atr(data, period):
    data['tr'] = tr(data)
    return data['tr'].rolling(period).mean()

def supertrend(df, period=7, atr_multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1
        if df['close'][current] > df['upperband'][previous]:
            df.at[current, 'in_uptrend'] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df.at[current, 'in_uptrend'] = False
        else:
            df.at[current, 'in_uptrend'] = df['in_uptrend'][previous]
            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df.at[current, 'lowerband'] = df['lowerband'][previous]
            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df.at[current, 'upperband'] = df['upperband'][previous]
    return df

def check_buy_sell_signals(df, exchange):
    global in_position
    logging.info("Checking for buy and sell signals")
    logging.info(df.tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1

    try:
        if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
            logging.info("Changed to uptrend, buy")
            if not in_position:
                order = exchange.create_market_buy_order('ETH/USD', 0.05)
                logging.info(order)
                in_position = True
            else:
                logging.info("Already in position, nothing to do")
        if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
            logging.info("Changed to downtrend, sell")
            if in_position:
                order = exchange.create_market_sell_order('ETH/USD', 0.05)
                logging.info(order)
                in_position = False
            else:
                logging.info("You aren't in position, nothing to sell")
    except ccxt.BaseError as e:
        logging.error(f"Error placing order: {e}")

def fetch_data_and_check_signals(exchange_id, exchange):
    logging.info(f"Fetching data from {exchange_id}")
    try:
        bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=100)
        df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        supertrend_data = supertrend(df)
        check_buy_sell_signals(supertrend_data, exchange)
    except ccxt.BaseError as e:
        logging.error(f"Error fetching data from {exchange_id}: {e}")

def run_bot():
    logging.info(f"Fetching new bars for {datetime.now().isoformat()}")
    for exchange_id, exchange in exchanges.items():
        fetch_data_and_check_signals(exchange_id, exchange)

# Schedule the bot to run every 10 seconds
schedule.every(10).seconds.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
