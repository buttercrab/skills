# Partial current program: illustrative source snapshot, not a runnable fixture.
import csv
import sqlite3

def import_rows(db, stream):
    rows = list(csv.DictReader(stream))
    errors = validate_all(rows)  # checks required fields, item-ID uniqueness, nonnegative count
    if errors:
        return {"accepted": False, "errors": errors}
    return {"accepted": False, "preview": rows}  # operator must approve separately

def approve(db, rows):
    with db:
        db.execute("DELETE FROM inventory")
        db.executemany("INSERT INTO inventory VALUES (?, ?, ?)", rows)
    return {"accepted": True}

def connect(path):
    return sqlite3.connect(path)
