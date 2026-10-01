import pytest
from hypothesis import given
from hypothesis import strategies as st

from pysnippets.numbers import (
    clamp_number,
    digitize,
    is_prime,
    num_to_range,
    to_roman_numeral,
)

ROMAN = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}


def from_roman(numeral: str) -> int:
    values = [ROMAN[c] for c in numeral]
    return sum(
        -v if v < nxt else v for v, nxt in zip(values, [*values[1:], 0], strict=True)
    )


@given(st.integers(1, 3999))
def test_roman_numerals_round_trip(n: int) -> None:
    numeral = to_roman_numeral(n)
    assert from_roman(numeral) == n
    assert "IIII" not in numeral
    assert "XXXX" not in numeral


@pytest.mark.parametrize("n", [0, -1, 4000])
def test_roman_numerals_reject_out_of_range(n: int) -> None:
    with pytest.raises(ValueError, match="1 to 3999"):
        to_roman_numeral(n)


@given(st.integers(), st.integers(), st.integers())
def test_clamp_number_stays_in_bounds(value: int, a: int, b: int) -> None:
    clamped = clamp_number(value, a, b)
    assert min(a, b) <= clamped <= max(a, b)
    if min(a, b) <= value <= max(a, b):
        assert clamped == value


@given(st.floats(-1e6, 1e6), st.floats(-1e6, 1e6), st.floats(-1e6, 1e6))
def test_num_to_range_maps_the_endpoints(lo: float, hi: float, out: float) -> None:
    if abs(hi - lo) > 1e-3:
        assert num_to_range(lo, lo, hi, out, out + 10) == pytest.approx(out)
        assert num_to_range(hi, lo, hi, out, out + 10) == pytest.approx(out + 10)


def naive_is_prime(n: int) -> bool:
    return n > 1 and all(n % d for d in range(2, n))


@given(st.integers(-10, 3000))
def test_is_prime_matches_trial_division(n: int) -> None:
    assert is_prime(n) == naive_is_prime(n)


def test_is_prime_on_a_large_square_of_a_prime() -> None:
    assert not is_prime(1_000_003**2)


@given(st.integers())
def test_digitize_round_trips(n: int) -> None:
    digits = digitize(n)
    assert int("".join(map(str, digits))) == abs(n)
    assert all(0 <= d <= 9 for d in digits)
