# crypto_data_service.py

import logging
from binance.client import Client
from binance.enums import KLINE_INTERVAL_1HOUR  # or whichever intervals you want

class CryptoDataService:
    """
    Responsible for fetching data from Binance and returning it
    in a format that can be easily displayed or used by other modules.
    """

    def __init__(self, api_key, api_secret, testnet=False):
        self.client = Client(api_key, api_secret, testnet=testnet)

    def get_balance(self, asset):
        try:
            balance = self.client.get_asset_balance(asset=asset)
            return float(balance['free'])
        except Exception as e:
            logging.error(f"Error fetching balance for {asset}: {e}")
            return None

    def get_all_balances(self, assets_list):
        """Fetch balances for a list of assets."""
        balances = {}
        for coin in assets_list:
            bal = self.get_balance(coin)
            if bal is not None:
                balances[coin] = bal
        return balances

    def get_price(self, symbol):
        """Get the current price of a symbol (e.g., 'BTCUSDT')."""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logging.error(f"Error fetching price for {symbol}: {e}")
            return None

    def get_24h_ticker_info(self, symbol):
        """Get 24-hour ticker info such as volume, price change, etc."""
        try:
            return self.client.get_ticker(symbol=symbol)
        except Exception as e:
            logging.error(f"Error fetching 24h ticker for {symbol}: {e}")
            return None

    def get_recent_trades(self, symbol, limit=50):
        """Get recent trades for a symbol."""
        try:
            return self.client.get_recent_trades(symbol=symbol, limit=limit)
        except Exception as e:
            logging.error(f"Error fetching recent trades for {symbol}: {e}")
            return None
        
    def get_klines(self, symbol, interval=KLINE_INTERVAL_1HOUR, limit=24):
        """
        Return a list of kline data for the symbol.
        Each item in the list is:
          [Open time, Open, High, Low, Close, Volume, Close time, ...]
        """
        try:
            # 'limit' sets how many candlesticks to fetch
            return self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        except Exception as e:
            logging.error(f"Error fetching klines for {symbol}: {e}")
            return None

    # Add more data-retrieval methods as needed (historical trades, klines, etc.)
