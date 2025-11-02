import requests
import pandas as pd
import os
import yfinance as yf
import time
import numpy as np

class Priceloader:
    def __init__(self, index = "SPX"):
        self.index = index
        self.ticker_info = self._load_tickers()
    
    def _load_tickers(self):
        '''
        Load all tickers from a given index and weights from slickcharts.com.
        '''
        # Slickcharts website url
        url_dict = {"SPX" : "https://www.slickcharts.com/sp500", "NDX" : "https://www.slickcharts.com/nasdaq100"}
        url = url_dict[self.index]
        
        # Define the "header" for the request package. Earlier I had an 403 error, this is to mimic a normal human request.
        head = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"),
            "Accept-Language": "en-US,en;q=0.9",}
        request = requests.get(url, headers=head)

        # Read the first table from the HTML string (I know it is the first table on the page)
        df = pd.read_html(request.text, flavor="lxml")[0]

        # Remove the . sign to - in tickers (Berkshire)
        df["Symbol"] = df["Symbol"].str.replace(".", "-")
        # Remove the % sign, and covert the weight to a float. 
        df["Weight"] = df["Weight"].str.replace("%", "").str.strip().astype(float)
        df["Adj Weight"] = df["Weight"]/df["Weight"].sum()
        df["Weight"] = df["Weight"]/100
        clean_df = df[["Company", "Symbol", "Weight", "Adj Weight"]]
        return clean_df
    
    def _load_price_data(self, start_date = "2005-01-01", end_date = "2025-01-01" ,batch_size = 10, include_NA_bool = False):
        tickers = self.ticker_info["Symbol"].tolist()
        os.makedirs("price_data_by_ticker", exist_ok=True)
        file_names = []
        for ticker_index in range(0, len(tickers), batch_size):
                batch = tickers[ticker_index:ticker_index+batch_size]
                data = yf.download(batch, start=start_date, end=end_date, timeout=45) # Add a timeout of 45s since I hav had trouble.
                close_and_vol = data.loc[:, ["Close", "Volume"]]
                
                for ticker in close_and_vol.columns.levels[1]:
                    df_ticker = close_and_vol.loc[:, [('Close', ticker), ('Volume', ticker)]].copy()
                    df_ticker.columns = ['Close', 'Volume']
                    # Make a parquet file for either only tickers where there is no NaN or for every ticker depending on include_NA_bool.
                    if include_NA_bool:  
                        df_ticker.to_parquet(f"price_data_by_ticker/{ticker}.parquet")
                        file_names.append(ticker)
                    elif not df_ticker["Close"].isna().any():
                        df_ticker.to_parquet(f"price_data_by_ticker/{ticker}.parquet")
                time.sleep(0.1)
        print("Price histories have successfully been downloaded and saved into separate parquet files.")


loader = Priceloader("SPX")

loader._load_price_data()