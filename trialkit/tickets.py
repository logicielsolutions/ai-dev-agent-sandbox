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


def owner_load(tickets: list[Ticket], today: date, cap: int = 3) -> list[tuple[str, int, int, bool]]:
    """How loaded each owner is: (owner, open, late, over_cap) per owner.

    Done tickets are skipped, so an owner with only done tickets is left out.
    Late means a due date before `today`; over_cap means open > `cap`.
    Sorted by open count, highest first, then by owner name.
    """
    counts: dict[str, list[int]] = {}
    for t in tickets:
        if t.stage == "done":
            continue
        c = counts.setdefault(t.owner, [0, 0])
        c[0] += 1
        if t.due is not None and t.due < today:
            c[1] += 1
    rows = [(owner, n_open, n_late, n_open > cap) for owner, (n_open, n_late) in counts.items()]
    return sorted(rows, key=lambda row: (-row[1], row[0]))
