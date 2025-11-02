import yfinance as yf
batch = ["AMZN", "GOOGL", "fdsklfsd"]
data = yf.download(batch, start="2005-01-01", end="2025-01-01")
close_and_vol = data.loc[:, ["Close", "Volume"]]

for ticker in close_and_vol.columns.levels[1]:
    df_ticker = close_and_vol.loc[:, [('Close', ticker), ('Volume', ticker)]].copy()
    df_ticker.columns = ['Close', 'Volume']
    df_ticker = df_ticker.reset_index() # I like to have the index in a 
    
    
    # df_ticker= close_and_vol["Close"][ticker]
    # df_ticker["Volume"] = close_and_vol["Volume"][ticker]
    print(df_ticker)

