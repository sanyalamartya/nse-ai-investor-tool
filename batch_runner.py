from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term, rank_stocks

def load_nse_tickers(filename="nse_symbols_full.csv"):
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
            recommendation = recommend_term(technicals, fundamentals)

            results.append({
                "ticker": ticker,
                "fundamentals": fundamentals,
                "technicals": technicals,
                "recommendation": recommendation
            })

        except Exception as e:
            results.append({
                "ticker": ticker,
                "error": str(e)
            })

    return results

# NEW FUNCTION that wraps analyze_all_stocks() and ranks the results
def get_ranked_stocks():
    analyzed = analyze_all_stocks()
    return rank_stocks(analyzed)
