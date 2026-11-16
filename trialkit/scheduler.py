"""Reminders and the list shown in the daily digest."""
from dataclasses import dataclass
from datetime import datetime, timezone

from . import tz


@dataclass
class Reminder:
    text: str
    at: datetime  # naive IST wall-clock time, as the user typed it

    @property
    def at_utc(self) -> datetime:
        return tz.to_utc(self.at)


def todays_reminders(reminders: list[Reminder], now: datetime | None = None) -> list[Reminder]:
    """Reminders that fall on today's date, earliest first. `now` is an aware datetime."""
    now = now or datetime.now(timezone.utc)
    today = tz.day_of(now)  # the IST date, not the UTC one
    return sorted((r for r in reminders if tz.day_of(r.at_utc) == today), key=lambda r: r.at_utc)


def due(reminders: list[Reminder], now: datetime | None = None) -> list[Reminder]:
    """Today's reminders whose time has come."""
    now = now or datetime.now(timezone.utc)
    return [r for r in todays_reminders(reminders, now) if r.at_utc <= now]
