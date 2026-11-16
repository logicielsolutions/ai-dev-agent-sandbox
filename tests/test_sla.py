from datetime import date, datetime

from trialkit.sla import due_date, due_for, opened_on


def test_opened_on_midday():
    assert opened_on(datetime(2026, 11, 17, 12, 0)) == date(2026, 11, 17)


def test_due_date_midweek():
    # Tue 17 Nov 11:00 IST, 1 working day -> Wed 18 Nov
    assert due_date(datetime(2026, 11, 17, 11, 0), 1) == date(2026, 11, 18)


def test_due_for_ops():
    assert due_for("ops", datetime(2026, 11, 16, 14, 0)) == date(2026, 11, 17)
