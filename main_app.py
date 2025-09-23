import streamlit as st
from openai import OpenAI
from data_fetcher import get_stock_data, get_fundamentals
from technical_analysis import analyze_technical_signals
from recommendation_engine import recommend_term, rank_stocks
from batch_runner import analyze_all_stocks, get_ranked_stocks

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----- AI Explanation for single stock -----
def generate_ai_explanation(ticker, fundamentals, technicals, recommendation):
    prompt = f"""
    You are a stock analyst assistant. Explain in 2-3 simple bullet points why the stock {ticker} is recommended for {recommendation}-term investment.

    Fundamentals: {fundamentals}
    Technicals: {technicals}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI explanation failed: {e}"

# ----- Streamlit App UI -----
def main():
    st.title("📈 Get AI-based investment horizon recommendations")
    st.write("### Enter NSE Stock Symbol (e.g., INFY, TCS)")

    ticker = st.text_input("Enter Symbol")

    if st.button("Analyze") and ticker:
        try:
            stock_data = get_stock_data(ticker)
            fundamentals = get_fundamentals(ticker)
            technicals = analyze_technical_signals(stock_data)
            recommendation = recommend_term(technicals)

            st.success(f"📌 Recommended Term: **{recommendation.title()}-Term Investment**")

            # Show AI Explanation
            st.markdown("----")
            st.subheader("🧠 AI Explanation")
            explanation = generate_ai_explanation(ticker, fundamentals, technicals, recommendation)
            st.write(explanation)

            # Show Fundamentals & Technicals
            st.markdown("----")
            st.subheader("📊 Fundamentals")
            st.json(fundamentals)

            st.subheader("🔧 Technical Indicators")
            st.json(technicals)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    # ----- Batch Scanner -----
    st.markdown("---")
    st.header("🔍 Or run batch scan for all stocks")

    if st.button("Run Batch Scan"):
        with st.spinner("Analyzing all stocks... this may take a minute."):
            try:
                results = analyze_all_stocks()
                st.success("✅ Batch scan completed.")
                st.write(f"Total stocks analyzed: **{len(results)}**")

                # Rank by each term
                for term in ["short", "mid", "long"]:
                    st.subheader(f"🤖 AI Ranking of Top 5 Stocks for {term.title()}-Term")
                    try:
                        ranked = get_ranked_stocks(results, term)
                        st.markdown(ranked)
                    except Exception as e:
                        st.error(f"AI ranking failed for {term}-term: {e}")

            except Exception as e:
                st.error(f"Batch scan failed: {e}")

if __name__ == "__main__":
    main()
