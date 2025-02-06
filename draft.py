from __future__ import annotations
import numpy as np
import pickle
from typing import Callable, TypeAlias


def get_atoms() -> list[Atom]:
    with open("atoms.pickled", "rb") as f:
        data = pickle.load(f)
    return data


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Utils:
    @classmethod
    def years_to_milliseconds(cls, years: int):
        ms_per_year = 3.1556926080000003814697265625e10
        return years * ms_per_year


"""AtomicNumber
Element
Symbol
AtomicMass
NumberofNeutrons
NumberofProtons
NumberofElectrons
Period
Group
Phase
Radioactive
Natural
Metal
Nonmetal
Metalloid
Type
AtomicRadius
Electronegativity
FirstIonization
Density
MeltingPoint
BoilingPoint
NumberOfIsotopes
Discoverer
Year
SpecificHeat
NumberofShells
NumberofValence
"""


class Atom:
    Z: int
    A: int
    N: int
    e: int
    shells: int
    valence: int
    name: str
    symbol: str
    mass: float
    isotopes: int

    def __init__(
        self,
        z,
        n,
        name,
        symbol,
        e=None,
        shells=None,
        valence=None,
        mass=None,
        isotopes=0,
    ):
        self.Z = z
        self.N = n
        self.A = z + n
        self.name = name
        self.symbol = symbol
        self.e = e
        self.shells = shells
        self.valence = valence
        self.mass = mass
        self.isotopes = isotopes


class Constants:
    avogadro = 6.02214070409084099072e23


class DecayMode:
    alpha = 1
    proton = 2
    neutron = 3
    positron = 4
    electron = 5


class Decay:
    Function: TypeAlias = Callable[["Isotope"], "Isotope"]

    @staticmethod
    def alpha(nuclide: Isotope) -> Isotope:
        z = nuclide.Z - 2
        n = nuclide.N - 2
        atom = next(filter(lambda a: a.Z == z, get_atoms()))
        return Isotope(
            None,
            z,
            n,
            emission=None,
            mother=nuclide,
            daughter=None,
            name=atom.name,
            symbol=atom.symbol,
        )


class Isotope(Atom):
    half_life: int
    a_daughter: Atom
    mother: Isotope
    emission: Decay.Function
    stable: int
    chain_first: int

    def __init__(
        self,
        hl: int,
        z: int,
        n: int,
        emission: Decay.Function = None,
        name: str = None,
        symbol: str = None,
        daughter: Atom = None,
        mother: Isotope = None,
    ):
        super().__init__(z, n, f"{name}-{z + n}", f"{symbol}-{z + n}")
        self.half_life = hl
        self.emission = emission
        self.a_daughter = daughter
        self.stable = self.a_daughter is None
        self.mother = mother
        self.chain_first = self.mother is None

    def count(self, at: int, n0: int):
        return n0 * np.exp((-np.log(2) * at) / self.half_life)

    def ms_decay_p(self):
        decayed = 0.0
        t = 500
        while decayed == 0.0:
            decayed = Constants.avogadro - self.count(t, Constants.avogadro)
            t += 100
        ms_average = decayed / t
        return ms_average / Constants.avogadro

    def emit(self):
        return self.emission

    def decay(self):
        self.emit()

    def daughter_isotope(self):
        return self.emission(self)


class Uranium235(Isotope):
    def __init__(self):
        super().__init__(22.21e18, 92, 143, Decay.alpha, "Uranium", "U")


isotope = Uranium235()
print(isotope.daughter_isotope().name)
# atoms = get_atoms()
# for atom in atoms:
#     print(f"{atom.name}: {atom.isotopes}")
