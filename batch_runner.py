import pandas as pd
from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term, rank_stocks

# ✅ Load all NSE equity tickers from CSV
def load_nse_tickers():
    try:
        df = pd.read_csv("data/nse_eq_symbols.csv")  # Ensure this file exists
        symbols = df["Symbol"].dropna().unique().tolist()
        return symbols
    except Exception as e:
        print(f"Error loading tickers: {e}")
        return []

# ✅ Analyze all stocks and gather data
def analyze_all_stocks():
    tickers = load_nse_tickers()
    results = []

    for ticker in tickers:
        try:
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)
            term = recommend_term(technicals, fundamentals)  # 🔁 Updated to use both technical + fundamental
            results.append({
                "ticker": ticker,
                "fundamentals": fundamentals,
                "technicals": technicals,
                "term": term
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return results

# ✅ Get top N ranked stocks for the given investment term
def get_ranked_stocks(results, term="short", top_n=5):
    filtered = [r for r in results if r["term"] == term]
    return rank_stocks(filtered, term)[:top_n]
