from datetime import date

from trialkit.tickets import Ticket, late_and_quiet, working_days_between


def test_same_day_is_zero():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 16)) == 0


def test_skips_the_weekend():
    # Fri 13 Nov -> Tue 17 Nov: Mon and Tue count
    assert working_days_between(date(2026, 11, 13), date(2026, 11, 17)) == 2


def test_one_week():
    assert working_days_between(date(2026, 11, 16), date(2026, 11, 23)) == 5


# late_and_quiet: "today" is Tue 17 Nov 2026; a comment today is never quiet.
TODAY = date(2026, 11, 17)


def _t(key, owner="ana", stage="todo", due=None, last_comment=TODAY):
    return Ticket(key, owner, stage, due, last_comment)


def test_empty_input():
    assert late_and_quiet([], TODAY) == {}


def test_done_skipped_even_if_late_and_quiet():
    t = _t("A-1", stage="done", due=date(2026, 11, 1), last_comment=None)
    assert late_and_quiet([t], TODAY) == {}


def test_due_none_not_late():
    assert late_and_quiet([_t("A-1", due=None)], TODAY) == {}


def test_due_today_not_late():
    assert late_and_quiet([_t("A-1", due=TODAY)], TODAY) == {}


def test_due_yesterday_late():
    t = _t("A-1", due=date(2026, 11, 16))
    assert late_and_quiet([t], TODAY) == {"ana": {"late": ["A-1"], "quiet": []}}


def test_no_comment_is_quiet():
    t = _t("A-1", last_comment=None)
    assert late_and_quiet([t], TODAY) == {"ana": {"late": [], "quiet": ["A-1"]}}


def test_late_and_quiet_both():
    t = _t("A-1", due=date(2026, 11, 16), last_comment=None)
    assert late_and_quiet([t], TODAY) == {"ana": {"late": ["A-1"], "quiet": ["A-1"]}}


def test_quiet_boundary_across_weekend():
    # Fri 13 -> Tue 17 is 2 working days (quiet); Mon 16 -> Tue 17 is 1 (not quiet)
    tickets = [
        _t("A-1", last_comment=date(2026, 11, 13)),
        _t("A-2", last_comment=date(2026, 11, 16)),
    ]
    assert late_and_quiet(tickets, TODAY) == {"ana": {"late": [], "quiet": ["A-1"]}}


def test_quiet_boundary_within_week():
    # Mon 16 -> Wed 18 is 2 working days (quiet); Tue 17 -> Wed 18 is 1 (not quiet)
    wed = date(2026, 11, 18)
    tickets = [
        _t("A-1", last_comment=date(2026, 11, 16)),
        _t("A-2", last_comment=date(2026, 11, 17)),
    ]
    assert late_and_quiet(tickets, wed) == {"ana": {"late": [], "quiet": ["A-1"]}}


def test_custom_quiet_after():
    # Thu 12 -> Tue 17 is 3 working days (quiet); Fri 13 -> Tue 17 is 2 (not quiet)
    tickets = [
        _t("A-1", last_comment=date(2026, 11, 12)),
        _t("A-2", last_comment=date(2026, 11, 13)),
    ]
    assert late_and_quiet(tickets, TODAY, quiet_after=3) == {
        "ana": {"late": [], "quiet": ["A-1"]}
    }


def test_input_order_kept_and_owners_in_first_flag_order():
    late = date(2026, 11, 10)
    tickets = [
        _t("Z-9", owner="bo", due=late),
        _t("A-1", owner="ana", last_comment=None),
        _t("B-5", owner="bo", last_comment=None),
        _t("A-0", owner="ana", due=late),
        _t("B-1", owner="bo", due=late),
    ]
    result = late_and_quiet(tickets, TODAY)
    assert list(result) == ["bo", "ana"]
    assert result == {
        "bo": {"late": ["Z-9", "B-1"], "quiet": ["B-5"]},
        "ana": {"late": ["A-0"], "quiet": ["A-1"]},
    }


def test_owner_with_nothing_flagged_left_out():
    tickets = [
        _t("C-1", owner="cy"),  # fresh comment, no due date
        _t("C-2", owner="cy", stage="done", last_comment=None),
        _t("A-1", owner="ana", last_comment=None),
    ]
    assert late_and_quiet(tickets, TODAY) == {"ana": {"late": [], "quiet": ["A-1"]}}
