from datetime import date

from trialkit.tickets import Ticket, owner_load

MON = date(2026, 11, 23)
SUN = date(2026, 11, 22)


def test_no_tickets():
    assert owner_load([], MON) == []


def test_done_tickets_are_skipped():
    tickets = [Ticket("A-1", "ann", stage="done", due=SUN), Ticket("B-1", "bob")]
    assert owner_load(tickets, MON) == [("bob", 1, 0, False)]


def test_late_needs_a_due_date_before_today():
    tickets = [
        Ticket("A-1", "ann", due=SUN),
        Ticket("A-2", "ann", due=MON),  # due today: not late
        Ticket("A-3", "ann", due=None),
        Ticket("A-4", "ann", stage="review", due=date(2026, 11, 1)),
    ]
    assert owner_load(tickets, MON) == [("ann", 4, 2, True)]


def test_over_cap_is_strictly_more_than_cap():
    three = [Ticket(f"A-{i}", "ann") for i in range(3)]
    four = [Ticket(f"B-{i}", "bob") for i in range(4)]
    assert owner_load(three + four, MON) == [("bob", 4, 0, True), ("ann", 3, 0, False)]
    assert owner_load(three, MON, cap=2) == [("ann", 3, 0, True)]


def test_sorted_by_open_desc_then_owner_name():
    tickets = [
        Ticket("C-1", "cat"),
        Ticket("B-1", "bob"),
        Ticket("B-2", "bob"),
        Ticket("A-1", "ann"),
        Ticket("D-1", "dan", stage="done"),
    ]
    assert owner_load(tickets, MON) == [
        ("bob", 2, 0, False),
        ("ann", 1, 0, False),
        ("cat", 1, 0, False),
    ]
