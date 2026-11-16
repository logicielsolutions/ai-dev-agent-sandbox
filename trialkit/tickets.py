"""Board tickets, as the daily digest sees them."""
from dataclasses import dataclass
from collections.abc import Iterable
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


def owner_load(
    tickets: Iterable[Ticket], today: date, cap: int = 3
) -> list[tuple[str, int, int, bool]]:
    """Per-owner load of open (non-done) tickets.

    Returns ``(owner, open, late, over_cap)`` tuples, where ``open`` counts the
    owner's tickets not in stage ``"done"``, ``late`` counts those open tickets
    with a due date strictly before ``today`` (due today is not late), and
    ``over_cap`` is ``open > cap``. Done tickets are ignored entirely, so owners
    with only done tickets do not appear. Sorted by open count descending, then
    owner name ascending. ``tickets`` may be any iterable; it is iterated once.
    """
    counts: dict[str, list[int]] = {}
    for t in tickets:
        if t.stage == "done":
            continue
        c = counts.setdefault(t.owner, [0, 0])
        c[0] += 1
        if t.due is not None and t.due < today:
            c[1] += 1
    rows = [(owner, o, l, o > cap) for owner, (o, l) in counts.items()]
    rows.sort(key=lambda r: (-r[1], r[0]))
    return rows
