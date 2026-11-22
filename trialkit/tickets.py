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


_STAGE_ORDER = {"in_progress": 0, "review": 1, "todo": 2}


def _ticket_number(key: str) -> int:
    """The numeric part of a key like "AIT-42", so AIT-9 sorts before AIT-10."""
    return int(key.rsplit("-", 1)[-1])


def standup_order(tickets: list[Ticket], today: date) -> list[str]:
    """Ticket keys in the order to walk through them at stand-up.

    Done tickets are left out. Late tickets (due before `today`) come first, most
    overdue first. The rest follow by stage: in_progress, then review, then todo.
    Ties are broken by ticket number. The input list is not changed.
    """
    late, on_time = [], []
    for t in tickets:
        if t.stage == "done":
            continue
        if t.due is not None and t.due < today:
            late.append(t)
        else:
            on_time.append(t)
    late.sort(key=lambda t: (t.due, _ticket_number(t.key)))
    on_time.sort(key=lambda t: (_STAGE_ORDER.get(t.stage, len(_STAGE_ORDER)), _ticket_number(t.key)))
    return [t.key for t in late + on_time]
