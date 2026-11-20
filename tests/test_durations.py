import pytest

from trialkit.durations import parse_duration


@pytest.mark.parametrize(
    "text, seconds",
    [
        ("1h30m", 5400),
        ("45m", 2700),
        ("2h", 7200),
        ("90s", 90),
        ("1h5s", 3605),
        ("1h2m3s", 3723),
        ("0s", 0),
    ],
)
def test_valid_durations(text, seconds):
    assert parse_duration(text) == seconds


@pytest.mark.parametrize(
    "text, seconds",
    [
        (" 10M ", 600),
        ("  1H2M3S\t", 3723),
        ("1h2M3s", 3723),
    ],
)
def test_spaces_and_case_ignored(text, seconds):
    assert parse_duration(text) == seconds


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
        "1s1m",
        "1h1h",
        "1.5h",
        "h",
        "1 h",
        "1h 30m",
    ],
)
def test_invalid_strings_raise_value_error(text):
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("value", [None, 90, 1.5, b"1h", ["1h"]])
def test_non_string_raises_type_error(value):
    with pytest.raises(TypeError):
        parse_duration(value)
