from datetime import date

from trialkit.tickets import Ticket, late_and_quiet, working_days_between


def test_same_day_is_zero():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 16)) == 0


def test_skips_the_weekend():
    # Fri 13 Nov -> Tue 17 Nov: Mon and Tue count
    assert working_days_between(date(2026, 11, 13), date(2026, 11, 17)) == 2


def test_one_week():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 23)) == 5


TODAY = date(2026, 11, 17)  # Tuesday


def test_late_and_quiet_flags_per_owner_in_input_order():
    tickets = [
        Ticket("A-1", "ann", due=date(2026, 11, 16), last_comment=date(2026, 11, 17)),  # late only
        Ticket("A-2", "ann", due=date(2026, 11, 20), last_comment=None),  # quiet only
        Ticket("B-1", "bob", due=date(2026, 11, 1), last_comment=date(2026, 11, 12)),  # both
        Ticket("A-3", "ann", due=date(2026, 11, 10), last_comment=date(2026, 11, 13)),  # both (2 wd)
    ]
    assert late_and_quiet(tickets, TODAY) == {
        "ann": {"late": ["A-1", "A-3"], "quiet": ["A-2", "A-3"]},
        "bob": {"late": ["B-1"], "quiet": ["B-1"]},
    }


def test_done_tickets_skipped_and_clean_owners_omitted():
    tickets = [
        Ticket("A-1", "ann", stage="done", due=date(2026, 1, 1)),
        Ticket("B-1", "bob", due=TODAY, last_comment=TODAY),  # due today is not late
    ]
    assert late_and_quiet(tickets, TODAY) == {}


def test_quiet_threshold_boundary_and_custom_value():
    t = [Ticket("A-1", "ann", last_comment=date(2026, 11, 16))]  # 1 working day
    assert late_and_quiet(t, TODAY) == {}
    assert late_and_quiet(t, TODAY, quiet_after=1) == {"ann": {"late": [], "quiet": ["A-1"]}}
    t = [Ticket("A-1", "ann", last_comment=date(2026, 11, 13))]  # 2 working days over weekend
    assert late_and_quiet(t, TODAY) == {"ann": {"late": [], "quiet": ["A-1"]}}


def test_no_due_date_is_not_late():
    t = [Ticket("A-1", "ann", last_comment=TODAY)]
    assert late_and_quiet(t, TODAY) == {}
