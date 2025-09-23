from data_fetcher import get_stock_data, get_fundamentals, load_nse_tickers
from recommendation_engine import recommend_term
import pandas as pd

def analyze_all_stocks():
    tickers = load_nse_tickers()
    results = []

    for symbol in tickers:
        try:
            data = get_stock_data(symbol)
            fundamentals = get_fundamentals(symbol)
            if data and fundamentals:
                term = recommend_term(fundamentals, data)
                results.append({"symbol": symbol, "term": term})
        except Exception:
            continue  # skip failures

    df = pd.DataFrame(results)

    short_df = df[df["term"] == "short"].head(5).reset_index(drop=True)
    mid_df = df[df["term"] == "mid"].head(5).reset_index(drop=True)
    long_df = df[df["term"] == "long"].head(5).reset_index(drop=True)

    return short_df, mid_df, long_df, len(df)
