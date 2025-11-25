from .orders import OrderSide

# basis points, 1 bps = 0.01%
def apply_slippage_bps(price: float, side: OrderSide, slippage_bps):
    if slippage_bps == 0:
        return price
    factor = slippage_bps / 10000.0
    if side == OrderSide.BUY:
        return price * (1 + factor)
    else:
        return price * (1 - factor)