from datetime import date

from trialkit.tickets import Ticket, owner_load

TODAY = date(2026, 11, 17)


def t(key, owner, stage="todo", due=None):
    return Ticket(key=key, owner=owner, stage=stage, due=due)


def test_no_tickets_gives_empty_list():
    assert owner_load([], TODAY) == []


def test_only_done_tickets_gives_empty_list():
    assert owner_load([t("AIT-1", "asha", "done", date(2026, 11, 1))], TODAY) == []


def test_counts_open_and_late_per_owner():
    tickets = [
        t("AIT-1", "asha", "todo", date(2026, 11, 16)),        # late
        t("AIT-2", "asha", "in_progress", date(2026, 11, 17)),  # due today: not late
        t("AIT-3", "asha", "review"),                           # no due date: not late
        t("AIT-4", "ben", "todo", date(2026, 11, 18)),
    ]
    assert owner_load(tickets, TODAY) == [("asha", 3, 1, False), ("ben", 1, 0, False)]


def test_done_tickets_are_skipped_even_if_late():
    tickets = [
        t("AIT-1", "asha", "done", date(2026, 11, 1)),
        t("AIT-2", "asha", "todo", date(2026, 11, 2)),
    ]
    assert owner_load(tickets, TODAY) == [("asha", 1, 1, False)]


def test_over_cap_is_strictly_more_than_cap():
    three = [t(f"AIT-{i}", "asha") for i in range(3)]
    four = [t(f"AIT-{i}", "ben") for i in range(10, 14)]
    assert owner_load(three + four, TODAY) == [("ben", 4, 0, True), ("asha", 3, 0, False)]


def test_custom_cap():
    tickets = [t("AIT-1", "asha"), t("AIT-2", "asha"), t("AIT-3", "ben")]
    assert owner_load(tickets, TODAY, cap=1) == [("asha", 2, 0, True), ("ben", 1, 0, False)]
    assert owner_load(tickets, TODAY, cap=0) == [("asha", 2, 0, True), ("ben", 1, 0, True)]


def test_sorted_by_open_count_then_owner_name():
    tickets = [
        t("AIT-1", "dev"),
        t("AIT-2", "cara"), t("AIT-3", "cara"),
        t("AIT-4", "bo"),
        t("AIT-5", "amir"), t("AIT-6", "amir"),
    ]
    assert [row[0] for row in owner_load(tickets, TODAY)] == ["amir", "cara", "bo", "dev"]


def test_late_count_does_not_affect_order():
    tickets = [
        t("AIT-1", "zed", "todo", date(2026, 11, 1)),
        t("AIT-2", "ann", "todo"),
    ]
    assert owner_load(tickets, TODAY) == [("ann", 1, 0, False), ("zed", 1, 1, False)]


def test_does_not_change_the_input():
    tickets = [t("AIT-2", "ben"), t("AIT-1", "asha", "done")]
    before = list(tickets)
    owner_load(tickets, TODAY)
    assert tickets == before
