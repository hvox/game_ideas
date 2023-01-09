from fractions import Fraction
from typing import Any


RECIPES: dict[str, tuple[Fraction, dict[str, Fraction]]] = {}
for recipe_description in (
    # Logistics
    ("transport-belt", 0.25, {"iron-plate": 0.5, "iron-gear-wheel": 0.5}),
    ("underground-belt", 0.5, {"iron-plate": 5, "transport-belt": 2.5}),
    ("splitter", 1, {"electronic-circuit": 5, "iron-plate": 5, "transport-belt": 4}),
    ("inserter", 0.5, {"electronic-circuit": 1, "iron-gear-wheel": 1, "iron-plate": 1}),
    ("pipe", 0.5, {"iron-plate": 1}),
    ("car", 2, {"engine-unit": 8, "iron-plate": 20, "steel-plate": 5}),
    # Production
    ("assembling-machine-1", 0.5, {"electronic-circuit": 3, "iron-gear-wheel": 5, "iron-plate": 9}),
    # Intermediate products
    ("copper-cable", 0.25, {"copper-plate": 0.5}),
    ("iron-gear-wheel", 0.5, {"iron-plate": 2}),
    ("electronic-circuit", 0.5, {"copper-cable": 3, "iron-plate": 1}),
    ("engine-unit", 10, {"iron-gear-wheel": 1, "pipe": 2, "steel-plate": 1}),
    ("automation-science-pack", 5, {"copper-plate": 1, "iron-gear-wheel": 1}),
    ("logistic-science-pack", 6, {"inserter": 1, "transport-belt": 1}),
    # Military
    ("firearm-magazine", 1, {"iron-plate": 4})
):
    recipe: Any  # typecheckers are very dumb when it comes to for-loops
    target_material, creation_time, recipe = recipe_description
    time = Fraction(creation_time).limit_denominator(100)
    ingridients = {mat: Fraction(x).limit_denominator(100) for mat, x in recipe.items()}
    RECIPES[target_material] = (time, ingridients)
