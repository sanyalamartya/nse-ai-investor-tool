import streamlit as st
import openai
from openai import OpenAI

from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term, rank_stocks
from batch_runner import analyze_all_stocks, get_ranked_stocks

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_ai_explanation(ticker, fundamentals, technicals, recommendation):
    prompt = f"""
    You are a stock analyst assistant. Explain to a beginner investor in simple language why the stock {ticker} has been recommended as {recommendation}.

    Fundamentals: {fundamentals}
    Technical Indicators: {technicals}

    Give the explanation in 2-3 bullet points, easy to understand.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Failed to generate explanation."

def main():
    st.title("📈 Get AI-based investment horizon recommendations")
    st.write("### Enter NSE Stock Symbol (e.g., INFY, TCS)")

    ticker = st.text_input("Enter Symbol")
    if st.button("Analyze") and ticker:
        try:
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)
            recommendation = recommend_term(technicals, fundamentals)

            st.success(f"📌 Recommended Term: **{recommendation}**")
            st.markdown("----")

            st.write("🧠 **AI Explanation**")
            explanation = generate_ai_explanation(ticker, fundamentals, technicals, recommendation)
            st.write(explanation)

            st.markdown("📊 **Fundamentals**")
            st.json(fundamentals)

            st.markdown("🔧 **Technical Indicators**")
            st.json(technicals)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    st.markdown("---")
    st.write("### 🔍 Or run batch scan for all stocks")

    if st.button("Run Batch Scan"):
        with st.spinner("Scanning all stocks... this may take a few minutes."):
            results = analyze_all_stocks()

        st.success("✅ Batch scan completed.")
        st.write(f"Total stocks analyzed: **{len(results)}**")

        short_ranked = get_ranked_stocks(results, term="short")
        mid_ranked = get_ranked_stocks(results, term="mid")
        long_ranked = get_ranked_stocks(results, term="long")

        st.markdown("## 📊 Top 5 Short-Term Recommendations")
        if short_ranked:
            for i, stock in enumerate(short_ranked[:5], 1):
                st.markdown(f"{i}. **{stock['Ticker']}** - {stock['AI Explanation']}")
        else:
            st.warning("No short-term recommendations found.")

        st.markdown("## ⏳ Top 5 Mid-Term Recommendations")
        if mid_ranked:
            for i, stock in enumerate(mid_ranked[:5], 1):
                st.markdown(f"{i}. **{stock['Ticker']}** - {stock['AI Explanation']}")
        else:
            st.warning("No mid-term recommendations found.")

        st.markdown("## 📈 Top 5 Long-Term Recommendations")
        if long_ranked:
            for i, stock in enumerate(long_ranked[:5], 1):
                st.markdown(f"{i}. **{stock['Ticker']}** - {stock['AI Explanation']}")
        else:
            st.warning("No long-term recommendations found.")

if __name__ == "__main__":
    main()
