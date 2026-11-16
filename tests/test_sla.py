from datetime import date, datetime

from trialkit.sla import due_date, due_for, opened_on


def test_opened_on_midday():
    assert opened_on(datetime(2026, 11, 17, 12, 0)) == date(2026, 11, 17)


def test_due_date_midweek():
    # Tue 17 Nov 11:00 IST, 1 working day -> Wed 18 Nov
    assert due_date(datetime(2026, 11, 17, 11, 0), 1) == date(2026, 11, 18)


def test_due_for_ops():
    assert due_for("ops", datetime(2026, 11, 16, 14, 0)) == date(2026, 11, 17)


# Regression tests for AIT-301 / AIT-302 (SLA due dates wrong around weekends
# and for tickets opened in the early hours IST).


def test_ait_301_friday_ticket_counts_working_days_over_the_weekend():
    # Fri 20 Nov 11:00 IST, 2 working days -> Mon 23 (1), Tue 24 (2)
    assert due_date(datetime(2026, 11, 20, 11, 0), 2) == date(2026, 11, 24)


def test_ait_302_early_morning_ist_ticket_opens_on_the_ist_day():
    # Mon 23 Nov 03:00 IST is still Sun 22 Nov in UTC; it was opened on Monday
    assert opened_on(datetime(2026, 11, 23, 3, 0)) == date(2026, 11, 23)
    # 2 working days -> Tue 24 (1), Wed 25 (2)
    assert due_date(datetime(2026, 11, 23, 3, 0), 2) == date(2026, 11, 25)


def test_opened_on_just_after_midnight_ist():
    # 00:10 IST Wed 18 Nov is 18:40 UTC Tue 17 Nov
    assert opened_on(datetime(2026, 11, 18, 0, 10)) == date(2026, 11, 18)


def test_opened_on_late_evening_ist():
    assert opened_on(datetime(2026, 11, 18, 23, 50)) == date(2026, 11, 18)


def test_code_ticket_opened_thursday():
    # Thu 19 Nov, 3 working days -> Fri 20, Mon 23, Tue 24
    assert due_for("code", datetime(2026, 11, 19, 10, 0)) == date(2026, 11, 24)


def test_ticket_opened_on_saturday():
    # Sat 21 Nov, 1 working day -> Mon 23
    assert due_date(datetime(2026, 11, 21, 10, 0), 1) == date(2026, 11, 23)
