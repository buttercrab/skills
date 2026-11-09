from importlib.resources import files
import json


def normalize(value):
    mapping = json.loads(files("riverfmt").joinpath("defaults.json").read_text(encoding="utf-8"))
    return mapping.get(value, value.strip().lower())
