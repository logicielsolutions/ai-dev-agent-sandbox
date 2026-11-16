from datetime import datetime, timedelta, timezone

import pytest

from trialkit import tz
from trialkit.notify import next_send_time

UTC = timezone.utc


def ist(*args):
    """An aware UTC moment for an IST wall-clock time."""
    return tz.to_utc(datetime(*args))


# --- the two reported cases -------------------------------------------------

def test_report_monday_late_evening_waits_for_tuesday_nine():
    # Mon 23 Nov 22:00 IST went out at once; it must wait until Tue 09:00 IST.
    assert next_send_time(ist(2026, 11, 23, 22, 0)) == ist(2026, 11, 24, 9, 0)


def test_report_friday_late_evening_waits_for_monday_nine():
    # Fri 27 Nov 23:00 IST must go Mon 30 Nov 09:00 IST, not Saturday.
    assert next_send_time(ist(2026, 11, 27, 23, 0)) == ist(2026, 11, 30, 9, 0)


# --- quiet-hours boundaries -------------------------------------------------

@pytest.mark.parametrize(
    "queued, expected",
    [
        ((2026, 11, 23, 21, 0), (2026, 11, 24, 9, 0)),    # Mon 21:00: quiet starts
        ((2026, 11, 26, 23, 59), (2026, 11, 27, 9, 0)),   # Thu late -> Fri 09:00
        ((2026, 11, 27, 21, 0), (2026, 11, 30, 9, 0)),    # Fri 21:00 -> Mon
        ((2026, 11, 24, 0, 30), (2026, 11, 24, 9, 0)),    # Tue 00:30 (Mon UTC) -> Tue 09:00
        ((2026, 11, 23, 2, 0), (2026, 11, 23, 9, 0)),     # Mon 02:00 (Sun UTC) -> Mon 09:00
        ((2026, 11, 28, 1, 0), (2026, 11, 30, 9, 0)),     # Sat 01:00 (Fri UTC) -> Mon
        ((2026, 11, 29, 23, 0), (2026, 11, 30, 9, 0)),    # Sun 23:00 -> Mon
        ((2026, 11, 24, 8, 59), (2026, 11, 24, 9, 0)),    # one minute before nine
    ],
)
def test_quiet_times_wait_for_next_weekday_nine(queued, expected):
    assert next_send_time(ist(*queued)) == ist(*expected)


@pytest.mark.parametrize(
    "queued",
    [
        (2026, 11, 23, 9, 0),     # Mon 09:00: quiet hours over
        (2026, 11, 23, 20, 59),   # Mon 20:59: last minute before quiet
        (2026, 11, 27, 20, 0),    # Fri 20:00
    ],
)
def test_working_hours_go_at_once(queued):
    t = ist(*queued)
    assert next_send_time(t) == t


def test_result_is_utc_even_for_ist_input():
    queued = datetime(2026, 11, 23, 22, 0, tzinfo=tz.IST)
    result = next_send_time(queued)
    assert result.utcoffset() == timedelta(0)
    assert result == ist(2026, 11, 24, 9, 0)


def test_working_hours_ist_input_comes_back_as_same_moment_in_utc():
    queued = datetime(2026, 11, 24, 15, 0, tzinfo=tz.IST)
    result = next_send_time(queued)
    assert result == queued and result.utcoffset() == timedelta(0)


# --- the helper at the root of the bug -------------------------------------

def test_to_ist_converts_instead_of_relabelling():
    moment = datetime(2026, 11, 23, 16, 30, tzinfo=UTC)          # Mon 22:00 IST
    local = tz.to_ist(moment)
    assert (local.day, local.hour, local.minute) == (23, 22, 0)
    assert local == moment                                        # same instant


def test_to_ist_rejects_naive_input():
    with pytest.raises(ValueError):
        tz.to_ist(datetime(2026, 11, 23, 22, 0))
