"""Response-time targets (SLA) for board tickets, in working days."""
from datetime import date, datetime

from .tickets import add_working_days

SLA_DAYS = {"code": 3, "research": 2, "docs": 2, "ops": 1}


def opened_on(opened_at: datetime) -> date:
    """The day a ticket was opened, in IST. `opened_at` is naive IST wall-clock time.

    It is already IST, so take its date as is. Converting to UTC first moves
    anything opened before 05:30 IST back to the previous day.
    """
    if opened_at.tzinfo is not None:
        raise ValueError("expected a naive IST datetime")
    return opened_at.date()


def due_date(opened_at: datetime, sla_days: int) -> date:
    """When a reply is due: `sla_days` working days after the day it was opened."""
    return add_working_days(opened_on(opened_at), sla_days)


def due_for(ticket_type: str, opened_at: datetime) -> date:
    return due_date(opened_at, SLA_DAYS[ticket_type])
