
import pandas as pd
import yfinance as yf
import os
import time
import requests

##### Link for the Wikipedia page for S&P500 #####
URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
##### A dictionary tricking wikipedia thinking we are an actual user #####
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

START_DATE = "2005-01-01"
END_DATE = "2025-01-01"

class PriceLoader:
    def __init__(self, data_directory = "data/sp500prices/"):
        self.data_path = data_directory
        os.makedirs(self.data_path, exist_ok=True)
        self.tickers = self._get_sp500_tickers()
    
    def _get_sp500_tickers(self):
        url = URL
        headers = HEADERS

        response = requests.get(url, headers=headers)
        table = pd.read_html(response.text)

        list_of_tickers = table[0]['Symbol'].tolist()
        tickers = [x.replace('.', '-') for x in list_of_tickers]

        return tickers

    def _download_all_data(self):
        for ticker in self.tickers:
            file_path = os.path.join(self.data_path, f"{ticker}.parquet")
            if not os.path.exists(file_path):
                try:
                    print(f"Downloading: {ticker}")
                    data = yf.download(ticker, start= START_DATE, end= END_DATE)
                    if data.empty:
                        print(f"The data for ticker {ticker} is empty")
                        continue
                    data.to_parquet(file_path)
                except Exception as e:
                    print(f"Failed to download ticker: {ticker}, Error: {e}")
                time.sleep(0.1)
    
    def get_prices(self):
        self._download_all_data()
        price_data = []

        for ticker in self.tickers:
            file_path = os.path.join(self.data_path, f"{ticker}.parquet")
            if os.path.exists(file_path):
                ticker_data = pd.read_parquet(file_path)
                prices = ticker_data['Close']
                prices.name = ticker
                price_data.append(prices)
        df = pd.concat(price_data, axis = 1)
        return df
    

    
