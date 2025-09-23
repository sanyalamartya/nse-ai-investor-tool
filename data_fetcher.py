import pandas as pd
import yfinance as yf

# ---------------------- NSE Ticker Loader ---------------------- #
def load_nse_tickers():
    """
    Load list of NSE stock tickers from the 'nse_symbols_full' file.
    Each symbol will be converted to the format used by Yahoo Finance (e.g., TCS -> TCS.NS).
    """
    try:
        with open("nse_symbols_full", "r") as f:
            tickers = [line.strip() for line in f if line.strip()]

        formatted = [symbol.upper() + ".NS" for symbol in tickers]
        return formatted

    except Exception as e:
        print(f"❌ Error loading tickers: {e}")
        return []

# ---------------------- Stock Price Data ---------------------- #
def get_stock_data(symbol, period="6mo", interval="1d"):
    """
    Fetch historical stock price data using yfinance.
    """
    try:
        if not symbol.upper().endswith(".NS"):
            symbol += ".NS"

        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)

        if data.empty:
            print(f"⚠️ No historical data found for {symbol}")
            return None
        return data

    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None

# ---------------------- Fundamentals ---------------------- #
def get_fundamentals(symbol):
    """
    Fetch basic financial data for a given symbol using yfinance.
    """
    try:
        if not symbol.upper().endswith(".NS"):
            symbol += ".NS"

        ticker = yf.Ticker(symbol)
        info = ticker.info

        if not info or 'symbol' not in info:
            print(f"⚠️ No fundamental data found for {symbol}")
            return None

        fundamentals = {
            "symbol": info.get("symbol"),
            "longName": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "priceToBook": info.get("priceToBook"),
            "returnOnEquity": info.get("returnOnEquity"),
            "debtToEquity": info.get("debtToEquity"),
            "revenueGrowth": info.get("revenueGrowth"),
            "profitMargins": info.get("profitMargins"),
            "dividendYield": info.get("dividendYield"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        }

        return fundamentals

    except Exception as e:
        print(f"❌ Error fetching fundamentals for {symbol}: {e}")
        return None
