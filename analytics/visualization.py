import matplotlib.pyplot as plt
import pandas as pd

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