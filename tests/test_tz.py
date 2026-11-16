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
    utc = datetime(2026, 11, 23, 16, 30, tzinfo=timezone.utc)
    local = tz.to_ist(utc)
    assert (local.hour, local.minute, local.day) == (22, 0, 23)
    assert local == utc   # same instant


def test_to_ist_rejects_naive_input():
    with pytest.raises(ValueError):
        tz.to_ist(datetime(2026, 11, 23, 22, 0))
