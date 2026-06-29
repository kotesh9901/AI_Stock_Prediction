import yfinance as yf

def fetch_stock_data(stock):

    # Download stock data
    df = yf.download(stock, period="1y")

    # Convert MultiIndex columns to normal columns
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    # Remove missing values
    df = df.dropna()

    # Moving averages
    df["MA_50"] = df["Close"].rolling(50).mean()
    df["MA_200"] = df["Close"].rolling(200).mean()

    # Remove NaN rows
    df = df.dropna()

    # Latest row
    latest = df.iloc[-1]

    # Features for AI
    features = [
        latest["Open"],
        latest["High"],
        latest["Low"],
        latest["Close"],
        latest["Volume"],
        latest["MA_50"],
        latest["MA_200"]
    ]

    return features