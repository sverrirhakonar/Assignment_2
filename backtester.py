import pandas as pd
from strategies.base_strategy import Strategy
from strategies.BenchmarkStrategy import BenchmarkStrategy
from strategies.ma_strategy import MovingAverageStrategy
from strategies.MACDStrategy import MACDStrategy
from strategies.RSIStrategy import RSIStrategy
from strategies.VolatilityBreakoutStrategy import VolatilityBreakoutStrategy


class Backtester:
    def __init__(self, initial_cash = 1_000_000):
        self.initial_cash = initial_cash
    
    def run(self, strategy, price_data):
        cash = self.initial_cash
        holdings = pd.Series(0, price_data.columns)
        portfolio_history = []

        signals_df = strategy.generate_signals(price_data)

        for date in price_data.index:
            prices_today = price_data.loc[date]
            signals_today = signals_df.loc[date]
            stocks_to_buy = signals_today[signals_today == 1].index
            for ticker in stocks_to_buy:
                current_price = prices_today[ticker]
                if cash >= current_price:
                    holdings[ticker] += 1
                    cash -= current_price
            holdings_value = (holdings * prices_today).sum()
            total_value = cash + holdings_value
            portfolio_history.append({'total_value': total_value, 'cash': cash, 'holdings_value': holdings_value})
        results_df = pd.DataFrame(portfolio_history, index=price_data.index)
        return results_df






