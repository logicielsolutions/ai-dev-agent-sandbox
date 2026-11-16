from decimal import Decimal
from fractions import Fraction

import pytest

from trialkit.durations import format_duration


@pytest.mark.parametrize(
    "seconds, expected",
    [
        (5400, "1h30m"),
        (45, "45s"),
        (0, "0s"),
        (3605, "1h5s"),
        (3600, "1h"),
        (90061, "25h1m1s"),
        (1, "1s"),
        (59, "59s"),
        (60, "1m"),
        (61, "1m1s"),
        (3599, "59m59s"),
        (3660, "1h1m"),
        (86400, "24h"),
    ],
)
def test_format_duration(seconds, expected):
    assert format_duration(seconds) == expected


@pytest.mark.parametrize("seconds", [-1, -3600])
def test_negative_raises_value_error(seconds):
    with pytest.raises(ValueError):
        format_duration(seconds)


@pytest.mark.parametrize(
    "seconds",
    [True, False, 1.0, 5400.0, 0.5, "5400", None, Decimal(5), Fraction(5), [60]],
)
def test_non_int_raises_type_error(seconds):
    with pytest.raises(TypeError):
        format_duration(seconds)


def test_negative_float_is_a_type_error():
    # The type check comes first: -1.0 is not an int at all.
    with pytest.raises(TypeError):
        format_duration(-1.0)
