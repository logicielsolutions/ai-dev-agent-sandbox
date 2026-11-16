from datetime import datetime, timedelta, timezone

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


# Regression: quiet hours were checked on the UTC wall clock, not IST.

def test_weeknight_after_nine_pm_ist_waits_for_next_morning():
    t = datetime(2026, 11, 23, 16, 30, tzinfo=UTC)     # Mon 23 Nov 22:00 IST
    assert next_send_time(t) == datetime(2026, 11, 24, 3, 30, tzinfo=UTC)   # Tue 09:00 IST


def test_friday_night_waits_for_monday():
    t = datetime(2026, 11, 27, 17, 30, tzinfo=UTC)     # Fri 27 Nov 23:00 IST
    assert next_send_time(t) == datetime(2026, 11, 30, 3, 30, tzinfo=UTC)   # Mon 09:00 IST


def test_just_before_nine_pm_ist_goes_at_once():
    t = datetime(2026, 11, 23, 15, 29, tzinfo=UTC)     # Mon 20:59 IST
    assert next_send_time(t) == t


def test_nine_pm_ist_exactly_is_quiet():
    t = datetime(2026, 11, 23, 15, 30, tzinfo=UTC)     # Mon 21:00 IST
    assert next_send_time(t) == datetime(2026, 11, 24, 3, 30, tzinfo=UTC)


def test_nine_am_ist_exactly_goes_at_once():
    t = datetime(2026, 11, 24, 3, 30, tzinfo=UTC)      # Tue 09:00 IST
    assert next_send_time(t) == t


def test_after_midnight_ist_but_previous_day_in_utc():
    t = datetime(2026, 11, 23, 20, 0, tzinfo=UTC)      # Tue 24 Nov 01:30 IST (still Mon in UTC)
    assert next_send_time(t) == datetime(2026, 11, 24, 3, 30, tzinfo=UTC)   # Tue 09:00 IST


def test_monday_early_ist_is_sunday_in_utc():
    t = datetime(2026, 11, 29, 21, 0, tzinfo=UTC)      # Mon 30 Nov 02:30 IST (Sun in UTC)
    assert next_send_time(t) == datetime(2026, 11, 30, 3, 30, tzinfo=UTC)   # Mon 09:00 IST


def test_saturday_early_ist_is_friday_in_utc():
    t = datetime(2026, 11, 27, 19, 0, tzinfo=UTC)      # Sat 28 Nov 00:30 IST (Fri in UTC)
    assert next_send_time(t) == datetime(2026, 11, 30, 3, 30, tzinfo=UTC)   # Mon 09:00 IST


def test_non_utc_input_zone_is_handled():
    ist = timezone(timedelta(hours=5, minutes=30))
    t = datetime(2026, 11, 23, 22, 0, tzinfo=ist)      # Mon 22:00 IST given in IST
    assert next_send_time(t) == datetime(2026, 11, 24, 3, 30, tzinfo=UTC)


def test_result_is_utc():
    t = datetime(2026, 11, 23, 16, 30, tzinfo=UTC)
    assert next_send_time(t).utcoffset() == timedelta(0)
