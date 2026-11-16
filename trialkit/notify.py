"""Quiet hours for pings: nothing goes out 21:00-09:00 IST or at weekends."""
from datetime import datetime, timedelta, timezone

from . import tz

QUIET_FROM = 21   # 21:00 IST
QUIET_UNTIL = 9   # 09:00 IST


def _at_nine(local: datetime) -> datetime:
    return local.replace(hour=QUIET_UNTIL, minute=0, second=0, microsecond=0)


def _next_weekday_at_nine(local: datetime) -> datetime:
    d = local + timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return _at_nine(d)


def next_send_time(moment: datetime) -> datetime:
    """When a ping queued at `moment` (aware) may go out, as aware UTC.
    Inside working hours it goes at once; otherwise at the next 09:00 IST on a weekday."""
    local = tz.to_ist(moment)
    if local.weekday() >= 5:
        target = _next_weekday_at_nine(local)
    elif local.hour >= QUIET_FROM:
        target = _next_weekday_at_nine(local)
    elif local.hour < QUIET_UNTIL:
        target = _at_nine(local)
    else:
        return moment.astimezone(timezone.utc)
    return target.astimezone(timezone.utc)
