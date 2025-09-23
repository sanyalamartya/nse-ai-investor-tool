import os
from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term, rank_stocks

def load_nse_tickers(filename="nse_symbols_full.csv"):
    # Fallback tickers if file not found
    if not os.path.exists(filename):
        return ["TCS", "INFY", "RELIANCE", "HDFCBANK", "ICICIBANK"]
    
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

def get_ranked_stocks(results):
    return rank_stocks(results)
