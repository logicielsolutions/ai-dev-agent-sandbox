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


def late_and_quiet(tickets: list[Ticket], today: date, quiet_after: int = 2) -> dict[str, dict[str, list[str]]]:
    """Per owner, the keys of open tickets that are late and/or quiet.

    Done tickets are skipped. A ticket is late when it has a due date before
    `today`, and quiet when it has no comment yet or its last comment is at
    least `quiet_after` working days before `today`. A ticket can be both.
    Returns owner -> {"late": [...], "quiet": [...]}, keys in input order;
    owners with nothing flagged are left out.
    """
    result: dict[str, dict[str, list[str]]] = {}
    for t in tickets:
        if t.stage == "done":
            continue
        late = t.due is not None and t.due < today
        quiet = t.last_comment is None or working_days_between(t.last_comment, today) >= quiet_after
        if not (late or quiet):
            continue
        flags = result.setdefault(t.owner, {"late": [], "quiet": []})
        if late:
            flags["late"].append(t.key)
        if quiet:
            flags["quiet"].append(t.key)
    return result
