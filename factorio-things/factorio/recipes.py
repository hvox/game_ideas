from fractions import Fraction
from pathlib import Path
from typing import NamedTuple


class Recipe(NamedTuple):
    creation_time: Fraction
    ingredients: dict[str, Fraction]

    def __str__(self) -> str:
        # TODO: implement better string representation for amounts
        ingredients = (f"{ing}:{x}" for ing, x in self.ingredients.items())
        return f"time:{self.creation_time} + " + " + ".join(ingredients)


def read_recipes(item_group: str) -> dict[str, Recipe]:
    recipes = {}
    path = Path(__file__).with_suffix("") / (item_group + ".tsv")
    for row in path.read_text().strip("\n").split("\n")[1:]:
        ingredients = {}
        material, creation_time, rest = row.split("\t")
        for ingridient, amount in (ing.split(":") for ing in rest.split(", ")):
            ingredients[ingridient] = Fraction(amount)
        recipes[material] = Recipe(Fraction(creation_time), ingredients)
    return recipes


LOGISTICS = read_recipes("logistics")
PRODUCTION = read_recipes("production")
INTERMEDIATE = read_recipes("intermediate_products")
COMBAT = read_recipes("combat")
RECIPES = LOGISTICS | PRODUCTION | INTERMEDIATE | COMBAT
