import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker + ".NS")

        # Technical indicators (based on price history)
        hist = stock.history(period="6mo")
        if hist.empty:
            raise ValueError("No historical data found for this symbol.")

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
            "Bollinger_Upper": hist['UpperBand'].iloc[-1],
            "Bollinger_Lower": hist['LowerBand'].iloc[-1],
            "Close_vs_Bollinger": "Above upper band" if hist['Close'].iloc[-1] > hist['UpperBand'].iloc[-1] else (
                "Below lower band" if hist['Close'].iloc[-1] < hist['LowerBand'].iloc[-1] else "Within band"
            )
        }

        # Fundamentals (using yfinance info)
        info = stock.info
        fundamentals = {
            "PE_ratio": info.get("trailingPE", None),
            "EPS": info.get("trailingEps", None),
            "Book_value": info.get("bookValue", None),
            "ROE": info.get("returnOnEquity", None),
            "Market_cap": info.get("marketCap", None),
            "Dividend_yield": info.get("dividendYield", None),
        }

        return {
            "technicals": technicals,
            "fundamentals": fundamentals,
        }

    except Exception as e:
        raise RuntimeError(f"Failed to fetch data for {ticker}: {str(e)}")
