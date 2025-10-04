import pandas as pandas
from base_strategy import Strategy

class VolatilityBreakoutStrategy(Strategy):

    def __init__(self, window = 20):
        self.window = window

    
    def generate_signals(self, price_data):
        daily_returns = price_data.pct_change()
        rolling_std = daily_returns.rolling(window=self.window).std()
    
        breakout_condition = daily_returns > rolling_std
        signals_df = breakout_condition.astype(int).shift(1)
        
        return signals_df
