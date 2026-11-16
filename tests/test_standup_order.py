import copy
from datetime import date

from trialkit.tickets import Ticket, standup_order

TODAY = date(2026, 11, 18)  # Wed


def t(key, stage="todo", due=None):
    return Ticket(key=key, owner="harpreet", stage=stage, due=due)


def test_empty():
    assert standup_order([], TODAY) == []


def test_done_tickets_left_out_even_when_late():
    tickets = [t("AIT-1", "done", date(2026, 11, 1)), t("AIT-2", "done"), t("AIT-3")]
    assert standup_order(tickets, TODAY) == ["AIT-3"]


def test_late_first_most_overdue_first():
    tickets = [
        t("AIT-1", "in_progress"),
        t("AIT-2", "todo", date(2026, 11, 17)),
        t("AIT-3", "review", date(2026, 11, 10)),
        t("AIT-4", "in_progress", date(2026, 11, 14)),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-4", "AIT-2", "AIT-1"]


def test_due_today_or_later_is_not_late():
    tickets = [
        t("AIT-1", "todo", TODAY),
        t("AIT-2", "todo", date(2026, 11, 25)),
        t("AIT-3", "in_progress", TODAY),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-1", "AIT-2"]


def test_rest_by_stage():
    tickets = [t("AIT-1", "todo"), t("AIT-2", "review"), t("AIT-3", "in_progress")]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-2", "AIT-1"]


def test_within_stage_by_ticket_number_not_text():
    tickets = [t("AIT-10"), t("AIT-9"), t("AIT-100"), t("AIT-2")]
    assert standup_order(tickets, TODAY) == ["AIT-2", "AIT-9", "AIT-10", "AIT-100"]


def test_late_ties_by_ticket_number():
    due = date(2026, 11, 12)
    tickets = [t("AIT-10", "todo", due), t("AIT-9", "review", due)]
    assert standup_order(tickets, TODAY) == ["AIT-9", "AIT-10"]


def test_full_mix():
    tickets = [
        t("AIT-12", "todo"),
        t("AIT-5", "done"),
        t("AIT-11", "review"),
        t("AIT-10", "in_progress", date(2026, 11, 16)),
        t("AIT-9", "in_progress"),
        t("AIT-8", "todo", date(2026, 11, 13)),
        t("AIT-7", "review", date(2026, 11, 20)),
    ]
    assert standup_order(tickets, TODAY) == [
        "AIT-8", "AIT-10", "AIT-9", "AIT-7", "AIT-11", "AIT-12",
    ]


def test_input_list_not_changed():
    tickets = [
        t("AIT-3", "todo"),
        t("AIT-1", "review", date(2026, 11, 2)),
        t("AIT-2", "done"),
    ]
    before = copy.deepcopy(tickets)
    standup_order(tickets, TODAY)
    assert tickets == before
