from __future__ import annotations

from fractions import Fraction
from graphlib import TopologicalSorter
from itertools import chain
from pathlib import Path
from typing import Iterable

from frozendict import frozendict

Real = int | float | Fraction


class Material:
    name: str
    time: Fraction
    ingredients: frozendict[str, Fraction]

    def __init__(self, name: str, time: Real = 0, ingredients: Iterable = {}):
        self.name = name
        self.time = to_fraction(time)
        self.ingredients = frozendict({k: to_fraction(v) for k, v in dict(ingredients).items()})

    def __repr__(self):
        return self.name

    # def __str__(self):
    #     ingredients = ", ".join(f"{k}:{v}" for k, v in self.ingredients.items())
    #     return self.name + "(" + ingredients + ")"

    def to_tsv_row(self) -> str:
        ingredients = ", ".join(f"{k}:{v}" for k, v in self.ingredients.items())
        return self.name + "\t" + str(self.time) + "\t" + ingredients

    @staticmethod
    def from_tsv_row(row: str) -> Material:
        name, time, ingredients_str = row.split("\t")
        ingredients = {k: Fraction(v) for k, v in (s.split(":") for s in ingredients_str.split(", "))}
        return Material(name, Fraction(time), ingredients)

    @property
    def is_liquid(self) -> bool:
        liquids = "water petroleum-gas light-oil heavy-oil sulfuric-acid lubricant".split()
        return self.name in liquids

    @property
    def items_per_lane(self) -> int:
        return 60 * (1000 if self.is_liquid else 15)

    @property
    def buildings(self) -> Fraction:
        production_speed = {
            "space-science-pack": self.time,
            "iron-plate": self.time,
            "coper-plate": self.time,
            "steel-plate": self.time * 5,
            "stone-brick": self.time,
        }
        return production_speed.get(self.name) or (self.time if self.is_liquid else self.time / Fraction(0.75))

    @property
    def color(self) -> int:
        return ((sum(self.name.split("-")[0].encode()) ^ 3) & 7) + 1

    @staticmethod
    def load_materials() -> frozendict[str, Material]:
        path = Path(__file__).resolve().parent / "materials.tsv"
        recipes = map(Material.from_tsv_row, path.read_text().splitlines()[1:])
        materials = {recipe.name: recipe for recipe in recipes}
        for ingr in chain(*(mat.ingredients for mat in materials.values())):
            materials.setdefault(ingr, Material(ingr, Fraction(0), {}))
        graph = {name: mat.ingredients for name, mat in materials.items()}
        materials = {mat: materials[mat] for mat in TopologicalSorter(graph).static_order()}
        result = frozendict(materials)
        setattr(Material, "materials", result)
        return result

    def __bool__(self):
        return bool(self.ingredients)

    def __iter__(self):
        materials = getattr(Material, "materials")
        for ingr, amount in self.ingredients.items():
            yield materials[ingr], amount


def to_fraction(x: int | float | Fraction | Real) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x).limit_denominator(10**12)
