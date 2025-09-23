# 🔁 Batch Analysis Section
st.markdown("## 🔍 Run Batch Analysis on All NSE Stocks")

if st.button("Run Batch Analysis"):
    with st.spinner("Analyzing all NSE stocks..."):
        from batch_runner import analyze_all_stocks, get_top_5_by_term
        
        results = analyze_all_stocks()
        top_5 = get_top_5_by_term(results)

    st.success("✅ Batch analysis completed!")

    for term, stocks in top_5.items():
        with st.expander(f"Top 5 Stocks for {term}"):
            for stock in stocks:
                st.markdown(f"**{stock['Ticker']}**  \n📌 *{stock['Recommendation']}*")
                st.write("🔧 Technicals:")
                st.json(stock["Technicals"])
                st.write("📊 Fundamentals:")
                st.json(stock["Fundamentals"])
