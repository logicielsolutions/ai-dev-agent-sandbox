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
        # Fri 20 Nov + 1 -> Mon 23; + 2 -> Tue 24; + 5 -> Fri 27
        (date(2026, 11, 20), 1, date(2026, 11, 23)),
        (date(2026, 11, 20), 2, date(2026, 11, 24)),
        (date(2026, 11, 20), 5, date(2026, 11, 27)),
        # Wed 18 Nov + 3 -> Mon 23 (Thu, Fri, Mon)
        (date(2026, 11, 18), 3, date(2026, 11, 23)),
        # Mon 16 Nov + 10 -> Mon 30 Nov (two full weeks)
        (date(2026, 11, 16), 10, date(2026, 11, 30)),
        # Started on a weekend: Sat 21 / Sun 22 Nov + 1 -> Mon 23
        (date(2026, 11, 21), 1, date(2026, 11, 23)),
        (date(2026, 11, 22), 2, date(2026, 11, 24)),
        # 0 working days is the start day itself
        (date(2026, 11, 18), 0, date(2026, 11, 18)),
    ],
)
def test_add_working_days_counts_each_weekend_day_out(start, n, expected):
    assert add_working_days(start, n) == expected
