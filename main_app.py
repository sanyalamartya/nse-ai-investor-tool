import streamlit as st
from batch_runner import analyze_single_stock
import pandas as pd

st.set_page_config(page_title="AI-based NSE Stock Recommender", layout="wide")

# 🔷 Title
st.markdown("# 📈 AI-based NSE Stock Recommender")
st.markdown("### 🔷 Analyze Individual NSE Stock")

# 🔍 Input
symbol = st.text_input("Enter NSE Symbol (e.g., INFY, TCS)", "")

# Button
if st.button("Analyze") and symbol:
    try:
        # Normalize symbol to uppercase and add .NS if not present
        symbol_clean = symbol.strip().upper()
        if not symbol_clean.endswith(".NS"):
            symbol_clean += ".NS"

        st.info(f"Analyzing `{symbol_clean}`...")

        # Run analysis
        results = analyze_single_stock(symbol_clean)

        if results is None:
            st.error("❌ Could not fetch data for this symbol.")
        else:
            term = results.get("term", "Unknown")
            explanation = results.get("explanation", "")
            fundamentals = results.get("fundamentals", {})
            technicals = results.get("technicals", {})
            sentiment = results.get("sentiment", {})
            confidence = results.get("confidence", {})

            # 🎯 Categorization Result
            term_emoji = {"Short-Term": "🟢", "Mid-Term": "🟡", "Long-Term": "🔵"}
            st.markdown(f"## {term_emoji.get(term, '')} Recommended Holding Period: **{term}**")

            st.markdown("---")

            # 📊 Fundamental Insights
            st.markdown("### 💼 Fundamental Strength")
            if fundamentals:
                for key, value in fundamentals.items():
                    st.write(f"- **{key}**: {value}")
            else:
                st.warning("No fundamental data available.")

            # 📉 Technical Insights
            st.markdown("### 📉 Technical Analysis")
            if technicals:
                for key, value in technicals.items():
                    st.write(f"- **{key}**: {value}")
            else:
                st.warning("No technical analysis found.")

            # 📰 Sentiment
            if sentiment:
                st.markdown("### 📰 Sentiment & Macro View")
                for key, value in sentiment.items():
                    st.write(f"- **{key}**: {value}")

            # 🧠 NLP Explanation
            if explanation:
                st.markdown("### 🤖 AI-Generated Explanation")
                st.success(explanation)

            # 🔥 Confidence Levels
            if confidence:
                st.markdown("### 🔥 Investment Confidence by Term")
                conf_df = pd.DataFrame(list(confidence.items()), columns=["Term", "Confidence (%)"])
                st.dataframe(conf_df)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
