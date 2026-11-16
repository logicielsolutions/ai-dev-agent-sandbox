from datetime import date, datetime, timezone

import pytest

from trialkit.sla import due_date, due_for, opened_on


def test_opened_on_midday():
    assert opened_on(datetime(2026, 11, 17, 12, 0)) == date(2026, 11, 17)


def test_due_date_midweek():
    # Tue 17 Nov 11:00 IST, 1 working day -> Wed 18 Nov
    assert due_date(datetime(2026, 11, 17, 11, 0), 1) == date(2026, 11, 18)


def test_due_for_ops():
    assert due_for("ops", datetime(2026, 11, 16, 14, 0)) == date(2026, 11, 17)


# Regression: SLA due dates for tickets opened on a Friday or in the early IST hours.


def test_ait_301_friday_ticket_skips_the_whole_weekend():
    # Fri 20 Nov 11:00 IST, 2 working days -> Mon 23, Tue 24 (was Mon 23)
    assert due_date(datetime(2026, 11, 20, 11, 0), 2) == date(2026, 11, 24)


def test_ait_302_early_morning_ticket_counts_from_its_ist_day():
    # Mon 23 Nov 03:00 IST is Sun 22 Nov 21:30 UTC, but it was opened on Monday.
    assert opened_on(datetime(2026, 11, 23, 3, 0)) == date(2026, 11, 23)
    # 2 working days -> Tue 24, Wed 25 (was Tue 24)
    assert due_date(datetime(2026, 11, 23, 3, 0), 2) == date(2026, 11, 25)


@pytest.mark.parametrize("hour, minute", [(0, 0), (5, 29), (5, 30), (23, 59)])
def test_opened_on_is_the_ist_day_at_any_hour(hour, minute):
    assert opened_on(datetime(2026, 11, 18, hour, minute)) == date(2026, 11, 18)


def test_due_for_research_opened_friday():
    # Fri 20 Nov 18:00 IST, research = 2 working days -> Tue 24 Nov
    assert due_for("research", datetime(2026, 11, 20, 18, 0)) == date(2026, 11, 24)


def test_due_for_code_opened_thursday_early_morning():
    # Thu 19 Nov 01:00 IST, code = 3 working days -> Fri 20, Mon 23, Tue 24
    assert due_for("code", datetime(2026, 11, 19, 1, 0)) == date(2026, 11, 24)


def test_opened_on_rejects_aware_datetimes():
    with pytest.raises(ValueError):
        opened_on(datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc))
