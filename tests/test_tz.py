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


def test_day_of_just_after_ist_midnight():
    # 2026-11-16 18:45 UTC is 00:15 IST on Tue 17 Nov.
    assert tz.day_of(datetime(2026, 11, 16, 18, 45, tzinfo=timezone.utc)).isoformat() == "2026-11-17"
