import yfinance as yf

def get_stock_data(ticker, period="6mo", interval="1d"):
    stock = yf.Ticker(ticker + ".NS")
    return stock.history(period=period, interval=interval)

def get_fundamentals(ticker):
    try:
        stock = yf.Ticker(ticker + ".NS")
        info = stock.info

        return {
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "book_value": info.get("bookValue"),
            "dividend_yield": info.get("dividendYield"),
            "face_value": info.get("faceValue")
        }
    except Exception as e:
        return {"error": str(e)}
