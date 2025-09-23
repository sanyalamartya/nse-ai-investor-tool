import yfinance as yf
import pandas as pd

def analyze_technical_signals(stock_data):
    if stock_data is None or stock_data.empty:
        return {}

    df = stock_data.copy()

    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    latest_rsi = round(rsi.iloc[-1], 2)

    # MACD
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    latest_macd = round(macd.iloc[-1], 2)

    # EMA crossover
    ema_20 = df['Close'].ewm(span=20, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    crossover = "none"
    if ema_20.iloc[-2] < ema_50.iloc[-2] and ema_20.iloc[-1] > ema_50.iloc[-1]:
        crossover = "bullish"
    elif ema_20.iloc[-2] > ema_50.iloc[-2] and ema_20.iloc[-1] < ema_50.iloc[-1]:
        crossover = "bearish"

    # Bollinger Bands
    ma20 = df['Close'].rolling(window=20).mean()
    std20 = df['Close'].rolling(window=20).std()
    upper_band = ma20 + 2 * std20
    lower_band = ma20 - 2 * std20
    close = df['Close'].iloc[-1]

    if close > upper_band.iloc[-1]:
        bollinger_signal = "breakout"
    elif close < lower_band.iloc[-1]:
        bollinger_signal = "breakdown"
    else:
        bollinger_signal = "neutral"

    return {
        "rsi": latest_rsi,
        "macd": latest_macd,
        "ema_crossover": crossover,
        "bollinger": bollinger_signal
    }
