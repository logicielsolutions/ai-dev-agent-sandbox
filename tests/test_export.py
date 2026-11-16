from datetime import date

from trialkit.export import save, to_csv
from trialkit.tickets import Ticket


def test_header_and_rows():
    text = to_csv([Ticket("AIT-1", "asha", "todo", due=date(2026, 11, 20))])
    assert text.splitlines() == ["key,owner,stage,due", "AIT-1,asha,todo,2026-11-20"]


def test_missing_due_is_blank():
    text = to_csv([Ticket("AIT-2", "ben", "review")])
    assert text.splitlines()[1] == "AIT-2,ben,review,"


def test_save_writes_file(tmp_path):
    path = save([Ticket("AIT-3", "cara", "done")], str(tmp_path), "week.csv")
    assert open(path).read().startswith("key,owner,stage,due\n")
