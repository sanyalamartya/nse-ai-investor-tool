# main_app.py

import streamlit as st
from data_fetcher import get_stock_data, get_fundamentals
from batch_runner import analyze_all_stocks

# Set page layout
st.set_page_config(page_title="NSE AI Stock Recommender", layout="wide")
st.title("📊 AI-Based Investment Horizon Recommender")

# -------------------- Single Stock Analysis --------------------
st.header("🔍 Analyze a Single NSE Stock")

symbol = st.text_input("Enter NSE Symbol (e.g., INFY, TCS)")

if st.button("Analyze") and symbol:
    with st.spinner(f"Analyzing {symbol}..."):
        if not symbol.endswith(".NS"):
            symbol += ".NS"

        data = get_stock_data(symbol)
        fundamentals = get_fundamentals(symbol)

        if data is None or fundamentals is None:
            st.error("⚠️ Could not fetch data for this symbol.")
        else:
            st.success(f"✅ Data fetched for {symbol}")
            
            # Simple rule-based recommendation
            pe = fundamentals.get("pe_ratio")
            eps = fundamentals.get("eps")
            roe = fundamentals.get("roe")
            book_value = fundamentals.get("book_value")

            score = {"short": 0, "mid": 0, "long": 0}
            explanation = []

            if pe and pe < 25:
                score["short"] += 1
                explanation.append("Low PE Ratio (<25)")

            if eps and eps > 20:
                score["short"] += 1
                score["mid"] += 1
                explanation.append("High EPS (>20)")

            if roe and roe > 0.15:
                score["mid"] += 1
                score["long"] += 1
                explanation.append("High ROE (>15%)")

            if pe and pe < 20:
                score["long"] += 1

            if book_value and book_value > 0:
                score["long"] += 1
                explanation.append("Positive Book Value")

            # Determine recommended term
            recommended_term = max(score, key=score.get)
            label = {
                "short": "📍 Short-Term",
                "mid": "⏳ Mid-Term",
                "long": "🏦 Long-Term"
            }.get(recommended_term, "N/A")

            st.subheader(f"🧭 Investment Horizon Recommendation: **{label}**")
            st.markdown("**Why?** " + ", ".join(explanation))

            with st.expander("📊 Fundamentals"):
                st.json(fundamentals)

# -------------------- Batch Scan Section --------------------
st.markdown("---")
st.header("📡 Batch Scan Across All NSE Stocks")

if st.button("Run Batch Scan"):
    with st.spinner("Scanning all stocks..."):
        results = analyze_all_stocks()

        st.success("✅ Batch scan completed")
        st.markdown(f"**Total Stocks Analyzed:** `{results['total_analyzed']}`")

        def display(title, stocks):
            st.subheader(title)
            if not stocks:
                st.info("No recommendations found.")
            else:
                st.table(stocks)

        display("📍 Top 5 Stocks for Short-Term", results["short_term"])
        display("⏳ Top 5 Stocks for Mid-Term", results["mid_term"])
        display("🏦 Top 5 Stocks for Long-Term", results["long_term"])
