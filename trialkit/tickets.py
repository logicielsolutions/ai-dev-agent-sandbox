"""Board tickets, as the daily digest sees them."""
import re
from dataclasses import dataclass
from datetime import date, timedelta

STAGES = ("todo", "in_progress", "review", "done")


@dataclass
class Ticket:
    key: str
    owner: str
    stage: str = "todo"
    due: date | None = None
    last_comment: date | None = None


def working_days_between(start: date, end: date) -> int:
    """Mon-Fri days after `start`, up to and including `end` (0 when end <= start)."""
    days, d = 0, start
    while d < end:
        d += timedelta(days=1)
        if d.weekday() < 5:
            days += 1
    return days


def add_working_days(start: date, n: int) -> date:
    """The date `n` working days (Mon-Fri) after `start`, not counting `start` itself."""
    d = start + timedelta(days=n)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


_TICKET_KEY = re.compile(r"([A-Za-z]{2,10})-([1-9][0-9]*)", re.ASCII)


def parse_ticket_key(text: str) -> tuple[str, int]:
    """Split a ticket key like "AIT-1093" into ("AIT", 1093).

    The project is 2 to 10 letters (returned upper case), then one dash, then a
    whole number of 1 or more with no leading zeros. Surrounding whitespace is
    ignored. Anything else raises ValueError; a non-string raises TypeError.
    """
    if not isinstance(text, str):
        raise TypeError(f"ticket key must be a string, not {type(text).__name__}")
    match = _TICKET_KEY.fullmatch(text.strip())
    if match is None:
        raise ValueError(f"not a ticket key: {text!r}")
    project, number = match.groups()
    return project.upper(), int(number)
