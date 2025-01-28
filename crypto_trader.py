import logging
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Define popular coins (you can add or remove coins as needed)
POPULAR_COINS = [
    'BTC',  # Bitcoin
    'ETH',  # Ethereum
    'BNB',  # Binance Coin
    'ADA',  # Cardano
    'SOL',  # Solana
    'XRP',  # Ripple
    'DOT',  # Polkadot
    'DOGE', # Dogecoin
    'LTC',  # Litecoin
    'HBAR' # Hedera
]

class AlgoTrader:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.testnet = os.getenv('TESTNET', 'false').lower() == 'true'
        self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
        self.popular_coins = POPULAR_COINS

    def get_balance(self, asset):
        """Get the balance of a specific asset."""
        try:
            balance = self.client.get_asset_balance(asset=asset)
            return float(balance['free'])
        except Exception as e:
            logging.error(f"Error fetching balance for {asset}: {e}")
            return None

    def get_all_balances(self):
        """Get balances for all popular coins."""
        balances = {}
        for coin in self.popular_coins:
            balance = self.get_balance(coin)
            if balance is not None:
                balances[coin] = balance
        return balances

    def get_price(self, symbol):
        """Get the current price of a symbol."""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logging.error(f"Error fetching price for {symbol}: {e}")
            return None

    def get_all_prices(self):
        """Get prices for all popular coins."""
        prices = {}
        for coin in self.popular_coins:
            symbol = f"{coin}USDT"  # Assuming trading pairs are against USDT
            price = self.get_price(symbol)
            if price is not None:
                prices[symbol] = price
        return prices

    def place_order(self, symbol, side, quantity):
        """Place a market order."""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logging.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing order for {symbol}: {e}")
            return None

# Example usage
trader = AlgoTrader()

# Get balances for all popular coins
balances = trader.get_all_balances()
logging.info(f"Balances: {balances}")

# Get prices for all popular coins
prices = trader.get_all_prices()
logging.info(f"Prices: {prices}")

# Place a simulated market buy order for 0.001 BTC
order = trader.place_order('BTCUSDT', SIDE_BUY, 0.001)