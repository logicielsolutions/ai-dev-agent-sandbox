from trialkit.progress import mentioned_users, percent_done, progress_line
from trialkit.tickets import Ticket


def test_nothing_done():
    assert percent_done([Ticket("AIT-1", "a", "todo")]) == 0


def test_all_done():
    assert progress_line([Ticket("AIT-1", "a", "done"), Ticket("AIT-2", "b", "done")]) == "100% done (2 tickets)"


def test_no_tickets():
    assert percent_done([]) == 0


def test_single_mention():
    assert mentioned_users("ping <@U0ATSB9B3AP> please") == ["U0ATSB9B3AP"]
