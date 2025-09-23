import pandas as pd
from data_fetcher import get_stock_data, get_fundamentals, load_nse_tickers

# Score function for investment horizon
def score_stock(data, fundamentals, term):
    score = 0

    # Validate input
    if data is None or fundamentals is None:
        return 0

    # Common financial metrics
    pe = fundamentals.get('PE')
    eps = fundamentals.get('EPS')
    roe = fundamentals.get('ROE')
    book_value = fundamentals.get('Book Value')

    # Price momentum - short-term
    if term == "short":
        if data['Close'].iloc[-1] > data['Close'].iloc[-5]:
            score += 1
        if data['Close'].iloc[-1] > data['Close'].mean():
            score += 1

    # Mid-term
    if term == "mid":
        if data['Close'].iloc[-1] > data['Close'].iloc[-20]:
            score += 1
        if pe and pe < 20:
            score += 1
        if roe and roe > 15:
            score += 1

    # Long-term
    if term == "long":
        if pe and pe < 15:
            score += 1
        if eps and eps > 0:
            score += 1
        if roe and roe > 15:
            score += 1
        if book_value and book_value > 0:
            score += 1

    return score


def analyze_all_stocks():
    tickers = load_nse_tickers()
    results = []

    for symbol in tickers:
        try:
            data = get_stock_data(symbol)
            fundamentals = get_fundamentals(symbol)

            if data is not None and fundamentals is not None:
                result = {
                    "symbol": symbol,
                    "data": data,
                    "fundamentals": fundamentals
                }
                results.append(result)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    return results


def get_ranked_stocks(results, term):
    scored = []

    for stock in results:
        symbol = stock['symbol']
        data = stock['data']
        fundamentals = stock['fundamentals']

        score = score_stock(data, fundamentals, term)
        scored.append({"symbol": symbol, "score": score})

    df = pd.DataFrame(scored)
    df = df.sort_values(by="score", ascending=False)

    return df.head(5)
