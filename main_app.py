import streamlit as st
from batch_runner import analyze_all_stocks, get_ranked_stocks
from recommendation_engine import recommend_term
from data_fetcher import get_stock_data, get_fundamentals

# App title
st.set_page_config(page_title="NSE AI Stock Recommender", layout="wide")
st.markdown("# 📈 AI-based Investment Horizon Recommendations")

# Section: Analyze a single stock
st.markdown("## 📉 Analyze a Single Stock")
symbol = st.text_input("Enter NSE Stock Symbol (e.g., INFY, TCS)")

if st.button("Analyze"):
    if symbol:
        st.info(f"Analyzing {symbol.upper()}...")
        data = get_stock_data(symbol)
        fundamentals = get_fundamentals(symbol)
        if data is not None and not data.empty and fundamentals:
            recommendation = recommend_term(fundamentals, data)
            st.success(f"📊 **Recommended Horizon: {recommendation.upper()}**")
        else:
            st.error("❌ Could not fetch data for this symbol.")
    else:
        st.warning("Please enter a stock symbol.")

st.markdown("---")

# Section: Batch scan for all stocks
st.markdown("## 🔍 Or run batch scan for all stocks")
if st.button("Run Batch Scan"):
    st.success("✅ Batch scan completed.")
    all_results = analyze_all_stocks()
    
    st.markdown(f"**Total stocks analyzed:** {len(all_results)}")

    # Top 5 for each horizon
    for term in ["short", "mid", "long"]:
        st.markdown(f"### 📌 Top 5 Stocks for {term.capitalize()}-Term")
        top_stocks = get_ranked_stocks(all_results, term=term)
        if not top_stocks.empty:
            st.dataframe(top_stocks.head(5), use_container_width=True)
        else:
            st.info(f"No top {term}-term stocks found.")
