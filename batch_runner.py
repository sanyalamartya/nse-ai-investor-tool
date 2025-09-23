import pandas as pd
from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term

def load_nse_tickers(filename="nse_symbols_full"):
    with open(filename, "r") as f:
        lines = f.readlines()
        tickers = [line.strip() for line in lines if line.strip() != "SYMBOL"]
    return tickers

def analyze_all_stocks():
    tickers = load_nse_tickers()
    results = []

    for ticker in tickers:
        try:
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)
            recommendation = recommend_term(technicals)

            results.append({
                "Ticker": ticker,
                "Recommendation": recommendation,
                "Fundamentals": fundamentals,
                "Technicals": technicals
            })

        except Exception as e:
            results.append({
                "Ticker": ticker,
                "Error": str(e)
            })

    return results

def get_top_5_by_term(results):
    short = []
    mid = []
    long = []

    for res in results:
        if "Recommendation" in res:
            rec = res["Recommendation"].lower()
            if "short" in rec:
                short.append(res)
            elif "mid" in rec:
                mid.append(res)
            elif "long" in rec:
                long.append(res)

    # Return top 5 from each (currently in order of appearance)
    return {
        "Short Term": short[:5],
        "Mid Term": mid[:5],
        "Long Term": long[:5]
    }

if __name__ == "__main__":
    results = analyze_all_stocks()
    top_5 = get_top_5_by_term(results)

    # Save to file or just print
    for term, stocks in top_5.items():
        print(f"\n🟢 Top 5 for {term}:")
        for stock in stocks:
            print(f" - {stock['Ticker']} | {stock['Recommendation']}")
