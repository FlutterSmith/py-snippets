from datetime import date, timedelta
from itertools import pairwise

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pysnippets.dates import daterange, is_weekday, is_weekend, months_diff

dates = st.dates(date(1900, 1, 1), date(2200, 12, 31))


@given(dates, st.integers(0, 400), st.integers(1, 10))
def test_daterange_length_and_step(start: date, days: int, step: int) -> None:
    result = list(daterange(start, start + timedelta(days), step))
    assert len(result) == len(range(0, days, step))
    assert all((b - a).days == step for a, b in pairwise(result))


def test_daterange_rejects_non_positive_step() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        list(daterange(date(2024, 1, 1), date(2024, 2, 1), 0))


@given(dates, dates)
def test_months_diff_is_antisymmetric(a: date, b: date) -> None:
    assert months_diff(a, b) == -months_diff(b, a)


@given(dates, st.integers(0, 600))
def test_months_diff_counts_whole_months(start: date, months: int) -> None:
    if start.day <= 28:
        year, month = divmod(start.month - 1 + months, 12)
        end = start.replace(year=start.year + year, month=month + 1)
        assert months_diff(start, end) == months
        assert months_diff(start, end - timedelta(days=1)) == max(months - 1, 0)


@given(dates)
def test_weekday_and_weekend_are_complements(day: date) -> None:
    assert is_weekday(day) != is_weekend(day)
