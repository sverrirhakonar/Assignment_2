import pandas as pd
from base_strategy import Strategy


class MovingAverageStrategy(Strategy):

    def __init__(self, short_window = 20, long_window = 50):
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, price_data):
        short_ma = price_data.rolling(window = self.short_window).mean()
        long_ma = price_data.rolling(window = self.long_window).mean()

        is_short_above_long = short_ma > long_ma 
        signals_df = is_short_above_long.astype(int).shift(1)
        
        return signals_df


