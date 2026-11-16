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


def late_and_quiet(
    tickets: list[Ticket], today: date, quiet_after: int = 2
) -> dict[str, dict[str, list[str]]]:
    """Group flagged ticket keys by owner: {owner: {"late": [...], "quiet": [...]}}.

    Done tickets are skipped. Late: `due` is set and before `today`. Quiet: no
    comment yet, or at least `quiet_after` working days since the last one.
    Keys keep input order; owners appear in order of their first flagged ticket
    and are left out when nothing of theirs is flagged.
    """
    flagged: dict[str, dict[str, list[str]]] = {}
    for t in tickets:
        if t.stage == "done":
            continue
        late = t.due is not None and t.due < today
        quiet = (
            t.last_comment is None
            or working_days_between(t.last_comment, today) >= quiet_after
        )
        if not (late or quiet):
            continue
        entry = flagged.setdefault(t.owner, {"late": [], "quiet": []})
        if late:
            entry["late"].append(t.key)
        if quiet:
            entry["quiet"].append(t.key)
    return flagged
