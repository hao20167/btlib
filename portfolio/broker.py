from dataclasses import dataclass

from .account import AccountState
from btlib.core.events import FillEvent, OrderSide
from btlib.execution.orders import Order
from btlib.execution.slippage import apply_slippage_bps
from btlib.execution.fees import proportion_commission


@dataclass
class Broker:
    account: AccountState
    slippage_bps: float = 0.0
    commission_rate: float = 0.0
    
    def process_order(self, order: Order, current_price: float, timestamp) -> FillEvent:
        fill_price = apply_slippage_bps(current_price, order.side, self.slippage_bps)
        notional = order.size * fill_price
        commission = proportion_commission(notional, rate=self.commission_rate)

        self.account.update_fill(
            symbol=order.symbol,
            side=order.side, 
            size=order.size,
            price=fill_price,
            commission=commission,
        )
        if self.account.trades:
            self.account.trades[-1].timestamp = timestamp

        return FillEvent(
            timestamp=timestamp,
            symbol=order.symbol,
            side=order.side,
            size=order.size,
            price=fill_price,
            commission=commission,
        )