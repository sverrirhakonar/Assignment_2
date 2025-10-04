import pandas as pandas
from .base_strategy import Strategy

class RSIStrategy(Strategy):
    def __init__(self, period=14, oversold_threshold=30):
        self.period = period
        self.oversold_threshold = oversold_threshold
    
    def generate_signals(self, price_data):
        delta = price_data.diff()

        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)

        avg_gain = gains.ewm(span=self.period, adjust=False).mean()
        avg_loss = losses.ewm(span=self.period, adjust=False).mean()

        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

        is_oversold = rsi < self.oversold_threshold
        signals_df = is_oversold.astype(int).shift(1)

        return signals_df