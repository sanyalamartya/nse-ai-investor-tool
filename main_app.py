import streamlit as st
from batch_runner import analyze_all_stocks, get_ranked_stocks

st.set_page_config(page_title="NSE Stock Screener", layout="centered")
st.title("📊 AI-based Investment Horizon Recommendations")
st.markdown("🔍 Or run batch scan for all stocks")

if st.button("Run Batch Scan"):
    with st.spinner("Scanning all NSE stocks..."):
        results = analyze_all_stocks()
        total_analyzed = len(results)

        # Get top 5 for each term
        short = get_ranked_stocks(results, term="short")
        mid = get_ranked_stocks(results, term="mid")
        long = get_ranked_stocks(results, term="long")

    st.success("✅ Batch scan completed.")
    st.markdown(f"**Total stocks analyzed:** {total_analyzed}")

    # Output top 5 for each term
    st.subheader("📌 Top 5 Stocks for Short-Term")
    if short:
        st.table(short)
    else:
        st.info("No top short-term stocks found.")

    st.subheader("📌 Top 5 Stocks for Mid-Term")
    if mid:
        st.table(mid)
    else:
        st.info("No top mid-term stocks found.")

    st.subheader("📌 Top 5 Stocks for Long-Term")
    if long:
        st.table(long)
    else:
        st.info("No top long-term stocks found.")
