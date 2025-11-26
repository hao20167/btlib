from dataclasses import dataclass, field
from typing import Dict, List
import pandas as pd
from btlib.execution.orders import OrderSide


@dataclass
class Position:
    symbol: str
    size: float = 0.0
    avg_price: float = 0.0

@dataclass
class Trade:
    timestamp: any
    symbol: str
    side: OrderSide
    size: float
    price: OrderSide
    commission: float

@dataclass
class AccountState:
    cash: float
    positions: Dict[str, Position] = field(default_factory=dict)
    trades: List[Trade] = field(default_factory=list)

    def update_fill(self, symbol: str, side: str, size: float, price: float, commission: float = 0.0):
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol=symbol)
        
        pos = self.positions[symbol]

        if side == "BUY":
            cost = size * price + commission
            self.cash -= cost
            new_size = pos.size + size
            if new_size != 0:
                pos.avg_price = (pos.avg_price * pos.size + price * size) / new_size
            pos.size = new_size
        else:
            revenue = size * price - commission
            self.cash += revenue
            pos.size -= size
            if pos.size == 0:
                pos.avg_price = 0.0
        
        self.trades.append(
            Trade(
                timestamp=None,
                symbol=symbol,
                side=side,
                size=size,
                price=price,
                commission=commission
            )
        )
    
    def total_value(self, prices: Dict[str, float]) -> float:
        value = self.cash
        for sym, pos in self.positions.items():
            last_price = prices.get(sym, pos.avg_price) # default=pos.avg_price
            value += pos.size * last_price
        return value