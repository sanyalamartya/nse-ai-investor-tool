import streamlit as st
from batch_runner import analyze_all_stocks, get_ranked_stocks
from data_fetcher import get_stock_data, get_fundamentals

st.set_page_config(page_title="AI-based Investment Horizon", layout="centered")

st.title("📊 AI-based Investment Horizon Recommendations")

# ─────────────────────────────
# Single Stock Analysis Section
# ─────────────────────────────
st.header("📉 Analyze a Single Stock")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., INFY, TCS)")

if st.button("Analyze"):
    if symbol:
        st.info(f"Analyzing {symbol.upper()}...")

        symbol_full = symbol.upper()
        if not symbol_full.endswith(".NS"):
            symbol_full += ".NS"

        data = get_stock_data(symbol_full)
        fundamentals = get_fundamentals(symbol_full)

        if data is None or fundamentals is None:
            st.error("❌ Could not fetch data for this symbol.")
        else:
            st.success("✅ Data fetched successfully!")
            st.subheader("Fundamentals")
            st.json(fundamentals)

            st.subheader("Recent Price Data")
            st.dataframe(data.tail(5))
    else:
        st.warning("Please enter a symbol to analyze.")

# ─────────────────────────────
# Batch Analysis Section
# ─────────────────────────────
st.markdown("---")
st.header("🔍 Or run batch scan for all stocks")

if st.button("Run Batch Scan"):
    st.info("Running batch scan. Please wait...")

    results = analyze_all_stocks()

    if not results:
        st.error("❌ No stocks were analyzed.")
    else:
        st.success("✅ Batch scan completed.")
        st.write(f"**Total stocks analyzed:** {len(results)}")

        st.subheader("📌 Top 5 Stocks for Short-Term")
        short = get_ranked_stocks(results, term="short")
        st.dataframe(short)

        st.subheader("📌 Top 5 Stocks for Mid-Term")
        mid = get_ranked_stocks(results, term="mid")
        st.dataframe(mid)

        st.subheader("📌 Top 5 Stocks for Long-Term")
        long = get_ranked_stocks(results, term="long")
        st.dataframe(long)
