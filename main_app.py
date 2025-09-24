import streamlit as st
import pandas as pd
from batch_runner import analyze_single_stock, analyze_all_stocks

# ---------------- UI Config ---------------- #
st.set_page_config(page_title="AI-based NSE Stock Recommender", layout="wide")
st.title("📈 AI-based NSE Stock Recommender")

# ---------------- Single Stock Section ---------------- #
st.header("🔍 Analyze Individual NSE Stock")
symbol = st.text_input("Enter NSE Symbol (e.g., INFY, TCS)", "")

if st.button("Analyze") and symbol:
    with st.spinner(f"Analyzing {symbol.upper()}..."):
        result = analyze_single_stock(symbol.upper())
    if result is None:
        st.error("❌ Could not fetch data for this symbol.")
    else:
        term = result["term"]
        explanation = result["explanation"]
        fundamentals = result["fundamentals"]
        technicals = result["technicals"]
        sentiment = result.get("sentiment", {})
        confidence = result.get("confidence", {})

        # 🎯 Categorization Result
        term_emoji = {"Short-Term": "🟢", "Mid-Term": "🟡", "Long-Term": "🔵"}
        st.markdown(f"## {term_emoji.get(term, '')} Recommended Holding Period: **{term}**")
        st.markdown("---")

        # 💼 Fundamental Strength
        st.subheader("💼 Fundamental Strength")
        for key, value in fundamentals.items():
            st.write(f"- **{key}**: {value}")

        # 📉 Technical Analysis
        st.subheader("📉 Technical Indicators")
        for key, value in technicals.items():
            st.write(f"- **{key}**: {value}")

        # 🧠 Explanation
        st.subheader("🧠 AI Explanation")
        st.success(explanation)

        # 🔥 Confidence Levels
        st.subheader("🔥 Confidence Scores by Term")
        st.dataframe(pd.DataFrame.from_dict(confidence, orient="index", columns=["Confidence (%)"]))

# ---------------- Batch Analysis Section ---------------- #
st.markdown("---")
st.header("📊 Batch Scan for All NSE Stocks")

if st.button("Run Batch Scan"):
    with st.spinner("Running analysis on all NSE stocks... (this may take time)"):
        batch_results = analyze_all_stocks()

    st.success(f"✅ Scanned {batch_results['count']} stocks successfully.")

    st.subheader("🟢 Top 5 Short-Term Picks")
    st.table(pd.DataFrame(batch_results["short"]))

    st.subheader("🟡 Top 5 Mid-Term Picks")
    st.table(pd.DataFrame(batch_results["mid"]))

    st.subheader("🔵 Top 5 Long-Term Picks")
    st.table(pd.DataFrame(batch_results["long"]))
