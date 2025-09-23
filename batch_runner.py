from data_fetcher import get_stock_data, get_fundamentals, load_nse_tickers
from recommendation_engine import rank_stocks

def analyze_all_stocks():
    tickers = load_nse_tickers()
    results = []

    for symbol in tickers:
        try:
            technicals = get_stock_data(symbol)
            fundamentals = get_fundamentals(symbol)

            if technicals and fundamentals:
                combined = {"symbol": symbol, **technicals, **fundamentals}
                results.append(combined)
        except Exception:
            pass  # Ignore failed fetches silently for now

    return results

def get_ranked_stocks(results, term="short"):
    return rank_stocks(results, term)
