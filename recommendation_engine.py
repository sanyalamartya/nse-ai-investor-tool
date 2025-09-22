def recommend_term(fundamentals, technicals):
    pe = fundamentals.get("pe_ratio", 0)
    eps = fundamentals.get("eps", 0)
    rsi = technicals.get("RSI", 50)
    volatility = technicals.get("Volatility", 0)

    score = 0
    if eps and eps > 20: score += 2
    if pe and pe < 20: score += 1
    if volatility and volatility < 10: score += 1
    if rsi and rsi > 60: score += 1

    if score >= 4:
        return "Long Term"
    elif 2 <= score < 4:
        return "Mid Term"
    else:
        return "Short Term"
