import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict

from .strategy import Strategy
from .events import MarketEvent, SignalEvent
from btlib.portfolio.account import AccountState
from btlib.portfolio.broker import Broker
from btlib.execution.orders import OrderSide, Order
from btlib.portfolio.account import Trade


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    account_history: pd.DataFrame
    trades: List[Trade]
    account: AccountState


class Backtest:
    def __init__(self, 
        data: pd.DataFrame, 
        symbol: str, 
        strategy_class: type[Strategy], 
        initial_cash: float, 
        slippage_bps: float = 0.0, 
        commission_rate: float = 0.0, 
        **strategy_kwargs
    ):
        self.data = data
        self.symbol = symbol
        self.strategy_class = strategy_class(data, symbol, **strategy_kwargs)
        self.account = AccountState(cash=initial_cash)
        self.broker = Broker(self.account, slippage_bps=slippage_bps, commission_rate=commission_rate)

        self._equity_records = []
        self._account_snapshots = []
    
    def run(self) -> BacktestResult:
        self.strategy_class.on_start()
        index = self.data.index

        for i, ts in enumerate(index):
            self.strategy_class.i = i
            bar = self.data.iloc[i]

            mkt_event = MarketEvent(timestamp=ts, data=bar)
            signals: list[SignalEvent] = self.strategy_class.on_bar()
            orders: list[Order] = []
            for sig in signals:
                orders.append(
                    Order(timestamp=sig.timestamp,
                        symbol=sig.symbol,
                        side=sig.symbol,
                        size=sig.size
                    )
                )
            for order in orders:
                current_price = bar["Close"]
                self.broker.process_order(order, current_price, ts)
            
            equity = self.account.total_value({self.symbol: bar["Close"]})
            self._equity_records.append((ts, equity))

            self._account_snapshots.append(
                {
                    "datetime": ts, 
                    "cash": self.account.cash, 
                    "equity": equity
                }
            )
        
        self.strategy_class.on_end()

        equity_series = pd.Series(
            [v for _, v in self._equity_records],
            index=[ts for ts, _ in self._equity_records],
            name="equity"
        )
        account_df = pd.DataFrame(self._account_snapshots).set_index("datetime")

        return BacktestResult(
            equity_curve=equity_series,
            account_history=account_df,
            trades=self.account.trades,
            account=self.account
        )

            