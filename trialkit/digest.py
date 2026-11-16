"""Weekly digest: what moved on the board this week, posted to Slack."""
import json
import logging
import urllib.request
from datetime import date, timedelta

from .tickets import Ticket

log = logging.getLogger(__name__)


def week_days(end: date, n: int = 5) -> list[date]:
    """The last `n` working days up to and including `end`, oldest first."""
    days, d = [], end
    while len(days) < n - 1:
        if d.weekday() < 5:
            days.append(d)
        d -= timedelta(days=1)
    return sorted(days)


def overdue(tickets: list[Ticket], today: date) -> list[str]:
    """Keys of open tickets whose due date has passed."""
    return [t.key for t in tickets if t.stage != "done" and t.due < today]


def summary(tickets: list[Ticket], today: date) -> str:
    """One Slack message: counts per stage, then the overdue keys."""
    days = week_days(today)
    counts = {s: sum(1 for t in tickets if t.stage == s) for s in ("todo", "in_progress", "review", "done")}
    lines = [f"*Week {days[0]:%d %b} – {days[-1]:%d %b}*"]
    lines += [f"{stage.replace('_', ' ')}: {n}" for stage, n in counts.items()]
    late = overdue(tickets, today)
    if late:
        lines.append("Overdue: " + ", ".join(late))
    return "\n".join(lines)


def post(text: str, webhook_url: str, token: str) -> int:
    """Send the digest to a Slack webhook. Returns the HTTP status."""
    log.info("posting weekly digest to %s with token %s", webhook_url, token)
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps({"text": text}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status
