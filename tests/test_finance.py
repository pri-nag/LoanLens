import pytest

from loan_engine.finance import apr_pct, pmt, pv


def test_emi_known_value():
    # Rs 10 lakh, 11% p.a., 60 months -> Rs 21,742 (standard EMI tables)
    assert pmt(1_000_000, 11, 60) == pytest.approx(21742, abs=1)


def test_pv_inverts_pmt():
    assert pv(pmt(750_000, 13.5, 48), 13.5, 48) == pytest.approx(750_000)


def test_zero_rate():
    assert pmt(120_000, 0, 12) == 10_000


def test_apr_equals_rate_without_fee_and_rises_with_fee():
    assert apr_pct(500_000, 12, 36, 0) == pytest.approx(12, abs=0.01)
    assert apr_pct(500_000, 12, 36, 10_000) > 13


@pytest.mark.parametrize("amount, rate, months, lender_emi", [
    (1_500_000, 9.99, 60, 31_863),
    (1_088_034, 10.7, 48, 27_963),
    (1_088_034, 10.7, 36, 35_466),
    (4_600_000, 10.7, 72, 86_852),
])
def test_emi_matches_hdfc_calculator(amount, rate, months, lender_emi):
    # HDFC Bank personal loan EMI calculator, read 2026-10-12
    assert round(pmt(amount, rate, months)) == lender_emi
