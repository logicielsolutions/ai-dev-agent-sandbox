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


_STANDUP_STAGE_ORDER = {"in_progress": 0, "review": 1, "todo": 2}
_KEY_NUMBER = re.compile(r"^(.*?)(\d+)$")


def _ticket_number(key: str) -> tuple[str, int]:
    """Sort key for a ticket key by its number, so AIT-9 comes before AIT-10."""
    match = _KEY_NUMBER.match(key)
    if match is None:
        return (key, -1)
    return (match.group(1), int(match.group(2)))


def standup_order(tickets: list[Ticket], today: date) -> list[str]:
    """Ticket keys in the order to go through them at stand-up.

    "done" tickets are left out. Late tickets (due set and before `today`) come
    first, most overdue first. The rest follow by stage: in_progress, then
    review, then todo. Ties, and tickets within a stage, go by ticket number.
    The input list is not changed.
    """
    late, rest = [], []
    for t in tickets:
        if t.stage == "done":
            continue
        if t.due is not None and t.due < today:
            late.append(t)
        else:
            rest.append(t)

    late = sorted(late, key=lambda t: (t.due, _ticket_number(t.key)))
    rest = sorted(
        rest,
        key=lambda t: (
            _STANDUP_STAGE_ORDER.get(t.stage, len(_STANDUP_STAGE_ORDER)),
            _ticket_number(t.key),
        ),
    )
    return [t.key for t in late + rest]
