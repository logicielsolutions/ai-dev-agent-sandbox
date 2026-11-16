import pytest

from trialkit.durations import parse_duration


@pytest.mark.parametrize(
    "text, expected",
    [("1h30m", 5400), ("45m", 2700), ("90s", 90), ("1h5s", 3605), (" 1H 30M ", 5400), ("0s", 0)],
)
def test_valid(text, expected):
    assert parse_duration(text) == expected


@pytest.mark.parametrize("text", ["", "5", "1x", "-1h", "1m1h", "1h1h", "1.5h", "   ", "h"])
def test_invalid_raises_value_error(text):
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("value", [None, 5, 1.5, b"1h"])
def test_non_string_raises_type_error(value):
    with pytest.raises(TypeError):
        parse_duration(value)
