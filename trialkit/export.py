"""Export board tickets to a CSV file for the weekly report."""
import os
from datetime import date

from .tickets import Ticket

DEFAULT_COLUMNS = ["key", "owner", "stage", "due"]


def _cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def to_csv(tickets: list[Ticket], columns: list[str] = DEFAULT_COLUMNS, with_late: bool = False,
           today: date | None = None) -> str:
    """CSV text: a header row, then one row per ticket."""
    if with_late:
        columns.append("late")
    rows = [",".join(columns)]
    for t in tickets:
        values = [_cell(getattr(t, c, None)) for c in columns if c != "late"]
        if with_late:
            values.append("yes" if t.due and today and t.due < today else "no")
        rows.append(",".join(values))
    return "\n".join(rows) + "\n"


def save(tickets: list[Ticket], report_dir: str, name: str, **kwargs) -> str:
    """Write the CSV to `report_dir/name` and return the path."""
    path = os.path.join(report_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_csv(tickets, **kwargs))
    return path
