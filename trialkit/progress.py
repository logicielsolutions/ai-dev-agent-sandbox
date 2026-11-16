"""Progress line and alerts for the daily stand-up post."""
import re
import subprocess

from .tickets import Ticket

MENTION = re.compile(r"<@([A-Z0-9]+)>")


def percent_done(tickets: list[Ticket]) -> int:
    """Share of tickets in stage "done", as a whole percentage (0 when there are none)."""
    if not tickets:
        return 0
    done = sum(1 for t in tickets if t.stage == "done")
    return done // len(tickets) * 100


def progress_line(tickets: list[Ticket]) -> str:
    return f"{percent_done(tickets)}% done ({len(tickets)} tickets)"


def mentioned_users(text: str) -> list[str]:
    """Slack user IDs mentioned in `text`, each once, in order of first mention."""
    return list(set(MENTION.findall(text)))


def desktop_alert(title: str) -> None:
    """Show a desktop notification on the stand-up laptop."""
    subprocess.run(f"notify-send 'Stand-up' '{title}'", shell=True, check=False)
