import yfinance as yf
from nsetools import Nse

nse = Nse()

def get_stock_data(ticker, period="6mo", interval="1d"):
    stock = yf.Ticker(ticker + ".NS")
    return stock.history(period=period, interval=interval)

def get_fundamentals(ticker):
    try:
        info = nse.get_quote(ticker)
        return {
            "pe_ratio": info.get("p/e"),
            "eps": info.get("eps"),
            "book_value": info.get("book_value"),
            "dividend_yield": info.get("dividend_yield"),
            "face_value": info.get("face_value")
        }
    except Exception as e:
        return {"error": str(e)}
