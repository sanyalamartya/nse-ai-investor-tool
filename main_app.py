import streamlit as st
import pandas as pd
from batch_runner import analyze_single_stock, analyze_all_stocks

st.set_page_config(page_title="📈 AI-Based NSE Stock Recommender", layout="wide")

# 🔷 Title
st.title("📊 AI-Based NSE Stock Recommender")

# ---------------------- Tabs for Two Features ---------------------- #
tab1, tab2 = st.tabs(["🔍 Analyze Individual Stock", "📊 Batch Scan Top Picks"])

# ====================== TAB 1: Individual Stock ====================== #
with tab1:
    st.subheader("🔎 Enter NSE Symbol (e.g., INFY, TCS)")
    symbol = st.text_input("Stock Symbol")

    if st.button("Analyze") and symbol:
        st.info(f"Analyzing {symbol.upper()}...")

        result = analyze_single_stock(symbol.upper() + ".NS")
        if not result:
            st.error("❌ Could not fetch data. Please check the symbol or try again later.")
        else:
            term = result["term"]
            fundamentals = result["fundamentals"]
            technicals = result["technicals"]
            sentiment = result.get("sentiment", {})
            explanation = result["explanation"]
            confidence = result.get("confidence", {})

            # Display recommendation
            st.markdown(f"## ✅ Recommended Term: **{term}**")

            st.markdown("---")
            st.markdown("### 📊 Fundamentals")
            for k, v in fundamentals.items():
                st.write(f"- **{k}**: {v}")

            st.markdown("### 📈 Technicals")
            for k, v in technicals.items():
                st.write(f"- **{k}**: {v}")

            if sentiment:
                st.markdown("### 📰 Sentiment")
                for k, v in sentiment.items():
                    st.write(f"- **{k}**: {v}")

            st.markdown("### 🧠 AI Explanation")
            st.success(explanation)

            if confidence:
                st.markdown("### 🔥 Confidence Scores")
                df_conf = pd.DataFrame(list(confidence.items()), columns=["Term", "Confidence"])
                st.dataframe(df_conf)

# ====================== TAB 2: Batch Screening ====================== #
with tab2:
    st.subheader("📂 Run Batch Analysis on All NSE Stocks")

    if st.button("🔁 Run Full Scan"):
        st.info("⏳ Scanning all stocks... please wait.")
        result = analyze_all_stocks()

        if result:
            st.success(f"✅ Screened {result['count']} stocks!")

            st.markdown("### 🟢 Top 5: Short-Term Picks")
            df_short = pd.DataFrame(result["short"])
            st.table(df_short)

            st.markdown("### 🟡 Top 5: Mid-Term Picks")
            df_mid = pd.DataFrame(result["mid"])
            st.table(df_mid)

            st.markdown("### 🔵 Top 5: Long-Term Picks")
            df_long = pd.DataFrame(result["long"])
            st.table(df_long)
        else:
            st.error("⚠️ No results to show. Something went wrong.")

