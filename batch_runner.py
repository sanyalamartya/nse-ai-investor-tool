# batch_runner.py

from data_fetcher import get_stock_data, get_fundamentals, load_nse_tickers

def score_stock(fundamentals, hist):
    score = {"short": 0, "mid": 0, "long": 0}

    if not fundamentals or hist is None or hist.empty:
        return score

    pe = fundamentals.get("pe_ratio")
    eps = fundamentals.get("eps")
    roe = fundamentals.get("roe")
    book_value = fundamentals.get("book_value")

    # Short-term logic
    if pe and pe < 25:
        score["short"] += 1
    if eps and eps > 20:
        score["short"] += 1

    # Mid-term logic
    if eps and eps > 20:
        score["mid"] += 1
    if roe and roe > 0.15:
        score["mid"] += 1

    # Long-term logic
    if pe and pe < 20:
        score["long"] += 1
    if roe and roe > 0.15:
        score["long"] += 1
    if book_value and book_value > 0:
        score["long"] += 1

    return score

def analyze_all_stocks():
    tickers = load_nse_tickers()
    short_term, mid_term, long_term = [], [], []
    total_analyzed = 0

    for symbol in tickers:
        try:
            data = get_stock_data(symbol)
            fundamentals = get_fundamentals(symbol)

            if data is None or fundamentals is None:
                continue

            total_analyzed += 1
            scores = score_stock(fundamentals, data)

            short_term.append({"symbol": symbol, "score": scores["short"]})
            mid_term.append({"symbol": symbol, "score": scores["mid"]})
            long_term.append({"symbol": symbol, "score": scores["long"]})

        except Exception as e:
            print(f"[ERROR] Failed to analyze {symbol}: {e}")

    def top5(lst):
        return sorted(lst, key=lambda x: x["score"], reverse=True)[:5]

    return {
        "short_term": top5(short_term),
        "mid_term": top5(mid_term),
        "long_term": top5(long_term),
        "total_analyzed": total_analyzed
    }
