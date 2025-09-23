import pandas as pd
from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term, rank_stocks
import time

def load_nse_tickers(filename="nse_symbols_full.csv"):
    df = pd.read_csv(filename)
    tickers = df["SYMBOL"].dropna().unique().tolist()
    return tickers

def analyze_all_stocks(limit=None):
    tickers = load_nse_tickers()
    if limit:
        tickers = tickers[:limit]  # Optional: only run first few for testing

    print(f"📊 Total tickers loaded: {len(tickers)}")

    results = []

    for idx, ticker in enumerate(tickers):
        try:
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)
            recommendation = recommend_term(technicals, fundamentals)

            results.append({
                "Ticker": ticker,
                "Recommendation": recommendation,
                "Fundamentals": fundamentals,
                "Technicals": technicals
            })

            print(f"[{idx+1}/{len(tickers)}] ✅ Processed {ticker}")

            time.sleep(0.5)  # Delay to avoid rate-limiting (adjust as needed)

        except Exception as e:
            print(f"[{idx+1}/{len(tickers)}] ❌ Skipped {ticker} due to error: {e}")

    return results

def get_ranked_stocks(results, term="long"):
    term_results = [r for r in results if r["Recommendation"].lower() == term]
    ranked = rank_stocks(term_results)
    return ranked
