def recommend_term(technicals):
    """
    Recommend an investment horizon based on technical indicators.

    Parameters:
    - technicals (dict): Dictionary containing technical indicators like MACD and RSI.

    Returns:
    - str: One of "Short Term", "Medium Term", or "Long Term"
    """
    macd = technicals.get("macd", 0)
    rsi = technicals.get("rsi", 0)

    if macd > 0 and 40 < rsi < 60:
        return "Short Term"
    elif macd > 0 and rsi <= 40:
        return "Medium Term"
    elif macd > 0 and rsi >= 60:
        return "Long Term"
    else:
        return "Short Term"
