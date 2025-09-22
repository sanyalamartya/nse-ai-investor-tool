import streamlit as st
from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term

st.set_page_config(page_title="NSE AI Stock Analyzer", layout="centered")

st.title("📈 NSE AI Stock Analyzer")
st.subheader("Get AI-based investment horizon recommendations")

ticker = st.text_input("Enter NSE Stock Symbol (e.g., INFY, TCS)", value="INFY").upper()

if st.button("Analyze"):
    try:
        with st.spinner("Fetching data and running analysis..."):
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)
            recommendation = recommend_term(fundamentals, technicals)

        st.success(f"📌 Recommended Term: **{recommendation}**")
        st.markdown("### 📊 Fundamentals")
        st.json(fundamentals)
        st.markdown("### 📈 Technicals")
        st.json(technicals)

    except Exception as e:
        st.error(f"Error analyzing {ticker}: {e}")
