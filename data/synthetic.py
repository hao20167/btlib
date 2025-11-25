from typing import Optional
import numpy as np
import pandas as pd
import datetime


def generate_random_walk(
    start_price: float,
    n: int = 500,
    mu: float = 0.0,
    sigma: float = 1.0,
    freq: str = "D",
    seed: Optional[int] = None,
    start: datetime.datetime = "2001-01-01"
) -> pd.DataFrame:
    
    rng = np.random.default_rng(seed)
    steps = rng.normal(loc=mu, scale=sigma, size=n)
    prices = start_price + np.cumsum(steps)

    index = pd.date_range(start="2000-01-01", periods=n, freq=freq)
    close = prices
    open_ = np.concatenate([[prices[0]], prices[:-1]])
    high = np.maximum(open_, close) + np.abs(rng.normal(0, sigma * 0.5, size=n))
    low = np.minimum(open_, close) - np.abs(rng.normal(0, sigma * 0.5, size=n))
    volumn = rng.integers(1000, 10000, size=n)

    df = pd.DataFrame(
        {
            "Open": open_,
            "High": high,
            "Low": low,
            "Close": close,
            "Volumn": volumn
        },
        index=index
    )
    df.index.name="datetime"

    return df

# Geometric Brownian Motion path
def generate_gbm(
    start_price: float,
    n: int = 500,
    mu: float = 0.05,
    sigma: float = 0.2,
    dt: float = 1/252,
    freq: str = "B",
    seed: Optional[int] = None,
    start: datetime.datetime = "2001-01-01"
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    z = rng.normal(size=n)
    increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    log_price = np.log(start_price) + np.cumsum(increments)
    prices = np.exp(log_price)

    index = pd.date_range(start=start, periods=n, freq=freq)
    close = prices
    open_ = np.concatenate([[prices[0]], prices[:-1]])
    high = np.maximum(open_, close) + np.abs(rng.normal(0, sigma * 0.5, size=n))
    low = np.minimum(open_, close) - np.abs(rng.normal(0, sigma * 0.5, size=n))
    volumn = rng.integers(1000, 10000, size=n)

    df = pd.DataFrame(
        {
            "Open": open_,
            "High": high,
            "Low": low,
            "Close": close,
            "Volumn": volumn
        },
        index=index
    )
    df.index.name="datetime"

    return df