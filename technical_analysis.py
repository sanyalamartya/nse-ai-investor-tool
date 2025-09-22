import ta

def analyze_technical_signals(df):
    df = df.copy()
    df = ta.add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume")

    signals = {
        "RSI": df["momentum_rsi"].iloc[-1],
        "MACD": df["trend_macd"].iloc[-1],
        "Volatility": df["volatility_bbm"].std()
    }

    if signals["RSI"] > 70:
        signals["trend"] = "Overbought"
    elif signals["RSI"] < 30:
        signals["trend"] = "Oversold"
    else:
        signals["trend"] = "Neutral"

    return signals
