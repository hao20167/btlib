import pandas as pd

def split_train_test(df: pd.DataFrame, train_ratio: float = 0.7):
    n = len(df)
    split = int(n * train_ratio)
    train = df.iloc[:split]
    test = df.iloc[split:]
    return train, test