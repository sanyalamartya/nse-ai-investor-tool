def rank_stocks(stock_data, term):
    scored = []

    for stock in stock_data:
        score = 0

        # Sample scoring logic (tweak as needed)
        if stock.get("pe_ratio") and stock["pe_ratio"] < 25:
            score += 1
        if stock.get("eps") and stock["eps"] > 10:
            score += 1
        if stock.get("roe") and stock["roe"] > 10:
            score += 1

        # Technicals
        if term == "short":
            if stock.get("macd_signal") == "bullish":
                score += 1
            if stock.get("ema_signal") == "bullish":
                score += 1
        elif term == "mid":
            if stock.get("rsi_signal") == "bullish":
                score += 1
            if stock.get("ema_signal") == "bullish":
                score += 1
        elif term == "long":
            if stock.get("eps_growth") and stock["eps_growth"] > 10:
                score += 1
            if stock.get("revenue_growth") and stock["revenue_growth"] > 10:
                score += 1

        if score > 0:
            scored.append({"symbol": stock["symbol"], "score": score})

    # Sort and return top 5
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:5]
