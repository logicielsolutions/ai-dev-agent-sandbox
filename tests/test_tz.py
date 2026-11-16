from datetime import datetime, timezone

import pytest

from trialkit import tz


def test_to_utc_shifts_back_five_and_a_half_hours():
    assert tz.to_utc(datetime(2026, 11, 17, 9, 0)) == datetime(2026, 11, 17, 3, 30, tzinfo=timezone.utc)


def test_to_utc_rejects_aware_input():
    with pytest.raises(ValueError):
        tz.to_utc(datetime(2026, 11, 17, 9, 0, tzinfo=timezone.utc))


def test_day_of_midday():
    assert tz.day_of(tz.to_utc(datetime(2026, 11, 17, 12, 0))).isoformat() == "2026-11-17"


def test_to_ist_converts_the_instant():
    # 16:30 UTC is 22:00 IST: same moment, IST wall-clock time.
    moment = datetime(2026, 11, 23, 16, 30, tzinfo=timezone.utc)
    local = tz.to_ist(moment)
    assert (local.hour, local.minute) == (22, 0)
    assert local == moment


def test_to_ist_rejects_naive_input():
    with pytest.raises(ValueError):
        tz.to_ist(datetime(2026, 11, 23, 16, 30))
