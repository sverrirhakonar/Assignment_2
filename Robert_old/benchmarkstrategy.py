import pandas as pd
from strategy import Strategy


class BenchmarkStrategy(Strategy):
    """Returns signals at day 0 but no other date to buy all stocks"""
    count = 0
    def generate_signals(self, price_data, cash = 1000000):
        BenchmarkStrategy.count += 1
        if BenchmarkStrategy.count == 1:
            signals_df = pd.DataFrame(0,price_data.index, price_data.columns)
            signals_df.iloc[0] = 1
            return signals_df
        else: 
            return pd.DataFrame(0,price_data.index, price_data.columns)

