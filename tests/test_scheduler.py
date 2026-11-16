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


def test_evening_digest_leaves_out_tomorrows_early_morning_reminder():
    # Regression: Mon 16 Nov evening digest (18:30 IST = 13:00 UTC) listed a reminder
    # for Tue 17 Nov 02:00 IST (= Mon 20:30 UTC) under "today".
    rs = [Reminder("tue 2am", ist(2026, 11, 17, 2, 0)), Reminder("mon 10pm", ist(2026, 11, 16, 22, 0))]
    now = datetime(2026, 11, 16, 13, 0, tzinfo=timezone.utc)  # 18:30 IST Mon
    assert [r.text for r in todays_reminders(rs, now)] == ["mon 10pm"]


def test_after_ist_midnight_today_is_the_ist_date():
    # 01:00 IST Tue is still Mon in UTC; "today" must be Tuesday.
    rs = [Reminder("tue 2am", ist(2026, 11, 17, 2, 0)), Reminder("mon 10pm", ist(2026, 11, 16, 22, 0))]
    now = datetime(2026, 11, 16, 19, 30, tzinfo=timezone.utc)  # 01:00 IST Tue
    assert [r.text for r in todays_reminders(rs, now)] == ["tue 2am"]
    assert due(rs, now) == []
