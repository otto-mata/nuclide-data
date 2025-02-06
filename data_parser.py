import csv
import math

TIME_CONVERSION_RATIO = {
    "y": 3.15576e10,
    "d": 8.64e7,
    "h": 3.6e6,
    "m": 6e4,
    "s": 1e3,
    "ms": 1,
    "ns": 1e-3,
    "us": 1e-6,
    "ps": 1e-9,
    "fs": 1e-12,
}


def unify_half_life(numeric: float, unit: str):
    ratio = TIME_CONVERSION_RATIO.get(unit)
    if not unit:
        return math.inf
    return numeric * ratio


with open("walletcards.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        half_life = row[10]
        if half_life == "STABLE":
            half_life = math.inf
        if isinstance(half_life, str) and not len(half_life):
            continue
        print(unify_half_life(float(half_life), row[11]), "ms")
