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


from trialkit.tickets import Ticket, owner_load

TODAY = date(2026, 11, 16)


def test_owner_load_empty():
    assert owner_load([], TODAY) == []


def test_owner_load_only_done_is_empty():
    assert owner_load([Ticket("A-1", "ann", stage="done")], TODAY) == []


def test_owner_load_skips_done():
    tickets = [
        Ticket("A-1", "ann", stage="todo"),
        Ticket("A-2", "ann", stage="done"),
        Ticket("B-1", "bob", stage="done"),
    ]
    assert owner_load(tickets, TODAY) == [("ann", 1, 0, False)]


def test_owner_load_late_counting():
    tickets = [
        Ticket("A-1", "ann", due=date(2026, 11, 15)),  # late
        Ticket("A-2", "ann", stage="review", due=TODAY),  # due today: not late
        Ticket("A-3", "ann", stage="in_progress"),  # no due: not late
        Ticket("A-4", "ann", due=date(2026, 11, 17)),  # future: not late
    ]
    assert owner_load(tickets, TODAY) == [("ann", 4, 1, True)]


def test_owner_load_done_overdue_not_late():
    tickets = [
        Ticket("A-1", "ann", stage="done", due=date(2026, 11, 1)),
        Ticket("A-2", "ann"),
    ]
    assert owner_load(tickets, TODAY) == [("ann", 1, 0, False)]


def test_owner_load_over_cap_boundary():
    at_cap = [Ticket(f"A-{i}", "ann") for i in range(3)]
    assert owner_load(at_cap, TODAY) == [("ann", 3, 0, False)]
    over = at_cap + [Ticket("A-9", "ann")]
    assert owner_load(over, TODAY) == [("ann", 4, 0, True)]


def test_owner_load_custom_cap():
    tickets = [Ticket("A-1", "ann"), Ticket("A-2", "ann")]
    assert owner_load(tickets, TODAY, cap=1) == [("ann", 2, 0, True)]
    assert owner_load(tickets, TODAY, cap=2) == [("ann", 2, 0, False)]


def test_owner_load_sort_by_open_desc_then_name():
    tickets = [
        Ticket("C-1", "cat"),
        Ticket("B-1", "bob"),
        Ticket("B-2", "bob"),
        Ticket("A-1", "ann"),
        Ticket("D-1", "dan"),
        Ticket("D-2", "dan"),
    ]
    assert owner_load(tickets, TODAY) == [
        ("bob", 2, 0, False),
        ("dan", 2, 0, False),
        ("ann", 1, 0, False),
        ("cat", 1, 0, False),
    ]


def test_owner_load_accepts_generator():
    gen = (Ticket(f"A-{i}", "ann", due=date(2026, 11, 10)) for i in range(2))
    assert owner_load(gen, TODAY) == [("ann", 2, 2, False)]
