from datetime import date

from trialkit.tickets import working_days_between


def test_same_day_is_zero():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 16)) == 0


def test_skips_the_weekend():
    # Fri 13 Nov -> Tue 17 Nov: Mon and Tue count
    assert working_days_between(date(2026, 11, 13), date(2026, 11, 17)) == 2


def test_one_week():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 23)) == 5


from trialkit.tickets import add_working_days


def test_add_working_days_midweek():
    # Mon 16 Nov + 2 -> Wed 18 Nov
    assert add_working_days(date(2026, 11, 16), 2) == date(2026, 11, 18)


def test_add_working_days_into_next_week():
    # Thu 19 Nov + 2 -> Mon 23 Nov
    assert add_working_days(date(2026, 11, 19), 2) == date(2026, 11, 23)


import copy

import pytest

from trialkit.tickets import Ticket, standup_order

TODAY = date(2026, 11, 18)


def test_standup_leaves_out_done():
    tickets = [Ticket("AIT-1", "a", stage="done"), Ticket("AIT-2", "a", stage="todo")]
    assert standup_order(tickets, TODAY) == ["AIT-2"]


def test_standup_done_is_left_out_even_when_late():
    tickets = [Ticket("AIT-1", "a", stage="done", due=date(2026, 11, 1))]
    assert standup_order(tickets, TODAY) == []


def test_standup_late_first_most_overdue_first():
    tickets = [
        Ticket("AIT-1", "a", stage="in_progress"),
        Ticket("AIT-2", "a", stage="todo", due=date(2026, 11, 17)),
        Ticket("AIT-3", "a", stage="review", due=date(2026, 11, 10)),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-2", "AIT-1"]


def test_standup_due_today_or_later_is_not_late():
    tickets = [
        Ticket("AIT-1", "a", stage="todo", due=TODAY),
        Ticket("AIT-2", "a", stage="todo", due=date(2026, 11, 20)),
        Ticket("AIT-3", "a", stage="in_progress"),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-1", "AIT-2"]


def test_standup_rest_by_stage():
    tickets = [
        Ticket("AIT-1", "a", stage="todo"),
        Ticket("AIT-2", "a", stage="review"),
        Ticket("AIT-3", "a", stage="in_progress"),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-3", "AIT-2", "AIT-1"]


def test_standup_ticket_number_is_numeric_not_text():
    tickets = [
        Ticket("AIT-10", "a", stage="todo"),
        Ticket("AIT-9", "a", stage="todo"),
        Ticket("AIT-100", "a", stage="todo"),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-9", "AIT-10", "AIT-100"]


def test_standup_equally_late_sorted_by_number():
    late = date(2026, 11, 16)
    tickets = [
        Ticket("AIT-10", "a", stage="todo", due=late),
        Ticket("AIT-9", "a", stage="review", due=late),
    ]
    assert standup_order(tickets, TODAY) == ["AIT-9", "AIT-10"]


def test_standup_does_not_change_input():
    tickets = [
        Ticket("AIT-10", "a", stage="todo"),
        Ticket("AIT-2", "a", stage="done"),
        Ticket("AIT-9", "a", stage="in_progress", due=date(2026, 11, 1)),
    ]
    before = copy.deepcopy(tickets)
    standup_order(tickets, TODAY)
    assert tickets == before


def test_standup_empty():
    assert standup_order([], TODAY) == []


def test_standup_unknown_stage_raises():
    with pytest.raises(ValueError):
        standup_order([Ticket("AIT-1", "a", stage="blocked")], TODAY)
