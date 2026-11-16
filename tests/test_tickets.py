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


@pytest.mark.parametrize(
    "start, n, expected",
    [
        (date(2026, 11, 20), 1, date(2026, 11, 23)),  # Fri + 1 -> Mon
        (date(2026, 11, 20), 2, date(2026, 11, 24)),  # Fri + 2 -> Tue (was Mon)
        (date(2026, 11, 18), 5, date(2026, 11, 25)),  # Wed + 5 -> next Wed (was Mon)
        (date(2026, 11, 16), 10, date(2026, 11, 30)),  # two full weeks
        (date(2026, 11, 21), 1, date(2026, 11, 23)),  # Sat + 1 -> Mon
        (date(2026, 11, 22), 2, date(2026, 11, 24)),  # Sun + 2 -> Tue
        (date(2026, 11, 18), 0, date(2026, 11, 18)),  # zero days -> same day
    ],
)
def test_add_working_days_skips_weekends_inside_the_span(start, n, expected):
    assert add_working_days(start, n) == expected


@pytest.mark.parametrize("start", [date(2026, 11, d) for d in range(16, 30)])
@pytest.mark.parametrize("n", range(0, 12))
def test_add_working_days_agrees_with_working_days_between(start, n):
    end = add_working_days(start, n)
    assert end.weekday() < 5 or n == 0
    assert working_days_between(start, end) == n


def test_add_working_days_rejects_negative():
    with pytest.raises(ValueError):
        add_working_days(date(2026, 11, 18), -1)
