import pandas as pd
from .base_strategy import Strategy


class BenchmarkStrategy(Strategy):

    def generate_signals(self, price_data):
        signals_df = pd.DataFrame(0,price_data.index, price_data.columns)
        signals_df.iloc[0] = 1
        return signals_df

        