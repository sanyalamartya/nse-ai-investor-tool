def ai_rank_stocks(term, stocks):
    prompt = f"""
You are an investment advisor helping prioritize stocks for a {term} investor.
Based on the fundamentals and technical indicators, rank the following stocks from best to worst, and explain briefly why each is ranked that way.

Respond with the list in this format:

1. TICKER - Explanation
2. TICKER - Explanation
...

Stocks:

"""

    for stock in stocks:
        prompt += f"\nTicker: {stock['Ticker']}\n"
        prompt += f"Fundamentals: {stock.get('Fundamentals', {})}\n"
        prompt += f"Technicals: {stock.get('Technicals', {})}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "❌ Failed to rank stocks with AI."
