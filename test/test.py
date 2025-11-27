import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', '..')))


from btlib.data.loader import load_price
from btlib.core.engine import Backtest
from btlib.analytics.metrics import compute_basic_metrics

from btlib.core.strategy import Strategy

import pandas as pd
import numpy as np

from btlib.indicators.basic import sma

class SMACrossLongOnly(Strategy):    
    def on_start(self):
        window = self.params.get("window", 20)
        self.data["sma"] = sma(self.data["Close"], window)
    
    def on_bar(self):
        rng = np.random.default_rng(seed=36)
        bar = self.current_bar
        ts = self.current_time

        if pd.isna(bar["sma"]):
            return []

        signals = []
        if bar["Close"] > bar["sma"]:
            signals.append(self.buy(size=self.params.get("size", 1.0)))
        elif bar["Close"] < bar["sma"]:
            signals.append(self.sell(size=self.params.get("size", 1.0)))
        
        return signals

# print(pd.to_datetime("2025-11-11"))

df = load_price("input/AAPL_1h_twelvedata.csv", start="2025-11-11")
bt = Backtest(
    data=df,
    symbol="AAPL",
    strategy_class=SMACrossLongOnly,
    initial_cash=10000,
    window=20,
    size=500
)
result = bt.run()

metrics = compute_basic_metrics(result.equity_curve)
print(metrics)

from btlib.analytics.visualization import plot_equity_curve, plot_drawdown, plot_backtest

# print(result.trades)

plot_backtest(series=df, result=result)

plot_equity_curve(result.equity_curve)
plot_drawdown(result.equity_curve)