def fixed_commission(amount: float, commission: float = 0.0) -> float:
    return commission

def proportion_commission(amount: float, rate: float = 0.0005, min_commission: float = 0.0) -> float:
    fee = amount * rate
    return max(fee, min_commission)