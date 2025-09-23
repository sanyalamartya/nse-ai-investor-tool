from data_fetcher import get_stock_data, get_fundamentals
from recommendation_engine import rank_stocks

def load_nse_tickers():
    # Use a broader, realistic list for testing
    return [
        "TCS", "INFY", "RELIANCE", "HDFCBANK", "ICICIBANK", "SBIN", "WIPRO", "LT",
        "AXISBANK", "KOTAKBANK", "ITC", "BAJFINANCE", "BHARTIARTL", "ADANIENT",
        "ASIANPAINT", "MARUTI", "ULTRACEMCO", "TECHM", "HINDUNILVR", "TITAN",
        "POWERGRID", "NTPC", "HCLTECH", "ONGC", "JSWSTEEL", "COALINDIA",
        "BAJAJFINSV", "SUNPHARMA", "BPCL", "TATAMOTORS", "VEDL", "INDUSINDBK",
        "GRASIM", "DRREDDY", "BRITANNIA", "CIPLA", "UPL", "SHREECEM", "TATASTEEL",
        "HINDALCO", "HEROMOTOCO", "BAJAJ-AUTO", "EICHERMOT", "DIVISLAB", "SBILIFE",
        "ICICIPRULI", "HDFCLIFE", "ADANIPORTS", "GAIL"
    ]

def analyze_all_stocks():
    tickers = load_nse_tickers()
    print(f"🔍 Total tickers to analyze: {len(tickers)}")
    
    results = []
    for ticker in tickers:
        try:
            print(f"📈 Fetching data for: {ticker}")
            technicals = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)

            if technicals and fundamentals:
                results.append({
                    "ticker": ticker,
                    "technicals": technicals,
                    "fundamentals": fundamentals
                })
            else:
                print(f"⚠️ Skipped {ticker}: Missing data.")
        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")
            continue

    print(f"✅ Total stocks successfully analyzed: {len(results)}")
    return results

def get_ranked_stocks(results, term="short"):
    return rank_stocks(results, term)
