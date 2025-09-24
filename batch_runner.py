import yfinance as yf
import numpy as np
import pandas as pd
from data_fetcher import load_nse_tickers

# ---------------------- Term Categorization Logic ---------------------- #
def categorize_term(volatility, trend_strength, eps_growth):
    if volatility < 0.02 and trend_strength > 0.5:
        return "Short-Term"
    elif 0.02 <= volatility <= 0.05 and trend_strength > 0.3:
        return "Mid-Term"
    elif eps_growth > 0.10:
        return "Long-Term"
    else:
        return "Mid-Term"

# ---------------------- Explanation Generator ---------------------- #
def generate_explanation(term, fundamentals, technicals):
    expl = []
    if term == "Short-Term":
        expl.append("Low volatility and strong price momentum suggest a short-term opportunity.")
    elif term == "Mid-Term":
        expl.append("Balanced fundamentals and medium volatility make this a mid-term candidate.")
    elif term == "Long-Term":
        expl.append("High EPS growth and stable financials support long-term investment potential.")

    if "Trend" in technicals:
        expl.append(f"Trend: {technicals['Trend']}")
    if "EPS Growth" in fundamentals:
        expl.append(f"EPS Growth: {fundamentals['EPS Growth']}")

    return " ".join(expl)

# ---------------------- Core Function: Analyze One Stock ---------------------- #
def analyze_single_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="6mo")
        info = ticker.info

        if hist.empty or not info:
            print(f"⚠️ No data for {symbol}")
            return None

        # Fundamental Metrics
        pe_ratio = info.get("trailingPE")
        roe = info.get("returnOnEquity")
        eps = info.get("trailingEps")
        debt_to_equity = info.get("debtToEquity")
        eps_growth = info.get("earningsQuarterlyGrowth", 0) or 0

        fundamentals = {
            "P/E Ratio": round(pe_ratio, 2) if pe_ratio else "N/A",
            "ROE": f"{round(roe * 100, 1)}%" if roe else "N/A",
            "EPS": round(eps, 2) if eps else "N/A",
            "Debt/Equity": round(debt_to_equity, 2) if debt_to_equity else "N/A",
            "EPS Growth": f"{round(eps_growth * 100, 1)}%" if eps_growth else "N/A"
        }

        # Technical Metrics
        hist['Return'] = hist['Close'].pct_change()
        volatility = hist['Return'].std()

        hist['SMA_20'] = hist['Close'].rolling(20).mean()
        trend_strength = (hist['SMA_20'].iloc[-1] - hist['SMA_20'].iloc[0]) / hist['SMA_20'].iloc[0]

        technicals = {
            "Volatility": round(volatility, 4),
            "Trend": "Bullish" if trend_strength > 0.05 else "Sideways" if trend_strength > 0 else "Bearish"
        }

        # Categorization
        term = categorize_term(volatility, trend_strength, eps_growth)

        # Confidence
        confidence = {
            "Short-Term": round((1 - volatility) * 100),
            "Mid-Term": round((trend_strength + 0.5) * 100),
            "Long-Term": round((eps_growth + 0.1) * 100)
        }

        # Explanation
        explanation = generate_explanation(term, fundamentals, technicals)

        return {
            "term": term,
            "explanation": explanation,
            "fundamentals": fundamentals,
            "technicals": technicals,
            "sentiment": {},
            "confidence": confidence
        }

    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")
        return None

# ---------------------- Batch Runner ---------------------- #
def analyze_all_stocks():
    tickers = load_nse_tickers()
    print(f"✅ Loaded {len(tickers)} tickers.")

    top_short, top_mid, top_long = [], [], []
    all_results = []

    for symbol in tickers:
        result = analyze_single_stock(symbol)
        if result:
            all_results.append((symbol, result))

            score = (
                result["confidence"].get("Short-Term", 0) +
                result["confidence"].get("Mid-Term", 0) +
                result["confidence"].get("Long-Term", 0)
            )
            entry = {"symbol": symbol, "score": score}

            if result["term"] == "Short-Term":
                top_short.append(entry)
            elif result["term"] == "Mid-Term":
                top_mid.append(entry)
            elif result["term"] == "Long-Term":
                top_long.append(entry)

    # Top 5
    top_short = sorted(top_short, key=lambda x: x["score"], reverse=True)[:5]
    top_mid = sorted(top_mid, key=lambda x: x["score"], reverse=True)[:5]
    top_long = sorted(top_long, key=lambda x: x["score"], reverse=True)[:5]

    return {
        "short": top_short,
        "mid": top_mid,
        "long": top_long,
        "count": len(all_results)
    }
