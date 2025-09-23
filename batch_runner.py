import pandas as pd

def load_nse_tickers(filename="nse_symbols_full"):
    with open(filename, "r") as f:
        lines = f.readlines()
    # Remove header if exists and strip whitespace
    tickers = [line.strip() for line in lines if line.strip() != "SYMBOL"]
    return tickers
