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


# Regression tests for the quiet-hours bug report. Times are written in IST, as users enter them.
import pytest

from trialkit import tz


@pytest.mark.parametrize(
    "queued, expected",
    [
        ((2026, 11, 23, 22, 0), (2026, 11, 24, 9, 0)),   # Mon 22:00 -> Tue 09:00 (reported)
        ((2026, 11, 27, 23, 0), (2026, 11, 30, 9, 0)),   # Fri 23:00 -> Mon 09:00 (reported)
        ((2026, 11, 23, 21, 0), (2026, 11, 24, 9, 0)),   # quiet hours start at 21:00 sharp
        ((2026, 11, 27, 21, 30), (2026, 11, 30, 9, 0)),  # Fri evening skips the weekend
        ((2026, 11, 28, 1, 0), (2026, 11, 30, 9, 0)),    # Sat 01:00 IST is still Fri in UTC
        ((2026, 11, 29, 23, 0), (2026, 11, 30, 9, 0)),   # Sun night -> Mon 09:00
        ((2026, 11, 24, 3, 0), (2026, 11, 24, 9, 0)),    # Tue 03:00 IST is still Mon in UTC
    ],
)
def test_quiet_hours_in_ist(queued, expected):
    assert next_send_time(tz.to_utc(datetime(*queued))) == tz.to_utc(datetime(*expected))


@pytest.mark.parametrize("queued", [(2026, 11, 23, 9, 0), (2026, 11, 23, 20, 59), (2026, 11, 27, 20, 59)])
def test_working_hours_in_ist_go_at_once(queued):
    t = tz.to_utc(datetime(*queued))
    assert next_send_time(t) == t
