from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def recommend_term(technicals):
    """
    Determine the recommended investment horizon based on technical signals.
    Looks at trend indicators like moving average crossovers, Bollinger bands, RSI, etc.
    """
    if technicals.get("ema_crossover") == "bullish":
        return "short"
    elif technicals.get("bollinger_signal") == "breakout" and technicals.get("rsi") < 70:
        return "mid"
    elif technicals.get("trend") == "strong uptrend":
        return "long"
    else:
        return "mid"  # Default to mid if mixed signals

def rank_stocks(results, term="short"):
    """
    Uses GPT to rank stocks for the specified term ('short', 'mid', 'long') based on fundamentals and technicals.
    """
    prompt = f"""
You are an AI financial analyst. Analyze the following stock data and rank the stocks for a {term}-term investment horizon.

Use both fundamentals and technical indicators. Consider:
- Low PE ratio
- High EPS and ROE
- Solid book value
- Bullish technical signals (EMA crossover, RSI, MACD, Bollinger bands)

Pick the top 5 stocks with a one-line reason each.

Data: {results}

Format:
1. SYMBOL - Reason
2. SYMBOL - Reason
3. SYMBOL - Reason
4. SYMBOL - Reason
5. SYMBOL - Reason
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI ranking failed: {e}"
