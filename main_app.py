import streamlit as st
from batch_runner import analyze_all_stocks, get_ranked_stocks

# Other imports...
from recommendation_engine import recommend_term  # if used individually elsewhere

def display_ranked_stocks(rankings, title):
    st.markdown(f"### 😎 AI Ranking of Top 5 Stocks for {title}-Term")
    if not rankings:
        st.info("No stocks found for this term.")
        return

    for i, stock in enumerate(rankings, start=1):
        st.markdown(f"**{i}. {stock['ticker']}** - {stock['explanation']}")

def main():
    st.title("📊 AI-based Investment Horizon Recommendations")

    st.markdown("## 🔍 Or run batch scan for all stocks")
    if st.button("Run Batch Scan"):
        with st.spinner("Analyzing all stocks..."):
            results = analyze_all_stocks()
            st.success("✅ Batch scan completed.")
            st.markdown(f"**Total stocks analyzed:** {len(results)}")

            # Show top 5 per term
            short_ranked = get_ranked_stocks(results, term="short", top_n=5)
            display_ranked_stocks(short_ranked, "Short")

            mid_ranked = get_ranked_stocks(results, term="mid", top_n=5)
            display_ranked_stocks(mid_ranked, "Mid")

            long_ranked = get_ranked_stocks(results, term="long", top_n=5)
            display_ranked_stocks(long_ranked, "Long")

if __name__ == "__main__":
    main()
