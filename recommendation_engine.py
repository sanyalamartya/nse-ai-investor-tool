def recommend_term(fundamentals, data):
    pe = fundamentals.get("pe_ratio")
    eps = fundamentals.get("eps")
    bv = fundamentals.get("book_value")
    roe = fundamentals.get("roe")

    if pe is None or eps is None or bv is None or roe is None:
        return "unknown"

    score = 0

    if pe < 20:
        score += 1
    if eps > 10:
        score += 1
    if bv and bv > 100:
        score += 1
    if roe and roe > 0.15:
        score += 1

    if score >= 3:
        return "short"
    elif score == 2:
        return "mid"
    else:
        return "long"
