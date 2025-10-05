# Assignment 2: Multi-Signal Strategy Simulation on S&P 500
Design, implement, and evaluate multiple technical indicators across a large equity universe using object-oriented Python, with attention to execution speed and capital constraints.

## How to Run
1.  **Set up your environment**. Make sure you have your Python environment (like Anaconda) ready.
2.  **Open the notebook**. Open the `strategyComparison.ipynb` file in Jupyter Notebook.
3.  **Run the code**. Run the cells in the notebook from top to bottom.
4.  **See the results**. The notebook will show you the cumulative performance for all strategies.

## What's Inside? (File Descriptions)
* **`strategyComparison.ipynb`** - The main notebook. **Run this to see the cumulative performance for all strategies**
* **`PriceLoader.py`** - Loads every ticker in the S&P 500 from Wikipedia, downloads the price history for them, and makes a separate parquet file for each in the **`data/sp500prices`** folder.
* **`backtester.py`** - A backtester used to backtest and track performance of different trading strategies.
* Inside the folder strategies, we have the following trading strategies that we test in **`strategyComparison.ipynb`**:
* **`BenchmarkStrategy.py`** - A strategy with the logic: Buy X shares of each ticker on the first day
* **`MovingAverageStrategy.py`** - A strategy with the logic: Buy if 20-day MA > 50-day MA
* **`VolatilityBreakoutStrategy`** - A strategy with the logic: Buy if daily return > rolling 20-day std dev
* **`MACDStrategy`** - A strategy with the logic: Buy if MACD line crosses above signal line
* **`RSIStrategy`** - Buy if RSI < 30 (oversold)
* Other files include:
* **`test.py`** - Which tests the Priceloader in **`PriceLoader.py`**
* In addition to these files, we have a folder called Robert_old, which is old code used while developing the assignment. This code should be ignored.







