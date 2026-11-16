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
        (59, "59s"),
    ],
)
def test_format_duration(seconds, expected):
    assert format_duration(seconds) == expected


def test_negative_raises_value_error():
    with pytest.raises(ValueError):
        format_duration(-1)


@pytest.mark.parametrize("bad", [True, False, 1.0, 5400.0, "60", None])
def test_non_int_raises_type_error(bad):
    with pytest.raises(TypeError):
        format_duration(bad)
