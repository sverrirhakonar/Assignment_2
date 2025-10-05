from benchmarkstrategy import BenchmarkStrategy 
import pandas as pd

# class Backtester:
#     def __init__(self):
#         self.history = pd.DataFrame()
#         #self.cash = 
    
#     def update_history(self, new_signal: pd.DataFrame):
#         """
#         Add a new one-row DataFrame (with same columns) to self.history.
#         """
#         if self.history.empty:
#             # First time: just copy it
#             self.history = new_signal.copy()
#         else:
#             # Append new data to the bottom
#             self.history = pd.concat([self.history, new_signal], axis=0)
    
#     def get_history(self):
#         """Return the full accumulated DataFrame. HERNA REIKNA ALLT
#         """
#         return self.history


class Backtester:
    def __init__(self, initial_cash=1_000_000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.signals = pd.DataFrame()        # stores all signal rows
        self.holdings = pd.DataFrame()       # stores cumulative shares
        self.cash_history = []               # cash each step
        self.portfolio_value = []            # total portfolio value each step

    def update_history(self, new_signal: pd.DataFrame, prices: pd.DataFrame):
        """
        Update holdings, cash, and portfolio value based on new signals and prices.
        new_signal: 1-row DataFrame (tickers as columns)
        prices:     1-row DataFrame (tickers as columns)
        """
        # Store signals
        if self.signals.empty:
            self.signals = new_signal.copy()
        else:
            self.signals = pd.concat([self.signals, new_signal], axis=0)

        # Compute trade cost (buys positive, sells negative)
        trade_cost = (new_signal * prices).sum(axis=1).iloc[0]
        self.cash -= trade_cost

        # Update holdings
        if self.holdings.empty:
            current_holdings = new_signal.copy()
        else:
            current_holdings = self.holdings.iloc[[-1]] + new_signal

        self.holdings = pd.concat([self.holdings, current_holdings], axis=0)

        # Compute portfolio value
        total_stock_value = (current_holdings * prices).sum(axis=1).iloc[0]
        total_value = self.cash + total_stock_value

        # Save cash and portfolio history
        self.cash_history.append(self.cash)
        self.portfolio_value.append(total_value)

    def get_summary(self):
        """
        Combine signals, holdings, cash, and portfolio value into one DataFrame.
        Returns a DataFrame indexed by dates with:
        - Signal columns (tickers)
        - Holding columns (prefixed with '_held')
        - Cash
        - PortfolioValue
        """
        df_signals = self.signals.add_prefix("sig_")
        df_holdings = self.holdings.add_prefix("held_")

        # Combine everything
        summary = pd.concat([df_signals, df_holdings], axis=1)
        summary["Cash"] = self.cash_history
        summary["PortfolioValue"] = self.portfolio_value

        return summary

def Backtest(strategy_name,price_df):
    '''Skilar df med ollu ur thessu'''
    strategy_dict = {"BenchmarkStrategy" : BenchmarkStrategy}
    b = Backtester()
    s = strategy_dict[strategy_name]()
    for i in range(len(price_df)):
        prices = price_df.iloc[[i]]
        signals = s.generate_signals(prices)
        b.update_history(signals, prices)



    # for trading_day in price_df:
    #     signals = s.generate_signals(trading_day)
    #     b.update_history(signals)
    
    hist = b.get_summary()
    print(hist)

    

