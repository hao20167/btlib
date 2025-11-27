import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import mplfinance as mpf
import numpy as np

from btlib.core.engine import BacktestResult
from btlib.execution.orders import OrderSide

def plot_equity_curve(equity_curve: pd.Series):
    plt.figure()
    equity_curve.plot()
    plt.title("Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.tight_layout()
    plt.show()

def plot_drawdown(equity_curve: pd.Series):
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1.0
    plt.figure()
    drawdown.plot()
    plt.title("Drawdown")
    plt.xlabel("Time")
    plt.ylabel("Drawdown")
    plt.tight_layout()
    plt.show()

def plot_backtest(series: pd.DataFrame, result: BacktestResult):
    trades = result.trades # List[Trade]

    # series['timestamp'] = pd.to_datetime(series['datetime'])
    # series.set_index('timestamp')
    series.index = pd.to_datetime(series.index)

    buy_x, buy_y, buy_sizes = [], [], []
    sell_x, sell_y, sell_sizes = [], [], []

    for item in trades:
        ts = item.timestamp
        idxs = series.index.get_indexer([ts], method='nearest')
        if idxs.size == 0 or idxs[0] == -1:
            print('Invalid trade!')
            raise NotImplementedError
            continue

        idx = idxs[0]
        price = series['Close'].iloc[idx]

        base = 40
        k = 10
        marker_size = base + k * abs(float(item.size / 10))

        if item.side == OrderSide.BUY:
            buy_x.append(idx)
            buy_y.append(price)
            buy_sizes.append(marker_size)
        else:
            sell_x.append(idx)
            sell_y.append(price)
            sell_sizes.append(marker_size)

    plt.style.use('default')
    fig, (ax_price, ax_vol) = plt.subplots(
        2, 1,
        sharex=True,
        gridspec_kw={'height_ratios': [3, 1]},
        figsize=(12, 7)
    )

    fig.patch.set_facecolor('#f5f5f5')
    ax_price.set_facecolor('#f9fafb')
    ax_vol.set_facecolor('#f9fafb')

    x = np.arange(len(series))
    width = 0.6

    for i, (idx, row) in enumerate(series.iterrows()):
        o, h, l, c, v = row["Open"], row["High"], row["Low"], row["Close"], row["Volume"]

        if c >= o:
            color = '#26a69a'
            edgecolor = '#1b5e20'
        else:
            color = '#ef5350'
            edgecolor = '#b71c1c'

        ax_price.vlines(i, l, h, linewidth=1.0, color=edgecolor, alpha=0.8)

        rect = Rectangle(
            (i - width/2, min(o, c)),
            width,
            max(abs(c - o), 0.1),
            facecolor=color,
            edgecolor=edgecolor,
            linewidth=1.0
        )
        ax_price.add_patch(rect)
    
    if buy_x:
        ax_price.scatter(
            buy_x, buy_y,
            marker='^',
            s=buy_sizes,
            color='#2e7d32',
            zorder=3,
            label='BUY'
        )
    if sell_x:
        ax_price.scatter(
            sell_x, sell_y,
            marker='v',
            s=sell_sizes,
            color='#c62828',
            zorder=3,
            label='SELL'
        )

    ax_price.set_ylabel("Price", fontsize=11)
    # ax_price.set_title("")
    ax_price.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
    ax_price.legend(loc='upper left')

    colors_vol = ['#26a69a' if c >= o else '#ef5350' for o, c in zip(series["Open"], series["Close"])]
    ax_vol.bar(x, series['Volume'].values, width=0.6, alpha=0.8, edgecolor='none', color=colors_vol)
    ax_vol.set_ylabel("Volume", fontsize=11)
    ax_vol.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

    ax_vol.set_xticks(x[::max(1, len(x)//10)])
    ax_vol.set_xticklabels(series.index.strftime('%D %H:%M')[::max(1, len(x)//10)], rotation=45, ha='right')

    plt.tight_layout()
    plt.show()
    