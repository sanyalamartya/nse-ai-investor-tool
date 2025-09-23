import streamlit as st
from recommendation_engine import recommend_term, get_ranked_stocks
from batch_runner import analyze_all_stocks

# Page settings
st.set_page_config(page_title="AI Stock Horizon Recommender", layout="centered")

def main():
    st.image("https://cdn-icons-png.flaticon.com/512/2331/2331970.png", width=60)
    st.title("📊 AI-based Investment Horizon Recommendations")

    # --- Section 1: Manual Stock Symbol Input ---
    st.markdown("### 📈 Analyze a Single Stock")

    symbol = st.text_input("Enter NSE Stock Symbol (e.g., INFY, TCS)", "")
    if st.button("Analyze"):
        if symbol.strip() == "":
            st.warning("Please enter a valid stock symbol.")
        else:
            try:
                from data_fetcher import fetch_stock_data
                data = fetch_stock_data(symbol.strip().upper())
                technicals = data["technicals"]
                fundamentals = data["fundamentals"]
                term = recommend_term(technicals)

                st.success(f"✅ Recommended Investment Horizon: **{term.capitalize()}-Term**")
                st.subheader("🧠 Fundamentals")
                st.json(fundamentals)
                st.subheader("📊 Technical Indicators")
                st.json(technicals)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

    # --- Section 2: Batch Scan Button ---
    st.markdown("---")
    st.markdown("### 🔍 Or run batch scan for all stocks")

    if st.button("Run Batch Scan"):
        with st.spinner("Running batch scan..."):
            results = analyze_all_stocks()
            st.success("✅ Batch scan completed.")
            st.markdown(f"**Total stocks analyzed:** {len(results)}")

            # Display top 5 for each term
            for term in ["short", "mid", "long"]:
                st.markdown(f"### 🤖 AI Ranking of Top 5 Stocks for {term.capitalize()}-Term")
                top_ranked = get_ranked_stocks(results, term=term)
                if not top_ranked:
                    st.info(f"No top {term}-term stocks found.")
                    continue

                for i, stock in enumerate(top_ranked, start=1):
                    st.markdown(f"{i}. **{stock['ticker']}** - {stock['explanation']}")

if __name__ == "__main__":
    main()
