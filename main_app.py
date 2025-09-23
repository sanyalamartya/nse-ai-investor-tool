import streamlit as st
import openai
from openai import OpenAI

from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Generate AI explanation using OpenAI
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

# Streamlit UI and logic
def main():
    st.title("📈 Get AI-based investment horizon recommendations")
    st.write("### Enter NSE Stock Symbol (e.g., INFY, TCS)")

    ticker = st.text_input("Enter Symbol")

    if st.button("Analyze") and ticker:
        try:
            # Fetch data
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)

            # Recommendation logic (make sure this line has 'technicals' passed in!)
            recommendation = recommend_term(technicals)

            # Show recommendation
            st.success(f"📌 Recommended Term: **{recommendation}**")
            st.markdown("----")

            # AI Explanation
            st.write("🧠 **AI Explanation**")
            explanation = generate_ai_explanation(ticker, fundamentals, technicals, recommendation)
            st.write(explanation)

            # Fundamentals
            st.markdown("📊 **Fundamentals**")
            st.json(fundamentals)

            # Technicals
            st.markdown("🔧 **Technical Indicators**")
            st.json(technicals)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Run the app
if __name__ == "__main__":
    main()
