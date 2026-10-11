"""Loan maths: EMI, present value, and APR including processing fee."""


def pmt(principal: float, annual_rate_pct: float, months: int) -> float:
    """Monthly EMI on a reducing-balance loan."""
    r = annual_rate_pct / 1200
    if r == 0:
        return principal / months
    f = (1 + r) ** months
    return principal * r * f / (f - 1)


def pv(emi: float, annual_rate_pct: float, months: int) -> float:
    """Largest principal that a given EMI can repay."""
    r = annual_rate_pct / 1200
    if r == 0:
        return emi * months
    f = (1 + r) ** months
    return emi * (f - 1) / (r * f)


def apr_pct(principal: float, annual_rate_pct: float, months: int, upfront_fee: float) -> float:
    """Annual rate at which (principal - fee) equals the EMI stream (RBI KFS style APR)."""
    emi = pmt(principal, annual_rate_pct, months)
    net = principal - upfront_fee
    lo, hi = 0.0, 200.0
    for _ in range(100):  # pv falls as the rate rises, so bisection converges
        mid = (lo + hi) / 2
        if pv(emi, mid, months) > net:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 2)
