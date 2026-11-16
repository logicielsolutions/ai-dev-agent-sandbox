import copy
from datetime import date

import pytest

from trialkit.tickets import Ticket, standup_order

TODAY = date(2026, 11, 18)


def t(key, stage="todo", due=None):
    return Ticket(key, "asha", stage, due=due)


def test_empty():
    assert standup_order([], TODAY) == []


def test_done_tickets_are_left_out_even_when_late():
    tickets = [t("AIT-1", "done"), t("AIT-2", "done", due=date(2026, 11, 1)), t("AIT-3")]
    assert standup_order(tickets, TODAY) == ["AIT-3"]


def test_late_first_most_overdue_first():
    tickets = [
        t("AIT-1", "in_progress"),
        t("AIT-2", "todo", due=date(2026, 11, 17)),
        t("AIT-3", "review", due=date(2026, 11, 10)),
        t("AIT-4", "in_progress", due=date(2026, 11, 15)),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-4", "AIT-2", "AIT-1"]


def test_due_today_or_later_is_not_late():
    tickets = [
        t("AIT-1", "todo", due=TODAY),
        t("AIT-2", "todo", due=date(2026, 11, 30)),
        t("AIT-3", "review", due=date(2026, 11, 17)),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-1", "AIT-2"]


def test_rest_by_stage_in_progress_review_todo():
    tickets = [t("AIT-1", "todo"), t("AIT-2", "review"), t("AIT-3", "in_progress")]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-2", "AIT-1"]


def test_within_stage_sorted_by_ticket_number_not_text():
    tickets = [t("AIT-10", "todo"), t("AIT-9", "todo"), t("AIT-100", "todo"), t("AIT-2", "todo")]
    assert standup_order(tickets, TODAY) == ["AIT-2", "AIT-9", "AIT-10", "AIT-100"]


def test_equally_late_sorted_by_ticket_number():
    due = date(2026, 11, 16)
    tickets = [t("AIT-10", "todo", due), t("AIT-9", "review", due), t("AIT-11", "in_progress", due)]
    assert standup_order(tickets, TODAY) == ["AIT-9", "AIT-10", "AIT-11"]


def test_full_mix():
    tickets = [
        t("AIT-12", "todo"),
        t("AIT-3", "done", due=date(2026, 11, 1)),
        t("AIT-10", "review"),
        t("AIT-9", "review"),
        t("AIT-20", "in_progress", due=date(2026, 11, 20)),
        t("AIT-7", "todo", due=date(2026, 11, 16)),
        t("AIT-8", "in_progress", due=date(2026, 11, 12)),
        t("AIT-1", "in_progress"),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-8", "AIT-7", "AIT-1", "AIT-20", "AIT-9", "AIT-10", "AIT-12"]


def test_input_list_is_not_changed():
    tickets = [t("AIT-10", "todo"), t("AIT-2", "in_progress", due=date(2026, 11, 1)), t("AIT-5", "done")]
    before = copy.deepcopy(tickets)
    standup_order(tickets, TODAY)
    assert tickets == before


def test_unknown_stage_raises():
    with pytest.raises(ValueError):
        standup_order([t("AIT-1", "blocked")], TODAY)
