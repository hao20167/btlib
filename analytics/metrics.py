import numpy as np
import pandas as pd


def compute_basic_metrics(equity_curve: pd.Series, risk_free_rate: float = 0.0) -> dict:
    returns = equity_curve.pct_change().dropna()

    total_return = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1
    avg_return = returns.mean()
    vol = returns.std()

    if vol != 0:
        sharpe = (avg_return - risk_free_rate) / vol
    else:
        sharpe = np.nan
    
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    max_dd = drawdown.min()

    return {
        "total_return": float(total_return),
        "avg_return": float(avg_return),
        "volatility": float(vol),
        "sharpe": float(sharpe),
        "max_drawdown": float(max_dd)
    }