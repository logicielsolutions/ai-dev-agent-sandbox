from datetime import date

from trialkit.digest import overdue, summary, week_days
from trialkit.tickets import Ticket

FRI = date(2026, 11, 20)


def test_week_days_are_working_days_oldest_first():
    days = week_days(FRI)
    assert days == sorted(days)
    assert all(d.weekday() < 5 for d in days)


def test_overdue_skips_done():
    ts = [Ticket("AIT-1", "a", "todo", due=date(2026, 11, 18)), Ticket("AIT-2", "a", "done", due=date(2026, 11, 1))]
    assert overdue(ts, FRI) == ["AIT-1"]


def test_summary_mentions_overdue():
    ts = [Ticket("AIT-1", "a", "in_progress", due=date(2026, 11, 18))]
    text = summary(ts, FRI)
    assert "in progress: 1" in text
    assert "Overdue: AIT-1" in text
