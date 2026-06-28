from data_fetcher import get_stock_data

df = get_stock_data("TCS.NS")

print(df.head())