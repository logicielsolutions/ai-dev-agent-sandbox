from datetime import date, datetime

from trialkit.sla import due_date, due_for, opened_on


def test_opened_on_midday():
    assert opened_on(datetime(2026, 11, 17, 12, 0)) == date(2026, 11, 17)


def test_due_date_midweek():
    # Tue 17 Nov 11:00 IST, 1 working day -> Wed 18 Nov
    assert due_date(datetime(2026, 11, 17, 11, 0), 1) == date(2026, 11, 18)


def test_due_for_ops():
    assert due_for("ops", datetime(2026, 11, 16, 14, 0)) == date(2026, 11, 17)


import pytest


# Regression tests for the weekend / early-morning SLA bug.

def test_ait_301_friday_ticket_skips_the_weekend():
    # Fri 20 Nov 11:00 IST, 2 working days -> Mon 23, Tue 24 (was Mon 23)
    assert due_date(datetime(2026, 11, 20, 11, 0), 2) == date(2026, 11, 24)


def test_ait_302_monday_before_0530_ist_counts_as_monday():
    # Mon 23 Nov 03:00 IST is still Sun 22 Nov in UTC; the SLA day is the IST day
    assert opened_on(datetime(2026, 11, 23, 3, 0)) == date(2026, 11, 23)
    assert due_date(datetime(2026, 11, 23, 3, 0), 2) == date(2026, 11, 25)


@pytest.mark.parametrize("hour, minute", [(0, 0), (5, 29), (5, 30), (23, 59)])
def test_opened_on_is_the_ist_calendar_day_at_any_hour(hour, minute):
    assert opened_on(datetime(2026, 11, 18, hour, minute)) == date(2026, 11, 18)


def test_opened_on_rejects_aware_datetimes():
    from datetime import timezone
    with pytest.raises(ValueError):
        opened_on(datetime(2026, 11, 18, 3, 0, tzinfo=timezone.utc))


def test_due_for_code_ticket_on_thursday_crosses_weekend():
    # Thu 19 Nov, 3 working days -> Fri 20, Mon 23, Tue 24
    assert due_for("code", datetime(2026, 11, 19, 10, 0)) == date(2026, 11, 24)


def test_weekend_ticket_counts_from_monday():
    # Sat 21 Nov, 2 working days -> Mon 23, Tue 24
    assert due_date(datetime(2026, 11, 21, 15, 0), 2) == date(2026, 11, 24)
