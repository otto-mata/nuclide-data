import csv
import math
import uncertainties
import uncertainties.umath


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

PROTON_WEIGHT = 1.0072764665789
NEUTRON_WEIGHT = 1.00866491588


class Decay:
    @staticmethod
    def from_string(_in: str):
        modes = _in.split(",")
        for mode in modes:
            mode = mode.strip()
            mode_tokens = mode.split(" ")
            print(mode_tokens[0])


class Atom:
    Z: int
    A: int
    N: int
    e: int
    name: str
    symbol: str
    mass: float
    isotopes: int

    def __init__(
        self,
        z,
        name,
        symbol,
        n=None,
        a=None,
        mass=None,
        isotopes=0,
    ):
        self.Z = z
        self.N = n
        if self.N is None:
            if a is None:
                raise ValueError("Atom must have A or N set")
            self.N = a - z
        self.A = a
        if self.A is None:
            self.A = z + n
        self.name = name
        self.symbol = symbol
        self.e = z
        self.mass = mass
        self.isotopes = isotopes


def unify_half_life(numeric: float, unit: str):
    ratio = TIME_CONVERSION_RATIO.get(unit)
    if not unit:
        return math.inf
    return numeric * ratio


def isotopes() -> list[dict]:
    rows = []
    entries: list[dict] = []
    headers: list[str] = []
    with open("walletcards.csv") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            rows.append(row)

    for row in rows:
        d = dict()
        for pair in zip(headers, row):
            d[pair[0]] = pair[1]
        entries.append(d)
    return entries


def N(mass: uncertainties.Variable, z: uncertainties.Variable):
    z_w = z * PROTON_WEIGHT
    n_w = math.ceil(mass.nominal_value) - z_w
    n = n_w / NEUTRON_WEIGHT
    return math.ceil(n.nominal_value)


def elements() -> list[Atom]:
    rows = []
    entries: list[dict[str, str]] = []
    headers: list[str] = []
    atoms: list[Atom] = []
    with open("ptable.csv") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            rows.append(row)

    for row in rows:
        d = dict()
        for pair in zip(headers, row):
            d[pair[0].strip()] = pair[1].strip()
        entries.append(d)

    for entry in entries:
        z = int(entry["atomicNumber"])
        atomic_mass = entry["atomicMass"]
        if atomic_mass.strip("[]") != atomic_mass:
            atomic_mass = atomic_mass.strip("[]") + "(0)"
        n = N(
            uncertainties.ufloat_fromstr(atomic_mass),
            uncertainties.Variable(z, 0),
        )
        a = Atom(z, entry["name"], entry["symbol"], n=n)
        atoms.append(a)
    return atoms


# periodic_table = elements()
# isotopes_list = isotopes()


# def find_isotopes(z: int):
#     istps = []
#     for isotope in isotopes_list:
#         if int(isotope["Atomic Number (Z)"]) == z:
#             istps.append(isotope)
#     return istps


# for element in filter(lambda a: a.Z == 93, periodic_table):
#     print(f"{element.symbol}: ", end="")
#     print(
#         *[
#             f"{isotope['Element']}-{isotope['Atomic Mass (A)']}"
#             for isotope in find_isotopes(element.Z)
#         ],
#         sep=", ",
#     )

for isotope in isotopes():
    decay = isotope["Decay Modes"]
    if decay:
        Decay.from_string(decay)
