import pytest

from trialkit.durations import parse_duration


@pytest.mark.parametrize(
    "text, seconds",
    [
        ("1h30m", 5400),
        ("45m", 2700),
        ("90s", 90),
        ("1h5s", 3605),
        ("1h30m15s", 5415),
        ("0s", 0),
    ],
)
def test_valid_durations(text, seconds):
    assert parse_duration(text) == seconds


@pytest.mark.parametrize("text", ["1h 30m", " 1 h 30 m ", "1h30m "])
def test_spaces_are_ignored(text):
    assert parse_duration(text) == 5400


@pytest.mark.parametrize("text", ["1H30M", "1h30M", "1H 30m"])
def test_any_case(text):
    assert parse_duration(text) == 5400


@pytest.mark.parametrize(
    "text",
    ["", " ", "   ", "\t", "5", "1x", "-1h", "1m1h", "1h1h", "1.5h", "h", "1h\n", "١h"],
)
def test_invalid_durations_raise_value_error(text):
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("value", [None, 5, b"1h"])
def test_non_strings_raise_type_error(value):
    with pytest.raises(TypeError):
        parse_duration(value)
