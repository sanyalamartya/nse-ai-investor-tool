import streamlit as st
import openai
from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term, generate_ai_explanation
def generate_ai_explanation(ticker, fundamentals, technicals, recommendation):
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    prompt = f"""
    You are a stock analyst assistant. Explain to a beginner investor in simple language why the stock {ticker} has been recommended for a {recommendation} investment.

    Fundamentals: {fundamentals}
    Technical Indicators: {technicals}

    Give the explanation in 2-3 bullet points, easy to understand.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
        )
        explanation = response.choices[0].message.content.strip()
        return explanation

    except Exception as e:
        return f"AI explanation could not be generated: {e}"

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
        # AI Explanation using LLM
explanation = generate_ai_explanation(ticker, fundamentals, technicals, recommendation)

st.markdown("### 🤖 AI Explanation")
st.info(explanation)

        st.markdown("### 📊 Fundamentals")
        st.json(fundamentals)
        st.markdown("### 📈 Technicals")
        st.json(technicals)

    except Exception as e:
        st.error(f"Error analyzing {ticker}: {e}")
