def fixed_fraction_position_size(equity: float, fraction: float, price: float) -> float:
    risk_amount = equity * fraction
    if price <= 0:
        return 0.0
    size = risk_amount / price
    return max(size, 0.0)