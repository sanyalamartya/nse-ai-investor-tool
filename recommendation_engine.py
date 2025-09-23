def recommend_term(technicals, fundamentals):
    # Simple logic based on indicators
    if technicals.get("EMA_Crossover") == "Bullish" and technicals.get("RSI") < 70:
        return "short"
    elif technicals.get("MACD") == "Bullish" or technicals.get("Bollinger") == "Breakout":
        return "mid"
    else:
        return "long"


def rank_stocks(stocks):
    ranked = []
    for stock in stocks:
        try:
            fundamentals = stock.get("Fundamentals", {})
            technicals = stock.get("Technicals", {})

            score = 0
            reasons = []

            # PE ratio check
            pe = fundamentals.get("PE Ratio")
            if pe and 5 < pe < 20:
                score += 2
                reasons.append("attractive PE")

            # EPS check
            eps = fundamentals.get("EPS")
            if eps and eps > 10:
                score += 2
                reasons.append("strong EPS")

            # Book value check
            book = fundamentals.get("Book Value")
            if book and book > 100:
                score += 1
                reasons.append("high book value")

            # EMA crossover
            if technicals.get("EMA_Crossover") == "Bullish":
                score += 2
                reasons.append("bullish EMA")

            # Bollinger breakout
            if technicals.get("Bollinger") == "Breakout":
                score += 1
                reasons.append("bollinger breakout")

            # MACD
            if technicals.get("MACD") == "Bullish":
                score += 1
                reasons.append("bullish MACD")

            stock["Score"] = score
            stock["Reasons"] = reasons
            ranked.append(stock)

        except Exception:
            continue

    return sorted(ranked, key=lambda x: x["Score"], reverse=True)


def get_ranked_stocks(results, term):
    filtered = [s for s in results if s.get("Recommendation") == term]
    ranked = rank_stocks(filtered)
    return ranked
