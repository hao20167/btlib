from abc import ABC, abstractmethod
import pandas as pd
from .events import SignalEvent, OrderSide


class Strategy(ABC):
    def __init__(self, data: pd.DataFrame, symbol: str, **kwargs):
        self.data = data
        self.symbol = symbol
        self.i = 0
        self.params = kwargs
    
    def on_start(self):
        pass

    @abstractmethod
    def on_bar(self) -> list[SignalEvent]:
        raise NotImplementedError

    def on_end(self):
        pass

    @property
    def current_bar(self) -> pd.Series:
        return self.data.iloc[self.i]

    @property
    def current_time(self):
        return self.data.index[self.i]
    
    def buy(self, size: float = 1.0) -> SignalEvent:
        return SignalEvent(self.current_time, self.symbol, OrderSide.BUY, size)
    
    def sell(self, size: float = 1.0) -> SignalEvent:
        return SignalEvent(self.current_time, self.symbol, OrderSide.SELL, size)