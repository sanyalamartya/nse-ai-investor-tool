import streamlit as st
import openai
from openai import OpenAI

from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term

# 🔁 Lazy import for batch functions
# They are imported only when batch button is clicked

# Initialize OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Generate AI explanation
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
    except Exception as e:
        return "Failed to generate explanation."

# Main app
def main():
    st.set_page_config(page_title="NSE AI Stock Recommender", layout="wide")
    st.title("📈 AI-based NSE Stock Recommender")

    st.markdown("### 🔹 Analyze Individual NSE Stock")
    ticker = st.text_input("Enter NSE Symbol (e.g., INFY, TCS)")

    if st.button("Analyze") and ticker:
        try:
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)
            recommendation = recommend_term(technicals)

            st.success(f"📌 Recommended Term: **{recommendation}**")
            st.markdown("---")

            st.write("🧠 **AI Explanation**")
            explanation = generate_ai_explanation(ticker, fundamentals, technicals, recommendation)
            st.write(explanation)

            st.markdown("📊 **Fundamentals**")
            st.json(fundamentals)

            st.markdown("🔧 **Technical Indicators**")
            st.json(technicals)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    # 🔁 Batch Mode Section
    st.markdown("---")
    st.markdown("## 🔍 Run Batch Analysis on All NSE Stocks")

    if st.button("Run Batch Analysis"):
        from batch_runner import analyze_all_stocks, get_top_5_by_term

        with st.spinner("Analyzing all NSE stocks... this may take a few minutes ⏳"):
            results = analyze_all_stocks()
            top_5 = get_top_5_by_term(results)

        st.success("✅ Batch analysis completed!")

        for term, stocks in top_5.items():
            with st.expander(f"Top 5 Stocks for {term}"):
                for stock in stocks:
                    st.markdown(f"**{stock['Ticker']}**  \n📌 *{stock['Recommendation']}*")
                    st.write("🔧 Technicals:")
                    st.json(stock.get("Technicals", {}))
                    st.write("📊 Fundamentals:")
                    st.json(stock.get("Fundamentals", {}))


if __name__ == "__main__":
    main()
