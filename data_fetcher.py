import yfinance as yf

def load_nse_tickers():
    # Sample list for demo – replace with actual NSE symbols
    return ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

def get_stock_data(symbol):
    try:
        data = yf.Ticker(symbol)
        hist = data.history(period="3mo")
        
        # Example of computing simple technical signals
        recent_close = hist["Close"].iloc[-1]
        prev_close = hist["Close"].iloc[-2]

        return {
            "recent_close": recent_close,
            "prev_close": prev_close,
            "ema_signal": "bullish" if recent_close > hist["Close"].ewm(span=20).mean().iloc[-1] else "bearish",
            "macd_signal": "bullish",  # Placeholder
            "rsi_signal": "bullish"    # Placeholder
        }
    except:
        return None

def get_fundamentals(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        return {
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "roe": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else None,
            "eps_growth": info.get("earningsQuarterlyGrowth", 0) * 100 if info.get("earningsQuarterlyGrowth") else None,
            "revenue_growth": info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else None,
        }
    except:
        return None
