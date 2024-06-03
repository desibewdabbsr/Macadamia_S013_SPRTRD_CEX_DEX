# Macadamia_S013_SPRTRD_CEX_DEX

## Overview
MacaDamia_S013_SPRTRD_CEX_DEX is a cryptocurrency trading bot that utilizes the Supertrend indicator to generate buy and sell signals for ETH/USD trading pairs across multiple centralized and decentralized exchanges.

## Features
- Supports multiple exchanges including Binance US, Binance, Coinbase Pro, and Kraken.
- Utilizes the Supertrend indicator to identify potential buy and sell opportunities.
- Runs a check for trading signals every 10 seconds.

## Prerequisites
- Python 3.7 or higher
- API keys and secrets for the supported exchanges

## Installation
1. Clone the repository:

git clone https://github.com/desibewdabbsr/Macadamia_S013_SPRTRD_CEX_DEX.git

2. Navigate to the cloned repository directory.
3. Install the required dependencies:

pip install -r requirements.txt


## Configuration
Create a `config.py` file in the root directory with the following content, replacing the placeholders with your actual API keys and secrets:

```python
# Binance US credentials
BINANCEUS_API_KEY = 'your_binanceus_api_key'
BINANCEUS_SECRET_KEY = 'your_binanceus_secret_key'

# Binance credentials
BINANCE_API_KEY = 'your_binance_api_key'
BINANCE_SECRET_KEY = 'your_binance_secret_key'

# Coinbase Pro credentials
COINBASEPRO_API_KEY = 'your_coinbasepro_api_key'
COINBASEPRO_SECRET_KEY = 'your_coinbasepro_secret_key'
COINBASEPRO_PASSWORD = 'your_coinbasepro_password'

# Kraken credentials
KRAKEN_API_KEY = 'your_kraken_api_key'
KRAKEN_SECRET_KEY = 'your_kraken_secret_key'

Usage
Run the bot using the following command:

python run_bot.py

Disclaimer
Trading cryptocurrencies involves significant risk and can result in the loss of your invested capital. Use this bot at your own risk. The creators and contributors are not responsible for any financial losses incurred.






The bot uses the Supertrend indicator as its primary strategy to book profits. Here’s how it works:

Supertrend Calculation: The Supertrend indicator is calculated using the average of the high and low prices, along with a multiplier of the Average True Range (ATR). It creates two bands around the price, an upper and a lower band.

Trend Determination: The bot determines the trend by comparing the current price with these bands. If the price is above the upper band, the market is considered in an uptrend, suggesting a buy signal. Conversely, if the price is below the lower band, the market is in a downtrend, indicating a sell signal.

Position Entry: When the bot identifies a change from a downtrend to an uptrend, it executes a buy order. This is based on the assumption that the uptrend will continue and lead to a profitable opportunity.

Position Exit: Similarly, when the bot notices a change from an uptrend to a downtrend, it executes a sell order. This is to book profits (or cut losses) assuming that the downtrend might lead to a decrease in price.

Profit Booking: The profit is booked when the bot sells the asset at a higher price than the buying price during an uptrend.


------------------------------------------------------------------------------

