import argparse
from .parser import parse_lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as stream:
        rows = parse_lines(stream)
    print("label\tvalue")
    for label, value in rows:
        print(f"{label}\t{value}")
