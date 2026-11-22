import pytest

from trialkit.durations import format_duration


def test_examples():
    cases = {
        5400: "1h30m",
        45: "45s",
        0: "0s",
        3605: "1h5s",
        3600: "1h",
        90061: "25h1m1s",
    }
    for seconds, expected in cases.items():
        assert format_duration(seconds) == expected, seconds


def test_minutes_and_seconds():
    assert format_duration(60) == "1m"
    assert format_duration(61) == "1m1s"
    assert format_duration(3599) == "59m59s"


def test_negative_raises_value_error():
    with pytest.raises(ValueError):
        format_duration(-1)


def test_float_raises_type_error():
    with pytest.raises(TypeError):
        format_duration(5400.0)


def test_bool_raises_type_error():
    with pytest.raises(TypeError):
        format_duration(True)
    with pytest.raises(TypeError):
        format_duration(False)


def test_other_types_raise_type_error():
    for bad in ("60", None, [60]):
        with pytest.raises(TypeError):
            format_duration(bad)
