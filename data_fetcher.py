import pandas as pd

# ---------------------- NSE Ticker Loader ---------------------- #
def load_nse_tickers():
    """
    Load and return list of formatted NSE stock tickers for Yahoo Finance.
    Reads from 'nse_symbols_full' which contains one symbol per line.
    """
    try:
        # Read symbol file
        df = pd.read_csv("nse_symbols_full", header=None)

        if df.empty:
            raise ValueError("⚠️ NSE ticker file is empty.")

        # Clean and extract symbols
        symbols = df[0].dropna().astype(str).str.strip().str.upper()

        # Filter out invalid values (e.g., if by mistake some row has numbers)
        valid_symbols = symbols[symbols.str.match("^[A-Z]{1,10}$")]

        # Append ".NS" for Yahoo Finance
        formatted = [s + ".NS" for s in valid_symbols]

        return formatted

    except FileNotFoundError:
        print("❌ 'nse_symbols_full' file not found.")
        return []

    except Exception as e:
        print(f"❌ Error loading NSE tickers: {e}")
        return []
