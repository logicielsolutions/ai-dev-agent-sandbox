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
        ("2m3s", 123),
        ("0s", 0),
        ("0h0m0s", 0),
        ("100h", 360000),
    ],
)
def test_valid_durations(text, expected):
    assert parse_duration(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (" 10M ", 600),
        ("1H30M", 5400),
        ("1h2M3S", 3723),
        ("\t45m\n", 2700),
    ],
)
def test_case_and_surrounding_spaces(text, expected):
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
        "+1h",
        "1m1h",
        "1s1m",
        "1h1h",
        "1m1m",
        "1.5h",
        "h",
        "1h30",
        "1 h",
        "1h 30m",
        "١h",  # Arabic-Indic digit one
    ],
)
def test_invalid_strings_raise_value_error(text):
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("value", [None, 90, 1.5, True, b"1h", ["1h"]])
def test_non_string_raises_type_error(value):
    with pytest.raises(TypeError):
        parse_duration(value)
