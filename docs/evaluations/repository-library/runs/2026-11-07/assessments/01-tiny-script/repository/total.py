"""Print a receipt CSV total. Input files must be trusted local exports."""
import csv
import sys
from decimal import Decimal


def total(path):
    with open(path, newline="", encoding="utf-8") as stream:
        return sum((Decimal(row["amount"]) for row in csv.DictReader(stream)), Decimal(0))


if __name__ == "__main__":
    print(f"{total(sys.argv[1]):.2f}")
