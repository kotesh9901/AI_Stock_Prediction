import yfinance as yf

def get_chart_data(stock):

    df = yf.download(stock, period="30d")

    # Handle MultiIndex columns from yfinance
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    labels = df.index.strftime("%d-%m").tolist()
    prices = df["Close"].round(2).tolist()

    return labels, prices