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


def test_evening_digest_excludes_early_next_morning():
    # Reported case: Mon 16 Nov 18:30 IST digest (13:00 UTC).
    rs = [Reminder("tue 2am", ist(2026, 11, 17, 2, 0)), Reminder("mon 11pm", ist(2026, 11, 16, 23, 0))]
    now = datetime(2026, 11, 16, 13, 0, tzinfo=timezone.utc)
    assert [r.text for r in todays_reminders(rs, now)] == ["mon 11pm"]


def test_just_after_ist_midnight_today_is_the_ist_day():
    # 19:00 UTC Mon is 00:30 IST Tue.
    rs = [Reminder("tue 2am", ist(2026, 11, 17, 2, 0)), Reminder("mon 11pm", ist(2026, 11, 16, 23, 0))]
    now = datetime(2026, 11, 16, 19, 0, tzinfo=timezone.utc)
    assert [r.text for r in todays_reminders(rs, now)] == ["tue 2am"]
