# data_fetcher.py

import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    """
    Fetch 6 months of daily stock price data from Yahoo Finance.
    """
    try:
        if not symbol.endswith('.NS'):
            symbol += '.NS'
        df = yf.download(symbol, period='6mo', interval='1d', progress=False)
        return df if not df.empty else None
    except Exception as e:
        print(f"[ERROR] Failed to fetch stock data for {symbol}: {e}")
        return None

def get_fundamentals(symbol):
    """
    Fetch key fundamental indicators using yfinance.
    """
    try:
        if not symbol.endswith('.NS'):
            symbol += '.NS'
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "symbol": symbol,
            "pe_ratio": info.get("trailingPE", None),
            "eps": info.get("trailingEps", None),
            "roe": info.get("returnOnEquity", None),
            "book_value": info.get("bookValue", None)
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch fundamentals for {symbol}: {e}")
        return None

def load_nse_tickers():
    """
    Load all NSE stock symbols from a CSV file (must include 'Symbol' column).
    The file should be named 'nse_tickers.csv' and located in the root directory.
    """
    try:
        df = pd.read_csv("nse_tickers.csv")  # Make sure the file is in the repo
        symbols = df['Symbol'].dropna().unique().tolist()
        return [sym.strip().upper() + ".NS" for sym in symbols if isinstance(sym, str)]
    except Exception as e:
        print(f"[ERROR] Failed to load NSE tickers from CSV: {e}")
        return []
