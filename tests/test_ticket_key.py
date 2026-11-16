import pytest

from trialkit.tickets import parse_ticket_key


@pytest.mark.parametrize(
    "text, expected",
    [
        ("AIT-1093", ("AIT", 1093)),
        ("ait-7", ("AIT", 7)),
        (" OPS-12 ", ("OPS", 12)),
        ("Ops-12", ("OPS", 12)),
        ("AB-1", ("AB", 1)),                    # shortest project, smallest number
        ("ABCDEFGHIJ-9", ("ABCDEFGHIJ", 9)),    # longest project
        ("AIT-10", ("AIT", 10)),                # zero allowed after the first digit
        ("AIT-100200300", ("AIT", 100200300)),
        ("\tAIT-5\n", ("AIT", 5)),
    ],
)
def test_valid_keys(text, expected):
    assert parse_ticket_key(text) == expected


def test_returns_a_real_int():
    project, number = parse_ticket_key("AIT-42")
    assert type(project) is str and type(number) is int


@pytest.mark.parametrize(
    "text",
    [
        "AIT",            # no number
        "AIT-0",          # number must be 1 or more
        "AIT-012",        # leading zero
        "A1T-5",          # digit in project
        "AIT-1-2",        # two dashes
        "",
        "   ",
        "-5",             # no project
        "A-5",            # project too short
        "ABCDEFGHIJK-5",  # project too long (11)
        "AIT-",           # dash but no number
        "AIT--5",
        "AIT_5",
        "AIT 5",
        "AIT - 5",        # spaces inside the key
        "AIT-+5",
        "AIT--0",
        "AIT-5a",
        "AIT-1.5",
        "ÄIT-5",          # letters are ASCII only
        "AIT-١٢",         # non-ASCII digits
    ],
)
def test_invalid_keys_raise_value_error(text):
    with pytest.raises(ValueError):
        parse_ticket_key(text)


@pytest.mark.parametrize("value", [None, 1093, 7.0, b"AIT-7", ["AIT-7"], ("AIT", 7)])
def test_non_string_raises_type_error(value):
    with pytest.raises(TypeError):
        parse_ticket_key(value)
