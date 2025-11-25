from dataclasses import dataclass
from enum import Enum
import pandas as pd
from typing import Any
from btlib.execution.orders import OrderSide


@dataclass
class MarketEvent:
    timestamp: any
    data: Any


@dataclass
class SignalEvent:
    timestamp: any
    symbol: str
    side: OrderSide
    size: float


@dataclass
class FillEvent:
    timestamp: any
    symbol: str
    side: OrderSide
    size: float
    price: float
    commission: float = 0.0