import pytest

from trialkit.durations import parse_duration


@pytest.mark.parametrize(
    "text, expected",
    [
        ("1h30m", 5400),
        ("45m", 2700),
        ("2h", 7200),
        ("90s", 90),
        ("1h5s", 3605),
        ("1h2m3s", 3723),
        (" 10M ", 600),
        ("1H2M3S", 3723),
        ("0s", 0),
    ],
)
def test_parse_duration_valid(text, expected):
    assert parse_duration(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "abc",
        "5",
        "1x",
        "-1h",
        "1m1h",
        "1h1h",
        "1.5h",
        "1 h",
        "1h 30m",
        "+1h",
        "h",
        "1h30",
        "١h",  # non-ASCII digit
    ],
)
def test_parse_duration_invalid_raises_value_error(text):
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("value", [None, 5400, 1.5, b"1h", ["1h"]])
def test_parse_duration_non_string_raises_type_error(value):
    with pytest.raises(TypeError):
        parse_duration(value)
