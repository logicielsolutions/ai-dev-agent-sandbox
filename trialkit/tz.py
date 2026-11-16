"""Time zone helpers. Everything a user sees is in IST (UTC+05:30)."""
from datetime import date, datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30), "IST")


def to_utc(local: datetime) -> datetime:
    """Turn an IST wall-clock time (naive) into an aware UTC datetime."""
    if local.tzinfo is not None:
        raise ValueError("expected a naive IST datetime")
    return local.replace(tzinfo=IST).astimezone(timezone.utc)


def day_of(moment: datetime) -> date:
    """The calendar day a moment falls on, in IST."""
    return moment.date()


def to_ist(moment: datetime) -> datetime:
    """An aware datetime shown in IST."""
    if moment.tzinfo is None:
        raise ValueError("expected an aware datetime")
    return moment.replace(tzinfo=IST)
