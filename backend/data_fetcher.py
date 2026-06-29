import yfinance as yf

def fetch_stock_data(stock):

    df = yf.download(stock, period="1y")

    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna()

    df["MA_50"] = df["Close"].rolling(50).mean()
    df["MA_200"] = df["Close"].rolling(200).mean()

    df = df.dropna()

    latest = df.iloc[-1]

    features = [
        float(latest["Open"]),
        float(latest["High"]),
        float(latest["Low"]),
        float(latest["Close"]),
        float(latest["Volume"]),
        float(latest["MA_50"]),
        float(latest["MA_200"])
    ]

    return features