from datetime import date

from trialkit.tickets import Ticket, late_and_quiet

MON = date(2026, 11, 16)
FRI = date(2026, 11, 13)
THU = date(2026, 11, 12)
SUN = date(2026, 11, 15)


def test_empty():
    assert late_and_quiet([], MON) == {}


def test_late_needs_a_due_date_before_today():
    tickets = [
        Ticket("A-1", "ann", due=SUN, last_comment=MON),
        Ticket("A-2", "ann", due=MON, last_comment=MON),  # due today: not late
        Ticket("A-3", "ann", due=None, last_comment=MON),
    ]
    assert late_and_quiet(tickets, MON) == {"ann": {"late": ["A-1"], "quiet": []}}


def test_quiet_with_no_comment_or_old_comment():
    tickets = [
        Ticket("A-1", "ann", last_comment=None),
        Ticket("A-2", "ann", last_comment=THU),  # Fri + Mon = 2 working days
        Ticket("A-3", "ann", last_comment=FRI),  # only Mon = 1 working day
    ]
    assert late_and_quiet(tickets, MON) == {"ann": {"late": [], "quiet": ["A-1", "A-2"]}}


def test_weekend_does_not_count_towards_quiet():
    # Last comment Friday, checked Monday: 1 working day, even though 3 calendar days passed.
    assert late_and_quiet([Ticket("A-1", "ann", last_comment=FRI)], MON) == {}


def test_quiet_after_is_configurable():
    t = [Ticket("A-1", "ann", last_comment=FRI)]
    assert late_and_quiet(t, MON, quiet_after=1) == {"ann": {"late": [], "quiet": ["A-1"]}}
    assert late_and_quiet([Ticket("A-2", "ann", last_comment=THU)], MON, quiet_after=3) == {}


def test_a_ticket_can_be_late_and_quiet():
    t = [Ticket("A-1", "ann", due=FRI, last_comment=None)]
    assert late_and_quiet(t, MON) == {"ann": {"late": ["A-1"], "quiet": ["A-1"]}}


def test_done_tickets_are_skipped():
    t = [Ticket("A-1", "ann", stage="done", due=FRI, last_comment=None)]
    assert late_and_quiet(t, MON) == {}


def test_owners_without_flags_are_left_out_and_order_is_kept():
    tickets = [
        Ticket("B-2", "bob", due=FRI, last_comment=MON),
        Ticket("C-1", "cat", stage="review", last_comment=MON),  # fine
        Ticket("A-1", "ann", last_comment=None),
        Ticket("B-1", "bob", due=SUN, last_comment=None),
    ]
    result = late_and_quiet(tickets, MON)
    assert result == {
        "bob": {"late": ["B-2", "B-1"], "quiet": ["B-1"]},
        "ann": {"late": [], "quiet": ["A-1"]},
    }
    assert list(result) == ["bob", "ann"]
