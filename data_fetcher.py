import pandas as pd
import yfinance as yf

def load_nse_tickers():
    try:
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        df = pd.read_csv(url)
        tickers = df['SYMBOL'].tolist()
        return [symbol + ".NS" for symbol in tickers]
    except Exception as e:
        print("Error loading NSE tickers:", e)
        return []

def get_stock_data(symbol):
    try:
        df = yf.download(symbol, period="6mo", progress=False)
        return df if not df.empty else None
    except Exception:
        return None

def get_fundamentals(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "book_value": info.get("bookValue"),
            "roe": info.get("returnOnEquity")
        }
    except Exception:
        return None
