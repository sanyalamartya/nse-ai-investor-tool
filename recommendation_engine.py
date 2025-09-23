import openai
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def recommend_term(technicals):
    # Use basic logic for horizon recommendation
    if technicals.get("ema_crossover") == "bullish" and technicals.get("rsi") < 70:
        return "short"
    elif technicals.get("bollinger_signal") == "breakout":
        return "mid"
    else:
        return "long"

def rank_stocks(results, term):
    scored_stocks = []

    for result in results:
        if result.get("recommended_term") != term:
            continue

        fundamentals = result.get("fundamentals", {})
        technicals = result.get("technicals", {})

        # Scoring based on fundamentals
        score = 0
        explanation_parts = []

        pe_ratio = fundamentals.get("pe_ratio")
        if pe_ratio and pe_ratio < 20:
            score += 1
            explanation_parts.append("low PE ratio")

        eps = fundamentals.get("eps")
        if eps and eps > 10:
            score += 1
            explanation_parts.append("high EPS")

        roe = fundamentals.get("roe")
        if roe and roe > 10:
            score += 1
            explanation_parts.append("high ROE")

        book_value = fundamentals.get("book_value")
        if book_value and book_value > 100:
            score += 1
            explanation_parts.append("solid book value")

        # Scoring based on technicals
        if technicals.get("ema_crossover") == "bullish":
            score += 1
            explanation_parts.append("bullish EMA crossover")

        if technicals.get("rsi") and 30 < technicals["rsi"] < 70:
            score += 1
            explanation_parts.append("neutral RSI")

        if technicals.get("bollinger_signal") == "breakout":
            score += 1
            explanation_parts.append("Bollinger band breakout")

        # Store score and description
        scored_stocks.append({
            "ticker": result["ticker"],
            "score": score,
            "fundamentals": fundamentals,
            "technicals": technicals,
            "explanation_parts": explanation_parts
        })

    # Sort by score (desc)
    ranked = sorted(scored_stocks, key=lambda x: x["score"], reverse=True)

    # Generate AI explanations
    for stock in ranked:
        stock["explanation"] = generate_ranking_explanation(stock)

    return ranked


def generate_ranking_explanation(stock):
    prompt = f"""
You are an investment assistant. Explain in 1-2 lines why the stock {stock['ticker']} is ranked high.
Here are its strengths:

- Fundamentals: {stock['fundamentals']}
- Technical Indicators: {stock['technicals']}

Make it beginner-friendly, concise, and persuasive.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"{stock['ticker']} - " + ", ".join(stock['explanation_parts'])

def get_ranked_stocks(results, term="short", top_n=5):
    ranked = rank_stocks(results, term)
    return ranked[:top_n]
