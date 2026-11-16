from datetime import date

from trialkit.tickets import working_days_between


def test_same_day_is_zero():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 16)) == 0


def test_skips_the_weekend():
    # Fri 13 Nov -> Tue 17 Nov: Mon and Tue count
    assert working_days_between(date(2026, 11, 13), date(2026, 11, 17)) == 2


def test_one_week():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 23)) == 5


from trialkit.tickets import add_working_days


def test_add_working_days_midweek():
    # Mon 16 Nov + 2 -> Wed 18 Nov
    assert add_working_days(date(2026, 11, 16), 2) == date(2026, 11, 18)


def test_add_working_days_into_next_week():
    # Thu 19 Nov + 2 -> Mon 23 Nov
    assert add_working_days(date(2026, 11, 19), 2) == date(2026, 11, 23)


import pytest

from trialkit.tickets import parse_ticket_key


@pytest.mark.parametrize(
    "text, expected",
    [
        ("AIT-1093", ("AIT", 1093)),
        ("ait-7", ("AIT", 7)),
        (" OPS-12 ", ("OPS", 12)),
        ("AIT-1\n", ("AIT", 1)),
        ("\tAiT-10\t", ("AIT", 10)),
        ("AB-1", ("AB", 1)),  # 2-letter boundary
        ("ABCDEFGHIJ-5", ("ABCDEFGHIJ", 5)),  # 10-letter boundary
    ],
)
def test_parse_ticket_key_valid(text, expected):
    assert parse_ticket_key(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "AIT",
        "AIT-",
        "AIT-0",
        "AIT-012",
        "A1T-5",
        "AIT-1-2",
        "A-1",
        "ABCDEFGHIJK-5",  # 11 letters
        "AIT 5",
        "AIT - 5",
        "AIT--5",
        "-5",
        "+5",
        "AIT-+5",
        "AIT--1",
        "AIT-1.0",
        "AIT-\u0661\u0662",  # Arabic-Indic digits
        "AIT-\uff11",  # full-width digit
        "\u00c9TE-5",  # non-ASCII letter
        "AIT\u20135",  # en dash
        "AIT-5x",
    ],
)
def test_parse_ticket_key_invalid(text):
    with pytest.raises(ValueError):
        parse_ticket_key(text)


@pytest.mark.parametrize("value", [None, 5, b"AIT-1"])
def test_parse_ticket_key_type_error(value):
    with pytest.raises(TypeError):
        parse_ticket_key(value)
