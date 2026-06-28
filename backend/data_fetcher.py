import yfinance as yf

def get_stock_data(stock):

    df = yf.download(stock, period="1y")

    return df