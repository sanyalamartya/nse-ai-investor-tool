def recommend_term(technicals, fundamentals=None):
    """
    Determines investment horizon based on combined technical and fundamental analysis.
    
    Inputs:
    - technicals: dict with RSI, MACD, EMA signals, Bollinger band signals
    - fundamentals: dict with key ratios (optional, for AI or future scoring)

    Output:
    - str: One of "Short Term", "Mid Term", "Long Term"
    """

    rsi = technicals.get("rsi", 50)
    macd = technicals.get("macd", 0)
    ema_crossover = technicals.get("ema_crossover", "none")  # "bullish", "bearish", "none"
    bollinger_signal = technicals.get("bollinger", "neutral")  # "breakout", "breakdown", "neutral"

    score = 0

    # RSI scoring
    if rsi > 65:
        score += 2  # strong upward momentum
    elif rsi < 35:
        score -= 1  # oversold, possible bounce
    else:
        score += 0

    # MACD scoring
    if macd > 0.5:
        score += 2
    elif macd > 0:
        score += 1
    else:
        score -= 1

    # EMA crossover scoring
    if ema_crossover == "bullish":
        score += 2
    elif ema_crossover == "bearish":
        score -= 2

    # Bollinger band scoring
    if bollinger_signal == "breakout":
        score += 1
    elif bollinger_signal == "breakdown":
        score -= 1

    # Optional: add fundamentals score boost in future

    # Final classification
    if score >= 4:
        return "Long Term"
    elif 1 <= score < 4:
        return "Mid Term"
    else:
        return "Short Term"
