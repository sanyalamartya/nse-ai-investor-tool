import pandas as pd
import streamlit as st
import openai
from openai import OpenAI

from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term

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
        explanation = response.choices[0].message.content.strip()
    except Exception as e:
        explanation = "Failed to generate explanation."
        st.error(f"OpenAI API error: {e}")

    return explanation


# Streamlit UI
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
            explanation = generate_ai_explanation(ticker, fundamentals, technicals, recommendation)

        st.success(f"📌 Recommended Term: **{recommendation}**")

        st.markdown("### 🧠 AI Explanation")
        st.markdown(explanation)

        st.markdown("### 📊 Fundamentals")
        st.json(fundamentals)

        st.markdown("### 📈 Technical Indicators")
        st.json(technicals)
        import batch_runner

st.markdown("---")
st.header("📊 Run Full Market Scan (Batch Mode)")

if st.button("Run Batch Analysis"):
    with st.spinner("Analyzing all stocks... this may take a few minutes ⏳"):
        results = batch_runner.analyze_all_stocks()
        df = pd.DataFrame(results)
        df.to_csv("batch_results.csv", index=False)
        st.success("Batch analysis completed and saved to batch_results.csv ✅")

        # Display top 5 per term
        for term in ["Short Term", "Medium Term", "Long Term"]:
            st.subheader(f"Top 5 Recommendations: {term}")
            top_df = df[df["Recommendation"] == term].head(5)
            st.table(top_df[["Ticker", "Recommendation"]])

    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
