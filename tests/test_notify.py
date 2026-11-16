from datetime import datetime, timezone

from trialkit.notify import next_send_time

UTC = timezone.utc


def test_working_hours_go_at_once():
    t = datetime(2026, 11, 24, 9, 30, tzinfo=UTC)      # Tue 15:00 IST
    assert next_send_time(t) == t


def test_early_morning_waits_for_nine():
    t = datetime(2026, 11, 24, 2, 30, tzinfo=UTC)      # Tue 08:00 IST
    assert next_send_time(t) == datetime(2026, 11, 24, 3, 30, tzinfo=UTC)   # Tue 09:00 IST


def test_weekend_waits_for_monday():
    t = datetime(2026, 11, 28, 6, 30, tzinfo=UTC)      # Sat 12:00 IST
    assert next_send_time(t) == datetime(2026, 11, 30, 3, 30, tzinfo=UTC)   # Mon 09:00 IST
