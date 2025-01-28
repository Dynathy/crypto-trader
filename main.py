# cli.py

import os
import logging
import typer
from dotenv import load_dotenv
import plotext as plt
from datetime import datetime, timezone
from binance.enums import KLINE_INTERVAL_1HOUR

from crypto_data_service import CryptoDataService

# If you want human-readable timestamps, uncomment the next line:
# from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
TESTNET = os.getenv('TESTNET', 'false').lower() == 'true'

app = typer.Typer(help="A fancy CLI for Binance data with ASCII charts.")

# Make a global instance of our data service
data_service = CryptoDataService(API_KEY, API_SECRET, testnet=TESTNET)

POPULAR_COINS = [
    "BTC", 
    "ETH", 
    "BNB", 
    "ADA", 
    "SOL", 
    "XRP", 
    "DOT", 
    "DOGE", 
    "LTC", 
    "HBAR"
]


@app.command()
def balances(
    coins: list[str] = typer.Option(
        None, 
        "--coins", "-c", 
        help="Space-separated list of coins to get balances for (defaults to popular coins)."
    )
):
    """
    Show balances for a list of coins.
    """
    if not coins:
        coins = POPULAR_COINS
    results = data_service.get_all_balances(coins)
    for coin, bal in results.items():
        typer.echo(f"{coin} balance: {bal}")


@app.command()
def price(symbol: str):
    """
    Show current price for a given symbol, e.g. BTCUSDT.
    """
    p = data_service.get_price(symbol)
    if p is None:
        typer.secho(f"Error fetching price for {symbol}", fg=typer.colors.RED)
    else:
        typer.echo(f"The current price of {symbol} is {p}")


@app.command()
def ticker(symbol: str):
    """
    Show 24h ticker info (like volume, priceChange, etc.).
    """
    info = data_service.get_24h_ticker_info(symbol)
    if info is None:
        typer.secho("Error fetching 24h ticker!", fg=typer.colors.RED)
        return
    typer.echo(f"Symbol: {symbol}")
    typer.echo(f" - Price Change: {info['priceChange']}")
    typer.echo(f" - Price Change %: {info['priceChangePercent']}")
    typer.echo(f" - Weighted Avg Price: {info['weightedAvgPrice']}")
    typer.echo(f" - Volume: {info['volume']}")


@app.command()
def trades(symbol: str, limit: int = 10):
    """
    Show recent trades for the specified symbol.
    """
    t = data_service.get_recent_trades(symbol, limit=limit)
    if t is None:
        typer.secho("Error fetching recent trades!", fg=typer.colors.RED)
        return
    typer.echo(f"Recent trades for {symbol} (showing {limit}):")
    for trade in t:
        price = trade['price']
        qty = trade['qty']
        time_stamp = trade['time']
        typer.echo(f"  Price: {price}, Qty: {qty}, Time: {time_stamp}")


@app.command()
def candlestick_chart(
    symbol: str = typer.Argument("BTCUSDT", help="Symbol to chart."),
    interval: str = typer.Option("1h", help="Kline interval like '1m', '15m', '1h', '1d'"),
    limit: int = typer.Option(24, help="Number of candles to fetch.")
):
    """
    Plot an ASCII-based candlestick chart in the terminal using plotext.
    """
    # Map human-readable intervals to Binance intervals
    intervals_map = {
        "1m": "1m",
        "3m": "3m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "2h": "2h",
        "4h": "4h",
        "6h": "6h",
        "8h": "8h",
        "12h": "12h",
        "1d": "1d",
        # ... add more if needed
    }
    binance_interval = intervals_map.get(interval, "1h")  # fallback

    klines = data_service.client.get_klines(symbol=symbol, interval=binance_interval, limit=limit)
    if not klines:
        typer.secho("Error fetching klines for chart!", fg=typer.colors.RED)
        return

    # Prepare data for plotext
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []

    for k in klines:
        # k = [Open time, Open, High, Low, Close, Volume, Close time, ...]
        open_price = float(k[1])
        high_price = float(k[2])
        low_price = float(k[3])
        close_price = float(k[4])
        time_stamp = k[6]  # or k[6] for the closing time
        dates.append(time_stamp)
        # Ensure timestamp is correctly converted from milliseconds
        # Convert timestamp to a readable date
        #time_string = datetime.fromtimestamp(time_stamp / 1000, tz=timezone.utc).strftime('%d/%m/%Y')
        #dates.append(time_string)
        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)

    # Clear any existing plot data
    plt.clear_data()

    # Construct the data dictionary that plotext expects
    ohlc_data = {
        "Open": opens,
        "High": highs,
        "Low": lows,
        "Close": closes
    }

    lowest_price = min(lows + opens + closes + highs)
    highest_price = max(lows + opens + closes + highs)

    # Optional: add a little padding so the candles don't hug the chart edges
    lowest_price *= 0.95
    highest_price *= 1.05

    # Now pass the dictionary to candlestick
    plt.candlestick(dates, ohlc_data)

    plt.title(f"{symbol} Candlestick Chart ({interval} interval)")
    plt.xlabel("Time")
    plt.ylabel("Price")

    # Adjust figure size if you like
    #plt.plotsize(80, 25)
    plt.ylim(lowest_price, highest_price)
    plt.canvas_color("black")      # Match your terminal background
    plt.axes_color("black")        # Make the axes background match
    plt.ticks_color("white")       # If you want your tick labels to be white
    #plt.frame(False)               # or plt.box(False) in some versions

    # Display in terminal
    plt.show()

def main():
    app()

if __name__ == "__main__":
    main()
