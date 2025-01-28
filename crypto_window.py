# crypto_window.py

import tkinter as tk
import logging

class CryptoWindow(tk.Toplevel):
    """
    Represents a window displaying data for a specific coin.
    """
    def __init__(self, master, data_service, symbol):
        super().__init__(master)

        self.title(f"Data for {symbol}")
        self.data_service = data_service
        self.symbol = symbol

        # For styling
        self.config(bg="#F0F0F0")

        # Grab the 24h ticker info
        ticker_info = self.data_service.get_24h_ticker_info(self.symbol)

        if ticker_info:
            volume_label = tk.Label(self, text=f"24h Volume: {ticker_info['volume']}", bg="#F0F0F0")
            volume_label.pack(pady=5)

            price_change_label = tk.Label(self, text=f"24h Price Change: {ticker_info['priceChange']}", bg="#F0F0F0")
            price_change_label.pack(pady=5)

            # Add more labels or info as needed
        else:
            error_label = tk.Label(self, text="Error fetching data", bg="#F0F0F0", fg="red")
            error_label.pack(pady=5)
