import pandas as pd
from .base_strategy import Strategy

class MACDStrategy(Strategy):

    def __init__(self, short_window = 12, long_window = 26, signal_window = 9):
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window

    def generate_signals(self, price_data):
        short_ema = price_data.ewm(span=self.short_window, adjust=False).mean()
        long_ema = price_data.ewm(span=self.long_window, adjust=False).mean()

        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=self.signal_window, adjust=False).mean()

        is_macd_above_signal = macd_line > signal_line
        crossover_events = (is_macd_above_signal.astype(int).diff() > 0)

        signals_df = pd.DataFrame(0, index=price_data.index, columns=price_data.columns)
        buy_signals = crossover_events.shift(1)
        signals_df[buy_signals] = 1

        return signals_df

