import os
import pandas as pd
from .validation import validate_dataframe

def load_price(path: str, start=None, end=None) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    
    df = pd.read_csv(path)
    df.index = df['datetime']
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_convert(None)

    # print('this is ', pd.to_datetime(df.index[0]) >= pd.to_datetime(start))
    # df = pd.read_csv(path, parse_dates=["datetime"], index_col="datetime")

    _ = validate_dataframe(df=df, strict=True)

    if start is not None:
        df = df[df.index >= pd.to_datetime(start)]
    if end is not None:
        df = df[df.index <= pd.to_datetime(end)]

    return df
