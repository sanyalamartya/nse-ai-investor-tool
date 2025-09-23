import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    """Used for analyzing a single stock."""
    stock = yf.Ticker(ticker + ".NS")
    hist = stock.history(period="6mo")

    if hist.empty:
        raise ValueError("No historical data found for this symbol.")

    # Technical indicators
    hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
    hist['EMA50'] = hist['Close'].ewm(span=50, adjust=False).mean()
    hist['UpperBand'] = hist['Close'].rolling(window=20).mean() + 2 * hist['Close'].rolling(window=20).std()
    hist['LowerBand'] = hist['Close'].rolling(window=20).mean() - 2 * hist['Close'].rolling(window=20).std()

    technicals = {
        "latest_close": hist['Close'].iloc[-1],
        "EMA20": hist['EMA20'].iloc[-1],
        "EMA50": hist['EMA50'].iloc[-1],
        "Above_EMA20": hist['Close'].iloc[-1] > hist['EMA20'].iloc[-1],
        "Above_EMA50": hist['Close'].iloc[-1] > hist['EMA50'].iloc[-1],
        "Close_vs_Bollinger": "Above upper band" if hist['Close'].iloc[-1] > hist['UpperBand'].iloc[-1]
                              else "Below lower band" if hist['Close'].iloc[-1] < hist['LowerBand'].iloc[-1]
                              else "Within band"
    }

    info = stock.info
    fundamentals = {
        "PE_ratio": info.get("trailingPE"),
        "EPS": info.get("trailingEps"),
        "Book_value": info.get("bookValue"),
        "ROE": info.get("returnOnEquity"),
        "Market_cap": info.get("marketCap"),
        "Dividend_yield": info.get("dividendYield")
    }

    return {
        "technicals": technicals,
        "fundamentals": fundamentals
    }


def get_stock_data(ticker):
    """Used by batch_runner to return only technical data."""
    stock = yf.Ticker(ticker + ".NS")
    hist = stock.history(period="6mo")

    if hist.empty:
        return None

    hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
    hist['EMA50'] = hist['Close'].ewm(span=50, adjust=False).mean()
    hist['UpperBand'] = hist['Close'].rolling(window=20).mean() + 2 * hist['Close'].rolling(window=20).std()
    hist['LowerBand'] = hist['Close'].rolling(window=20).mean() - 2 * hist['Close'].rolling(window=20).std()

    return {
        "latest_close": hist['Close'].iloc[-1],
        "EMA20": hist['EMA20'].iloc[-1],
        "EMA50": hist['EMA50'].iloc[-1],
        "Above_EMA20": hist['Close'].iloc[-1] > hist['EMA20'].iloc[-1],
        "Above_EMA50": hist['Close'].iloc[-1] > hist['EMA50'].iloc[-1],
        "Close_vs_Bollinger": "Above upper band" if hist['Close'].iloc[-1] > hist['UpperBand'].iloc[-1]
                              else "Below lower band" if hist['Close'].iloc[-1] < hist['LowerBand'].iloc[-1]
                              else "Within band"
    }


def get_fundamentals(ticker):
    """Used by batch_runner to return only fundamental data."""
    stock = yf.Ticker(ticker + ".NS")
    info = stock.info

    return {
        "PE_ratio": info.get("trailingPE"),
        "EPS": info.get("trailingEps"),
        "Book_value": info.get("bookValue"),
        "ROE": info.get("returnOnEquity"),
        "Market_cap": info.get("marketCap"),
        "Dividend_yield": info.get("dividendYield")
    }
