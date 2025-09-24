import pandas as pd

# ---------------------- NSE Ticker Loader ---------------------- #
def load_nse_tickers():
    """
    Load list of NSE stock tickers from a CSV file.
    Assumes the file 'nse_symbols_full.csv' exists with a column 'Symbol'.
    """
    try:
        df = pd.read_csv("nse_symbols_full.csv")

        # Accept flexible column names
        symbol_col = None
        for col in df.columns:
            if col.strip().lower() in ["symbol", "ticker", "nse_symbol"]:
                symbol_col = col
                break

        if not symbol_col:
            raise ValueError("No valid 'Symbol' column found in ticker file.")

        tickers = df[symbol_col].dropna().unique()

        # Format for Yahoo Finance (append .NS)
        formatted = [symbol.strip().upper() + ".NS" for symbol in tickers if isinstance(symbol, str)]

        return formatted

    except Exception as e:
        print(f"❌ Error loading tickers: {e}")
        return []
