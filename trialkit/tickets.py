"""Board tickets, as the daily digest sees them."""
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


# Order of the not-late tickets in the standup; "done" tickets are left out.
STANDUP_STAGE_ORDER = {"in_progress": 0, "review": 1, "todo": 2}


def ticket_number(key: str) -> tuple[str, int]:
    """Sort key for a ticket key: ("AIT", 9) for "AIT-9", so AIT-9 sorts before AIT-10."""
    prefix, sep, number = key.rpartition("-")
    if not sep or not number.isdigit():
        raise ValueError(f"not a ticket key: {key!r}")
    return prefix, int(number)


def standup_order(tickets: list[Ticket], today: date) -> list[str]:
    """Ticket keys in the order to go through them at standup.

    "done" tickets are left out. Late tickets (due set and before `today`) come
    first, most overdue first. The rest follow by stage: in_progress, review,
    then todo. Ties are broken by ticket number (AIT-9 before AIT-10).
    The input list is not changed.
    """
    late, rest = [], []
    for t in tickets:
        if t.stage == "done":
            continue
        if t.stage not in STANDUP_STAGE_ORDER:
            raise ValueError(f"unknown stage {t.stage!r} on {t.key}")
        if t.due is not None and t.due < today:
            late.append(t)
        else:
            rest.append(t)
    late.sort(key=lambda t: (t.due, ticket_number(t.key)))
    rest.sort(key=lambda t: (STANDUP_STAGE_ORDER[t.stage], ticket_number(t.key)))
    return [t.key for t in late + rest]
