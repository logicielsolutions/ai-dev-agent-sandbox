from datetime import date, datetime

from trialkit.sla import due_date, due_for, opened_on


def test_opened_on_midday():
    assert opened_on(datetime(2026, 11, 17, 12, 0)) == date(2026, 11, 17)


def test_due_date_midweek():
    # Tue 17 Nov 11:00 IST, 1 working day -> Wed 18 Nov
    assert due_date(datetime(2026, 11, 17, 11, 0), 1) == date(2026, 11, 18)


def test_due_for_ops():
    assert due_for("ops", datetime(2026, 11, 16, 14, 0)) == date(2026, 11, 17)


def test_ait_301_friday_ticket_skips_the_weekend():
    # Fri 20 Nov 11:00 IST, 2 working days -> Mon 23, Tue 24 Nov (was Mon 23 Nov)
    assert due_date(datetime(2026, 11, 20, 11, 0), 2) == date(2026, 11, 24)


def test_ait_302_early_morning_ticket_counts_from_the_ist_day():
    # Mon 23 Nov 03:00 IST is Sun 22 Nov in UTC; the SLA counts from Mon 23 Nov -> Wed 25 Nov (was Tue 24 Nov)
    assert opened_on(datetime(2026, 11, 23, 3, 0)) == date(2026, 11, 23)
    assert due_date(datetime(2026, 11, 23, 3, 0), 2) == date(2026, 11, 25)


def test_opened_just_after_midnight_ist():
    assert opened_on(datetime(2026, 11, 18, 0, 5)) == date(2026, 11, 18)


def test_opened_on_rejects_aware_input():
    import pytest
    from datetime import timezone

    with pytest.raises(ValueError):
        opened_on(datetime(2026, 11, 18, 9, 0, tzinfo=timezone.utc))
