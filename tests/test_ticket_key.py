import pytest

from trialkit.tickets import parse_ticket_key


@pytest.mark.parametrize(
    "text, expected",
    [
        ("AIT-1093", ("AIT", 1093)),
        ("ait-7", ("AIT", 7)),
        (" OPS-12 ", ("OPS", 12)),
        ("Ab-1", ("AB", 1)),
        ("ABCDEFGHIJ-10", ("ABCDEFGHIJ", 10)),
    ],
)
def test_valid(text, expected):
    assert parse_ticket_key(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "AIT", "AIT-0", "AIT-012", "A1T-5", "AIT-1-2",
        "", "   ", "A-1", "ABCDEFGHIJK-1", "AIT-", "-5", "AIT--5", "AIT 5",
        "AIT-+5", "AIT-1.5", "AIT- 5", "ÄIT-5", "AIT-١", "AIT-5\nX",
    ],
)
def test_invalid_raises_value_error(text):
    with pytest.raises(ValueError):
        parse_ticket_key(text)


@pytest.mark.parametrize("value", [None, 1093, b"AIT-1", ("AIT", 1)])
def test_non_string_raises_type_error(value):
    with pytest.raises(TypeError):
        parse_ticket_key(value)
