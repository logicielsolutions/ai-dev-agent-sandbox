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


def test_add_working_days_from_friday_skips_the_weekend():
    # Fri 20 Nov + 2 -> Mon 23, Tue 24 Nov
    assert add_working_days(date(2026, 11, 20), 2) == date(2026, 11, 24)


def test_add_working_days_across_two_weekends():
    # Fri 20 Nov + 6 -> Mon 30 Nov
    assert add_working_days(date(2026, 11, 20), 6) == date(2026, 11, 30)


def test_add_working_days_from_a_weekend_day():
    # Sat 21 Nov + 1 -> Mon 23 Nov
    assert add_working_days(date(2026, 11, 21), 1) == date(2026, 11, 23)


def test_add_zero_working_days():
    assert add_working_days(date(2026, 11, 18), 0) == date(2026, 11, 18)
