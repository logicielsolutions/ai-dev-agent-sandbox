from datetime import date, timedelta

import pytest

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


def test_add_working_days_from_friday_skips_the_weekend():
    # Fri 20 Nov + 2 -> Mon 23 (1), Tue 24 (2)
    assert add_working_days(date(2026, 11, 20), 2) == date(2026, 11, 24)


def test_add_working_days_one_from_friday():
    assert add_working_days(date(2026, 11, 20), 1) == date(2026, 11, 23)


def test_add_working_days_across_two_weekends():
    # Wed 18 Nov + 7 -> Fri 27 Nov
    assert add_working_days(date(2026, 11, 18), 7) == date(2026, 11, 27)


def test_add_working_days_from_sunday():
    # Sun 22 Nov + 2 -> Mon 23 (1), Tue 24 (2)
    assert add_working_days(date(2026, 11, 22), 2) == date(2026, 11, 24)


def test_add_working_days_zero_is_start():
    assert add_working_days(date(2026, 11, 18), 0) == date(2026, 11, 18)


def test_add_working_days_matches_working_days_between():
    start = date(2026, 11, 16)
    for offset in range(7):
        s = start + timedelta(days=offset)
        for n in range(1, 12):
            assert working_days_between(s, add_working_days(s, n)) == n


def test_add_working_days_rejects_negative():
    with pytest.raises(ValueError):
        add_working_days(date(2026, 11, 18), -1)
