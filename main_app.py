import streamlit as st
from batch_runner import analyze_all_stocks
from data_fetcher import get_stock_data, get_fundamentals
from recommendation_engine import recommend_term

st.set_page_config(page_title="AI Investment Recommendations", layout="centered")

st.markdown("📊 # AI-based Investment Horizon Recommendations")

# --- Single Stock Analyzer ---
st.markdown("📈 **Analyze a Single Stock**")
symbol = st.text_input("Enter NSE Stock Symbol (e.g., INFY, TCS)")

if st.button("Analyze"):
    if symbol:
        st.info(f"Analyzing {symbol}...")
        data = get_stock_data(symbol + ".NS")
        fundamentals = get_fundamentals(symbol + ".NS")

        if data and fundamentals:
            recommendation = recommend_term(fundamentals, data)
            st.success(f"📊 **Recommended Horizon: {recommendation.upper()}**")
        else:
            st.error("❌ Could not fetch data for this symbol.")

# --- Batch Analyzer ---
st.markdown("🔍 **Or run batch scan for all stocks**")
if st.button("Run Batch Scan"):
    st.info("Scanning all NSE stocks. Please wait...")
    short_top5, mid_top5, long_top5, total_analyzed = analyze_all_stocks()
    st.success("✅ Batch scan completed.")
    st.markdown(f"**Total stocks analyzed:** {total_analyzed}")

    st.markdown("📌 ### Top 5 Stocks for Short-Term")
    st.dataframe(short_top5)

    st.markdown("📌 ### Top 5 Stocks for Mid-Term")
    st.dataframe(mid_top5)

    st.markdown("📌 ### Top 5 Stocks for Long-Term")
    st.dataframe(long_top5)
