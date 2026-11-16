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
        (60, "1m"),
        (61, "1m1s"),
        (3660, "1h1m"),
        (1, "1s"),
        (59, "59s"),
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
    "value",
    [True, False, 1.0, 5400.0, 0.0, -1.5, "45", None, Decimal("45"), Fraction(45, 1), [45]],
)
def test_non_int_raises_type_error(value):
    with pytest.raises(TypeError):
        format_duration(value)


def test_int_subclass_other_than_bool_is_accepted():
    class Seconds(int):
        pass

    assert format_duration(Seconds(5400)) == "1h30m"
