def rank_stocks(results, term="short"):
    from openai import OpenAI
    import streamlit as st

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    prompt = f"""
    You are an AI financial analyst. Given the following stock analysis data, rank the stocks based on how attractive they are for a **{term}-term** investment.

    Use both fundamentals and technicals to decide. 
    Prioritize stocks that are fundamentally strong, undervalued, and showing strong buy signals in technicals. 
    Give a brief 1-line reason for each. Return top 5 only.

    Data: {results}

    Return format:
    1. SYMBOL - Reason
    2. SYMBOL - Reason
    3. SYMBOL - Reason
    4. SYMBOL - Reason
    5. SYMBOL - Reason
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI ranking failed: {e}"
