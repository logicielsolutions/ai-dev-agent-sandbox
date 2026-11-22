from datetime import date

from trialkit.tickets import Ticket, standup_order

TODAY = date(2026, 11, 23)


def test_done_tickets_are_left_out():
    tickets = [Ticket("AIT-1", "a", "done"), Ticket("AIT-2", "a", "todo")]
    assert standup_order(tickets, TODAY) == ["AIT-2"]


def test_late_first_most_overdue_first():
    tickets = [
        Ticket("AIT-1", "a", "in_progress"),
        Ticket("AIT-2", "a", "todo", due=date(2026, 11, 20)),
        Ticket("AIT-3", "a", "review", due=date(2026, 11, 10)),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-2", "AIT-1"]


def test_due_today_or_later_is_not_late():
    tickets = [
        Ticket("AIT-1", "a", "todo", due=TODAY),
        Ticket("AIT-2", "a", "todo", due=date(2026, 11, 30)),
        Ticket("AIT-3", "a", "todo", due=date(2026, 11, 22)),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-1", "AIT-2"]


def test_late_done_ticket_is_still_left_out():
    tickets = [Ticket("AIT-1", "a", "done", due=date(2026, 11, 1))]
    assert standup_order(tickets, TODAY) == []


def test_stage_order_for_the_rest():
    tickets = [
        Ticket("AIT-1", "a", "todo"),
        Ticket("AIT-2", "a", "review"),
        Ticket("AIT-3", "a", "in_progress"),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-2", "AIT-1"]


def test_numeric_order_within_a_group():
    tickets = [
        Ticket("AIT-10", "a", "todo"),
        Ticket("AIT-9", "a", "todo"),
        Ticket("AIT-100", "a", "todo"),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-9", "AIT-10", "AIT-100"]


def test_numeric_order_breaks_ties_between_equally_late_tickets():
    due = date(2026, 11, 20)
    tickets = [Ticket("AIT-10", "a", "todo", due=due), Ticket("AIT-9", "a", "review", due=due)]
    assert standup_order(tickets, TODAY) == ["AIT-9", "AIT-10"]


def test_input_is_not_mutated():
    tickets = [
        Ticket("AIT-2", "a", "todo"),
        Ticket("AIT-1", "a", "done"),
        Ticket("AIT-3", "a", "in_progress", due=date(2026, 11, 1)),
    ]
    snapshot = [(t.key, t.stage, t.due) for t in tickets]
    standup_order(tickets, TODAY)
    assert [(t.key, t.stage, t.due) for t in tickets] == snapshot


def test_empty_list():
    assert standup_order([], TODAY) == []
