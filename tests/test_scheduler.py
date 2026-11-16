from datetime import datetime, timezone

from trialkit.scheduler import Reminder, due, todays_reminders


def ist(*a):
    return datetime(*a)


def test_todays_reminders_sorted():
    rs = [Reminder("b", ist(2026, 11, 17, 15, 0)), Reminder("a", ist(2026, 11, 17, 10, 0))]
    now = datetime(2026, 11, 17, 6, 0, tzinfo=timezone.utc)  # 11:30 IST
    assert [r.text for r in todays_reminders(rs, now)] == ["a", "b"]


def test_other_days_are_left_out():
    rs = [Reminder("tomorrow", ist(2026, 11, 18, 10, 0))]
    now = datetime(2026, 11, 17, 6, 0, tzinfo=timezone.utc)
    assert todays_reminders(rs, now) == []


def test_due_only_once_the_time_has_come():
    rs = [Reminder("a", ist(2026, 11, 17, 10, 0)), Reminder("b", ist(2026, 11, 17, 15, 0))]
    now = datetime(2026, 11, 17, 6, 0, tzinfo=timezone.utc)  # 11:30 IST
    assert [r.text for r in due(rs, now)] == ["a"]


def test_early_morning_ist_reminder_is_not_listed_on_the_previous_evening():
    # Regression: Mon 16 Nov 18:30 IST digest listed a Tue 02:00 IST reminder as "today"
    # because the IST->UTC instant (Mon 20:30 UTC) was bucketed by its UTC date.
    rs = [Reminder("late", ist(2026, 11, 16, 22, 0)), Reminder("tue", ist(2026, 11, 17, 2, 0))]
    now = datetime(2026, 11, 16, 13, 0, tzinfo=timezone.utc)  # Mon 18:30 IST
    assert [r.text for r in todays_reminders(rs, now)] == ["late"]


def test_early_morning_ist_reminder_is_listed_on_its_own_day():
    rs = [Reminder("tue", ist(2026, 11, 17, 2, 0))]
    now = datetime(2026, 11, 16, 20, 30, tzinfo=timezone.utc)  # Tue 02:00 IST, still Mon in UTC
    assert [r.text for r in todays_reminders(rs, now)] == ["tue"]
    assert [r.text for r in due(rs, now)] == ["tue"]
